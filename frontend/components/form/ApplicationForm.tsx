"use client";

import { useState } from "react";
import DocumentTypeSelector from "./DocumentTypeSelector";
import UploadFile from "./UploadFile";
import JobDescription from "./JobDescription";
import AnalysisButton from "./AnalysisButton";


export default function ApplicationForm() {
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
            uploadedFile={uploadedFile}
            setUploadedFile={setUploadedFile}
            jobDescription={jobDescription}
            setJobDescription={setJobDescription}
            isAnalyzing={isAnalyzing}
            setIsAnalyzing={setIsAnalyzing}
            />
        </div>
    );
}