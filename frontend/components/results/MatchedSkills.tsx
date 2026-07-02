import Panel from "../ui/Panel";
import PanelLabel from "../ui/PanelLabel";
import Chip from "../ui/Chip";

import type { AnalysisResult } from "../../types/AnalysisResult";
import { CheckCircle2 } from "lucide-react";


type Props = {
    analysisResult: AnalysisResult | null;
    setAnalysisResult: React.Dispatch<
        React.SetStateAction<AnalysisResult | null>
    >;
};

const MatchedSkills = ({ analysisResult, setAnalysisResult }: Props) => {
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
            <CheckCircle2 size={15} color="#5EC97A"/>
            <PanelLabel>Matched Skills</PanelLabel>
        </div>
        <div className="flex flex-wrap gap-2">
            {analysisResult.matchedSkills.map(
                (skill, i) => (
                    <Chip key={i} variant="green">
                        {skill}
                    </Chip>
                ),
            )}
        </div>
    </Panel>
  )
}

export default MatchedSkills