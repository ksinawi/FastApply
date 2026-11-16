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
      <main className="max-w-7xl mx-auto px-4 sm:px-6 pb-16">
        <Hero/>
        <div className="grid gap-8 grid-cols-1 lg:grid-cols-2">
          <ApplicationForm
          setAnalysisResult={setAnalysisResult}
          />
          <ResultsForm analysisResult={analysisResult}/>
        </div>
      </main>
    </Container>
  )
}

export default Page