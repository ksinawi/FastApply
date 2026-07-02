import Panel from "../ui/Panel";
import ScoreRing from "../ui/ScoreRing";

import type { AnalysisResult } from "../../types/AnalysisResult"

type Props = {
    analysisResult: AnalysisResult | null;
    setAnalysisResult: React.Dispatch<
        React.SetStateAction<AnalysisResult | null>
    >;
};

const Score = ({ analysisResult, setAnalysisResult }: Props) => {
    if (!analysisResult) {
      return (
        <Panel>
          <p className="text-sm text-gray-400">No analysis yet.</p>
        </Panel>
      );
    }
  
    return (
      <Panel>
        <div className="flex items-center gap-6">
          <ScoreRing score={analysisResult.matchScore} />
          <div>
            <p className="text-xs uppercase tracking-widest mb-1"
               style={{ color: "#7A7A88", letterSpacing: "0.12rem" }}>
              Match Score
            </p>
  
            <p className="text-sm leading-relaxed"
               style={{ color: "#EEE9DF", maxWidth: 260 }}>
              {analysisResult.matchScore >= 80
                ? "Strong alignment. A few targeted additions could push this above 85."
                : analysisResult.matchScore >= 60
                  ? "Solid foundation. Apply the recommendations below to close the gap."
                  : "Room to grow. The tailored version below addresses the key gaps."}
            </p>
          </div>
        </div>
      </Panel>
    );
  };

export default Score