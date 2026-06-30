import Panel from "../ui/Panel";
import PanelLabel from "../ui/PanelLabel";

type Props = {
    jobDescription: string;
    setJobDescription: React.Dispatch<
        React.SetStateAction<string>
    >;
};

const JobDescription = ({
    jobDescription,
    setJobDescription
}: Props) => {
  return (
    <Panel>
        <PanelLabel>Job Description</PanelLabel>
        <p className="text-xs mt-0.5 mb-4" style={{color: "#7A7A88"}}>
            Paste the full posting - more details yields better results
        </p>
        <textarea 
         value={jobDescription} 
         onChange={(e) => setJobDescription(e.target.value)}
         placeholder="We are looking for a Senior Software Engineer with 5+ years experience in Python..."
         className="w-full resize-none text-sm outline-none transition-colors duration-150"
         rows={8}
         style={{
            background: "#1C1C21",
            border: "1px solid rgba(255, 255, 255, 0.07)",
            borderRadius: "0.25rem",
            padding: "0.875rem 1rem",
            color: "#EEE9DF",
            fontFamily: "'DM Sans', sans-serif",
            lineHeight: 1.65
         }} 
         onFocus={(e) => {
            e.currentTarget.style.borderColor = "rgba(212,169,66,0.4)";
         }}
         onBlur={(e) => {
            e.currentTarget.style.borderColor = "rgba(255, 255, 255, 0.07)"
         }}
        />
    </Panel>
  )
}

export default JobDescription