const Container = ({ children }: { children: React.ReactNode }) => {
    return (
        <div className="min-h-screen"
        style={{
          background: "#0C0C0F",
          fontFamily: "var(--font-dm-sans), sans-serif",
        }}>
            {children}
        </div>
    );
};

export default Container;