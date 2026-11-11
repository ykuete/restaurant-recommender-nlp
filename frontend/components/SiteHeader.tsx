import Link from "next/link";
import Logo from "@/components/Logo";

export default function SiteHeader() {
  return (
    <header className="border-b border-line bg-white">
      <div className="mx-auto flex max-w-6xl flex-wrap items-center justify-between gap-4 px-6 py-4">
        <Logo />
        <nav aria-label="Main" className="flex flex-wrap items-center gap-2">
          <Link
            href="/#how"
            className="rounded-full px-3.5 py-2.5 font-medium text-subtle hover:text-ink"
          >
            How it works
          </Link>
          <Link
            href="/#about"
            className="rounded-full px-3.5 py-2.5 font-medium text-subtle hover:text-ink"
          >
            About the data
          </Link>
        </nav>
      </div>
    </header>
  );
}
