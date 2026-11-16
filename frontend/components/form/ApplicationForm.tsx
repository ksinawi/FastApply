"use client";

import { useState } from "react";
import DocumentTypeSelector from "./DocumentTypeSelector";
import UploadFile from "./UploadFile";
import JobDescription from "./JobDescription";
import AnalysisButton from "./AnalysisButton";

import type { AnalysisResult } from "../../types/AnalysisResult"

type Props = {
    setAnalysisResult: React.Dispatch<
        React.SetStateAction<AnalysisResult | null>
    >;
};

export default function ApplicationForm({setAnalysisResult}: Props) {
    const [documentType, setDocumentType] = useState<"resume" | "coverLetter">("resume");
    const [uploadedFile, setUploadedFile] = useState<File | null>(null,);
    const [isDragging, setIsDragging] = useState<boolean>(false);
    const [jobDescription, setJobDescription] = useState("")
    const [researchCompany, setResearchCompany] = useState(false)
    const [isAnalyzing, setIsAnalyzing] = useState(false)

    return (
        <div className="flex flex-col gap-5">
            <DocumentTypeSelector
            documentType={documentType}
            setDocumentType={setDocumentType}
            />
            <UploadFile
            documentType={documentType}
            uploadedFile={uploadedFile}
            setUploadedFile={setUploadedFile}
            isDragging={isDragging}
            setIsDragging={setIsDragging}
            />
            <JobDescription
            jobDescription={jobDescription}
            setJobDescription={setJobDescription}
            documentType={documentType}
            researchCompany={researchCompany}
            setResearchCompany={setResearchCompany}
            />
            <AnalysisButton
            documentType={documentType}
            uploadedFile={uploadedFile}
            jobDescription={jobDescription}
            researchCompany={researchCompany}
            isAnalyzing={isAnalyzing}
            setIsAnalyzing={setIsAnalyzing}
            setAnalysisResult={setAnalysisResult}
            />
        </div>
    );
}