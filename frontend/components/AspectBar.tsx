import type { AspectScore } from "@/lib/types";

/** Positive share of an aspect's mentions: dark green on a light orange track. */
export default function AspectBar({
  aspect,
  highlight = false,
}: {
  aspect: AspectScore;
  highlight?: boolean;
}) {
  return (
    <div>
      <div className="flex justify-between text-sm">
        <span className={highlight ? "font-semibold" : undefined}>{aspect.label}</span>
        <span className="font-semibold">{aspect.positive}%</span>
      </div>
      <div
        className="mt-1 h-2 overflow-hidden rounded bg-negative-soft"
        role="img"
        aria-label={`${aspect.label}: ${aspect.positive}% positive from ${aspect.mentions} mentions`}
      >
        <div className="h-2 rounded bg-positive" style={{ width: `${aspect.positive}%` }} />
      </div>
    </div>
  );
}
