import Panel from "../ui/Panel";
import PanelLabel from "../ui/PanelLabel";
import Chip from "../ui/Chip";

import type { AnalysisResult } from "../../types/AnalysisResult";
import { AlertCircle } from "lucide-react";

type Props = {
    analysisResult: AnalysisResult | null;
    setAnalysisResult: React.Dispatch<
        React.SetStateAction<AnalysisResult | null>
    >;
};

const MissingSkills = ({ analysisResult, setAnalysisResult }: Props) => {
    if (!analysisResult) {
        return (
          <Panel>
            <p className="text-sm text-gray-400">No analysis yet.</p>
          </Panel>
        );
      }

    return (
        <Panel>
           <div className="flex items-center gap-2 mb-4">
                <AlertCircle size={15} color="#D4A942"/>
                <PanelLabel>Missing Keywords</PanelLabel>
           </div>
           <div className="flex flex-wrap gap-2">
            {analysisResult.missingKeywords.map(
                (kw, i) => (
                    <Chip key={i} variant="amber">{kw}</Chip>
                ),
            )}
           </div>
        </Panel>
    )
}

export default MissingSkills;
