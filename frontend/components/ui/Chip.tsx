function Chip({
    children,
    variant,
  }: {
    children: React.ReactNode;
    variant: "green" | "amber";
  }) {
    const styles =
      variant === "green"
        ? {
            background: "rgba(94,201,122,0.08)",
            color: "#5EC97A",
            border: "1px solid rgba(94,201,122,0.2)",
          }
        : {
            background: "rgba(212,169,66,0.08)",
            color: "#D4A942",
            border: "1px solid rgba(212,169,66,0.2)",
          };
  
    return (
      <span
        className="text-xs font-medium px-2.5 py-1"
        style={{ borderRadius: "var(--radius)", ...styles }}
      >
        {children}
      </span>
    );
  }

  export default Chip;