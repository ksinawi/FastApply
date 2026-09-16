import type { AnalysisResult } from "../../types/AnalysisResult"

type Props = {
    analysisResult: AnalysisResult | null;
}

const DownloadButton = ({analysisResult}: Props) => {
    const downloadDocument = async () => {
        if(!analysisResult) return;

        const isResume = analysisResult.kind === "resume";
        const endpoint = isResume ? "/download" : "/download_cover_letter";
        const body = isResume
            ? { resume: analysisResult.tailoredResume }
            : { coverLetter: analysisResult.tailoredCoverLetter };
        const filename = isResume ? "Tailored_Resume.pdf" : "Tailored_Cover_Letter.pdf";

        try {
            const response = await fetch(`http://localhost:8000${endpoint}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(body),
            });

            if (!response.ok) {
                throw new Error("Error: Failed to generate PDF");
            }

            const blob = await response.blob();

            const url = window.URL.createObjectURL(blob);

            const a = document.createElement("a");
            a.href = url;
            a.download = filename;

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
