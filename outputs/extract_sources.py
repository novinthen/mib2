"""
Stage 0 extraction utility for MIB 2.0.

Extracts the FULL contents of the two source .docx files in document order,
including body paragraphs, tables, headers/footers, footnotes, endnotes,
text boxes (w:txbxContent) and drawing/image objects, and reports any
content that extraction could not render as text (image-only objects,
embedded objects, charts).

Usage:  python outputs/extract_sources.py
Writes: outputs/extracted/<name>.txt  and  outputs/extracted/<name>_manifest.json
"""

import json
import os
import re
import zipfile
from xml.etree import ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
MC = "{http://schemas.openxmlformats.org/markup-compatibility/2006}"
V = "{urn:schemas-microsoft-com:vml}"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUTS = os.path.join(ROOT, "inputs")
OUTDIR = os.path.join(ROOT, "outputs", "extracted")


def text_of_run(el):
    out = []
    for node in el.iter():
        tag = node.tag
        if tag == W + "t":
            out.append(node.text or "")
        elif tag == W + "tab":
            out.append("\t")
        elif tag in (W + "br", W + "cr"):
            out.append("\n")
        elif tag == W + "noBreakHyphen":
            out.append("-")
    return "".join(out)


def para_text(p):
    """Text of a paragraph EXCLUDING nested textbox content (handled separately)."""
    parts = []
    for child in p.iter():
        if child.tag == W + "t":
            # skip if inside a txbxContent that is a descendant of this paragraph
            parts.append(child.text or "")
        elif child.tag == W + "tab":
            parts.append("\t")
        elif child.tag in (W + "br",):
            parts.append("\n")
    return "".join(parts)


def para_style(p):
    ppr = p.find(W + "pPr")
    if ppr is None:
        return ""
    st = ppr.find(W + "pStyle")
    if st is None:
        return ""
    return st.get(W + "val", "")


def numbering_info(p):
    ppr = p.find(W + "pPr")
    if ppr is None:
        return None
    npr = ppr.find(W + "numPr")
    if npr is None:
        return None
    ilvl = npr.find(W + "ilvl")
    numid = npr.find(W + "numId")
    return {
        "ilvl": ilvl.get(W + "val") if ilvl is not None else "0",
        "numId": numid.get(W + "val") if numid is not None else "0",
    }


def walk_block(el, lines, stats, depth=0):
    """Walk body-level block children in document order."""
    for child in el:
        tag = child.tag
        if tag == W + "p":
            style = para_style(child)
            num = numbering_info(child)
            txt = para_text(child).strip()
            # detect drawings/images/objects inside paragraph
            for d in child.iter():
                if d.tag == A + "blip":
                    stats["images"] += 1
                    rid = d.get(R + "embed") or d.get(R + "link") or "?"
                    lines.append(f"[IMAGE OBJECT rId={rid}]")
                elif d.tag == V + "imagedata":
                    stats["vml_images"] += 1
                    lines.append("[VML IMAGE OBJECT]")
                elif d.tag == W + "object":
                    stats["embedded_objects"] += 1
                    lines.append("[EMBEDDED OBJECT]")
                elif d.tag == W + "drawing":
                    stats["drawings"] += 1
            if txt:
                prefix = ""
                if style.lower().startswith("heading") or re.match(r"^h[1-6]$", style.lower()):
                    lvl = re.sub(r"\D", "", style) or "1"
                    prefix = "#" * min(int(lvl), 6) + " "
                    stats["headings"] += 1
                elif num:
                    prefix = "  " * int(num["ilvl"]) + "- "
                lines.append(prefix + txt)
                stats["paragraphs"] += 1
            # textboxes
            for tb in child.iter(W + "txbxContent"):
                stats["textboxes"] += 1
                lines.append("[TEXTBOX START]")
                walk_block(tb, lines, stats, depth + 1)
                lines.append("[TEXTBOX END]")
        elif tag == W + "tbl":
            stats["tables"] += 1
            lines.append(f"[TABLE {stats['tables']} START]")
            for tr in child.findall(W + "tr"):
                cells = []
                for tc in tr.findall(W + "tc"):
                    sub = []
                    walk_block(tc, sub, stats, depth + 1)
                    cells.append(" / ".join(x for x in sub if x.strip()))
                lines.append(" | ".join(cells))
            lines.append(f"[TABLE {stats['tables']} END]")
        elif tag == W + "sdt":
            content = child.find(W + "sdtContent")
            if content is not None:
                walk_block(content, lines, stats, depth + 1)
        elif tag == MC + "AlternateContent":
            # take the Choice branch
            choice = child.find(MC + "Choice")
            fb = child.find(MC + "Fallback")
            target = choice if choice is not None else fb
            if target is not None:
                for tb in target.iter(W + "txbxContent"):
                    stats["textboxes"] += 1
                    lines.append("[TEXTBOX START]")
                    walk_block(tb, lines, stats, depth + 1)
                    lines.append("[TEXTBOX END]")


