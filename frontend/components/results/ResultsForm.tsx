"use client";

import { useState } from "react";
import Score from "./Score";

import type { AnalysisResult } from "../../types/AnalysisResult"
import MatchedSkills from "./MatchedSkills";
import Recommendations from "./Recommendations";
import TailoredResults from "./TailoredResults";
import { Sparkles } from "lucide-react";
import MissingSkills from "./MissingSkills";
import DownloadButton from "./DownloadButton";

type Props = {
  analysisResult: AnalysisResult | null;
};

const ResultsForm = ({analysisResult}: Props) => {
    const [copied, setCopied] = useState(false);

  return (
    <div className="flex flex-col gap-5">
      {analysisResult ? (
        <>
          <Score
          analysisResult={analysisResult}
          />
          <MatchedSkills
          analysisResult={analysisResult}
          />
          <MissingSkills
          analysisResult={analysisResult}
          />
          <Recommendations
          analysisResult={analysisResult}
          />
          <TailoredResults
          analysisResult={analysisResult}
          copied={copied}
          setCopied={setCopied}
          />
          <DownloadButton
          analysisResult={analysisResult}
          />
        </>
      ) : (
        <div className="flex flex-col items-center justify-center text-center h-full min-h-96" style={{border: "1.5px dashed rgba(255,255,255,0.07)", borderRadius: "0.25rem"}}>
          <div className="flex items-center justify-center size-14 mb-5" style={{background: "#1C1C21", borderRadius: "50%"}}>
            <Sparkles size={22} color="#7A7A88"/>
          </div>
          <p className="text-lg mb-2" style={{fontFamily: "var(--font-playfair), serif", color: "#EEE9DF"}}>
            Analysis Will Appear Here
          </p>
          <p className="text-sm max-w-xs" style={{color: "#7A7A88", lineHeight: 1.7}}>
            Upload your document and paste a job description, then click Analyze.
          </p>
        </div>
      )}
    </div>
  )
}

export default ResultsForm;