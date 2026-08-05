# Claude Code `/goal`: Build the MIB 2.0 Interactive Policy Portal

Paste this entire instruction into Claude Code while its working directory is the extracted `MIB 2.0` folder. The first line invokes the `/goal` workflow.

---

/goal Build a production-quality, responsive, accessible, data-driven website inside this folder for **MIB 2.0 — Malaysian Indian Progression Blueprint**. Treat the files already present in this folder as the authoritative project corpus. Work autonomously from discovery through implementation, testing, and final handover. Do not stop after producing a plan or mock-up: create and verify the working website.

## 1. Mission

Turn this policy package into a Cabinet-grade policy portal and public accountability platform—not a brochure and not a document-download landing page.

The finished product must serve four audiences:

1. Prime Minister and Cabinet: required decisions, funding, gates, risks, and delivery accountability.
2. Ministries and agencies: programmes owned, deliverables, phases, KPIs, dependencies, and verification duties.
3. Community and public: what changes for households, students, workers, entrepreneurs, and applicants.
4. Researchers and media: claims, evidence, assumptions, limitations, sources, conflicts, and audit trail.

Create two connected experience layers:

- **The Blueprint**: concise, visual, public-facing explanation.
- **The Evidence Room**: detailed registers, costing, sources, assumptions, risks, conflicts, validation status, and traceability.

The central product principle is: **every important public statement must be traceable to the canonical files, while uncertainty must remain visible rather than being smoothed over.**

## 2. Source-of-truth and non-negotiable integrity rules

Before coding, recursively inspect the current folder and read the relevant files. Expect source material under `inputs/` and canonical outputs under `outputs/`, including Markdown, CSV, Python scripts, and extracted source text.

Use this precedence order:

1. Machine-generated and machine-verified CSV registers and costing outputs.
2. `outputs/MIB_2.0_EXECUTIVE_PROPOSAL.md` and `outputs/TECHNICAL_ANNEXES.md`.
3. `outputs/FINAL_QA_REPORT.md`, `outputs/VERIFICATION_RESULTS.md`, `outputs/STATUS.md`, `outputs/ASSUMPTIONS_AND_DECISIONS.md`, and audit material.
4. Extracted source documents and original `.docx` inputs for provenance and context only.

Do not silently choose between conflicting values. If files disagree:

- identify the inconsistency;
- prefer a computed register value when its derivation is valid;
- display an explicit disclosure when the conflict is material;
- record the decision in a website-specific data-quality report;
- never fabricate a reconciliation.

Run the supplied verification/build scripts in an isolated, non-destructive way before importing data. Preserve all original policy files. Do not rewrite source registers merely to make the website pass.

The current package is expected to include, among other items:

- 16 retained programmes plus rejected/merged records;
- four pillars and cross-cutting elements;
- three six-year costing scenarios;
- 16 KPIs;
- responsibility assignments;
- claims and figures;
- sources;
- conflicts and duplications;
- risks and safeguards;
- assumptions and validation items;
- six Cabinet decisions;
- a six-year, three-phase delivery model.

Known headline figures must be derived from the source data, never hard-coded into multiple components. At the time this instruction was prepared, the reported figures included:

- central gross cost: RM1,484.273 million;
- conservative gross cost: RM1,158.487 million;
- expanded gross cost: RM1,875.220 million;
- central incremental new funding: RM847.677 million;
- confidence mix: 0.0% Confirmed, 31.9% Benchmarked, 68.1% Provisional;
- 30 outstanding validation items, six described as gating.

These values are orientation only. Recompute them from the current files and use the computed values. If the corpus changes, the website must update without manual edits.

Prominently preserve the material cautions in the package, including the lack of Confirmed cost lines, provisional costing share, missing KPI baselines, uninspected citations, contested mandates, legal/funding gates, and any open finding. Never present provisional estimates as appropriated funding, Cabinet approval, or guaranteed outcomes.

## 3. Repository and implementation approach

Create the website in a new `website/` directory inside the current MIB 2.0 folder. Do not disturb `inputs/`, `outputs/`, or the existing project-level files.

First inspect whether a website stack already exists. If none exists, use this default:

- Next.js with App Router;
- TypeScript in strict mode;
- Tailwind CSS;
- a restrained component system using accessible primitives;
- Recharts or an equivalent lightweight React chart library when charts materially improve comprehension;
- Lucide icons;
- static-first architecture with server-side build-time data ingestion;
- no database and no authentication for the first release;
- deployment compatible with Vercel, while avoiding unnecessary vendor lock-in.

