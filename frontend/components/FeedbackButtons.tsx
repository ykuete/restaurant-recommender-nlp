"use client";

import { useState } from "react";
import { sendFeedback } from "@/lib/api";

const thumb = (
  <path d="M7 11v9H4v-9zM7 11l4-8a2 2 0 0 1 2 2v4h5.5a2 2 0 0 1 2 2.3l-1.2 7A2 2 0 0 1 17.3 20H7" />
);

/** "Was this helpful?" -> POST /api/feedback, used to evaluate the ranking. */
export default function FeedbackButtons({
  businessId,
  query,
  label = "Was this helpful?",
}: {
  businessId: string;
  query: string;
  label?: string;
}) {
  const [status, setStatus] = useState<"idle" | "sending" | "saved" | "error">("idle");

  async function rate(helpful: boolean) {
    setStatus("sending");
    try {
      await sendFeedback({ business_id: businessId, query, helpful });
      setStatus("saved");
    } catch {
      setStatus("error");
    }
  }

  if (status === "saved")
    return (
      <span role="status" className="text-sm font-semibold text-positive">
        Thanks, feedback saved
      </span>
    );

  const button =
    "inline-flex size-11 items-center justify-center rounded-full border border-field bg-white text-ink hover:border-ink disabled:opacity-50";
  return (
    <span className="inline-flex items-center gap-2.5">
      <span className="text-sm text-muted">
        {status === "error" ? "Could not send. Try again?" : label}
      </span>
      <button type="button" aria-label="Helpful" disabled={status === "sending"} onClick={() => rate(true)} className={button}>
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
          {thumb}
        </svg>
      </button>
      <button type="button" aria-label="Not helpful" disabled={status === "sending"} onClick={() => rate(false)} className={button}>
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true" className="rotate-180">
          {thumb}
        </svg>
      </button>
    </span>
  );
}
