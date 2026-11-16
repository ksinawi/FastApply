import { FileText, Upload, X } from "lucide-react";

import Panel from "../ui/Panel";
import PanelLabel from "../ui/PanelLabel";
import React, { useState } from "react";
import ErrorMessage from "../ui/ErrorMessage";

const MAX_FILE_MB = 5;
const ACCEPTED = ["pdf", "docx", "txt"];

type Props = {
    documentType: "resume" | "coverLetter";
    uploadedFile: File | null;
    setUploadedFile: React.Dispatch<
        React.SetStateAction<File | null>
    >;

    isDragging: boolean;
    setIsDragging: React.Dispatch<
        React.SetStateAction<boolean>
    >;
};

const UploadFile = ({
    documentType,
    uploadedFile,
    setUploadedFile,
    isDragging,
    setIsDragging,
}: Props) => {

    const [fileError, setFileError] = useState<string | null>(null);

    const handleFileUpload = (file: File | null) => {
        if (!file) return;

        const extension = file.name.split(".").pop()?.toLowerCase() ?? "";
        if (!ACCEPTED.includes(extension)) {
            setFileError("Please upload a PDF, DOCX, or TXT file.");
            return;
        }
        if (file.size > MAX_FILE_MB * 1024 * 1024) {
            setFileError(`That file is too large. The limit is ${MAX_FILE_MB} MB.`);
            return;
        }

        setFileError(null);
        setUploadedFile(file);
    }

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>,) => {
        const file = e.target.files?.[0];
        handleFileUpload(file || null);
    }

    const handleDrop = (e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(false);
        const file = e.dataTransfer.files?.[0];
        handleFileUpload(file || null);
    };

    const handleDragOver = (e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(true);
    }

    const handleDragLeave = () => setIsDragging(false);
    
    return (
    <Panel>
        <PanelLabel>
            Upload Your{" "}
            {documentType === "resume"
                ? "resume"
                : "cover letter"}
        </PanelLabel>
        <p className="text-xs mt-0.5 mb-4" style={{ color: "#7A7A88" }}>
            PDF, DOCX, or TXT
        </p>
        {uploadedFile ? (
            <div 
                className="flex items-center justify-between px-4 py-3"
                style={{
                    background: "rgba(212,169,66,0.08)",
                    border: "1px solid rgba(212,169,66,0.25)",
                    borderRadius: "0.25rem"
                }}
            >
                <div className="flex items-center gap-3">
                    <div className="flex items-center justify-center size-8 shrink-0" style={{background: "rgba(212,169,66,0.15)", borderRadius: "0.25rem"}}>
                        <FileText size={14} color="#D4A942"/>
                    </div>
                    <div>
                        <p className="text-sm font-medium" style={{color: "#EEE9DF"}}>
                            {uploadedFile.name}
                        </p>
                        <p className="text-xs" style={{color: "#7A7A88"}}>
                            {(uploadedFile.size / 1024).toFixed(0)}{" "}
                            KB
                        </p>
                    </div>
                </div>
                <button type="button" aria-label="Remove file" onClick={() => setUploadedFile(null)} className="flex items-center justify-center size-6 transition-opacity hover:opacity-70" style={{color: "#7A7A88"}}>
                    <X size={14}/>
                </button>
            </div>
        ) : (
            <label 
            htmlFor="file-upload"
            onDrop={handleDrop}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            className="flex flex-col items-center justify-center cursor-pointer transition-all duration-200"
            style={{
                border: `1.5px dashed ${isDragging ? "#D4A942": "rgba(255,255,255,0.12)"}`,
                borderRadius: "0.25rem",
                background: isDragging
                    ? "rgba(212,169,66,0.04)"
                    : "transparent",
                padding: "2.5rem 1.5rem"
            }}
            >
                <div className="flex items-center justify-center size-10 mb-3" style={{background: "#1C1C21", borderRadius: "50%"}}>
                    <Upload size={18} color="#7A7A88"/>
                </div>
                <p className="text-sm font-medium" style={{color: "#EEE9DF"}}>
                    Drop file here, or{" "}
                    <span style={{color: "#D4A942"}}>browse</span>
                </p>
                <input id="file-upload" type="file" className="hidden" accept=".pdf,.docx,.txt" onChange={handleInputChange}/>
            </label>
        )}
        {fileError && <div className="mt-3"><ErrorMessage message={fileError}/></div>}
    </Panel>
    )
}

export default UploadFile