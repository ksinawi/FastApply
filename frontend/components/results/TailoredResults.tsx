import Panel from "../ui/Panel";
import PanelLabel from "../ui/PanelLabel";

import type { AnalysisResult } from "../../types/AnalysisResult";
import type { Resume } from "../../types/Resume";
import type { CoverLetter } from "../../types/CoverLetter";
import { Check, Copy, Sparkles } from "lucide-react";


type Props = {
    analysisResult: AnalysisResult | null;

    copied: boolean;
    setCopied: React.Dispatch<
        React.SetStateAction<boolean>
    >;
};

const dateRange = (start: string, end: string) => [start, end].filter(Boolean).join(" - ");

const contactLine = (contact: Resume["contact_info"] | CoverLetter["contact_info"]) =>
    [contact?.location, contact?.email, contact?.phone, ...(contact?.links ?? [])]
        .filter(Boolean)
        .join(" · ");

const resumeToPlainText = (resume: Resume): string => {
    const lines: string[] = [];
    const { contact_info } = resume;

    if (contact_info?.name) lines.push(contact_info.name);
    if (contactLine(contact_info)) lines.push(contactLine(contact_info).replaceAll(" · ", " | "));

    if (resume.skills?.length) {
        lines.push("", "SKILLS", resume.skills.join(", "));
    }

    if (resume.experience?.length) {
        lines.push("", "EXPERIENCE");
        resume.experience.forEach((exp) => {
            lines.push(`${exp.title} — ${exp.company} (${dateRange(exp.start_date, exp.end_date)})`);
            exp.responsibilities.forEach((r) => lines.push(`  • ${r}`));
        });
    }

    if (resume.projects?.length) {
        lines.push("", "PROJECTS");
        resume.projects.forEach((proj) => {
            const tech = proj.technologies?.length ? ` [${proj.technologies.join(", ")}]` : "";
            lines.push(`${proj.name}${tech} (${dateRange(proj.start_date, proj.end_date)})`);
            proj.description.forEach((d) => lines.push(`  • ${d}`));
        });
    }

    if (resume.education?.length) {
        lines.push("", "EDUCATION");
        resume.education.forEach((edu) => {
            lines.push(`${edu.degree} — ${edu.institution} (${dateRange(edu.start_date, edu.end_date)})`);
            if (edu.relevant_courses?.length) {
                lines.push(`  Relevant coursework: ${edu.relevant_courses.join(", ")}`);
            }
        });
    }

    return lines.join("\n");
};

const coverLetterToPlainText = (coverLetter: CoverLetter): string => {
    const lines: string[] = [];
    const { contact_info } = coverLetter;

    if (contact_info?.name) lines.push(contact_info.name);
    if (contactLine(contact_info)) lines.push(contactLine(contact_info).replaceAll(" · ", " | "));

    lines.push("", coverLetter.recipient, "", coverLetter.opening_paragraph);
    coverLetter.body_paragraphs.forEach((p) => lines.push("", p));
    lines.push("", coverLetter.closing_paragraph, "", coverLetter.signature);

    return lines.join("\n");
};

const ResumePreview = ({ resume }: { resume: Resume }) => (
    <>
        {resume.contact_info?.name && (
            <div>
                <p className="text-sm font-medium" style={{color: "#EEE9DF"}}>{resume.contact_info.name}</p>
                <p className="text-xs" style={{color: "#7A7A88"}}>{contactLine(resume.contact_info)}</p>
            </div>
        )}

        {resume.skills?.length > 0 && (
            <div>
                <PanelLabel>Skills</PanelLabel>
                <p className="text-xs leading-relaxed" style={{color: "#EEE9DF"}}>{resume.skills.join(", ")}</p>
            </div>
        )}

        {resume.experience?.length > 0 && (
            <div>
                <PanelLabel>Experience</PanelLabel>
                <div className="flex flex-col gap-3 mt-1">
                    {resume.experience.map((exp, i) => (
                        <div key={i}>
                            <div className="flex items-baseline justify-between gap-2">
                                <p className="text-xs font-medium" style={{color: "#EEE9DF"}}>{exp.title} — {exp.company}</p>
                                <p className="text-xs whitespace-nowrap" style={{color: "#7A7A88"}}>{dateRange(exp.start_date, exp.end_date)}</p>
                            </div>
                            <ul className="list-disc list-outside ml-4 mt-1">
                                {exp.responsibilities.map((r, j) => (
                                    <li key={j} className="text-xs leading-relaxed" style={{color: "#EEE9DF"}}>{r}</li>
                                ))}
                            </ul>
                        </div>
                    ))}
                </div>
            </div>
        )}

        {resume.projects?.length > 0 && (
            <div>
                <PanelLabel>Projects</PanelLabel>
                <div className="flex flex-col gap-3 mt-1">
                    {resume.projects.map((proj, i) => (
                        <div key={i}>
                            <div className="flex items-baseline justify-between gap-2">
                                <p className="text-xs font-medium" style={{color: "#EEE9DF"}}>
                                    {proj.name}{proj.technologies?.length ? ` (${proj.technologies.join(", ")})` : ""}
                                </p>
                                <p className="text-xs whitespace-nowrap" style={{color: "#7A7A88"}}>{dateRange(proj.start_date, proj.end_date)}</p>
                            </div>
                            <ul className="list-disc list-outside ml-4 mt-1">
                                {proj.description.map((d, j) => (
                                    <li key={j} className="text-xs leading-relaxed" style={{color: "#EEE9DF"}}>{d}</li>
                                ))}
                            </ul>
                        </div>
                    ))}
                </div>
            </div>
        )}

        {resume.education?.length > 0 && (
            <div>
                <PanelLabel>Education</PanelLabel>
                <div className="flex flex-col gap-2 mt-1">
                    {resume.education.map((edu, i) => (
                        <div key={i}>
                            <div className="flex items-baseline justify-between gap-2">
                                <p className="text-xs font-medium" style={{color: "#EEE9DF"}}>{edu.degree} — {edu.institution}</p>
                                <p className="text-xs whitespace-nowrap" style={{color: "#7A7A88"}}>{dateRange(edu.start_date, edu.end_date)}</p>
                            </div>
                            {edu.relevant_courses?.length > 0 && (
                                <p className="text-xs leading-relaxed" style={{color: "#7A7A88"}}>
                                    Relevant coursework: {edu.relevant_courses.join(", ")}
                                </p>
                            )}
                        </div>
                    ))}
                </div>
            </div>
        )}
    </>
);

