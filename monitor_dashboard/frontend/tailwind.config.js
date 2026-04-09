/** @type {import('tailwindcss').Config} */
// Linear Design System - Inspired by linear.app
// Ultra-minimal, precise, purple accent, developer-focused

module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Linear Design System
        // Primary: Dark theme with purple accent
        background: {
          DEFAULT: '#0D0D0F',      // Deep dark background
          secondary: '#141416',    // Secondary background
          tertiary: '#1C1C1F',     // Tertiary background
          hover: '#262629',        // Hover state
        },
        foreground: {
          DEFAULT: '#FFFFFF',      // Primary text
          secondary: '#8A8F98',    // Secondary text
          tertiary: '#5C5F66',     // Tertiary text
          muted: '#3D3F42',        // Muted text
        },
        primary: {
          50: '#faf5ff',
          100: '#f3e8ff',
          200: '#e9d5ff',
          300: '#d8b4fe',
          400: '#c084fc',
          500: '#a855f7',  // Linear Purple - Main accent
          600: '#9333ea',
          700: '#7e22ce',
          800: '#6b21a8',
          900: '#581c87',
          950: '#3b0764',
        },
        accent: {
          blue: '#448aff',    // Links, info
          green: '#00c853',   // Success
          yellow: '#ffc107',  // Warning
          red: '#ff5252',     // Error
          orange: '#ff9800',  // Highlights
        },
        border: {
          DEFAULT: '#262629',
          hover: '#3D3F42',
          active: '#a855f7',
        },
        // Semantic colors
        success: {
          bg: 'rgba(0, 200, 83, 0.1)',
          border: '#00c853',
          text: '#00c853',
        },
        warning: {
          bg: 'rgba(255, 193, 7, 0.1)',
          border: '#ffc107',
          text: '#ffc107',
        },
        error: {
          bg: 'rgba(255, 82, 82, 0.1)',
          border: '#ff5252',
          text: '#ff5252',
        },
        info: {
          bg: 'rgba(68, 138, 255, 0.1)',
          border: '#448aff',
          text: '#448aff',
        },
      },
      fontFamily: {
        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'sans-serif'],
        mono: ['JetBrains Mono', 'SF Mono', 'Monaco', 'monospace'],
      },
      fontSize: {
        xs: ['0.6875rem', { lineHeight: '1rem' }],     // 11px
        sm: ['0.8125rem', { lineHeight: '1.25rem' }],  // 13px
        base: ['0.9375rem', { lineHeight: '1.5rem' }], // 15px
        lg: ['1.0625rem', { lineHeight: '1.75rem' }],  // 17px
        xl: ['1.25rem', { lineHeight: '1.75rem' }],    // 20px
        '2xl': ['1.5rem', { lineHeight: '2rem' }],     // 24px
        '3xl': ['1.875rem', { lineHeight: '2.25rem' }],// 30px
      },
      spacing: {
        px: '1px',
        0: '0px',
        0.5: '0.125rem',  // 2px
        1: '0.25rem',     // 4px
        1.5: '0.375rem',  // 6px
        2: '0.5rem',      // 8px
        2.5: '0.625rem',  // 10px
        3: '0.75rem',     // 12px
        3.5: '0.875rem',  // 14px
        4: '1rem',        // 16px
        5: '1.25rem',     // 20px
        6: '1.5rem',      // 24px
        7: '1.75rem',     // 28px
        8: '2rem',        // 32px
        9: '2.25rem',     // 36px
        10: '2.5rem',     // 40px
        11: '2.75rem',    // 44px
        12: '3rem',       // 48px
        14: '3.5rem',     // 56px
        16: '4rem',       // 64px
        20: '5rem',       // 80px
        24: '6rem',       // 96px
        28: '7rem',       // 112px
        32: '8rem',       // 128px
      },
      borderRadius: {
        none: '0px',
        xs: '0.125rem',   // 2px
        sm: '0.25rem',    // 4px
        DEFAULT: '0.375rem', // 6px
        md: '0.5rem',     // 8px
        lg: '0.625rem',   // 10px
        xl: '0.75rem',    // 12px
        '2xl': '1rem',    // 16px
        '3xl': '1.5rem',  // 24px
        full: '9999px',
      },
      boxShadow: {
        sm: '0 1px 2px 0 rgba(0, 0, 0, 0.3)',
        DEFAULT: '0 1px 3px 0 rgba(0, 0, 0, 0.4), 0 1px 2px -1px rgba(0, 0, 0, 0.4)',
        md: '0 4px 6px -1px rgba(0, 0, 0, 0.4), 0 2px 4px -2px rgba(0, 0, 0, 0.4)',
        lg: '0 10px 15px -3px rgba(0, 0, 0, 0.4), 0 4px 6px -4px rgba(0, 0, 0, 0.4)',
        xl: '0 20px 25px -5px rgba(0, 0, 0, 0.4), 0 8px 10px -6px rgba(0, 0, 0, 0.4)',
        '2xl': '0 25px 50px -12px rgba(0, 0, 0, 0.5)',
        inner: 'inset 0 2px 4px 0 rgba(0, 0, 0, 0.3)',
        // Linear specific
        'glow-purple': '0 0 20px rgba(168, 85, 247, 0.3)',
        'glow-blue': '0 0 20px rgba(68, 138, 255, 0.3)',
      },
      backdropBlur: {
        xs: '2px',
      },
      animation: {
        'fade-in': 'fadeIn 0.2s ease-in-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      },
      transitionTimingFunction: {
        'linear': 'linear',
        'in': 'cubic-bezier(0.4, 0, 1, 1)',
        'out': 'cubic-bezier(0, 0, 0.2, 1)',
        'in-out': 'cubic-bezier(0.4, 0, 0.2, 1)',
      },
      transitionDuration: {
        50: '50ms',
        100: '100ms',
        150: '150ms',
        200: '200ms',
        250: '250ms',
        300: '300ms',
        400: '400ms',
        500: '500ms',
      },
    },
  },
  plugins: [],
}
