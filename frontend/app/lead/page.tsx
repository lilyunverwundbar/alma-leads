import Link from "next/link";
import { LeadForm } from "@/components/LeadForm";

export default function LeadPage() {
  return (
    <main className="shell">
      <header className="topbar">
        <div className="brand">Alma Legal</div>
        <Link className="nav-link" href="/internal">
          Attorney portal
        </Link>
      </header>
      <section className="lead-layout">
        <div className="hero">
          <h1>Alma Legal Intake</h1>
          <p>Share your contact details and CV so our attorneys can review your background and follow up.</p>
        </div>
        <LeadForm />
      </section>
    </main>
  );
}
