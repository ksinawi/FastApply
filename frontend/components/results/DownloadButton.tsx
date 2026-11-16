import { useState } from "react";
import { Download } from "lucide-react";

import { downloadPdf } from "../../lib/api";
import ErrorMessage from "../ui/ErrorMessage";
import type { AnalysisResult } from "../../types/AnalysisResult"

type Props = {
    analysisResult: AnalysisResult | null;
}

const DownloadButton = ({analysisResult}: Props) => {
    const [isDownloading, setIsDownloading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const downloadDocument = async () => {
        if (!analysisResult) return;

        setIsDownloading(true);
        setError(null);

        try {
            await downloadPdf(analysisResult);
        } catch (err) {
            console.error(err);
            setError(err instanceof Error ? err.message : "Failed to generate the PDF.");
        } finally {
            setIsDownloading(false);
        }
    }

    const canDownload = !!analysisResult && !isDownloading;

    return (
        <div className="flex flex-col gap-3">
            <button
              onClick={downloadDocument}
              disabled={!canDownload}
              className="flex items-center justify-center gap-2.5 w-full py-3.5 text-sm font-medium transition-all duration-200"
              style={{
                background: canDownload ? "#D4A942" : "#1C1C21",
                color: canDownload ? "#0C0C0F" : "#7A7A88",
                borderRadius: "0.25rem",
                border: "none",
                cursor: canDownload ? "pointer" : "not-allowed",
                letterSpacing: "0.02rem"
              }}
            >
                <Download size={16}/>
                {isDownloading ? "Preparing PDF..." : "Download PDF"}
            </button>
            <ErrorMessage message={error}/>
        </div>
    )
}

export default DownloadButton;
