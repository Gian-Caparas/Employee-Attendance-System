export interface Employee {
  id: number;
  employee_code: string;
  full_name: string;
  email: string;
  department: string | null;
  position: string | null;
  phone: string | null;
  date_hired: string | null;
  is_active: number;
  created_at: string;
}

export interface AttendanceRecord {
  id: number;
  employee_id: number;
  date: string;
  time_in: string | null;
  time_out: string | null;
  status: "present" | "late" | "absent" | "on_leave" | "half_day" | "holiday";
  minutes_late: number;
  notes: string | null;
  source: string;
  created_at: string;
}

export interface KPIs {
  total_employees: number;
  present_today: number;
  late_today: number;
  absent_today: number;
  on_leave_today: number;
}

export interface User {
  id: number;
  full_name: string;
  email: string;
  role: string;
  is_active: number;
  created_at: string;
}
