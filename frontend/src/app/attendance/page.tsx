"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Plus } from "lucide-react";

import Sidebar from "@/components/Sidebar";
import Header from "@/components/Header";
import DataTable from "@/components/DataTable";
import api from "@/lib/api";
import { isAuthenticated } from "@/lib/auth";
import { AttendanceRecord, Employee } from "@/types";

const statusColors: Record<string, string> = {
  present: "text-green-400",
  late: "text-yellow-400",
  absent: "text-red-400",
  on_leave: "text-purple-400",
  half_day: "text-blue-400",
  holiday: "text-gray-400",
};

export default function AttendancePage() {
  const router = useRouter();
  const [records, setRecords] = useState<AttendanceRecord[]>([]);
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({
    employee_id: "",
    date: new Date().toISOString().slice(0, 10),
    status: "present",
    minutes_late: 0,
  });

  useEffect(() => {
    if (!isAuthenticated()) {
      router.replace("/login");
      return;
    }
    loadData();
  }, [router]);

  async function loadData() {
    setLoading(true);
    try {
      const [recRes, empRes] = await Promise.all([
        api.get("/api/attendance", { params: { limit: 100 } }),
        api.get("/api/employees", { params: { limit: 100 } }),
      ]);
      setRecords(recRes.data.items);
      setEmployees(empRes.data.items);
    } finally {
      setLoading(false);
    }
  }

  async function handleCreate(e: React.FormEvent) {
    e.preventDefault();
    await api.post("/api/attendance", { ...form, employee_id: Number(form.employee_id) });
    setShowForm(false);
    loadData();
  }

  function employeeName(id: number) {
    return employees.find((e) => e.id === id)?.full_name || `#${id}`;
  }

  return (
    <div className="flex">
      <Sidebar />
      <main className="flex-1 ml-64 p-8">
        <Header
          title="Attendance"
          subtitle="Daily attendance records"
          action={
            <button
              onClick={() => setShowForm((v) => !v)}
              className="flex items-center gap-2 bg-primary hover:bg-primaryHover transition-colors text-white rounded-lg px-4 py-2 text-sm font-medium"
            >
              <Plus size={16} />
              Log Attendance
            </button>
          }
        />

        {showForm && (
          <form
            onSubmit={handleCreate}
            className="bg-surface border border-border rounded-xl p-5 mb-6 grid grid-cols-1 md:grid-cols-4 gap-3"
          >
            <select
              required
              value={form.employee_id}
              onChange={(e) => setForm({ ...form, employee_id: e.target.value })}
              className="bg-background border border-border rounded-lg px-3 py-2 text-white text-sm outline-none focus:border-primary"
            >
              <option value="">Select employee</option>
              {employees.map((emp) => (
                <option key={emp.id} value={emp.id}>
                  {emp.full_name}
                </option>
              ))}
            </select>
            <input
              required
              type="date"
              value={form.date}
              onChange={(e) => setForm({ ...form, date: e.target.value })}
              className="bg-background border border-border rounded-lg px-3 py-2 text-white text-sm outline-none focus:border-primary"
            />
            <select
              value={form.status}
              onChange={(e) => setForm({ ...form, status: e.target.value })}
              className="bg-background border border-border rounded-lg px-3 py-2 text-white text-sm outline-none focus:border-primary"
            >
              <option value="present">Present</option>
              <option value="late">Late</option>
              <option value="absent">Absent</option>
              <option value="on_leave">On Leave</option>
              <option value="half_day">Half Day</option>
              <option value="holiday">Holiday</option>
            </select>
            <input
              type="number"
              min={0}
              placeholder="Minutes late"
              value={form.minutes_late}
              onChange={(e) => setForm({ ...form, minutes_late: Number(e.target.value) })}
              className="bg-background border border-border rounded-lg px-3 py-2 text-white text-sm outline-none focus:border-primary"
            />
            <button
              type="submit"
              className="md:col-span-4 bg-primary hover:bg-primaryHover transition-colors text-white rounded-lg py-2 text-sm font-medium"
            >
              Save Record
            </button>
          </form>
        )}

        {loading ? (
          <p className="text-muted">Loading...</p>
        ) : (
          <DataTable
            data={records}
            keyExtractor={(r) => r.id}
            columns={[
              { header: "Employee", render: (r) => employeeName(r.employee_id) },
              { header: "Date", render: (r) => r.date },
              {
                header: "Status",
                render: (r) => (
                  <span className={statusColors[r.status] || "text-gray-300"}>
                    {r.status.replace("_", " ")}
                  </span>
                ),
              },
              { header: "Minutes Late", render: (r) => r.minutes_late },
              { header: "Source", render: (r) => r.source },
            ]}
          />
        )}
      </main>
    </div>
  );
}
