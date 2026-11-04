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
          main: "#101116",
          header: "#171A21",
          secondary: "#1C2029",
        },
        card: {
          primary: "#242A35",
          elevated: "#2C3441",
        },
        surface: {
          interactive: "#343E4B",
          hover: "#3D4857",
        },
        border: {
          charcoal: "#394452",
          subtle: "#2A323D",
        },
        brand: {
          blue: "#48A9FF",
          sky: "#48A9FF",
          skyDark: "#3190E8",
          primary: "#48A9FF",
          purple: "#48A9FF", // Maps legacy references smoothly to Aviation Blue
          purpleDark: "#3190E8",
          gold: "#F2B94B",
          amber: "#F2B94B",
          orange: "#F2B94B",
          teal: "#3ED1B0",
          green: "#3ED1B0",
          violet: "#A58BFA",
          red: "#F16D75",
        },
        text: {
          primary: "#F5F6FA",
          secondary: "#B8C3D2",
          muted: "#8592A3",
        },
      },
      fontFamily: {
        sans: [
          "Inter",
          "Manrope",
          "-apple-system",
          "BlinkMacSystemFont",
          "'SF Pro Display'",
          "'Segoe UI'",
          "Roboto",
          "sans-serif",
        ],
      },
      boxShadow: {
        card: "0 6px 20px rgba(0, 0, 0, 0.45)",
        elevated: "0 10px 30px rgba(0, 0, 0, 0.60)",
        glow: "0 0 24px rgba(72, 169, 255, 0.25)",
        goldGlow: "0 0 20px rgba(242, 185, 75, 0.25)",
      },
    },
  },
  plugins: [],
};

export default config;
