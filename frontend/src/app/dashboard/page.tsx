"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Users, UserCheck, Clock, UserX, CalendarOff } from "lucide-react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
} from "recharts";

import Sidebar from "@/components/Sidebar";
import Header from "@/components/Header";
import StatCard from "@/components/StatCard";
import api from "@/lib/api";
import { isAuthenticated } from "@/lib/auth";
import { KPIs } from "@/types";

export default function DashboardPage() {
  const router = useRouter();
  const [kpis, setKpis] = useState<KPIs | null>(null);
  const [trends, setTrends] = useState<any[]>([]);
  const [departments, setDepartments] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!isAuthenticated()) {
      router.replace("/login");
      return;
    }
    loadData();
  }, [router]);

  async function loadData() {
    try {
      const [kpiRes, trendsRes, deptRes] = await Promise.all([
        api.get("/api/analytics/kpis"),
        api.get("/api/analytics/trends?days=14"),
        api.get("/api/analytics/department-breakdown"),
      ]);
      setKpis(kpiRes.data);
      setTrends(trendsRes.data);
      setDepartments(deptRes.data);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex">
      <Sidebar />
      <main className="flex-1 ml-64 p-8">
        <Header title="Dashboard" subtitle="Overview of today's attendance" />

        {loading ? (
          <p className="text-muted">Loading...</p>
        ) : (
          <>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 mb-8">
              <StatCard label="Total Employees" value={kpis?.total_employees ?? 0} icon={Users} accentColor="#6366f1" />
              <StatCard label="Present Today" value={kpis?.present_today ?? 0} icon={UserCheck} accentColor="#22c55e" />
              <StatCard label="Late Today" value={kpis?.late_today ?? 0} icon={Clock} accentColor="#eab308" />
              <StatCard label="Absent Today" value={kpis?.absent_today ?? 0} icon={UserX} accentColor="#ef4444" />
              <StatCard label="On Leave" value={kpis?.on_leave_today ?? 0} icon={CalendarOff} accentColor="#a855f7" />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="bg-surface border border-border rounded-xl p-5">
                <h3 className="text-white font-medium mb-4">Attendance Trend (last 14 days)</h3>
                <ResponsiveContainer width="100%" height={260}>
                  <LineChart data={trends}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#252932" />
                    <XAxis dataKey="date" stroke="#9ca3af" fontSize={12} />
                    <YAxis stroke="#9ca3af" fontSize={12} />
                    <Tooltip contentStyle={{ backgroundColor: "#171a21", border: "1px solid #252932" }} />
                    <Line type="monotone" dataKey="present" stroke="#22c55e" strokeWidth={2} dot={false} />
                    <Line type="monotone" dataKey="late" stroke="#eab308" strokeWidth={2} dot={false} />
                    <Line type="monotone" dataKey="absent" stroke="#ef4444" strokeWidth={2} dot={false} />
                  </LineChart>
                </ResponsiveContainer>
              </div>

              <div className="bg-surface border border-border rounded-xl p-5">
                <h3 className="text-white font-medium mb-4">Employees by Department</h3>
                <ResponsiveContainer width="100%" height={260}>
                  <BarChart data={departments}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#252932" />
                    <XAxis dataKey="department" stroke="#9ca3af" fontSize={12} />
                    <YAxis stroke="#9ca3af" fontSize={12} />
                    <Tooltip contentStyle={{ backgroundColor: "#171a21", border: "1px solid #252932" }} />
                    <Bar dataKey="count" fill="#6366f1" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </>
        )}
      </main>
    </div>
  );
}
