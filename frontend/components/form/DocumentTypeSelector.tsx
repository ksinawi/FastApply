"use client"
import Panel from "../ui/Panel";
import PanelLabel from "../ui/PanelLabel";
import { FileText } from "lucide-react";

type Props = {
    documentType: "resume" | "coverLetter";
    setDocumentType: React.Dispatch<
        React.SetStateAction<"resume" | "coverLetter">
    >;
};

const DocumentTypeSelector = ({
    documentType,
    setDocumentType,
}: Props) => {
    return (
        <Panel>
            <PanelLabel>Document Type</PanelLabel>
            <div className="flex mt-3" style={{background: "#1C1C21", borderRadius: "0.25rem", padding: "3px"}}>
                {(["resume", "coverLetter"] as const).map(
                    (type) => (
                        <button key={type} onClick={() => {
                            setDocumentType(type);
                        }}
                        className="flex-1 flex items-center justify-center gap-2 py-2 text-sm transition-all duration-200"
                        style={{
                            borderRadius: "calc(0.25rem - 1px)",
                            background: 
                                documentType === type
                                    ? "#141418"
                                    : "transparent",
                            color: 
                                documentType === type
                                    ? "#EEE9DF"
                                    : "#7A7A88",
                            fontWeight:
                                documentType === type ? 500 : 400,
                            border:
                                documentType === type
                                    ? "1px solid rgba(255, 255, 255, 0.07)"
                                    : "1px solid transparent"
                        }}>
                            <FileText size={14}/>
                            {type === "resume"
                                ? "Resume"
                                : "Cover Letter"
                            }
                        </button>
                    ),
                )}
            </div>
        </Panel>
    );
};

export default DocumentTypeSelector;