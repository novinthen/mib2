import type { ConfidenceClass } from '@/types';

const STYLES: Record<ConfidenceClass, string> = {
  Confirmed: 'bg-green-100 text-green-800 border-green-200',
  Benchmarked: 'bg-blue-100 text-blue-800 border-blue-200',
  Provisional: 'bg-amber-100 text-amber-800 border-amber-200',
};

export const CONFIDENCE_MEANING: Record<ConfidenceClass, string> = {
  Confirmed: 'Published outturn or gazetted figure',
  Benchmarked: 'Benchmarked to a comparable programme or source',
  Provisional: 'Planning assumption pending validation',
};

/** Small chip showing a costing figure's confidence class. */
export default function ConfidenceBadge({
  confidence,
  className = '',
}: {
  confidence: ConfidenceClass;
  className?: string;
}) {
  const style = STYLES[confidence] ?? STYLES.Provisional;
  return (
    <span
      title={CONFIDENCE_MEANING[confidence]}
      className={`inline-flex items-center gap-1.5 text-xs font-semibold px-3 py-1 rounded-full border ${style} ${className}`}
    >
      <span className="w-1.5 h-1.5 rounded-full bg-current opacity-70" aria-hidden />
      {confidence}
    </span>
  );
}
