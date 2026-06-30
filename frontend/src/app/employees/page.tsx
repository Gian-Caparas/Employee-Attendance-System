"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Plus, Search, Trash2 } from "lucide-react";

import Sidebar from "@/components/Sidebar";
import Header from "@/components/Header";
import DataTable from "@/components/DataTable";
import api from "@/lib/api";
import { isAuthenticated } from "@/lib/auth";
import { Employee } from "@/types";

export default function EmployeesPage() {
  const router = useRouter();
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({
    employee_code: "",
    full_name: "",
    email: "",
    department: "",
    position: "",
  });

  useEffect(() => {
    if (!isAuthenticated()) {
      router.replace("/login");
      return;
    }
    loadEmployees();
  }, [router]);

  async function loadEmployees(searchTerm = "") {
    setLoading(true);
    try {
      const { data } = await api.get("/api/employees", { params: { search: searchTerm, limit: 100 } });
      setEmployees(data.items);
    } finally {
      setLoading(false);
    }
  }

  function handleSearchChange(value: string) {
    setSearch(value);
    loadEmployees(value);
  }

  async function handleCreate(e: React.FormEvent) {
    e.preventDefault();
    await api.post("/api/employees", form);
    setForm({ employee_code: "", full_name: "", email: "", department: "", position: "" });
    setShowForm(false);
    loadEmployees(search);
  }

  async function handleDelete(id: number) {
    if (!confirm("Delete this employee?")) return;
    await api.delete(`/api/employees/${id}`);
    loadEmployees(search);
  }

  return (
    <div className="flex">
      <Sidebar />
      <main className="flex-1 ml-64 p-8">
        <Header
          title="Employees"
          subtitle="Manage your employee directory"
          action={
            <button
              onClick={() => setShowForm((v) => !v)}
              className="flex items-center gap-2 bg-primary hover:bg-primaryHover transition-colors text-white rounded-lg px-4 py-2 text-sm font-medium"
            >
              <Plus size={16} />
              Add Employee
            </button>
          }
        />

        {showForm && (
          <form
            onSubmit={handleCreate}
            className="bg-surface border border-border rounded-xl p-5 mb-6 grid grid-cols-1 md:grid-cols-5 gap-3"
          >
            <input
              required
              placeholder="Employee Code"
              value={form.employee_code}
              onChange={(e) => setForm({ ...form, employee_code: e.target.value })}
              className="bg-background border border-border rounded-lg px-3 py-2 text-white text-sm outline-none focus:border-primary"
            />
            <input
              required
              placeholder="Full Name"
              value={form.full_name}
              onChange={(e) => setForm({ ...form, full_name: e.target.value })}
              className="bg-background border border-border rounded-lg px-3 py-2 text-white text-sm outline-none focus:border-primary"
            />
            <input
              required
              type="email"
              placeholder="Email"
              value={form.email}
              onChange={(e) => setForm({ ...form, email: e.target.value })}
              className="bg-background border border-border rounded-lg px-3 py-2 text-white text-sm outline-none focus:border-primary"
            />
            <input
              placeholder="Department"
              value={form.department}
              onChange={(e) => setForm({ ...form, department: e.target.value })}
              className="bg-background border border-border rounded-lg px-3 py-2 text-white text-sm outline-none focus:border-primary"
            />
            <input
              placeholder="Position"
              value={form.position}
              onChange={(e) => setForm({ ...form, position: e.target.value })}
              className="bg-background border border-border rounded-lg px-3 py-2 text-white text-sm outline-none focus:border-primary"
            />
            <button
              type="submit"
              className="md:col-span-5 bg-primary hover:bg-primaryHover transition-colors text-white rounded-lg py-2 text-sm font-medium"
            >
              Save Employee
            </button>
          </form>
        )}

        <div className="relative mb-4 max-w-sm">
          <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-muted" />
          <input
            placeholder="Search by name or code..."
            value={search}
            onChange={(e) => handleSearchChange(e.target.value)}
            className="w-full bg-surface border border-border rounded-lg pl-9 pr-3 py-2 text-white text-sm outline-none focus:border-primary"
          />
        </div>

        {loading ? (
          <p className="text-muted">Loading...</p>
        ) : (
          <DataTable
            data={employees}
            keyExtractor={(e) => e.id}
            columns={[
              { header: "Code", render: (e) => e.employee_code },
              { header: "Name", render: (e) => e.full_name },
              { header: "Email", render: (e) => e.email },
              { header: "Department", render: (e) => e.department || "—" },
              { header: "Position", render: (e) => e.position || "—" },
              {
                header: "",
                render: (e) => (
                  <button onClick={() => handleDelete(e.id)} className="text-muted hover:text-red-400">
                    <Trash2 size={16} />
                  </button>
                ),
              },
            ]}
          />
        )}
      </main>
    </div>
  );
}
