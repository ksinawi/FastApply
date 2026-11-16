import type { ResumeAnalysisResult, CoverLetterAnalysisResult, AnalysisResult } from "../types/AnalysisResult";

// Backend URL. NEXT_PUBLIC_API_URL overrides it (inlined at build time, so redeploy after
// changing it); otherwise production builds use the Render backend and dev uses localhost.
const DEFAULT_API_URL = process.env.NODE_ENV === "production"
    ? "https://fastapply-api.onrender.com"
    : "http://localhost:8000";

export const API_URL = (process.env.NEXT_PUBLIC_API_URL || DEFAULT_API_URL).replace(/\/+$/, "");

export class ApiError extends Error {}

async function errorMessage(response: Response, fallback: string): Promise<string> {
    try {
        const body = await response.json();
        if (typeof body?.detail === "string") return body.detail;
        // FastAPI validation errors come back as a list
        if (Array.isArray(body?.detail)) return "Some of the submitted information was invalid. Please check your inputs.";
    } catch {
        // response wasn't JSON
    }

    if (response.status === 429) return "Too many requests. Please wait a while and try again.";
    if (response.status >= 500) return "The server ran into a problem. Please try again in a moment.";
    return fallback;
}

async function request(path: string, init: RequestInit, fallback: string): Promise<Response> {
    let response: Response;

    try {
        response = await fetch(`${API_URL}${path}`, init);
    } catch {
        throw new ApiError("Couldn't reach the server. Check your connection, or try again in a minute if it's waking up.");
    }

    if (!response.ok) {
        throw new ApiError(await errorMessage(response, fallback));
    }

    return response;
}

export async function analyzeApplication(uploadedFile: File, jobDescription: string): Promise<ResumeAnalysisResult> {
    const formData = new FormData();
    formData.append("file", uploadedFile);
    formData.append("job_description", jobDescription);

    const response = await request("/process_application", { method: "POST", body: formData }, "Failed to analyze your resume.");
    const data = await response.json();

    return { ...data, kind: "resume" };
}

export async function analyzeCoverLetter(uploadedFile: File, jobDescription: string, researchCompany: boolean): Promise<CoverLetterAnalysisResult> {
    const formData = new FormData();
    formData.append("file", uploadedFile);
    formData.append("job_description", jobDescription);
    formData.append("research_company", String(researchCompany));

    const response = await request("/process_cover_letter", { method: "POST", body: formData }, "Failed to analyze your cover letter.");
    const data = await response.json();

    return { ...data, kind: "coverLetter" };
}

export async function downloadPdf(analysisResult: AnalysisResult): Promise<void> {
    const isResume = analysisResult.kind === "resume";
    const path = isResume ? "/download" : "/download_cover_letter";
    const body = isResume
        ? { resume: analysisResult.tailoredResume }
        : { coverLetter: analysisResult.tailoredCoverLetter };
    const filename = isResume ? "Tailored_Resume.pdf" : "Tailored_Cover_Letter.pdf";

    const response = await request(
        path,
        { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) },
        "Failed to generate the PDF.",
    );

    const url = window.URL.createObjectURL(await response.blob());
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
}
