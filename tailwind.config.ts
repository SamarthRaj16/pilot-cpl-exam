import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        bg: {
          main: "#19191D",
          secondary: "#202126",
        },
        card: {
          primary: "#292A30",
          elevated: "#303139",
        },
        surface: {
          interactive: "#373942",
          hover: "#434552",
        },
        border: {
          charcoal: "#40414B",
          subtle: "#33343d",
        },
        brand: {
          purple: "#9484F5",
          purpleDark: "#7b6ae6",
          blue: "#719CFF",
          teal: "#51C6C1",
          green: "#69CF9B",
          gold: "#E5C36C",
          orange: "#ECA85B",
          red: "#ED7078",
        },
      },
      fontFamily: {
        sans: [
          "-apple-system",
          "BlinkMacSystemFont",
          "'SF Pro Display'",
          "'Segoe UI'",
          "Roboto",
          "sans-serif",
        ],
      },
      boxShadow: {
        card: "0 4px 20px rgba(0, 0, 0, 0.35)",
        elevated: "0 8px 32px rgba(0, 0, 0, 0.45)",
        glow: "0 0 24px rgba(148, 132, 245, 0.25)",
      },
    },
  },
  plugins: [],
};

export default config;

