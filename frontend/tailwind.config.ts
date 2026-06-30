import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        background: "#0f1115",
        surface: "#171a21",
        border: "#252932",
        primary: "#6366f1",
        primaryHover: "#4f46e5",
        muted: "#9ca3af",
      },
    },
  },
  plugins: [],
};

export default config;
