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
          main: "#0B1220",
          secondary: "#101A2A",
        },
        card: {
          primary: "#131E30",
          elevated: "#1D2B40",
        },
        surface: {
          interactive: "#26374D",
          hover: "#2F435E",
        },
        border: {
          charcoal: "#29384C",
          subtle: "#1E2A3A",
        },
        brand: {
          sky: "#6EA8FE",
          skyDark: "#5694F0",
          primary: "#6EA8FE",
          purple: "#6EA8FE",        // Seamlessly maps legacy purple to Midnight Sky Blue
          purpleDark: "#5694F0",
          blue: "#6EA8FE",
          teal: "#36CFC0",
          green: "#34D399",
          gold: "#E9C46A",
          orange: "#E9C46A",
          red: "#F87171",
        },
        text: {
          primary: "#F1F5F9",
          secondary: "#A7B4C8",
          muted: "#718198",
        },
      },
      fontFamily: {
        sans: [
          "Inter",
          "-apple-system",
          "BlinkMacSystemFont",
          "'SF Pro Display'",
          "'Segoe UI'",
          "Roboto",
          "sans-serif",
        ],
      },
      boxShadow: {
        card: "0 4px 16px rgba(0, 0, 0, 0.35)",
        elevated: "0 8px 24px rgba(0, 0, 0, 0.45)",
        glow: "0 0 20px rgba(110, 168, 254, 0.20)",
      },
    },
  },
  plugins: [],
};

export default config;
