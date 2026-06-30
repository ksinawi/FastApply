const Panel = ({ children }: { children: React.ReactNode }) => {
    return (
      <div 
        className="p-5 border" 
        style={{ 
          background: "#141418", 
          borderColor: "rgba(255, 255, 255, 0.07)", 
          borderRadius: "0.5rem" 
        }}
      >
        {children}
      </div>
    );
  };

export default Panel