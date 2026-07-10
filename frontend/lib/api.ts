export type LeadState = "PENDING" | "REACHED_OUT";

export type Lead = {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
  resume_filename: string;
  state: LeadState;
  created_at: string;
  updated_at: string;
};

export const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000/api";

async function parseJson<T>(response: Response): Promise<T> {
  if (!response.ok) {
    let message = "Request failed";
    try {
      const payload = await response.json();
      message = payload.detail ?? message;
    } catch {
      message = response.statusText || message;
    }
    throw new Error(Array.isArray(message) ? message.map((item) => item.msg).join(", ") : message);
  }
  return response.json() as Promise<T>;
}

export async function submitLead(formData: FormData): Promise<Lead> {
  const response = await fetch(`${API_BASE_URL}/leads`, {
    method: "POST",
    body: formData,
  });
  return parseJson<Lead>(response);
}

export async function login(username: string, password: string): Promise<string> {
  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });
  const payload = await parseJson<{ access_token: string }>(response);
  return payload.access_token;
}

export async function fetchLeads(token: string): Promise<Lead[]> {
  const response = await fetch(`${API_BASE_URL}/leads`, {
    headers: { Authorization: `Bearer ${token}` },
    cache: "no-store",
  });
  return parseJson<Lead[]>(response);
}

export async function markReachedOut(token: string, leadId: number): Promise<Lead> {
  const response = await fetch(`${API_BASE_URL}/leads/${leadId}`, {
    method: "PATCH",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ state: "REACHED_OUT" }),
  });
  return parseJson<Lead>(response);
}