Use the current stable versions available to the environment, and commit a lockfile. Keep dependencies small. Do not introduce a CMS, external API, analytics tracker, AI chatbot, cookie banner, or user account system unless already configured in the repository.

Build a deterministic ingestion layer that reads the canonical `../outputs/` Markdown and CSV files during development/build, validates required columns and IDs, normalises the records, computes aggregates, and exposes typed data to the UI. Do not manually copy dozens of records into React components.

If static deployment cannot read files outside `website/` at build time, add a documented prebuild step that generates version-controlled website data under `website/src/generated/` from `../outputs/`. Generated files must carry a warning header and be reproducible with one command.

Create explicit TypeScript types for at least:

- Programme
- Pillar
- CostLine and CostScenario
- KPI
- ResponsibilityAssignment
- Claim
- Source
- RiskAndSafeguard
- Conflict
- Narrative
- AssumptionOrDecision
- ValidationItem where recoverable from the corpus

Validate foreign keys between programme, KPI, cost, responsibility, risk, claim, and source records. Build should fail on broken required references, duplicate primary IDs, malformed numeric values, or missing critical columns. Non-critical missing values should display as `Not established`, `Pending validation`, or the exact source status—not as zero.

## 4. Required information architecture

Implement these routes or their clean equivalents:

- `/` — Home and executive proposition
- `/why` — Why MIB 2.0
- `/pillars` — Four-pillar overview
- `/pillars/[slug]` — Pillar detail
- `/programmes` — Programme Explorer
- `/programmes/[id]` — Programme detail with permanent ID-based links
- `/roadmap` — Six-year roadmap
- `/costing` — Costing Lab and Follow the Ringgit
- `/kpis` — KPI dashboard
- `/governance` — governance, responsibilities, reporting, escalation
- `/decisions` — Cabinet decision mode
- `/risks` — risk matrix and safeguards
- `/impact` — illustrative public impact journeys
- `/evidence` — Evidence Room landing page
- `/evidence/claims` and `/evidence/claims/[id]`
- `/evidence/sources` and `/evidence/sources/[id]`
- `/evidence/conflicts`
- `/evidence/assumptions`
- `/evidence/quality` — limitations, verification, unresolved matters, and methodology
- `/downloads` — source package and individual downloadable files
- `/updates` — honest empty state and structure for future quarterly reporting

If some content cannot be extracted reliably, retain the route with a clear, useful explanation rather than inventing content.

## 5. Page and interaction requirements

### Home

The first viewport should communicate one argument immediately:

> Malaysia does not need another collection of disconnected grants. It needs a measurable progression system with named owners, published outcomes, and six years of sustained accountability.

Include:

- a concise executive proposition;
- derived headline metrics;
- four pillar entry points;
- a visual three-phase/six-year roadmap preview;
- gross versus incremental funding distinction;
- a prominent evidence/uncertainty disclosure;
- calls to explore programmes, Cabinet decisions, and evidence.

Avoid a generic full-screen stock-photo hero. Prioritise typography, data, structure, and subtle Malaysian visual cues.

### Programme Explorer

This is the core public tool. Provide fast client-side search, sorting, and composable filters for available fields such as:

- pillar;
- phase/year;
- lead ministry or agency;
- beneficiary group;
- programme status (retained, merged, rejected if included);
- costing confidence;
- baseline status;
- risk level.

Each card/row should show programme ID, name, pillar, owner, phase, concise outcome, and computed six-year central cost where applicable. Filters must work on mobile and be keyboard accessible. Show the number of matching programmes and provide a one-action reset.

### Programme detail

Present a readable policy chain:

**problem → structural cause → intervention → eligible population → delivery mechanism → outputs → outcomes → owner → phase → KPI → cost → risks → safeguards → evidence**.

Add deep links to all linked KPIs, responsibility records, claims, sources, costs, and risks. Show absent data honestly. Rejected or merged proposals must never look like adopted programmes.

### Costing Lab

Allow switching among conservative, central, and expanded scenarios without changing programme definitions. Provide derived views by programme, pillar, ministry, phase, cost category, and funding type when supported by the CSV.

Clearly distinguish:

- gross programme cost;
- existing funding;
- proposed reallocation;
- incremental new funding;
- Confirmed, Benchmarked, and Provisional confidence classes;
- 2026 price basis and rounding/precision limitations.

Include a restrained **Follow the Ringgit** flow or composition visual. Make exact values available in an accessible table. Never imply that all displayed sums are approved allocations. Explain that numerical precision reflects calculation, not certainty.

