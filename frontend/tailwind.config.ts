import type { Config } from 'tailwindcss';

const config: Config = {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        background: {
          primary: '#0a0a0f',
          secondary: '#12121a',
          tertiary: '#1a1a26'
        },
        tribe: {
          primary: '#ff6b35',
          secondary: '#f7931e'
        },
        teacher: {
          primary: '#00d4aa',
          secondary: '#00b4d8'
        },
        recon: {
          primary: '#8b5cf6',
          secondary: '#6366f1'
        }
      },
      boxShadow: {
        glow: '0 0 20px rgba(255,255,255,0.08)'
      }
    }
  },
  plugins: []
};

export default config;
