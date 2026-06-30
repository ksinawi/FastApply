const PanelLabel = ({ children }: { children: React.ReactNode }) => {
    return (
      <label 
        className="text-xs font-semibold uppercase tracking-wider block mb-2" 
        style={{ color: "#7A7A88" }} 
      >
        {children}
      </label>
    );
  };

export default PanelLabel