### KPI dashboard

Show Year 2, Year 4, and Year 6 values/targets when present, KPI type, baseline status, responsible data owner, verification source, and linked programme. Visually distinguish established baselines from Year-2 baseline-establishment tasks. Do not plot missing baselines as zero.

### Six-year roadmap

Create an interactive but readable three-phase timeline across Years 1–6. Show programme activity, dependencies, gates, major deliverables, and the independent mid-term evaluation gate if present. Provide a text/table alternative for accessibility and mobile.

### Governance and responsibilities

Explain the Task Force structure, proposed quarterly reporting cycle, lead/supporting entities, escalation path, verification duties, and mandate status. Distinguish existing mandates, mandates requiring confirmation, entities requiring establishment, and contested assignments.

### Cabinet decision mode

Create a focused decision view containing the six requested decisions from the proposal. For each decision show:

- requested action;
- rationale;
- financial/delivery implication;
- gating conditions;
- what it explicitly does **not** authorise;
- linked evidence, risks, and programmes.

Include a concise print stylesheet so this view can be printed or saved as a clear Cabinet briefing.

### Risks and safeguards

Build a filterable register and accessible risk matrix using likelihood/impact/residual-risk fields only when the data supports them. Red is reserved for genuinely high or critical risk. Every risk must link to its mitigation/safeguard, owner where available, and affected programme(s).

### Evidence Room

Make evidence traceability a signature feature. From any material claim or figure, users should be able to reach:

- claim ID;
- exact adopted wording/treatment;
- source and institution;
- reference period/population scope;
- verification status;
- direct evidence versus inference;
- known limitation;
- related conflict, rejected claim, assumption, or validation item.

Provide searchable/filterable claims and sources tables, stable detail links, and sensible empty states. Do not reproduce copyrighted source documents in full; link to the existing permitted source record or download only files already included in the local corpus.

### Public impact journeys

Create clearly labelled **illustrative policy pathways**, not fictional testimonials. Include pathways supported by the programme data, such as:

- a child with unresolved documentation;
- an SJKT pupil;
- a school leaver considering TVET;
- a low-income household;
- a microenterprise owner;
- a public-service applicant.

Each pathway should connect several relevant programme IDs and explain progression, expected touchpoints, and measurement. Do not create names, photographs, quotes, or claims of lived results.

### Downloads and updates

Offer organised downloads for the executive proposal, technical annexes, QA/verification reports, and public CSV registers. Explain file type and purpose. Do not expose material that the corpus itself marks private or restricted.

The Updates page should be launch-ready but must not fabricate implementation updates. Show a dated baseline/release note and explain what future quarterly reports will contain.

## 6. Design system and experience direction

The website must feel like a serious national policy institution: calm, precise, modern, and independent of party-campaign aesthetics.

Use a restrained palette such as:

- deep navy: institutional authority;
- warm gold: progression and milestones;
- teal: verified outcomes/evidence;
- amber: assumptions and caution;
- red: high risk or rejected/unsupported status only;
- off-white and cool grey surfaces for long-form reading.

Use strong typographic hierarchy, generous whitespace, crisp tables, compact information-dense cards, subtle borders, and restrained motion. Avoid gradients as decoration, glassmorphism, excessive rounded cards, animated counters, generic corporate illustrations, ethnic stereotypes, flag overuse, and decorative stock images.

Required responsive states:

- mobile phone;
- tablet;
- desktop;
- wide desktop for data tables.

Large tables must support responsive card/table views or horizontal scrolling with a visible cue. Sticky headers may be used where helpful. Provide breadcrumbs on detail pages and a persistent but unobtrusive global search or scoped search access.

## 7. Language architecture

English is the canonical policy language unless the current corpus supplies approved translations. Build the routing/content architecture so Bahasa Malaysia (`ms`) and Tamil (`ta`) can be added cleanly.

Do not silently generate and publish unreviewed translations of legal, constitutional, financial, or evidentiary statements as authoritative. If you add machine-draft translations, label them visibly as draft/unverified and keep English as the authoritative source. Prefer a complete English launch with translation-ready structure over misleading partial language parity.

## 8. Accessibility, performance, privacy, and SEO

Meet WCAG 2.2 AA as far as reasonably testable:

- semantic landmarks and headings;
- keyboard access and visible focus states;
- skip link;
- labelled controls;
- sufficient colour contrast;
- non-colour status cues;
- accessible chart summaries/tables;
- reduced-motion support;
- descriptive page titles and link text.

