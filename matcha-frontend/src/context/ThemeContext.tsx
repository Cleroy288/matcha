import React, { createContext, useContext, useState, useEffect } from "react";
/* eslint-disable react-refresh/only-export-components */

export const themes = {
  sunset: { name: "🍵", class: "theme-sunset", color: "#2d1b4e" },
  ocean: { name: "🔵", class: "theme-ocean", color: "#1a2a6c" },
  emerald: { name: "🟠", class: "theme-emerald", color: "#064e3b" },
  night: { name: "🟣", class: "theme-night", color: "#0E0A1A" },
};

type ThemeKey = keyof typeof themes;

interface ThemeContextType {
  theme: ThemeKey;
  setTheme: (theme: ThemeKey) => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<ThemeKey>(() => {
    return (localStorage.getItem("app_theme") as ThemeKey) || "sunset";
  });

  useEffect(() => {
    localStorage.setItem("app_theme", theme);
    const current = themes[theme];
    const root = document.documentElement;
    for (const t of Object.values(themes)) {
      root.classList.remove(t.class);
    }
    root.classList.add(current.class);

    // Fix for the iPhone status bar
    const meta = document.querySelector("meta[name='theme-color']");
    if (meta) meta.setAttribute("content", current.color);
  }, [theme]);

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      <div className={`app-wrapper ${themes[theme].class}`}>
        {children}
      </div>
    </ThemeContext.Provider>
  );
}

// Custom hook for consuming the theme easily
export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) throw new Error("useTheme must be used within ThemeProvider");
  return context;
};
