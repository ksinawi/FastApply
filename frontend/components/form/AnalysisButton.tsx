import { Sparkles } from "lucide-react";

type Props = {
    uploadedFile: File | null;
    setUploadedFile: React.Dispatch<
        React.SetStateAction<File | null>
    >;
    
    jobDescription: string;
    setJobDescription: React.Dispatch<
        React.SetStateAction<string>
    >;
    
    isAnalyzing: boolean;
    setIsAnalyzing: React.Dispatch<
        React.SetStateAction<boolean>
    >;
};

const AnalysisButton = ({
    uploadedFile,
    setUploadedFile,
    jobDescription,
    setJobDescription,
    isAnalyzing,
    setIsAnalyzing
}: Props) => {

    const analyzeDocument = () => {
        if(!uploadedFile || !jobDescription) return;
        setIsAnalyzing(true);
    }

    const canAnalyze = !!uploadedFile && !!jobDescription.trim() && !isAnalyzing;

  return (
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
  )
}

export default AnalysisButton