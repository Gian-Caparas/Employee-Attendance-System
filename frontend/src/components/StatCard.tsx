import { LucideIcon } from "lucide-react";

interface StatCardProps {
  label: string;
  value: number | string;
  icon: LucideIcon;
  accentColor?: string;
}

export default function StatCard({ label, value, icon: Icon, accentColor = "#6366f1" }: StatCardProps) {
  return (
    <div className="bg-surface border border-border rounded-xl p-5 flex items-center justify-between">
      <div>
        <p className="text-sm text-muted">{label}</p>
        <p className="text-2xl font-semibold text-white mt-1">{value}</p>
      </div>
      <div
        className="w-11 h-11 rounded-lg flex items-center justify-center"
        style={{ backgroundColor: `${accentColor}22` }}
      >
        <Icon size={22} color={accentColor} />
      </div>
    </div>
  );
}
