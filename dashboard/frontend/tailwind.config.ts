import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        navy: {
          950: '#0a0e1a',
          900: '#0f1629',
          800: '#151d35',
          700: '#1a2540',
        },
        cyan: {
          glow: '#00d4ff',
          dim: '#0891b2',
        },
      },
      animation: {
        pulseGlow: 'pulseGlow 2s ease-in-out infinite',
        flowDash: 'flowDash 1.5s linear infinite',
      },
      keyframes: {
        pulseGlow: {
          '0%, 100%': { opacity: '0.6' },
          '50%': { opacity: '1' },
        },
        flowDash: {
          to: { strokeDashoffset: '-20' },
        },
      },
    },
  },
  plugins: [],
};

export default config;
