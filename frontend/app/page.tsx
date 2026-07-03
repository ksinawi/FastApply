"use client"
import Header from "../components/layout/Header";
import Container from "../components/layout/Container"
import Hero from "../components/layout/Hero"
import ApplicationForm from "../components/form/ApplicationForm";
import ResultsForm from "@/components/results/ResultsForm";

import type { AnalysisResult } from "../types/AnalysisResult"
import { useState } from "react";

const Page = () => {
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);

  return (
    <Container>
      <Header/>
      <main className="max-w-7xl mx-auto px-6">
        <Hero/>
        <div className="grid gap-8" style={{ gridTemplateColumns: "1fr 1fr" }}>
          <ApplicationForm
          analysisResult={analysisResult}
          setAnalysisResult={setAnalysisResult}
          />
          <ResultsForm
          analysisResult={analysisResult}
          setAnalysisResult={setAnalysisResult}
          />
        </div>
      </main>
    </Container>
  )
}

export default Page