"use client";

import { useState } from "react";
import DocumentTypeSelector from "./DocumentTypeSelector";
import UploadFile from "./UploadFile";
import JobDescription from "./JobDescription";


export default function ApplicationForm() {
    const [documentType, setDocumentType] = useState<"resume" | "coverLetter">("resume");
    const [uploadedFile, setUploadedFile] = useState<File | null>(null,);
    const [isDragging, setIsDragging] = useState<boolean>(false);
    const [jobDescription, setJobDescription] = useState("")

    return (
        <div className="grid gap-8" style={{ gridTemplateColumns: "1fr 1fr" }}>
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
            </div>
        </div>
    );
}