const CoverLetterPreview = ({ coverLetter }: { coverLetter: CoverLetter }) => (
    <>
        {coverLetter.contact_info?.name && (
            <div>
                <p className="text-sm font-medium" style={{color: "#EEE9DF"}}>{coverLetter.contact_info.name}</p>
                <p className="text-xs" style={{color: "#7A7A88"}}>{contactLine(coverLetter.contact_info)}</p>
            </div>
        )}

        <div className="flex flex-col gap-3">
            <p className="text-xs leading-relaxed" style={{color: "#EEE9DF"}}>{coverLetter.recipient}</p>
            <p className="text-xs leading-relaxed" style={{color: "#EEE9DF"}}>{coverLetter.opening_paragraph}</p>
            {coverLetter.body_paragraphs.map((p, i) => (
                <p key={i} className="text-xs leading-relaxed" style={{color: "#EEE9DF"}}>{p}</p>
            ))}
            <p className="text-xs leading-relaxed" style={{color: "#EEE9DF"}}>{coverLetter.closing_paragraph}</p>
            <p className="text-xs leading-relaxed whitespace-pre-line" style={{color: "#EEE9DF"}}>{coverLetter.signature}</p>
        </div>
    </>
);

const TailoredResults = ({ analysisResult, copied, setCopied}: Props) => {
    if (!analysisResult) {
        return (
          <Panel>
            <p className="text-sm text-gray-400">No analysis yet.</p>
          </Panel>
        );
    }

    const handleCopy = () => {
        const text = analysisResult.kind === "resume"
            ? resumeToPlainText(analysisResult.tailoredResume)
            : coverLetterToPlainText(analysisResult.tailoredCoverLetter);

        navigator.clipboard.writeText(text).then(() => {
            setCopied(true);
            setTimeout(() => setCopied(false), 2000);
        }).catch((err) => console.error("Copy failed", err));
    };

    return (
        <Panel>
            <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-2">
                    <Sparkles size={15} color="#D4A942"/>
                    <PanelLabel>AI-Tailored Version</PanelLabel>
                </div>
                <button
                    onClick={handleCopy}
                    className="flex items-center gap-1.5 text-xs transition-opacity hover:opacity-70"
                    style={{
                    color: copied
                        ? "#5EC97A"
                        : "#7A7A88"
                    }}
                    >
                    {copied ? (
                        <Check size={13}/>
                    ) : (
                        <Copy size={13}/>
                    )}
                    {copied ? "Copied" : "Copy"}
                </button>
            </div>
            <div
                className="max-h-80 overflow-y-auto flex flex-col gap-4"
                style={{
                background: "#1C1C21",
                border: "1px solid rgba(255, 255, 255, 0.07)",
                borderRadius: "0.25rem",
                padding: "1rem",
                scrollbarWidth: "thin",
                scrollbarColor: "rgba(255,255,255,0.1) transparent"
                }}>
                {analysisResult.kind === "resume" ? (
                    <ResumePreview resume={analysisResult.tailoredResume} />
                ) : (
                    <CoverLetterPreview coverLetter={analysisResult.tailoredCoverLetter} />
                )}
            </div>
        </Panel>
    )
}

export default TailoredResults;
