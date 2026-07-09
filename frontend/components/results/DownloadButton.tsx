import type { AnalysisResult } from "../../types/AnalysisResult"

type Props = {
    analysisResult: AnalysisResult | null;
    setAnalysisResult: React.Dispatch<
        React.SetStateAction<AnalysisResult | null>
    >;
}

const DownloadButton = ({analysisResult, setAnalysisResult}: Props) => {
    const downloadDocument = () => {
        if(!analysisResult) return;
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
