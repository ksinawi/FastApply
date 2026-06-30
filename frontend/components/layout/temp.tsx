import { useState, useCallback } from "react";
import {
  FileText,
  Briefcase,
  CheckCircle2,
  AlertCircle,
  Sparkles,
  Upload,
  X,
  Copy,
  Check,
} from "lucide-react";

type AnalysisResult = {
  matchedSkills: string[];
  missingKeywords: string[];
  recommendations: string[];
  matchScore: number;
  tailoredContent: string;
};

function ScoreRing({ score }: { score: number }) {
  const r = 52;
  const circ = 2 * Math.PI * r;
  const offset = circ * (1 - score / 100);
  const color =
    score >= 80
      ? "#5EC97A"
      : score >= 60
        ? "#D4A942"
        : "#E05A5A";

  return (
    <div
      className="relative flex items-center justify-center"
      style={{ width: 128, height: 128 }}
    >
      <svg
        width="128"
        height="128"
        style={{ transform: "rotate(-90deg)" }}
      >
        <circle
          cx="64"
          cy="64"
          r={r}
          stroke="rgba(255,255,255,0.06)"
          strokeWidth="10"
          fill="none"
        />
        <circle
          cx="64"
          cy="64"
          r={r}
          stroke={color}
          strokeWidth="10"
          fill="none"
          strokeDasharray={circ}
          strokeDashoffset={offset}
          strokeLinecap="round"
          style={{
            transition:
              "stroke-dashoffset 1.2s cubic-bezier(0.16,1,0.3,1)",
          }}
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span
          className="text-3xl font-bold"
          style={{
            fontFamily: "'Playfair Display', serif",
            color,
          }}
        >
          {score}
        </span>
        <span
          className="text-xs tracking-widest uppercase"
          style={{
            color: "var(--muted-foreground)",
            letterSpacing: "0.12em",
          }}
        >
          match
        </span>
      </div>
    </div>
  );
}