Performance goals for production pages:

- Lighthouse performance, accessibility, best practices, and SEO target of 90+ on representative pages;
- avoid layout shift;
- optimise fonts and icons;
- lazy-load only genuinely heavy client modules;
- keep most pages server-rendered/static;
- do not ship the full raw corpus to every browser page.

Privacy requirements:

- no tracking by default;
- no form collection in v1;
- no third-party embeds that leak visitor data;
- no secrets in client bundles;
- secure default headers where supported.

SEO and sharing:

- meaningful metadata per route;
- canonical URLs based on a configurable site URL;
- sitemap and robots file;
- Open Graph metadata using a locally generated, policy-appropriate graphic;
- JSON-LD only where accurate and useful;
- permanent, human-readable or ID-based deep links.

## 9. Validation and testing

Implement and run:

1. Source-data ingestion tests.
2. Schema and required-column validation.
3. Primary-ID uniqueness checks.
4. Foreign-key/link integrity checks.
5. Independent recomputation of headline aggregates from cost lines.
6. Scenario reconciliation tests.
7. UI unit tests for key formatters and filters.
8. End-to-end smoke tests for the home page, programme filtering, one programme detail, scenario switching, evidence deep link, and 404.
9. Type checking, linting, production build, and route/link validation.
10. Accessibility checks on representative pages.

Create a `website/DATA_QUALITY_REPORT.md` recording:

- files ingested;
- rows imported per register;
- computed headline figures;
- validation warnings;
- unresolved inconsistencies;
- fields intentionally omitted;
- decisions made by the ingestion layer;
- date/time and command used to regenerate.

Create a visible website methodology/quality page generated from this report and the canonical QA documents, but never expose developer-only filesystem paths.

The build must not pass if a headline total is hard-coded and disagrees with source-derived totals. Avoid brittle snapshot tests of the entire UI; test data meaning and critical workflows.

## 10. Documentation and operator experience

Add a clear `website/README.md` covering:

- what the site is;
- prerequisites;
- installation;
- development command;
- data regeneration/import command;
- tests;
- production build;
- deployment to Vercel;
- how to update the portal after canonical CSV/Markdown changes;
- translation workflow;
- known limitations.

Provide convenient scripts such as:

- `dev`
- `build`
- `lint`
- `typecheck`
- `test`
- `test:e2e`
- `data:build`
- `data:check`
- `verify`

Make `verify` run the most important data validation, type checking, tests, and production build in a sensible order.

Add `.env.example` only if configuration is genuinely required. The site must run locally without external credentials.

## 11. Work sequence

Follow this sequence autonomously:

1. Inventory the corpus and repository state.
2. Read the executive proposal, technical annexes, QA/verification material, and all register headers; then inspect complete relevant records.
3. Run existing policy verification scripts without altering their inputs.
4. Write a concise implementation plan and source map inside `website/`.
5. Scaffold the site if required.
6. Build and test the ingestion/validation layer first.
7. Establish the design system and global shell.
8. Implement home, pillars, programmes, and programme details.
9. Implement costing, KPIs, roadmap, governance, decisions, risks, evidence, impact, downloads, and updates.
10. Add responsive states, accessibility, metadata, print styles, and polished empty/error states.
11. Run the complete verification suite and fix defects.
12. Perform a final visual QA pass at mobile and desktop widths.
13. Leave a concise completion report with commands run, results, known limitations, and exact next deployment step.

Do not ask for routine aesthetic or engineering choices. Make defensible decisions from this brief and document them. Ask only if blocked by missing permissions, an irreconcilable publication decision, or a choice that would materially alter policy meaning.

## 12. Definition of done

The goal is complete only when:

- a working website exists under `website/`;
- canonical records are ingested programmatically;
- all required core routes are implemented;
- Programme Explorer filters work;
- costing scenario switching and funding distinctions work;
- KPI, roadmap, governance, Cabinet decision, risk, evidence, impact, and download views work;
- material uncertainties are visible;
- permanent IDs link related records;
- source data is not silently modified;
- the site is responsive and keyboard usable;
- type checking, linting, tests, data checks, and production build pass;
- README and data-quality documentation are complete;
- the site can be deployed to Vercel without external credentials;
- the final report states anything still incomplete rather than claiming success prematurely.

Prioritise correctness and traceability first, comprehension second, visual polish third. The final experience should make a complex six-year policy package feel navigable without making it look more certain than the evidence allows.
