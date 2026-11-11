"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { useEffect, useMemo, useState } from "react";
import RestaurantCard from "@/components/RestaurantCard";
import SearchBar from "@/components/SearchBar";
import { recommend } from "@/lib/api";
import { aspectLabel } from "@/lib/aspects";
import { fromSearchParams, priceLabel } from "@/lib/format";
import type { RecommendResponse, RestaurantResult } from "@/lib/types";

type Sort = "match" | "stars" | "reviews";
const SORTS: { value: Sort; label: string }[] = [
  { value: "match", label: "Best match" },
  { value: "stars", label: "Top rated" },
  { value: "reviews", label: "Most reviewed" },
];
const sortKey: Record<Sort, (r: RestaurantResult) => number> = {
  match: (r) => r.match,
  stars: (r) => r.stars,
  reviews: (r) => r.review_count,
};

export default function ResultsView() {
  const params = useSearchParams();
  const key = params.toString();
  const req = useMemo(() => fromSearchParams(new URLSearchParams(key)), [key]);

  const [state, setState] = useState<{ key: string; data?: RecommendResponse; error?: string }>({
    key: "",
  });
  const [sort, setSort] = useState<Sort>("match");
  const [showBaseline, setShowBaseline] = useState(false);

  useEffect(() => {
    let cancelled = false;
    recommend({ ...req, k: 10 }).then(
      (data) => !cancelled && setState({ key, data }),
      (err: Error) => !cancelled && setState({ key, error: err.message }),
    );
    return () => {
      cancelled = true;
    };
  }, [key, req]);

  const loading = state.key !== key;
  const results = [...(state.data?.results ?? [])].sort((a, b) => sortKey[sort](b) - sortKey[sort](a));
  const filters = [
    req.city,
    req.cuisine,
    req.price?.length ? req.price.map((p) => priceLabel(p)).join(", ") : null,
    ...(req.dietary ?? []),
  ].filter(Boolean) as string[];

  return (
    <>
      <div className="border-b border-line bg-white">
        <div className="mx-auto max-w-6xl px-6 py-3">
          <SearchBar key={req.query} initialQuery={req.query} />
        </div>
      </div>

      <div className="mx-auto flex max-w-6xl flex-wrap items-start gap-7 px-6 pb-16 pt-8">
        <aside className="flex max-w-full flex-[1_1_280px] flex-col gap-5">
          <section className="rounded-2xl border border-line bg-white p-5">
            <h2 className="mb-1 font-semibold">How we read your request</h2>
            <p className="mb-3 text-sm text-muted">Aspects found in your words weigh most in the ranking.</p>
            <div className="flex flex-wrap gap-2">
              {(state.data?.query_aspects ?? []).map((a) => (
                <span key={a} className="rounded-full bg-surface-strong px-3 py-1.5 text-sm font-medium">
                  {aspectLabel(a)}
                </span>
              ))}
              {state.data && state.data.query_aspects.length === 0 && (
                <span className="text-sm text-muted">No specific aspect: overall match only.</span>
              )}
            </div>
          </section>

          <section className="rounded-2xl border border-line bg-white p-5">
            <h2 className="mb-3 font-semibold">Filters</h2>
            <div className="flex flex-wrap gap-2">
              {filters.map((f) => (
                <span key={f} className="rounded-full bg-ink px-3 py-1.5 text-sm font-medium text-white">
                  {f}
                </span>
              ))}
              {filters.length === 0 && <span className="text-sm text-muted">None</span>}
            </div>
            <Link href="/" className="mt-3.5 inline-block text-sm font-semibold text-accent">
              Edit filters
            </Link>
          </section>

          <section className="rounded-2xl border border-line bg-white p-5">
            <label className="flex cursor-pointer items-start gap-3">
              <input
                type="checkbox"
                checked={showBaseline}
                onChange={() => setShowBaseline(!showBaseline)}
                className="mt-0.5 size-5 accent-ink"
              />
              <span>
                <span className="block font-semibold">Compare with popularity baseline</span>
                <span className="block text-sm text-muted">
                  Top restaurants by weighted star rating alone, ignoring your request.
                </span>
              </span>
            </label>
            {showBaseline && (
              <ol className="mt-3.5 list-decimal space-y-1.5 pl-5 text-sm text-subtle">
                {(state.data?.baseline ?? []).map((b) => (
                  <li key={b.business_id}>
                    {b.name} · {b.stars.toFixed(1)} ★
                  </li>
                ))}
              </ol>
            )}
          </section>
        </aside>

        <section aria-labelledby="res-h" className="min-w-0 flex-[999_1_560px]">
          <div className="mb-5 flex flex-wrap items-end justify-between gap-4">
            <div>
              <h1 id="res-h" className="font-display text-3xl font-bold tracking-tight">
                {loading ? "Searching…" : `${results.length} matches`}
              </h1>
              <p className="text-muted">for “{req.query}”</p>
            </div>
            <div role="group" aria-label="Sort results" className="flex gap-1 rounded-full bg-surface-strong p-1">
              {SORTS.map((s) => (
                <button
                  key={s.value}
                  type="button"
                  aria-pressed={sort === s.value}
                  onClick={() => setSort(s.value)}
                  className={`min-h-10 rounded-full px-3.5 text-sm ${
                    sort === s.value ? "bg-white font-semibold text-ink shadow-sm" : "font-medium text-subtle"
                  }`}
                >
                  {s.label}
                </button>
              ))}
            </div>
          </div>

          {loading && <p className="text-muted">Loading results…</p>}
          {!loading && state.error && <p role="alert">{state.error}</p>}
          {!loading && !state.error && (
            <ol className="flex flex-col gap-4.5">
              {results.map((r, i) => (
                <RestaurantCard key={r.business_id} result={r} rank={i + 1} query={req.query} />
              ))}
            </ol>
          )}
        </section>
      </div>
    </>
  );
}
