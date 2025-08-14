import type { Config } from 'tailwindcss'

export default {
  content: ['src/renderer/**/*.{html,tsx,ts}'],
  theme: {
    extend: {
      colors: {
        base: '#0b0f17',
        panel: 'rgba(255,255,255,0.06)',
        neon: '#38bdf8',
        accent: '#a78bfa',
        warn: '#fbbf24',
        ok: '#34d399'
      },
      backdropBlur: {
        xs: '2px'
      },
      boxShadow: {
        glow: '0 0 24px rgba(56,189,248,0.25)',
        soft: '0 10px 30px rgba(0,0,0,0.25)'
      }
    }
  },
  plugins: []
} satisfies Config
