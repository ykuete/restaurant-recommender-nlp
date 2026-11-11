import Link from "next/link";
import AspectBar from "@/components/AspectBar";
import { formatCount, priceLabel } from "@/lib/format";
import type { RestaurantResult } from "@/lib/types";

export default function RestaurantCard({
  result,
  rank,
  query,
  children,
}: {
  result: RestaurantResult;
  rank: number;
  query: string;
  children?: React.ReactNode;
}) {
  const meta = [result.categories.slice(0, 2).join(", "), priceLabel(result.price), result.city]
    .filter(Boolean)
    .join(" · ");
  // Show the aspects the query asked about first, then the rest.
  const aspects = [...result.aspects]
    .sort(
      (a, b) =>
        Number(result.query_aspects.includes(b.key)) - Number(result.query_aspects.includes(a.key)),
    )
    .slice(0, 5);

  return (
    <li className="flex flex-wrap gap-6 rounded-3xl border border-line bg-white p-6">
      <div className="min-w-0 flex-[1_1_320px]">
        <div className="flex items-start gap-3.5">
          <span className="flex size-10 flex-none items-center justify-center rounded-xl bg-ink font-display text-lg font-bold text-white">
            {rank}
          </span>
          <div className="min-w-0">
            <h2 className="font-display text-2xl font-bold tracking-tight">{result.name}</h2>
            <p className="text-[15px] text-muted">{meta}</p>
            <p className="mt-1 text-sm text-subtle">
              <span className="text-accent" aria-hidden="true">
                ★
              </span>{" "}
              {result.stars.toFixed(1)} on Yelp · {formatCount(result.review_count)} reviews
            </p>
          </div>
        </div>

        <div className="mt-4 rounded-2xl bg-surface p-4">
          <p className="mb-1.5 text-xs font-semibold uppercase tracking-wider text-muted">
            Why it matches · AI summary
          </p>
          <p className="text-[15px] text-ink-soft">{result.summary}</p>
        </div>

        {result.snippet && (
          <blockquote className="mt-3.5 border-l-[3px] border-line pl-3.5 text-sm text-subtle">
            “{result.snippet.text}”{" "}
            <span className="text-muted">· {result.snippet.stars}★ review</span>
          </blockquote>
        )}

        <div className="mt-4 flex flex-wrap items-center gap-2.5">
          <Link
            href={`/restaurants/${encodeURIComponent(result.business_id)}?q=${encodeURIComponent(query)}`}
            className="inline-flex min-h-11 items-center rounded-full border-2 border-ink px-4.5 font-semibold text-ink"
          >
            View details
          </Link>
          {children}
        </div>
      </div>

      <div className="flex min-w-60 flex-[0_1_280px] flex-col gap-3.5">
        <p className="flex items-baseline gap-2">
          <span className="font-display text-5xl font-bold leading-none text-accent">
            {result.match}%
          </span>
          <span className="text-sm font-medium text-muted">match to your request</span>
        </p>
        <p className="text-xs font-semibold uppercase tracking-wider text-muted">
          Positive mentions by aspect
        </p>
        {aspects.map((a) => (
          <AspectBar key={a.key} aspect={a} highlight={result.query_aspects.includes(a.key)} />
        ))}
        {aspects.length === 0 && (
          <p className="text-sm text-muted">Not enough reviews to score aspects yet.</p>
        )}
      </div>
    </li>
  );
}
