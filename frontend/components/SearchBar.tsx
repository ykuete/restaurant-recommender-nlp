"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { useState } from "react";

/** Compact search box for the results page; keeps the current filters. */
export default function SearchBar({ initialQuery }: { initialQuery: string }) {
  const router = useRouter();
  const params = useSearchParams();
  const [query, setQuery] = useState(initialQuery);

  function submit(event: React.FormEvent) {
    event.preventDefault();
    if (query.trim().length < 2) return;
    const next = new URLSearchParams(params.toString());
    next.set("q", query.trim());
    router.push(`/results?${next}`);
  }

  return (
    <form
      role="search"
      onSubmit={submit}
      className="flex items-center gap-2 rounded-full border-2 border-ink bg-white py-1 pl-4.5 pr-1"
    >
      <label htmlFor="q2" className="sr-only">
        Search
      </label>
      <input
        id="q2"
        value={query}
        maxLength={300}
        onChange={(e) => setQuery(e.target.value)}
        className="min-h-10 min-w-0 flex-1 bg-transparent outline-none"
      />
      <button
        type="submit"
        className="rounded-full bg-accent px-5 py-2.5 font-semibold text-white hover:bg-accent-dark"
      >
        Search
      </button>
    </form>
  );
}
