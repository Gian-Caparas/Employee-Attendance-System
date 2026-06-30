import api from "./api";
import { User } from "@/types";

export async function login(email: string, password: string): Promise<void> {
  const { data } = await api.post("/api/auth/login", { email, password });
  localStorage.setItem("access_token", data.access_token);
}

export function logout(): void {
  localStorage.removeItem("access_token");
  window.location.href = "/login";
}

export function isAuthenticated(): boolean {
  if (typeof window === "undefined") return false;
  return !!localStorage.getItem("access_token");
}

export async function getCurrentUser(): Promise<User> {
  const { data } = await api.get("/api/auth/me");
  return data;
}
