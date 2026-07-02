function ScoreRing({score}: {score: number}) {
    const r = 52;
    const circ = 2 * Math.PI * r;
    const offset = circ * (1 - score / 100);
    const color =
        score >= 80
        ? "#5EC97A"
        : score >= 60
            ? "#D4A942"
            : "#E05A5A";

  return (
    <div
      className="relative flex items-center justify-center"
      style={{ width: 128, height: 128 }}
    >
      <svg
        width="128"
        height="128"
        style={{ transform: "rotate(-90deg)" }}
      >
        <circle
          cx="64"
          cy="64"
          r={r}
          stroke="rgba(255,255,255,0.06)"
          strokeWidth="10"
          fill="none"
        />
        <circle
          cx="64"
          cy="64"
          r={r}
          stroke={color}
          strokeWidth="10"
          fill="none"
          strokeDasharray={circ}
          strokeDashoffset={offset}
          strokeLinecap="round"
          style={{
            transition:
              "stroke-dashoffset 1.2s cubic-bezier(0.16,1,0.3,1)",
          }}
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span
          className="text-3xl font-bold"
          style={{
            fontFamily: "'Playfair Display', serif",
            color,
          }}
        >
          {score}
        </span>
        <span
          className="text-xs tracking-widest uppercase"
          style={{
            color: "#7A7A88",
            letterSpacing: "0.12em",
          }}
        >
          match
        </span>
      </div>
    </div>
  );
}

export default ScoreRing;