import type { Metadata } from "next";
import { Suspense } from "react";
import DetailView from "@/components/DetailView";

export const metadata: Metadata = { title: "Restaurant" };

export default function RestaurantPage() {
  // DetailView reads the id and the query from the URL, so it renders in
  // the browser inside a Suspense boundary.
  return (
    <Suspense fallback={<p className="mx-auto max-w-6xl px-6 py-10 text-muted">Loading restaurant…</p>}>
      <DetailView />
    </Suspense>
  );
}
