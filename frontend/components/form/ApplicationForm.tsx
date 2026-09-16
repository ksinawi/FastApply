"use client";

import { useState } from "react";
import DocumentTypeSelector from "./DocumentTypeSelector";
import UploadFile from "./UploadFile";
import JobDescription from "./JobDescription";
import AnalysisButton from "./AnalysisButton";

import type { AnalysisResult } from "../../types/AnalysisResult"

type Props = {
    analysisResult: AnalysisResult | null;
    setAnalysisResult: React.Dispatch<
        React.SetStateAction<AnalysisResult | null>
    >;
};

export default function ApplicationForm({analysisResult, setAnalysisResult}: Props) {
    const [documentType, setDocumentType] = useState<"resume" | "coverLetter">("resume");
    const [uploadedFile, setUploadedFile] = useState<File | null>(null,);
    const [isDragging, setIsDragging] = useState<boolean>(false);
    const [jobDescription, setJobDescription] = useState("")
    const [isAnalyzing, setIsAnalyzing] = useState(false)

    return (
        <div className="flex flex-col gap-5">
            <DocumentTypeSelector
            documentType={documentType}
            setDocumentType={setDocumentType}
            />
            <UploadFile
            documentType={documentType}
            setDocumentType={setDocumentType}
            uploadedFile={uploadedFile}
            setUploadedFile={setUploadedFile}
            isDragging={isDragging}
            setIsDragging={setIsDragging}
            />
            <JobDescription
            jobDescription={jobDescription}
            setJobDescription={setJobDescription}
            />
            <AnalysisButton
            documentType={documentType}
            uploadedFile={uploadedFile}
            jobDescription={jobDescription}
            isAnalyzing={isAnalyzing}
            setIsAnalyzing={setIsAnalyzing}
            analysisResult={analysisResult}
            setAnalysisResult={setAnalysisResult}
            />
        </div>
    );
}