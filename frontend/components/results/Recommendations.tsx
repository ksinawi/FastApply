import Panel from "../ui/Panel";
import PanelLabel from "../ui/PanelLabel";

import type { AnalysisResult } from "../../types/AnalysisResult";
import { Briefcase } from "lucide-react";


type Props = {
    analysisResult: AnalysisResult | null;
    setAnalysisResult: React.Dispatch<
        React.SetStateAction<AnalysisResult | null>
    >;
};

const Recommendations = ({analysisResult, setAnalysisResult}: Props) => {
    if (!analysisResult) {
        return (
          <Panel>
            <p className="text-sm text-gray-400">No analysis yet.</p>
          </Panel>
        );
      }

    return (
        <Panel>
            <div className="flex items-center gap-2 mb-5">
                <Briefcase size={15} color="#D4A942"/>
                <PanelLabel>Recommendations</PanelLabel>
            </div>
            <ol className="flex flex-col gap-4">
                {analysisResult.recommendations.map(
                    (rec, i) => (
                        <li key={i} className="flex gap-3 items-start">
                            <span 
                              className="shrink-0 flex items-center justify-center text-xs font-medium"
                              style={{
                                width: 22,
                                height: 22,
                                borderRadius: "50%",
                                background: "rgba(212,169,66,0.12)",
                                color: "#D4A942",
                                fontFamily:  "'DM Mono', monospace",
                                paddingTop: 1
                              }}
                            >
                                {i + 1}
                            </span>
                            <p className="text-sm leading-relaxed" style={{color: "#EEE9DF", paddingTop: 2}}>
                                {rec}
                            </p>
                        </li>
                    ),
                )}
            </ol>
        </Panel>
    );
}

export default Recommendations;