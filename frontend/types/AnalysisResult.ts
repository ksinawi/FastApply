import { Resume } from "./Resume";
import { CoverLetter } from "./CoverLetter";

export type ResumeAnalysisResult = {
    kind: "resume";
    matchedSkills: string[];
    missingKeywords: string[];
    recommendations: string[];
    matchScore: number;
    tailoredResume: Resume;
};

export type CoverLetterAnalysisResult = {
    kind: "coverLetter";
    matchedSkills: string[];
    missingKeywords: string[];
    recommendations: string[];
    matchScore: number;
    tailoredCoverLetter: CoverLetter;
};

export type AnalysisResult = ResumeAnalysisResult | CoverLetterAnalysisResult;