def extract(path):
    name = os.path.splitext(os.path.basename(path))[0]
    z = zipfile.ZipFile(path)
    names = z.namelist()
    stats = dict(paragraphs=0, headings=0, tables=0, textboxes=0, images=0,
                 vml_images=0, embedded_objects=0, drawings=0, footnotes=0,
                 endnotes=0, hyperlinks=0)
    lines = []

    doc = ET.fromstring(z.read("word/document.xml"))
    body = doc.find(W + "body")
    lines.append("===== BODY =====")
    walk_block(body, lines, stats)

    for part, label in (("word/footnotes.xml", "FOOTNOTES"),
                        ("word/endnotes.xml", "ENDNOTES")):
        if part in names:
            root = ET.fromstring(z.read(part))
            got = []
            for note in root:
                nid = note.get(W + "id")
                ntype = note.get(W + "type")
                if ntype in ("separator", "continuationSeparator", "continuationNotice"):
                    continue
                sub = []
                walk_block(note, sub, stats)
                body_txt = " ".join(x for x in sub if x.strip())
                if body_txt.strip():
                    got.append(f"[{label[:-1]} {nid}] {body_txt}")
            if got:
                lines.append(f"===== {label} =====")
                lines.extend(got)
                stats["footnotes" if label == "FOOTNOTES" else "endnotes"] = len(got)

    hdr_ftr = [n for n in names if re.match(r"word/(header|footer)\d*\.xml", n)]
    hf_lines = []
    for part in sorted(hdr_ftr):
        root = ET.fromstring(z.read(part))
        sub = []
        walk_block(root, sub, stats)
        txt = " | ".join(x for x in sub if x.strip())
        if txt.strip():
            hf_lines.append(f"[{part}] {txt}")
    if hf_lines:
        lines.append("===== HEADERS/FOOTERS =====")
        lines.extend(hf_lines)

    # hyperlink targets
    links = []
    for part in [n for n in names if n.endswith(".rels")]:
        rels = ET.fromstring(z.read(part))
        for rel in rels:
            if "hyperlink" in (rel.get("Type") or ""):
                links.append(rel.get("Target"))
    stats["hyperlinks"] = len(links)
    if links:
        lines.append("===== HYPERLINK TARGETS =====")
        lines.extend(sorted(set(links)))

    media = [n for n in names if n.startswith("word/media/")]
    charts = [n for n in names if "chart" in n and n.endswith(".xml")]
    embeddings = [n for n in names if n.startswith("word/embeddings/")]

    app = {}
    if "docProps/app.xml" in names:
        ax = ET.fromstring(z.read("docProps/app.xml"))
        for c in ax:
            app[c.tag.split("}")[-1]] = c.text
    core = {}
    if "docProps/core.xml" in names:
        cx = ET.fromstring(z.read("docProps/core.xml"))
        for c in cx:
            core[c.tag.split("}")[-1]] = c.text

    body_text = "\n".join(lines)
    manifest = {
        "file": os.path.basename(path),
        "size_bytes": os.path.getsize(path),
        "zip_parts": len(names),
        "stats": stats,
        "media_files": media,
        "charts": charts,
        "embeddings": embeddings,
        "app_properties": app,
        "core_properties": core,
        "extracted_chars": len(body_text),
        "extracted_words": len(body_text.split()),
    }
    os.makedirs(OUTDIR, exist_ok=True)
    with open(os.path.join(OUTDIR, name + ".txt"), "w", encoding="utf-8") as f:
        f.write(body_text)
    with open(os.path.join(OUTDIR, name + "_manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    return manifest


if __name__ == "__main__":
    for fn in sorted(os.listdir(INPUTS)):
        if fn.lower().endswith(".docx") and not fn.startswith("~$"):
            m = extract(os.path.join(INPUTS, fn))
            print(json.dumps(m, indent=2)[:2000])
            print("-" * 60)
