import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Employee Attendance & Tardiness Management System",
  description: "HR platform for attendance, tardiness, leave, and reporting.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
