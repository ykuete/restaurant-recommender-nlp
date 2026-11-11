import type { Metadata } from "next";
import { Suspense } from "react";
import ResultsView from "@/components/ResultsView";

export const metadata: Metadata = { title: "Results" };

export default function ResultsPage() {
  // ResultsView reads the URL (useSearchParams), so it renders in the browser
  // inside a Suspense boundary while the rest of the page is prerendered.
  return (
    <Suspense fallback={<p className="mx-auto max-w-6xl px-6 py-10 text-muted">Loading results…</p>}>
      <ResultsView />
    </Suspense>
  );
}
