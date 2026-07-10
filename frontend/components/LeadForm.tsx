"use client";

import { FormEvent, useState } from "react";
import { Send } from "lucide-react";
import { submitLead } from "@/lib/api";

export function LeadForm() {
  const [status, setStatus] = useState<"idle" | "saving" | "success" | "error">("idle");
  const [message, setMessage] = useState("");

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = event.currentTarget;
    setStatus("saving");
    setMessage("");

    try {
      await submitLead(new FormData(form));
      form.reset();
      setStatus("success");
      setMessage("Thanks. Your information was submitted and confirmation emails were queued.");
    } catch (error) {
      setStatus("error");
      setMessage(error instanceof Error ? error.message : "Unable to submit lead");
    }
  }

  return (
    <form className="panel" onSubmit={handleSubmit}>
      <h2>Tell us about your matter</h2>
      <label className="field">
        <span>First name</span>
        <input name="first_name" autoComplete="given-name" required />
      </label>
      <label className="field">
        <span>Last name</span>
        <input name="last_name" autoComplete="family-name" required />
      </label>
      <label className="field">
        <span>Email</span>
        <input name="email" type="email" autoComplete="email" required />
      </label>
      <label className="field">
        <span>Resume / CV</span>
        <input name="resume" type="file" accept=".pdf,.doc,.docx" required />
      </label>
      <button className="button" type="submit" disabled={status === "saving"}>
        <Send size={18} aria-hidden="true" />
        {status === "saving" ? "Submitting" : "Submit"}
      </button>
      {message ? <div className={`status ${status === "error" ? "error" : "success"}`}>{message}</div> : null}
    </form>
  );
}
