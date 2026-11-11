import Link from "next/link";

/** Grey placeholder cards shown while results load. */
export function ResultsSkeleton({ count = 3 }: { count?: number }) {
  return (
    <ol aria-hidden="true" className="flex flex-col gap-4.5">
      {Array.from({ length: count }, (_, i) => (
        <li key={i} className="flex animate-pulse flex-wrap gap-6 rounded-3xl border border-line bg-white p-6">
          <div className="flex-[1_1_320px] space-y-3">
            <div className="h-7 w-2/3 rounded bg-surface-strong" />
            <div className="h-4 w-1/3 rounded bg-surface-strong" />
            <div className="h-20 rounded-2xl bg-surface" />
          </div>
          <div className="flex-[0_1_280px] space-y-3">
            <div className="h-11 w-24 rounded bg-surface-strong" />
            <div className="h-2 rounded bg-surface-strong" />
            <div className="h-2 rounded bg-surface-strong" />
            <div className="h-2 rounded bg-surface-strong" />
          </div>
        </li>
      ))}
    </ol>
  );
}

export function EmptyState({ hasFilters }: { hasFilters: boolean }) {
  return (
    <div className="rounded-3xl border border-line bg-white p-8 text-center">
      <h2 className="font-display text-2xl font-bold">No matches</h2>
      <p className="mx-auto mt-2 max-w-md text-muted">
        {hasFilters
          ? "No restaurant fits every filter. Try removing one, or choose “Any city”."
          : "Try describing the meal differently, for example the dish, the mood or the budget."}
      </p>
      <Link
        href="/"
        className="mt-5 inline-flex min-h-11 items-center rounded-full bg-ink px-5 font-semibold text-white"
      >
        {hasFilters ? "Edit filters" : "New search"}
      </Link>
    </div>
  );
}

export function ErrorState({ message, onRetry }: { message: string; onRetry: () => void }) {
  return (
    <div role="alert" className="rounded-3xl border border-[#f2c4b0] bg-[#fdf1ea] p-8">
      <h2 className="font-display text-2xl font-bold">Something went wrong</h2>
      <p className="mt-2 text-subtle">{message}</p>
      <p className="mt-1 text-sm text-muted">
        If the service was asleep, the first search can take up to a minute.
      </p>
      <button
        type="button"
        onClick={onRetry}
        className="mt-5 inline-flex min-h-11 items-center rounded-full bg-accent px-5 font-semibold text-white hover:bg-accent-dark"
      >
        Try again
      </button>
    </div>
  );
}
