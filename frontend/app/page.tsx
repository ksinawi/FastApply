import Header from "../components/layout/Header";
import Container from "../components/layout/Container"
import Hero from "../components/layout/Hero"
import ApplicationForm from "../components/form/ApplicationForm";
import ResultsForm from "@/components/results/ResultsForm";

const Page = () => {
  return (
    <Container>
      <Header/>
      <main className="max-w-7xl mx-auto px-6">
        <Hero/>
        <div className="grid gap-8" style={{ gridTemplateColumns: "1fr 1fr" }}>
          <ApplicationForm/>
          <ResultsForm/>
        </div>
      </main>
    </Container>
  )
}

export default Page