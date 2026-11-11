"use client";

import Link from "next/link";
import { useParams, useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";
import FeedbackButtons from "@/components/FeedbackButtons";
import { getRestaurant } from "@/lib/api";
import { formatCount, priceLabel } from "@/lib/format";
import type { RestaurantDetail } from "@/lib/types";

export default function DetailView() {
  const { id } = useParams<{ id: string }>();
  const query = useSearchParams().get("q") ?? "";
  const [state, setState] = useState<{ id: string; data?: RestaurantDetail; error?: string }>({
    id: "",
  });
  const [tab, setTab] = useState("all");

  useEffect(() => {
    let cancelled = false;
    getRestaurant(id).then(
      (data) => !cancelled && setState({ id, data }),
      (err: Error) => !cancelled && setState({ id, error: err.message }),
    );
    return () => {
      cancelled = true;
    };
  }, [id]);

  const backHref = query ? `/results?q=${encodeURIComponent(query)}` : "/";
  const loading = state.id !== id;
  const r = state.data;

  if (loading)
    return (
      <div aria-busy="true" className="mx-auto max-w-6xl animate-pulse space-y-6 px-6 py-10">
        <span className="sr-only">Loading restaurant…</span>
        <div className="h-48 rounded-3xl bg-surface-strong" />
        <div className="grid gap-4 sm:grid-cols-3">
          <div className="h-28 rounded-2xl bg-white" />
          <div className="h-28 rounded-2xl bg-white" />
          <div className="h-28 rounded-2xl bg-white" />
        </div>
      </div>
    );
  if (state.error || !r)
    return (
      <div role="alert" className="mx-auto max-w-6xl px-6 py-10">
        <div className="rounded-3xl border border-[#f2c4b0] bg-[#fdf1ea] p-8">
          <h1 className="font-display text-2xl font-bold">Restaurant unavailable</h1>
          <p className="mt-2 text-subtle">{state.error}</p>
          <Link href={backHref} className="mt-5 inline-flex min-h-11 items-center font-semibold text-accent">
            {query ? "Back to results" : "New search"}
          </Link>
        </div>
      </div>
    );

  const tabs = ["all", ...new Set(r.snippets.map((s) => s.aspect))];
  const label = (key: string) =>
    key === "all" ? "All" : (r.snippets.find((s) => s.aspect === key)?.label ?? key);
  const shown = tab === "all" ? r.snippets : r.snippets.filter((s) => s.aspect === tab);
  const meta = [r.categories.slice(0, 2).join(", "), priceLabel(r.price), `${r.city}, ${r.state}`]
    .filter(Boolean)
    .join(" · ");

  return (
    <div className="mx-auto flex max-w-6xl flex-col gap-6 px-6 pb-16 pt-6">
      <Link href={backHref} className="inline-flex min-h-11 items-center gap-2 self-start font-semibold text-accent">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
          <path d="M15 18l-6-6 6-6" />
        </svg>
        {query ? "Back to results" : "New search"}
      </Link>

      <section className="flex flex-wrap items-end justify-between gap-8 rounded-3xl bg-ink p-8 text-white md:p-9">
        <div className="min-w-0 flex-[1_1_480px]">
          {query && <p className="mb-2.5 text-sm text-[#c9ccd1]">Recommended for “{query}”</p>}
          <h1 className="font-display text-4xl font-bold leading-[1.05] tracking-tight md:text-6xl">
            {r.name}
          </h1>
          <p className="mt-2.5 text-[17px] text-[#e3e5e8]">{meta}</p>
          <p className="mt-4 inline-block rounded-full bg-[#2a2d33] px-3 py-1.5 text-sm">
            <span className="text-accent-light" aria-hidden="true">★</span> {r.stars.toFixed(1)} on Yelp ·{" "}
            {formatCount(r.review_count)} reviews
          </p>
        </div>
      </section>

      {query && (
        <section className="flex flex-wrap items-center justify-between gap-3 rounded-3xl border border-line bg-white p-6">
          <p className="font-semibold">Was this a good recommendation for “{query}”?</p>
          <FeedbackButtons businessId={r.business_id} query={query} label="Rate it" />
        </section>
      )}

      <section aria-labelledby="ap-h">
        <h2 id="ap-h" className="font-display text-3xl font-bold tracking-tight">
          Aspect profile
        </h2>
        <p className="mb-4 mt-1 text-muted">
          Share of review sentences about each aspect that are positive.
        </p>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {r.aspects.map((a) => (
            <div key={a.key} className="rounded-2xl border border-line bg-white p-5">
              <div className="flex items-baseline justify-between">
                <h3 className="text-[17px] font-semibold">{a.label}</h3>
                <span className="font-display text-3xl font-bold">{a.positive}%</span>
              </div>
              <div
                className="mt-2.5 h-2.5 overflow-hidden rounded bg-negative-soft"
                role="img"
                aria-label={`${a.positive}% positive, ${a.negative}% negative`}
              >
                <div className="h-2.5 bg-positive" style={{ width: `${a.positive}%` }} />
              </div>
              <p className="mt-2 text-sm text-muted">
                {formatCount(a.mentions)} mentions · {a.negative}% negative
              </p>
            </div>
          ))}
        </div>
      </section>

      <section aria-labelledby="rv-h" className="rounded-3xl border border-line bg-white p-7">
        <div className="flex flex-wrap items-end justify-between gap-4">
          <div>
            <h2 id="rv-h" className="font-display text-3xl font-bold tracking-tight">
              What reviewers said
            </h2>
            <p className="mt-1 text-muted">Sentences behind the scores, tagged by aspect and sentiment.</p>
          </div>
          <div role="group" aria-label="Filter by aspect" className="flex flex-wrap gap-2">
            {tabs.map((t) => (
              <button
                key={t}
                type="button"
                aria-pressed={tab === t}
                onClick={() => setTab(t)}
                className={`min-h-11 rounded-full px-4 text-sm ${
                  tab === t
                    ? "border-2 border-ink bg-ink font-semibold text-white"
                    : "border border-field bg-white font-medium hover:border-ink"
                }`}
              >
                {label(t)}
              </button>
            ))}
          </div>
        </div>
        <ul className="mt-5 flex flex-col gap-3">
          {shown.map((s) => (
            <li key={s.text} className="flex flex-wrap items-start gap-x-4 gap-y-3 rounded-2xl bg-surface p-4">
              <span
                className={`flex-none rounded-full px-2.5 py-1 text-[13px] font-semibold ${
                  s.sentiment === "positive"
                    ? "bg-positive-soft text-positive-dark"
                    : "bg-[#fbe5d6] text-negative-text"
                }`}
              >
                {s.label} · {s.sentiment}
              </span>
              <p className="min-w-0 flex-[1_1_360px] text-ink-soft">“{s.text}”</p>
              <span className="text-[13px] text-muted">
                {s.stars}★ review · {s.year}
              </span>
            </li>
          ))}
          {shown.length === 0 && <li className="text-muted">No review sentences for this aspect yet.</li>}
        </ul>
      </section>

      {r.similar.length > 0 && (
        <section aria-labelledby="sim-h">
          <h2 id="sim-h" className="mb-4 font-display text-2xl font-bold tracking-tight">
            Similar by review content
          </h2>
          <div className="grid gap-4 sm:grid-cols-3">
            {r.similar.map((s) => (
              <Link
                key={s.business_id}
                href={`/restaurants/${encodeURIComponent(s.business_id)}${query ? `?q=${encodeURIComponent(query)}` : ""}`}
                className="block rounded-2xl border border-line bg-white p-5 text-ink hover:border-ink"
              >
                <p className="text-[17px] font-semibold">{s.name}</p>
                <p className="mt-0.5 text-sm text-muted">
                  {[s.categories[0], priceLabel(s.price), `${s.stars.toFixed(1)} ★`].filter(Boolean).join(" · ")}
                </p>
              </Link>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
