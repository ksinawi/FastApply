import { AlertCircle } from "lucide-react";

const ErrorMessage = ({ message }: { message: string | null }) => {
    if (!message) return null;

    return (
        <div
            role="alert"
            className="flex items-start gap-2.5 px-4 py-3 text-sm"
            style={{
                background: "rgba(229,98,98,0.08)",
                border: "1px solid rgba(229,98,98,0.3)",
                borderRadius: "0.25rem",
                color: "#F0A3A3",
                lineHeight: 1.5,
            }}
        >
            <AlertCircle size={16} className="shrink-0 mt-0.5" />
            <span>{message}</span>
        </div>
    );
};

export default ErrorMessage;
