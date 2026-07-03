function PanelLabel({
  children,
  style,
}: {
  children: React.ReactNode;
  style?: React.CSSProperties;
}) {
  return (
    <p
      className="text-xs uppercase tracking-widest"
      style={{
        color: "var(--muted-foreground)",
        letterSpacing: "0.12em",
        marginBottom: "0.05rem",
        ...style,
      }}
    >
      {children}
    </p>
  );
}

export default PanelLabel;