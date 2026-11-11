import Link from "next/link";

export function LogoMark({ size = 28 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 32 32" aria-hidden="true">
      <circle cx="14" cy="14" r="10" fill="none" stroke="#B93815" strokeWidth="3" />
      <path d="M21.5 21.5 29 29" stroke="currentColor" strokeWidth="3" strokeLinecap="round" />
      <path
        d="M10 11v6M14 10v8M18 11v6"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
      />
    </svg>
  );
}

export default function Logo() {
  return (
    <Link href="/" className="flex items-center gap-2.5 text-ink no-underline">
      <LogoMark />
      <span className="font-display text-xl font-bold tracking-tight">TasteLens</span>
    </Link>
  );
}
