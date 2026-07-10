"use client";

import { FormEvent, useEffect, useState } from "react";
import { CheckCircle, LogIn, RefreshCw } from "lucide-react";
import { fetchLeads, Lead, login, markReachedOut } from "@/lib/api";

const TOKEN_KEY = "alma_internal_token";

export function InternalLeads() {
  const [token, setToken] = useState("");
  const [leads, setLeads] = useState<Lead[]>([]);
  const [status, setStatus] = useState<"idle" | "loading" | "error">("idle");
  const [message, setMessage] = useState("");

  useEffect(() => {
    const stored = window.localStorage.getItem(TOKEN_KEY);
    if (stored) {
      setToken(stored);
      void loadLeads(stored);
    }
  }, []);

  async function loadLeads(activeToken = token) {
    if (!activeToken) return;
    setStatus("loading");
    setMessage("");
    try {
      setLeads(await fetchLeads(activeToken));
      setStatus("idle");
    } catch (error) {
      setStatus("error");
      setMessage(error instanceof Error ? error.message : "Unable to load leads");
    }
  }

  async function handleLogin(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    setStatus("loading");
    setMessage("");
    try {
      const newToken = await login(String(formData.get("username")), String(formData.get("password")));
      window.localStorage.setItem(TOKEN_KEY, newToken);
      setToken(newToken);
      await loadLeads(newToken);
    } catch (error) {
      setStatus("error");
      setMessage(error instanceof Error ? error.message : "Unable to sign in");
    }
  }

  async function handleReachedOut(leadId: number) {
    const updated = await markReachedOut(token, leadId);
    setLeads((current) => current.map((lead) => (lead.id === leadId ? updated : lead)));
  }

  if (!token) {
    return (
      <form className="panel" onSubmit={handleLogin}>
        <h2>Attorney sign in</h2>
        <label className="field">
          <span>Email</span>
          <input name="username" type="email" autoComplete="username" required />
        </label>
        <label className="field">
          <span>Password</span>
          <input name="password" type="password" autoComplete="current-password" required />
        </label>
        <button className="button" type="submit" disabled={status === "loading"}>
          <LogIn size={18} aria-hidden="true" />
          Sign in
        </button>
        {message ? <div className="status error">{message}</div> : null}
      </form>
    );
  }

  return (
    <section className="panel">
      <div className="toolbar">
        <h2>Lead queue</h2>
        <button className="button secondary" type="button" onClick={() => loadLeads()} disabled={status === "loading"}>
          <RefreshCw size={18} aria-hidden="true" />
          Refresh
        </button>
      </div>
      {message ? <div className="status error">{message}</div> : null}
      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Resume</th>
              <th>Submitted</th>
              <th>State</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {leads.map((lead) => (
              <tr key={lead.id}>
                <td>
                  {lead.first_name} {lead.last_name}
                </td>
                <td>{lead.email}</td>
                <td>{lead.resume_filename}</td>
                <td>{new Date(lead.created_at).toLocaleString()}</td>
                <td>
                  <span className={`badge ${lead.state === "PENDING" ? "pending" : "reached"}`}>{lead.state}</span>
                </td>
                <td>
                  <button
                    className="button secondary"
                    type="button"
                    onClick={() => handleReachedOut(lead.id)}
                    disabled={lead.state === "REACHED_OUT"}
                  >
                    <CheckCircle size={18} aria-hidden="true" />
                    Reached out
                  </button>
                </td>
              </tr>
            ))}
            {leads.length === 0 ? (
              <tr>
                <td colSpan={6}>No leads yet.</td>
              </tr>
            ) : null}
          </tbody>
        </table>
      </div>
    </section>
  );
}
