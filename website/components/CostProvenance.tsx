import type { CostLine, CostingAssumption, Source } from '@/types';
import ConfidenceBadge, { CONFIDENCE_MEANING } from './ConfidenceBadge';

/** Format a plain ringgit amount like "90000" -> "RM 90,000"; pass through if non-numeric. */
function formatRinggit(raw: string): string {
  const n = Number(String(raw).replace(/[, ]/g, ''));
  if (!raw || Number.isNaN(n)) return raw;
  return `RM ${n.toLocaleString('en-MY')}`;
}

/** Split a comma/semicolon-separated id list ("ASM-C01, ASM-050") into trimmed ids. */
function splitIds(raw: string): string[] {
  return (raw || '')
    .split(/[,;]+/)
    .map((s) => s.trim())
    .filter(Boolean);
}

function Row({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-[8rem_1fr] gap-1 sm:gap-4 py-2 border-t border-neutral-100 first:border-t-0">
      <dt className="text-xs font-semibold uppercase tracking-wide text-neutral-500 pt-0.5">{label}</dt>
      <dd className="text-sm text-neutral-800">{children}</dd>
    </div>
  );
}

/**
 * Progressive-disclosure "why this figure" panel for a set of cost lines.
 * Pure presentational — safe to render from both server and client components.
 */
export default function CostProvenance({
  costLines,
  sources,
  assumptions,
  defaultOpen = false,
}: {
  costLines: CostLine[];
  sources: Record<string, Source>;
  assumptions: Record<string, CostingAssumption>;
  defaultOpen?: boolean;
}) {
  if (costLines.length === 0) return null;

  return (
    <div className="space-y-3">
      {costLines.map((line) => {
        const asmIds = splitIds(line.assumption_ids);
        const asms = asmIds.map((id) => assumptions[id]).filter(Boolean) as CostingAssumption[];
        const primary = asms[0];

        // Resolve source: prefer the cost line's, else the assumption's.
        const sourceId = line.cost_source_id || primary?.cost_source_id || '';
        const source = sourceId ? sources[sourceId] : undefined;

        const method = line.cost_method || primary?.cost_method || '';
        const quantities = primary?.frequency_or_duration || '';
        const eligible = primary?.eligible_population || '';
        const benchmark = primary?.basis_and_benchmark || '';
        const validation = asms.map((a) => a.validation_item).filter(Boolean).join(', ');

        return (
          <details
            key={line.cost_line_id}
            open={defaultOpen}
            className="group rounded-xl border border-neutral-200 bg-white open:bg-neutral-50/60"
          >
            <summary className="flex items-center justify-between gap-3 cursor-pointer list-none px-4 py-3 select-none">
              <span className="flex items-center gap-2 text-sm font-semibold text-neutral-800">
                <svg
                  className="w-4 h-4 text-neutral-400 transition-transform group-open:rotate-90"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                  aria-hidden
                >
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
                Why this figure?
                <span className="hidden sm:inline font-normal text-neutral-500">
                  · RM {line.six_year_total.toFixed(1)}m over 6 years
                </span>
              </span>
              <ConfidenceBadge confidence={line.confidence} />
            </summary>

            <div className="px-4 pb-4">
              <dl>
                {method && <Row label="Method">{method}</Row>}

                {(primary?.unit_cost_rm || quantities) && (
                  <Row label="Key inputs">
                    {primary?.unit_cost_rm && (
                      <span className="font-medium">{formatRinggit(primary.unit_cost_rm)}</span>
                    )}
                    {primary?.unit_cost_rm && quantities && ' — '}
                    {quantities}
                  </Row>
                )}

                {eligible && (
                  <Row label="Population">
                    {eligible}
                    {primary?.participation_basis ? ` (${primary.participation_basis})` : ''}
                  </Row>
                )}

                {benchmark && <Row label="Benchmark">{benchmark}</Row>}

                {line.funding_split_basis && (
                  <Row label="Funding split">{line.funding_split_basis}</Row>
                )}

                <Row label="Source">
                  {source ? (
                    <span>
                      <span className="font-medium">{source.title}</span>
                      {source.issuing_institution ? ` — ${source.issuing_institution}` : ''}
                      {source.tier && (
                        <span className="ml-2 text-xs font-semibold text-neutral-500">
                          Tier {source.tier}
                        </span>
                      )}
                      {source.url && source.url.startsWith('http') && (
                        <>
                          {' '}
                          <a
                            href={source.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-primary-600 hover:text-primary-700 font-medium underline underline-offset-2"
                          >
                            view ↗
                          </a>
                        </>
                      )}
                      {source.limitations && (
                        <span className="mt-1.5 flex gap-1.5 text-xs text-amber-800 bg-amber-50 border border-amber-100 rounded-lg px-2.5 py-1.5">
                          <span aria-hidden>⚠</span>
                          <span>{source.limitations}</span>
                        </span>
                      )}
                    </span>
                  ) : (
                    <span className="text-neutral-500">Internal estimate — no external source cited.</span>
                  )}
                </Row>

                <Row label="Status">
                  <span className="text-neutral-700">{CONFIDENCE_MEANING[line.confidence]}</span>
                  {validation && (
                    <span className="ml-1 text-amber-800">· pending validation ({validation})</span>
                  )}
                </Row>

                {line.notes && (
                  <Row label="Note">
                    <span className="text-neutral-600">{line.notes}</span>
                  </Row>
                )}
              </dl>
            </div>
          </details>
        );
      })}
    </div>
  );
}
