import Panel from "../ui/Panel";
import PanelLabel from "../ui/PanelLabel";

import type { AnalysisResult } from "../../types/AnalysisResult";
import { Check, Copy, Sparkles } from "lucide-react";


type Props = {
    analysisResult: AnalysisResult | null;
    setAnalysisResult: React.Dispatch<
        React.SetStateAction<AnalysisResult | null>
    >;

    copied: boolean;
    setCopied: React.Dispatch<
        React.SetStateAction<boolean>
    >;
};

const TailoredResults = ({analysisResult, setAnalysisResult, copied, setCopied}: Props) => {
    if (!analysisResult) {
        return (
          <Panel>
            <p className="text-sm text-gray-400">No analysis yet.</p>
          </Panel>
        );
    }

    const handleCopy = () => {
        if(analysisResult) {
            navigator.clipboard.writeText(
                analysisResult.tailoredContent,
            );
            setCopied(true);
            setTimeout(() => setCopied(false), 2000);
        }
    };
    
    return (
        <Panel>
            <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-2">
                    <Sparkles size={15} color="#D4A942"/>
                    <PanelLabel>AI-Tailored Version</PanelLabel>
                </div>
                <button 
                    onClick={handleCopy}
                    className="flex items-center gap-1.5 text-xs transition-opacity hover:opacity-70"
                    style={{
                    color: copied
                        ? "#5EC97A"
                        : "#7A7A88"
                    }}
                    >
                    {copied ? (
                        <Check size={13}/>
                    ) : (
                        <Copy size={13}/>
                    )}
                    {copied ? "Copied" : "Copy"}
                </button>
            </div>
            <div 
                className="max-h-80 overflow-y-auto"
                style={{
                background: "#1C1C21",
                order: "1px solid rgba(255, 255, 255, 0.07)",
                borderRadius: "0.25rem",
                padding: "1rem",
                scrollbarWidth: "thin",
                scrollbarColor: "rgba(255,255,255,0.1) transparent"
                }}>
                <pre className="whitespace-pre-wrap text-xs leading-relaxed" style={{fontFamily: "'DM Mono', monospace", color: "#EEE9DF"}}>
                    {analysisResult.tailoredContent}
                </pre>
            </div>
        </Panel>
    )
}

export default TailoredResults;