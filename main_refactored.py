"""
Refactored main.py using industry-standard LangChain project structure

This demonstrates how to use the modular architecture for cleaner,
more maintainable code.
"""

from dotenv import load_dotenv

# Import the new modular components
from src.chains.experience_chain import ExperienceChain
from src.workflows.states import ResumeState

# Import existing components (to be refactored)
from src.format import LatexFormatter
from src.format import LatexCompiler


class AriaResumeGenerator:
    """Main resume generation orchestrator using modular architecture"""
    
    def __init__(self):
        """Initialize with modular components"""
        self.experience_chain = ExperienceChain()
        # TODO: Initialize other chains
        # self.skills_chain = SkillsChain()
        # self.project_chain = ProjectChain()
        # self.highlights_chain = HighlightsChain()
    
    def generate_resume(self, job_posting: str, company: str, position: str) -> ResumeState:
        """Generate a complete resume using the modular workflow"""
        
        print(f"🚀 Generating resume for {position} at {company}")
        
        # Initialize state
        state = ResumeState(
            job_posting=job_posting,
            company=company,
            position=position,
            experiences="",
            skills="", 
            project_names=[],
            project_summaries="",
            highlights="",
            resume_latex="",
            tex_file=None,
            pdf_file=None,
            context=[],
            generation_metadata={}
        )
        
        # Step 1: Generate experiences
        print("📝 Generating experiences...")
        experience_result = self.experience_chain.invoke({
            "job_posting": job_posting
        })
        state["experiences"] = experience_result["experiences"]
        state["company"] = company
        state["position"] = position
        
        # TODO: Add other steps
        # Step 2: Generate skills
        # Step 3: Select and summarize projects  
        # Step 4: Generate highlights
        # Step 5: Compile final resume
        
        print("✅ Resume generation complete!")
        return state
    
    def save_resume(self, result_state: ResumeState):
        # latex_code = LatexFormatter.format_resume(
        #     highlights=result_state["highlights"],
        #     experiences=result_state["experiences"],
        #     skills=result_state["skills"],
        #     projects=result_state["project_summaries"]
        # )
        latex_code = LatexFormatter.format_resume(
            highlights="",
            experiences=result_state["experiences"],
            skills="",
            projects=""
        )
        output_dir = f"./output/resumes/{result_state['company']}"
        latex_filename = f"{result_state['position']}.tex"
        return LatexCompiler.compile_latex(latex_code, output_dir, latex_filename)


def main():
    """Main execution function demonstrating the new architecture"""
    load_dotenv()
    
    # Sample job posting
    sample_job_posting = """
    Responsibilities

    Develop, train, and deploy machine learning models on Google Cloud Platform (GCP), leveraging tools such as VertexAI, GenApp Builder, PalmApi and BigQueryML.
    Collaborate with cross-functional teams to gather requirements, define project goals, and design scalable machine learning architectures.
    Conduct data preprocessing, feature engineering, and model evaluation to ensure high-quality and reliable models.
    Implement and optimize machine learning algorithms and pipelines to handle large-scale text-based datasets.
    Explore and experiment with generative AI techniques, including large language models, to solve complex text-related problems.
    Monitor and maintain deployed models, ensuring performance, scalability, and reliability in production environments.
    Stay up-to-date with the latest advancements in machine learning, generative AI, and text-based models, and proactively propose innovative solutions to enhance existing systems.

    Requirements

    Bachelor's or advanced degree in Computer Science, Engineering, or a related field.
    Strong experience in machine learning engineering, with a focus on developing and deploying models in production environments.
    Proficiency in using Google Cloud Platform (GCP) tools and services for machine learning, such as Vertex AI, BigQuery, and TensorFlow.
    Solid understanding of deep learning architectures, natural language processing (NLP), and generative AI models, particularly in the text domain.
    Proficiency in Python and experience with relevant libraries and frameworks, such as TensorFlow, PyTorch, or Keras.
    Experience with data preprocessing, feature engineering, and model evaluation techniques for text-based datasets.
    Familiarity with MLOps practices, version control, and CI/CD pipelines for machine learning.
    Strong problem-solving skills and the ability to work on complex projects independently or collaboratively.
    Excellent communication skills, with the ability to convey complex technical concepts to both technical and non-technical stakeholders.

    Preferred Qualifications

    Experience with large language models, such as GPT-3, BERT, or Transformer-based models.
    Familiarity with cloud-based machine learning services and technologies, beyond Google Cloud Platform.
    Knowledge of scalable distributed computing frameworks, such as Apache Spark or Hadoop.
    Contributions to open-source machine learning projects or research publications in the field.
    """
    
    # Create generator and run
    generator = AriaResumeGenerator()
    result_state = generator.generate_resume(
        job_posting=sample_job_posting,
        company="TechCorp",
        position="ML Engineer"
    )
    paths = generator.save_resume(result_state=result_state)
    print(paths)


if __name__ == "__main__":
    main()