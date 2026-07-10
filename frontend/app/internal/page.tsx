import Link from "next/link";
import { InternalLeads } from "@/components/InternalLeads";

export default function InternalPage() {
  return (
    <main className="shell">
      <header className="topbar">
        <div className="brand">Alma Legal</div>
        <Link className="nav-link" href="/lead">
          Public intake
        </Link>
      </header>
      <section className="internal-layout">
        <InternalLeads />
      </section>
    </main>
  );
}
