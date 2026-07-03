import { AnalysisResult } from "../types/AnalysisResult";

const API_URL = "http://localhost:8000";

export async function analyzeApplication(uploadedFile: File, jobDescription: string):Promise<AnalysisResult> {
    
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

    return await response.json()
}