import Header from "../components/layout/Header";
import Container from "../components/layout/Container"
import Hero from "../components/layout/Hero"
import ApplicationForm from "../components/form/ApplicationForm";

const Page = () => {
  return (
    <Container>
      <Header/>
      <main className="max-w-7xl mx-auto px-6">
        <Hero/>
        <ApplicationForm/>
      </main>
    </Container>
  )
}

export default Page