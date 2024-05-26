import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./_components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      screens: {
        'mob': { 'max': '767px' },   // => @media (max-width: 767px) { ... }
        'pc': { 'min': '768px' },   // => @media (max-width: 767px) { ... }
        // Custom breakpoints for desktop-first approach
        '2xl': { 'max': '1535px' }, // => @media (max-width: 1535px) { ... }
        'xl': { 'max': '1279px' },  // => @media (max-width: 1279px) { ... }
        'lg': { 'max': '1023px' },  // => @media (max-width: 1023px) { ... }
        'md': { 'max': '767px' },   // => @media (max-width: 767px) { ... }
        'sm': { 'max': '639px' },   // => @media (max-width: 639px) { ... }
      },
      colors: {
        primary: '#101010',
        secondary: '#31363F',
        passive: '#76ABAE',
      },
    },
  },
  plugins: [],
};

export default config;
