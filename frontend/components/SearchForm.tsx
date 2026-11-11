"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { toSearchParams } from "@/lib/format";
import type { DietaryOption } from "@/lib/types";

export const CITIES = [
  "Philadelphia",
  "Tampa",
  "Indianapolis",
  "Nashville",
  "Tucson",
  "New Orleans",
  "Saint Louis",
  "Reno",
  "Edmonton",
  "Boise",
];
export const CUISINES = [
  "Italian",
  "Mexican",
  "Japanese",
  "Chinese",
  "Thai",
  "Indian",
  "Mediterranean",
  "American (New)",
  "Breakfast & Brunch",
  "Pizza",
  "Seafood",
];
const PRICES = [1, 2, 3, 4];
const DIETS: { value: DietaryOption; label: string }[] = [
  { value: "vegetarian", label: "Vegetarian" },
  { value: "vegan", label: "Vegan" },
  { value: "gluten-free", label: "Gluten-free" },
  { value: "halal", label: "Halal" },
];
const EXAMPLES = [
  "quiet date-night spot with great pasta",
  "fast, cheap lunch near work",
  "brunch with great coffee and no long wait",
  "vegan-friendly tacos",
  "lively place for a group birthday",
];

const chip = (on: boolean) =>
  `min-h-11 rounded-full px-4 py-2 font-semibold cursor-pointer border ${
    on ? "border-ink bg-ink text-white" : "border-field bg-white text-ink hover:border-ink"
  }`;

function toggle<T>(list: T[], value: T): T[] {
  return list.includes(value) ? list.filter((v) => v !== value) : [...list, value];
}

export default function SearchForm() {
  const router = useRouter();
  const [query, setQuery] = useState("");
  const [city, setCity] = useState("Philadelphia");
  const [cuisine, setCuisine] = useState("");
  const [price, setPrice] = useState<number[]>([]);
  const [dietary, setDietary] = useState<DietaryOption[]>([]);
  const [error, setError] = useState("");

  function submit(event: React.FormEvent) {
    event.preventDefault();
    if (query.trim().length < 2) {
      setError("Describe what you are looking for, e.g. “cozy brunch with good coffee”.");
      return;
    }
    const params = toSearchParams({ query: query.trim(), city, cuisine, price, dietary });
    router.push(`/results?${params}`);
  }

  return (
    <div className="max-w-4xl">
      <form
        onSubmit={submit}
        className="rounded-2xl border-2 border-ink bg-white p-5 shadow-[0_1px_0_#15171a]"
      >
        <label htmlFor="q" className="mb-2 block text-sm font-semibold">
          What are you looking for?
        </label>
        <textarea
          id="q"
          rows={2}
          maxLength={300}
          value={query}
          onChange={(e) => {
            setQuery(e.target.value);
            setError("");
          }}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              e.currentTarget.form?.requestSubmit();
            }
          }}
          placeholder="e.g. quiet date-night spot with great pasta"
          aria-describedby={error ? "q-error" : undefined}
          aria-invalid={Boolean(error)}
          className="w-full resize-none bg-transparent text-xl leading-snug text-ink outline-none placeholder:text-muted/70 md:text-2xl"
        />
        {error && (
          <p id="q-error" role="alert" className="mt-2 text-sm font-medium text-accent-dark">
            {error}
          </p>
        )}
        <div className="mt-4 flex flex-wrap items-end justify-between gap-3 border-t border-line pt-4">
          <div className="flex flex-wrap gap-3">
            <div className="flex flex-col gap-1">
              <label htmlFor="city" className="text-xs font-semibold text-muted">
                City
              </label>
              <select
                id="city"
                value={city}
                onChange={(e) => setCity(e.target.value)}
                className="min-h-11 rounded-lg border border-field bg-white px-3"
              >
                {CITIES.map((c) => (
                  <option key={c}>{c}</option>
                ))}
                <option value="">Any city</option>
              </select>
            </div>
            <div className="flex flex-col gap-1">
              <label htmlFor="cuisine" className="text-xs font-semibold text-muted">
                Cuisine
              </label>
              <select
                id="cuisine"
                value={cuisine}
                onChange={(e) => setCuisine(e.target.value)}
                className="min-h-11 rounded-lg border border-field bg-white px-3"
              >
                <option value="">Any cuisine</option>
                {CUISINES.map((c) => (
                  <option key={c}>{c}</option>
                ))}
              </select>
            </div>
          </div>
          <button
            type="submit"
            className="inline-flex min-h-11 items-center gap-2 rounded-full bg-accent px-6 py-3 text-lg font-semibold text-white hover:bg-accent-dark"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" aria-hidden="true">
              <circle cx="11" cy="11" r="7" />
              <path d="m20 20-4-4" />
            </svg>
            Find restaurants
          </button>
        </div>
      </form>

      <div className="mt-6 flex flex-wrap gap-6">
        <fieldset>
          <legend className="mb-2 text-sm font-semibold text-muted">Budget</legend>
          <div className="flex gap-2">
            {PRICES.map((p) => (
              <button
                key={p}
                type="button"
                aria-pressed={price.includes(p)}
                onClick={() => setPrice(toggle(price, p))}
                className={`${chip(price.includes(p))} min-w-13`}
              >
                {"$".repeat(p)}
              </button>
            ))}
          </div>
        </fieldset>
        <fieldset>
          <legend className="mb-2 text-sm font-semibold text-muted">Dietary needs</legend>
          <div className="flex flex-wrap gap-2">
            {DIETS.map((d) => (
              <button
                key={d.value}
                type="button"
                aria-pressed={dietary.includes(d.value)}
                onClick={() => setDietary(toggle(dietary, d.value))}
                className={chip(dietary.includes(d.value))}
              >
                {d.label}
              </button>
            ))}
          </div>
        </fieldset>
      </div>

      <div className="mt-8">
        <p className="mb-2.5 text-sm font-semibold text-muted">Try one of these</p>
        <div className="flex flex-wrap gap-2.5">
          {EXAMPLES.map((text) => (
            <button
              key={text}
              type="button"
              onClick={() => {
                setQuery(text);
                setError("");
              }}
              className="min-h-11 rounded-xl border border-line bg-surface px-4 py-2.5 text-left text-[15px] hover:border-ink"
            >
              “{text}”
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
