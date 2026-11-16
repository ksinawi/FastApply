import { Sparkles } from "lucide-react";

import { useState } from "react";

import { analyzeApplication, analyzeCoverLetter } from "../../lib/api";
import ErrorMessage from "../ui/ErrorMessage";
import type { AnalysisResult } from "../../types/AnalysisResult"

type Props = {
    documentType: "resume" | "coverLetter";

    uploadedFile: File | null;

    jobDescription: string;

    researchCompany: boolean;

    isAnalyzing: boolean;
    setIsAnalyzing: React.Dispatch<
        React.SetStateAction<boolean>
    >;

    setAnalysisResult: React.Dispatch<
        React.SetStateAction<AnalysisResult | null>
    >;
};

const AnalysisButton = ({
    documentType,
    uploadedFile,
    jobDescription,
    researchCompany,
    isAnalyzing,
    setIsAnalyzing,
    setAnalysisResult
}: Props) => {

    const [error, setError] = useState<string | null>(null);

    const analyzeDocument = async () => {
        if(!uploadedFile || !jobDescription) return;

        setIsAnalyzing(true);
        setError(null);

        try {
            const result = documentType === "resume"
                ? await analyzeApplication(uploadedFile, jobDescription)
                : await analyzeCoverLetter(uploadedFile, jobDescription, researchCompany);
            setAnalysisResult(result);
        } catch (err) {
            console.error(err);
            setError(err instanceof Error ? err.message : "Something went wrong. Please try again.");
        } finally {
            setIsAnalyzing(false);
        }
    }

    const canAnalyze = !!uploadedFile && !!jobDescription.trim() && !isAnalyzing;

  return (
    <div className="flex flex-col gap-3">
    <button
     onClick={analyzeDocument}
     disabled={!canAnalyze}
     className="flex items-center justify-center gap-2.5 w-full py-3.5 text-sm font-medium transition-all duration-200"
     style={{
        background: canAnalyze
         ? "#D4A942"
         : "#1C1C21",
        color: canAnalyze
         ? "#0C0C0F"
         : "#7A7A88",
        borderRadius: "0.25rem",
        border: "none",
        cursor: canAnalyze ? "pointer" : "not-allowed",
        letterSpacing: "0.02rem"
     }}
     >
        {isAnalyzing ? (
            <>
                <span className="size-4 border-2 border-t-transparent rounded-full animate-spin" style={{borderColor: "rgba(12,12,15,0.3)", borderTopColor: "transparent"}}/>
                Analyzing Document...
            </>
        ) : (
            <>
                <Sparkles size={16}/>
                Analyze &amp; Optimise
            </>
        )}
     </button>
     {isAnalyzing && (
        <p className="text-xs text-center" style={{ color: "#7A7A88" }}>
            This usually takes 20–40 seconds.
        </p>
     )}
     <ErrorMessage message={error}/>
    </div>
  )
}

export default AnalysisButton