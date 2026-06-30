import { Sparkles } from "lucide-react";

const Header = () => {
  return (
    <header className="border-b" style={{ borderColor: "var(--border)" }}>
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div
              className="flex items-center justify-center size-8"
              style={{ background: "var(--primary)", borderRadius: "var(--radius)" }}
            >
              <Sparkles size={16} color="var(--primary-foreground)" />
            </div>
            <span
              className="text-sm font-medium tracking-wide uppercase"
              style={{ color: "var(--muted-foreground)", letterSpacing: "0.1em" }}
            >
              FastApply
            </span>
          </div>
          <span
            className="text-xs tracking-widest uppercase"
            style={{ color: "var(--muted-foreground)", letterSpacing: "0.12em" }}
          >
            AI Application
          </span>
        </div>
      </header>
  )
}

export default Header