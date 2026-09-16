import { ResumeAnalysisResult, CoverLetterAnalysisResult } from "../types/AnalysisResult";

const API_URL = "http://localhost:8000";

export async function analyzeApplication(uploadedFile: File, jobDescription: string):Promise<ResumeAnalysisResult> {

    const formData = new FormData();

    formData.append("file", uploadedFile);
    formData.append("job_description", jobDescription);

    const response = await fetch(`${API_URL}/process_application`, {
        method: "POST",
        body: formData,
    });

    if (!response.ok) {
        throw new Error("Error: Failed to analyze application.");
    }

    const data = await response.json();

    return { ...data, kind: "resume" };
}

export async function analyzeCoverLetter(uploadedFile: File, jobDescription: string):Promise<CoverLetterAnalysisResult> {

    const formData = new FormData();

    formData.append("file", uploadedFile);
    formData.append("job_description", jobDescription);

    const response = await fetch(`${API_URL}/process_cover_letter`, {
        method: "POST",
        body: formData,
    });

    if (!response.ok) {
        throw new Error("Error: Failed to analyze cover letter.");
    }

    const data = await response.json();

    return { ...data, kind: "coverLetter" };
}