export default function App() {
  const [documentType, setDocumentType] = useState<
    "resume" | "coverLetter"
  >("resume");
  const [uploadedFile, setUploadedFile] = useState<File | null>(
    null,
  );
  const [isDragging, setIsDragging] = useState(false);
  const [jobDescription, setJobDescription] = useState("");
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] =
    useState<AnalysisResult | null>(null);
  const [copied, setCopied] = useState(false);

  const handleFileUpload = (file: File) => {
    setUploadedFile(file);
    setAnalysisResult(null);
  };

  const handleInputChange = (
    e: React.ChangeEvent<HTMLInputElement>,
  ) => {
    const file = e.target.files?.[0];
    if (file) handleFileUpload(file);
  };

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files?.[0];
    if (file) handleFileUpload(file);
  }, []);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };
  const handleDragLeave = () => setIsDragging(false);

  const handleCopy = () => {
    if (analysisResult) {
      navigator.clipboard.writeText(
        analysisResult.tailoredContent,
      );
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const analyzeDocument = () => {
    if (!uploadedFile || !jobDescription) return;
    setIsAnalyzing(true);
    setTimeout(() => {
      setAnalysisResult({
        matchedSkills: [
          "JavaScript",
          "React",
          "TypeScript",
          "Problem Solving",
          "Team Collaboration",
          "Agile Development",
        ],
        missingKeywords: [
          "Node.js",
          "AWS",
          "CI/CD",
          "Docker",
          "Microservices",
        ],
        recommendations: [
          'Add quantifiable metrics — e.g. "Reduced load time by 40%" signals measurable impact.',
          "Weave in missing keywords naturally: AWS, Docker, and CI/CD appear prominently in the posting.",
          "Lead your summary with a seniority signal — name the team size you've led or the scale you've shipped at.",
          "Add a dedicated cloud/infrastructure skills row to your technical skills section.",
          "Reorder your experience bullets to surface the most relevant projects first.",
          "Consider listing any cloud certifications, even in-progress, to address a stated preference.",
        ],
        matchScore: 72,
        tailoredContent:
          documentType === "resume"
            ? `JOHN DOE
Senior Software Engineer

PROFESSIONAL SUMMARY
Results-driven Senior Software Engineer with 6+ years of experience building scalable web applications using JavaScript, React, and TypeScript. Proven track record of implementing CI/CD pipelines and cloud infrastructure on AWS. Experienced in Agile development and cross-functional team collaboration.

TECHNICAL SKILLS
• Frontend: React, TypeScript, JavaScript, HTML5, CSS3
• Backend: Node.js, REST APIs, Microservices Architecture
• Cloud & DevOps: AWS (EC2, S3, Lambda), Docker, CI/CD, Jenkins
• Tools: Git, JIRA, Agile/Scrum

PROFESSIONAL EXPERIENCE

Senior Software Engineer | Tech Company Inc. | 2020 – Present
• Led migration to microservices architecture, cutting deployment time by 60%
• Built and maintained CI/CD pipeline via Jenkins and Docker; release cadence improved 40%
• Architected and scaled AWS-hosted services to 100K+ daily active users
• Mentored 5 junior engineers in React and TypeScript best practices

Software Engineer | StartUp Co. | 2018 – 2020
• Built responsive SPAs in React and TypeScript with full test coverage
• Collaborated cross-functionally in two-week Agile sprints
• Improved application performance by 45% through profiling and optimization`
            : `Dear Hiring Manager,

I am writing to express my interest in the Senior Software Engineer role. With six years of experience shipping production React and TypeScript applications, and a recent focus on cloud infrastructure and DevOps, I believe I can contribute immediately to your team.

In my current role I implemented CI/CD pipelines using Jenkins and Docker that reduced our deployment window by 60% and doubled our release frequency. I also architected the AWS migration for our flagship product, which now serves over 100,000 daily users across EC2, S3, and Lambda.

Your emphasis on microservices and cloud-native development is directly aligned with the work I have been leading for the past three years. I thrive in Agile environments where close collaboration with product and design is the norm, and I bring experience mentoring junior engineers alongside my hands-on technical contributions.

I would welcome the opportunity to discuss how my background in React, TypeScript, AWS, and DevOps practices maps to your needs.

Thank you for your time and consideration.

Sincerely,
John Doe`,
      });
      setIsAnalyzing(false);
    }, 2200);
  };

  const canAnalyze =
    !!uploadedFile && !!jobDescription.trim() && !isAnalyzing;

  return (
    <div
      className="min-h-screen"
      style={{
        background: "var(--background)",
        fontFamily: "'DM Sans', sans-serif",
      }}
    >
      {/* Top bar */}
      <header
        className="border-b"
        style={{ borderColor: "var(--border)" }}
      >
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div
              className="flex items-center justify-center size-8"
              style={{
                background: "var(--primary)",
                borderRadius: "var(--radius)",
              }}
            >
              <Sparkles
                size={16}
                color="var(--primary-foreground)"
              />
            </div>
            <span
              className="text-sm font-medium tracking-wide uppercase"
              style={{
                color: "var(--muted-foreground)",
                letterSpacing: "0.1em",
              }}
            >
              ResuméAI
            </span>
          </div>
          <span
            className="text-xs tracking-widest uppercase"
            style={{
              color: "var(--muted-foreground)",
              letterSpacing: "0.12em",
            }}
          >
            Demo — mock analysis only
          </span>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-6 pt-14 pb-20">
        {/* Hero */}
        <div className="mb-14">
          <p
            className="text-xs tracking-widest uppercase mb-4"
            style={{
              color: "var(--primary)",
              letterSpacing: "0.14em",
            }}
          >
            AI-Powered Document Optimizer
          </p>
          <h1
            className="text-5xl leading-tight mb-4"
            style={{
              fontFamily: "'Playfair Display', serif",
              fontWeight: 600,
              color: "var(--foreground)",
              maxWidth: 560,
            }}
          >
            Make your application impossible to ignore.
          </h1>
          <p
            className="text-base"
            style={{
              color: "var(--muted-foreground)",
              maxWidth: 480,
            }}
          >
            Upload your résumé or cover letter, paste the job
            description, and receive a tailored rewrite with a
            match score and actionable edits.
          </p>
        </div>

        {/* Two-column layout */}
        <div
          className="grid gap-8"
          style={{ gridTemplateColumns: "1fr 1fr" }}
        >
          {/* ── LEFT: Inputs ── */}
          <div className="flex flex-col gap-5">
            {/* Document type toggle */}
            <Panel>
              <PanelLabel>Document type</PanelLabel>
              <div
                className="flex mt-3"
                style={{
                  background: "var(--muted)",
                  borderRadius: "var(--radius)",
                  padding: "3px",
                }}
              >
                {(["resume", "coverLetter"] as const).map(
                  (type) => (
                    <button
                      key={type}
                      onClick={() => {
                        setDocumentType(type);
                        setAnalysisResult(null);
                      }}
                      className="flex-1 flex items-center justify-center gap-2 py-2 text-sm transition-all duration-200"
                      style={{
                        borderRadius:
                          "calc(var(--radius) - 1px)",
                        background:
                          documentType === type
                            ? "var(--card)"
                            : "transparent",
                        color:
                          documentType === type
                            ? "var(--foreground)"
                            : "var(--muted-foreground)",
                        fontWeight:
                          documentType === type ? 500 : 400,
                        border:
                          documentType === type
                            ? "1px solid var(--border)"
                            : "1px solid transparent",
                      }}
                    >
                      <FileText size={14} />
                      {type === "resume"
                        ? "Résumé"
                        : "Cover Letter"}
                    </button>
                  ),
                )}
              </div>
            </Panel>

            {/* File upload */}
            <Panel>
              <PanelLabel>
                Upload your{" "}
                {documentType === "resume"
                  ? "résumé"
                  : "cover letter"}
              </PanelLabel>
              <p
                className="text-xs mt-0.5 mb-4"
                style={{ color: "var(--muted-foreground)" }}
              >
                PDF, DOCX, or TXT — max 10 MB
              </p>

              {uploadedFile ? (
                <div
                  className="flex items-center justify-between px-4 py-3"
                  style={{
                    background: "rgba(212,169,66,0.08)",
                    border: "1px solid rgba(212,169,66,0.25)",
                    borderRadius: "var(--radius)",
                  }}
                >
                  <div className="flex items-center gap-3">
                    <div
                      className="flex items-center justify-center size-8 shrink-0"
                      style={{
                        background: "rgba(212,169,66,0.15)",
                        borderRadius: "var(--radius)",
                      }}
                    >
                      <FileText
                        size={14}
                        color="var(--primary)"
                      />
                    </div>
                    <div>
                      <p
                        className="text-sm font-medium"
                        style={{ color: "var(--foreground)" }}
                      >
                        {uploadedFile.name}
                      </p>
                      <p
                        className="text-xs"
                        style={{
                          color: "var(--muted-foreground)",
                        }}
                      >
                        {(uploadedFile.size / 1024).toFixed(0)}{" "}
                        KB
                      </p>
                    </div>
                  </div>
                  <button
                    onClick={() => setUploadedFile(null)}
                    className="flex items-center justify-center size-6 transition-opacity hover:opacity-70"
                    style={{ color: "var(--muted-foreground)" }}
                  >
                    <X size={14} />
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
                    border: `1.5px dashed ${isDragging ? "var(--primary)" : "rgba(255,255,255,0.12)"}`,
                    borderRadius: "var(--radius)",
                    background: isDragging
                      ? "rgba(212,169,66,0.04)"
                      : "transparent",
                    padding: "2.5rem 1.5rem",
                  }}
                >
                  <div
                    className="flex items-center justify-center size-10 mb-3"
                    style={{
                      background: "var(--muted)",
                      borderRadius: "50%",
                    }}
                  >
                    <Upload
                      size={18}
                      color="var(--muted-foreground)"
                    />
                  </div>
                  <p
                    className="text-sm font-medium"
                    style={{ color: "var(--foreground)" }}
                  >
                    Drop file here, or{" "}
                    <span style={{ color: "var(--primary)" }}>
                      browse
                    </span>
                  </p>
                  <input
                    id="file-upload"
                    type="file"
                    className="hidden"
                    accept=".pdf,.doc,.docx,.txt"
                    onChange={handleInputChange}
                  />
                </label>
              )}
            </Panel>

            {/* Job description */}
            <Panel style={{ flex: 1 }}>
              <PanelLabel>Job description</PanelLabel>
              <p
                className="text-xs mt-0.5 mb-4"
                style={{ color: "var(--muted-foreground)" }}
              >
                Paste the full posting — more detail yields
                better results
              </p>
              <textarea
                value={jobDescription}
                onChange={(e) =>
                  setJobDescription(e.target.value)
                }
                placeholder="We are looking for a Senior Software Engineer with 5+ years experience in React, TypeScript, and cloud infrastructure..."
                className="w-full resize-none text-sm outline-none transition-colors duration-150"
                rows={8}
                style={{
                  background: "var(--muted)",
                  border: "1px solid var(--border)",
                  borderRadius: "var(--radius)",
                  padding: "0.875rem 1rem",
                  color: "var(--foreground)",
                  fontFamily: "'DM Sans', sans-serif",
                  lineHeight: 1.65,
                }}
                onFocus={(e) => {
                  e.currentTarget.style.borderColor =
                    "rgba(212,169,66,0.4)";
                }}
                onBlur={(e) => {
                  e.currentTarget.style.borderColor =
                    "var(--border)";
                }}
              />
            </Panel>

            {/* CTA */}
            <button
              onClick={analyzeDocument}
              disabled={!canAnalyze}
              className="flex items-center justify-center gap-2.5 w-full py-3.5 text-sm font-medium tracking-wide transition-all duration-200"
              style={{
                background: canAnalyze
                  ? "var(--primary)"
                  : "var(--muted)",
                color: canAnalyze
                  ? "var(--primary-foreground)"
                  : "var(--muted-foreground)",
                borderRadius: "var(--radius)",
                border: "none",
                cursor: canAnalyze ? "pointer" : "not-allowed",
                letterSpacing: "0.02em",
              }}
            >
              {isAnalyzing ? (
                <>
                  <span
                    className="size-4 border-2 border-t-transparent rounded-full animate-spin"
                    style={{
                      borderColor: "rgba(12,12,15,0.3)",
                      borderTopColor: "transparent",
                    }}
                  />
                  Analysing document…
                </>
              ) : (
                <>
                  <Sparkles size={16} />
                  Analyse &amp; Optimise
                </>
              )}
            </button>
          </div>

          {/* ── RIGHT: Results ── */}
          <div className="flex flex-col gap-5">
            {analysisResult ? (
              <>
                {/* Score */}
                <Panel>
                  <div className="flex items-center gap-6">
                    <ScoreRing
                      score={analysisResult.matchScore}
                    />
                    <div>
                      <p
                        className="text-xs uppercase tracking-widest mb-1"
                        style={{
                          color: "var(--muted-foreground)",
                          letterSpacing: "0.12em",
                        }}
                      >
                        Match score
                      </p>
                      <p
                        className="text-sm leading-relaxed"
                        style={{
                          color: "var(--foreground)",
                          maxWidth: 260,
                        }}
                      >
                        {analysisResult.matchScore >= 80
                          ? "Strong alignment. A few targeted additions could push this above 85."
                          : analysisResult.matchScore >= 60
                            ? "Solid foundation. Apply the recommendations below to close the gap."
                            : "Room to grow. The tailored version below addresses the key gaps."}
                      </p>
                    </div>
                  </div>
                </Panel>

                {/* Matched skills */}
                <Panel>
                  <div className="flex items-center gap-2 mb-4">
                    <CheckCircle2 size={15} color="#5EC97A" />
                    <PanelLabel style={{ marginBottom: 0 }}>
                      Matched skills
                    </PanelLabel>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {analysisResult.matchedSkills.map(
                      (skill, i) => (
                        <Chip key={i} variant="green">
                          {skill}
                        </Chip>
                      ),
                    )}
                  </div>
                </Panel>

                {/* Missing keywords */}
                <Panel>
                  <div className="flex items-center gap-2 mb-4">
                    <AlertCircle size={15} color="#D4A942" />
                    <PanelLabel style={{ marginBottom: 0 }}>
                      Missing keywords
                    </PanelLabel>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {analysisResult.missingKeywords.map(
                      (kw, i) => (
                        <Chip key={i} variant="amber">
                          {kw}
                        </Chip>
                      ),
                    )}
                  </div>
                </Panel>

                {/* Recommendations */}
                <Panel>
                  <div className="flex items-center gap-2 mb-5">
                    <Briefcase
                      size={15}
                      color="var(--primary)"
                    />
                    <PanelLabel style={{ marginBottom: 0 }}>
                      Recommendations
                    </PanelLabel>
                  </div>
                  <ol className="flex flex-col gap-4">
                    {analysisResult.recommendations.map(
                      (rec, i) => (
                        <li
                          key={i}
                          className="flex gap-3 items-start"
                        >
                          <span
                            className="shrink-0 flex items-center justify-center text-xs font-medium"
                            style={{
                              width: 22,
                              height: 22,
                              borderRadius: "50%",
                              background:
                                "rgba(212,169,66,0.12)",
                              color: "var(--primary)",
                              fontFamily:
                                "'DM Mono', monospace",
                              paddingTop: 1,
                            }}
                          >
                            {i + 1}
                          </span>
                          <p
                            className="text-sm leading-relaxed"
                            style={{
                              color: "var(--foreground)",
                              paddingTop: 2,
                            }}
                          >
                            {rec}
                          </p>
                        </li>
                      ),
                    )}
                  </ol>
                </Panel>

                {/* Tailored content */}
                <Panel>
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center gap-2">
                      <Sparkles
                        size={15}
                        color="var(--primary)"
                      />
                      <PanelLabel style={{ marginBottom: 0 }}>
                        AI-tailored version
                      </PanelLabel>
                    </div>
                    <button
                      onClick={handleCopy}
                      className="flex items-center gap-1.5 text-xs transition-opacity hover:opacity-70"
                      style={{
                        color: copied
                          ? "#5EC97A"
                          : "var(--muted-foreground)",
                      }}
                    >
                      {copied ? (
                        <Check size={13} />
                      ) : (
                        <Copy size={13} />
                      )}
                      {copied ? "Copied" : "Copy"}
                    </button>
                  </div>
                  <div
                    className="max-h-80 overflow-y-auto"
                    style={{
                      background: "var(--muted)",
                      border: "1px solid var(--border)",
                      borderRadius: "var(--radius)",
                      padding: "1rem",
                      scrollbarWidth: "thin",
                      scrollbarColor:
                        "rgba(255,255,255,0.1) transparent",
                    }}
                  >
                    <pre
                      className="whitespace-pre-wrap text-xs leading-relaxed"
                      style={{
                        fontFamily: "'DM Mono', monospace",
                        color: "var(--foreground)",
                      }}
                    >
                      {analysisResult.tailoredContent}
                    </pre>
                  </div>
                </Panel>
              </>
            ) : (
              /* Empty state */
              <div
                className="flex flex-col items-center justify-center text-center h-full min-h-96"
                style={{
                  border: "1.5px dashed rgba(255,255,255,0.07)",
                  borderRadius: "var(--radius)",
                }}
              >
                <div
                  className="flex items-center justify-center size-14 mb-5"
                  style={{
                    background: "var(--muted)",
                    borderRadius: "50%",
                  }}
                >
                  <Sparkles
                    size={22}
                    color="var(--muted-foreground)"
                  />
                </div>
                <p
                  className="text-lg mb-2"
                  style={{
                    fontFamily: "'Playfair Display', serif",
                    color: "var(--foreground)",
                  }}
                >
                  Analysis will appear here
                </p>
                <p
                  className="text-sm max-w-xs"
                  style={{
                    color: "var(--muted-foreground)",
                    lineHeight: 1.7,
                  }}
                >
                  Upload your document and paste a job
                  description, then click Analyse.
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

/* ── Small helper components ── */

function Panel({
  children,
  style,
}: {
  children: React.ReactNode;
  style?: React.CSSProperties;
}) {
  return (
    <div
      style={{
        background: "var(--card)",
        border: "1px solid var(--border)",
        borderRadius: "var(--radius)",
        padding: "1.25rem 1.5rem",
        ...style,
      }}
    >
      {children}
    </div>
  );
}

function PanelLabel({
  children,
  style,
}: {
  children: React.ReactNode;
  style?: React.CSSProperties;
}) {
  return (
    <p
      className="text-xs uppercase tracking-widest"
      style={{
        color: "var(--muted-foreground)",
        letterSpacing: "0.12em",
        marginBottom: "0.25rem",
        ...style,
      }}
    >
      {children}
    </p>
  );
}

function Chip({
  children,
  variant,
}: {
  children: React.ReactNode;
  variant: "green" | "amber";
}) {
  const styles =
    variant === "green"
      ? {
          background: "rgba(94,201,122,0.08)",
          color: "#5EC97A",
          border: "1px solid rgba(94,201,122,0.2)",
        }
      : {
          background: "rgba(212,169,66,0.08)",
          color: "#D4A942",
          border: "1px solid rgba(212,169,66,0.2)",
        };

  return (
    <span
      className="text-xs font-medium px-2.5 py-1"
      style={{ borderRadius: "var(--radius)", ...styles }}
    >
      {children}
    </span>
  );
}