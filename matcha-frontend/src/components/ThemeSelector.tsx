import { useTheme, themes } from "../context/ThemeContext";

export default function ThemeSelector() {
  const { theme, setTheme } = useTheme();

  return (
    <div className="theme-selector">
      {Object.entries(themes).map(([key, t]) => (
        <button
          key={key}
          className={theme === key ? "active" : ""}
          onClick={() => setTheme(key as keyof typeof themes)}
        >
          {t.name}
        </button>
      ))}
    </div>
  );
}