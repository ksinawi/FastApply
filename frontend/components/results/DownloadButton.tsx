import type { AnalysisResult } from "../../types/AnalysisResult"

type Props = {
    analysisResult: AnalysisResult | null;
}

const DownloadButton = ({analysisResult}: Props) => {
    const downloadDocument = async () => {
        if(!analysisResult) return;

        try {
            const response = await fetch("http://localhost:8000/download", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    tailoredContent: analysisResult.tailoredContent,
                }),
            });

            if (!response.ok) {
                throw new Error("Error: Failed to generate PDF");
            }

            const blob = await response.blob();

            const url = window.URL.createObjectURL(blob);

            const a = document.createElement("a");
            a.href = url;
            a.download = "Tailored_Resume.pdf";

            document.body.appendChild(a);
            a.click();
            a.remove();

            window.URL.revokeObjectURL(url);
        } catch (error) {
            console.error(error);
        }
    }

    const canDownload = !!analysisResult;

    return (
        <button 
          onClick={downloadDocument}
          disabled={!canDownload}
          className="flex items-center justify-center gap-2.5 w-full py-3.5 text-sm font-medium transition-all duration-200"
          style={{
            background: canDownload
             ? "#D4A942"
             : "#1C1C21",
            color: canDownload
             ? "#0C0C0F"
             : "#7A7A88",
            borderRadius: "0.25rem",
            border: "none",
            cursor: canDownload ? "pointer" : "not-allowed",
            letterSpacing: "0.02rem"
          }}
        >
            Download
        </button>
    )
}

export default DownloadButton;
