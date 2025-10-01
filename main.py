from dotenv import load_dotenv
from glob import glob
from langchain import hub
from langchain.chat_models import init_chat_model
from langchain_openai import OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import START, StateGraph
from langchain.prompts import PromptTemplate
from langchain_core.documents import Document
from typing_extensions import List, TypedDict
from IPython.display import Image, display
import json
import re
from formating import *


class State(TypedDict):
    job: str
    resume: str
    prompt: str
    context: List[Document]
    answer: str
    experiences: str
    skills: str
    project_names: List[str]
    projects: str
    highlights: str
    cover_letter: str
    company: str
    position: str
    tex_file: str
    pdf_file: str


class Aria:
    def __init__(self):
        self.llm = init_chat_model("gpt-4o-mini", model_provider="openai")
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
        self.vector_store = InMemoryVectorStore(self.embeddings)

        self.chunk_size = 1000
        self.chunk_overlap = 200
        self.add_start_index = True

        self.prompt = hub.pull("rlm/rag-prompt")

        self.build_graph()

    def extract_latex_experiences(self, text):
        """Extract LaTeX experience entries from LLM response"""
        # Remove markdown code block markers if present
        text = re.sub(r'```latex\n?', '', text)
        text = re.sub(r'```\n?', '', text)

        # Pattern to match \\resumeSubheading blocks
        pattern = r'(\\resumeSubheading\s*\{[^}]*\}\{[^}]*\}\s*\{[^}]*\}\{[^}]*\}\s*\\resumeItemListStart.*?\\resumeItemListEnd)'
        matches = re.findall(pattern, text, re.DOTALL)

        if matches:
            return '\n\n'.join(matches)

        # Fallback: look for any \\resumeSubheading pattern
        fallback_pattern = r'(\\resumeSubheading.*?)(?=\\resumeSubheading|$)'
        fallback_matches = re.findall(fallback_pattern, text, re.DOTALL)

        if fallback_matches:
            return '\n\n'.join(fallback_matches)

        return text.strip()

    def extract_latex_skills(self, text):
        """Extract LaTeX skills section from LLM response"""
        # Remove markdown code block markers if present
        text = re.sub(r'```latex\n?', '', text)
        text = re.sub(r'```\n?', '', text)

        # Pattern to match \\begin{itemize} ... \\end{itemize} block
        pattern = r'(\\begin\{itemize\}\[leftmargin=[^\]]*\].*?\\end\{itemize\})'
        match = re.search(pattern, text, re.DOTALL)

        if match:
            return match.group(1)

        # Fallback: look for \\small{\\item{ ... }} pattern
        fallback_pattern = r'(\\small\{\\item\{.*?\}\})'
        fallback_match = re.search(fallback_pattern, text, re.DOTALL)

        if fallback_match:
            return f"\\begin{{itemize}}[leftmargin=0.15in, label={{}}]\n{fallback_match.group(1)}\n\\end{{itemize}}"

        return text.strip()

    def extract_json_from_response(self, text):
        """Extract JSON array from LLM response for project selection"""
        # Pattern to match JSON array
        pattern = r'\[(.*?)\]'
        match = re.search(pattern, text, re.DOTALL)

        if match:
            try:
                json_str = '[' + match.group(1) + ']'
                return json.loads(json_str)
            except json.JSONDecodeError:
                pass

        # Fallback: try to extract quoted strings
        quoted_pattern = r'"([^"]+)"'
        quoted_matches = re.findall(quoted_pattern, text)

        if quoted_matches:
            return quoted_matches[:4]  # Return max 4 projects

        return []

    def extract_latex_experiences(self, text):
        """Extract LaTeX experience entries from LLM response"""
        # Pattern to match \resumeSubheading blocks
        pattern = r'(\\resumeSubheading\s*\{[^}]*\}\{[^}]*\}\s*\{[^}]*\}\{[^}]*\}\s*\\resumeItemListStart.*?\\resumeItemListEnd)'
        matches = re.findall(pattern, text, re.DOTALL)

        if matches:
            return '\n\n'.join(matches)

        # Fallback: look for any \resumeSubheading pattern
        fallback_pattern = r'(\\resumeSubheading.*?)(?=\\resumeSubheading|$)'
        fallback_matches = re.findall(fallback_pattern, text, re.DOTALL)

        if fallback_matches:
            return '\n\n'.join(fallback_matches)

        return text.strip()

    def extract_latex_skills(self, text):
        """Extract LaTeX skills section from LLM response"""
        # Pattern to match \begin{itemize} ... \end{itemize} block
        pattern = r'(\\begin\{itemize\}\[leftmargin=[^\]]*\].*?\\end\{itemize\})'
        match = re.search(pattern, text, re.DOTALL)

        if match:
            return match.group(1)

        # Fallback: look for \small{\item{ ... }} pattern
        fallback_pattern = r'(\\small\{\\item\{.*?\}\})'
        fallback_match = re.search(fallback_pattern, text, re.DOTALL)

        if fallback_match:
            return f"\\begin{{itemize}}[leftmargin=0.15in, label={{}}]\n{fallback_match.group(1)}\n\\end{{itemize}}"

        return text.strip()

    def extract_latex_projects(self, text):
        """Extract LaTeX project entries from LLM response"""
        # Remove markdown code block markers if present
        text = re.sub(r'```latex\n?', '', text)
        text = re.sub(r'```\n?', '', text)

        # Pattern to match \resumeProjectHeading blocks
        pattern = r'(\\resumeProjectHeading\s*\{[^}]*\}\s*\{[^}]*\}\s*\\resumeItemListStart.*?\\resumeItemListEnd)'
        matches = re.findall(pattern, text, re.DOTALL)

        if matches:
            return '\n\n'.join(matches)

        # Fallback: look for any \resumeProjectHeading pattern
        fallback_pattern = r'(\\resumeProjectHeading.*?)(?=\\resumeProjectHeading|$)'
        fallback_matches = re.findall(fallback_pattern, text, re.DOTALL)

        if fallback_matches:
            return '\n\n'.join(fallback_matches)

        return text.strip()

    def extract_latex_highlights(self, text):
        """Extract LaTeX highlights/qualifications from LLM response"""
        # Remove markdown code block markers if present
        text = re.sub(r'```latex\n?', '', text)
        text = re.sub(r'```\n?', '', text)

        # Pattern to match \resumeItem with proper brace matching
        def extract_resume_items(text):
            items = []
            lines = text.split('\n')
            current_item = ''
            brace_count = 0
            in_resume_item = False

            for line in lines:
                line = line.strip()
                if line.startswith('\\resumeItem{'):
                    if current_item and in_resume_item:
                        items.append(current_item.strip())
                    current_item = line
                    brace_count = line.count('{') - line.count('}')
                    in_resume_item = True
                elif in_resume_item:
                    current_item += ' ' + line
                    brace_count += line.count('{') - line.count('}')

                if in_resume_item and brace_count <= 0:
                    items.append(current_item.strip())
                    current_item = ''
                    in_resume_item = False
                    brace_count = 0

            # Add any remaining item
            if current_item and in_resume_item:
                items.append(current_item.strip())

            return items

        resume_items = extract_resume_items(text)

        if resume_items:
            return '\n'.join(resume_items)

        # Fallback: try simple regex for single-line items
        simple_pattern = r'\\resumeItem\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
        simple_matches = re.findall(simple_pattern, text)

        if simple_matches:
            return '\n'.join(simple_matches)

        # Ultimate fallback: return cleaned text
        return text.strip()

    def extract_json_from_response(self, text):
        """Extract JSON array from LLM response for project selection"""
        # Pattern to match JSON array
        pattern = r'\[(.*?)\]'
        match = re.search(pattern, text, re.DOTALL)

        if match:
            try:
                json_str = '[' + match.group(1) + ']'
                return json.loads(json_str)
            except json.JSONDecodeError:
                pass

        # Fallback: try to extract quoted strings
        quoted_pattern = r'"([^"]+)"'
        quoted_matches = re.findall(quoted_pattern, text)

        if quoted_matches:
            return quoted_matches[:4]  # Return max 4 projects

        return []

    def embed_pdf(self, path):
        loader = PyPDFLoader(path)
        docs = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            add_start_index=self.add_start_index,
        )

        all_splits = text_splitter.split_documents(docs)

        _ = self.vector_store.add_documents(documents=all_splits)

    def retrieve(self, state: State):
        retrieved_docs = self.vector_store.similarity_search(
            state["job"])
        return {"context": retrieved_docs}

    def build_graph(self):
        graph_builder = StateGraph(State)

        graph_builder.add_node("retrieve", self.retrieve)
        graph_builder.add_node("summarize_experiences",
                               self.summarize_experiences)
        graph_builder.add_node("summarize_technical_skills",
                               self.summarize_technical_skills)
        graph_builder.add_node("select_projects", self.select_projects)
        graph_builder.add_node("summarize_projects", self.summarize_projects)
        graph_builder.add_node("generate_highlights", self.generate_highlights)
        graph_builder.add_node("generate_cover_letter",
                               self.generate_cover_letter)

        graph_builder.add_edge(START, "summarize_experiences")
        graph_builder.add_edge("summarize_experiences",
                               "summarize_technical_skills")
        graph_builder.add_edge("summarize_technical_skills", "select_projects")
        graph_builder.add_edge("select_projects", "summarize_projects")
        graph_builder.add_edge("summarize_projects", "generate_highlights")
        graph_builder.add_edge("retrieve", "generate_cover_letter")
        graph_builder.add_edge("generate_highlights", "generate_cover_letter")
        graph_builder.set_finish_point("generate_cover_letter")

        self.graph = graph_builder.compile()

    def summarize_experiences(self, state: State):
        data = {}
        with open("./data/experiences.json", "r") as f:
            data = json.load(f)

        prompt = PromptTemplate.from_template("""
        You are an expert resume writer specializing in tailoring professional experiences to specific job requirements.
        
        Your task is to analyze the provided job posting and candidate experiences, then generate LaTeX-formatted resume entries that highlight the most relevant skills, achievements, and experiences for the target position.

        JOB POSTING:
        {job}

        CANDIDATE EXPERIENCES:
        {experiences}

        INSTRUCTIONS:
        1. Analyze the job posting to identify key requirements, skills, technologies, and qualifications
        2. Select the 3-4 most relevant experiences from the candidate's background
        3. For each selected experience, generate a LaTeX resume entry following this EXACT format:

        \\resumeSubheading
            {{Organization Name}}{{Start Date – End Date}}
            {{Job Title}}{{Location}}
            \\resumeItemListStart
                \\resumeItem{{Achievement/responsibility highlighting relevant skills with \\textbf{{bold keywords}}}}
                \\resumeItem{{Achievement/responsibility highlighting relevant skills with \\textbf{{bold keywords}}}}
                \\resumeItem{{Achievement/responsibility highlighting relevant skills with \\textbf{{bold keywords}}}}
                \\resumeItem{{Achievement/responsibility highlighting relevant skills with \\textbf{{bold keywords}}}}
                \\resumeItem{{Achievement/responsibility highlighting relevant skills with \\textbf{{bold keywords}}}}
            \\resumeItemListEnd

        FORMATTING GUIDELINES:
        - Use \\textbf{{}} to bold technical skills, technologies, methodologies, and key achievements mentioned in the job posting
        - Start each \\resumeItem with strong action verbs (Developed, Implemented, Designed, Led, Accelerated, etc.)
        - Quantify achievements with numbers/percentages when available (use \\% for percentages in LaTeX)
        - Tailor the language to match the job posting's terminology
        - Highlight transferable skills even if from different domains
        - Focus on impact and results, not just responsibilities
        - Ensure each experience shows progression and growth
        - Maximum 5 resume items per experience
        - Order experiences by relevance to the job posting
        - If location is not provided, leave it empty

        PRIORITIZATION CRITERIA:
        1. Direct skill/technology matches with job requirements
        2. Relevant industry experience
        3. Leadership and project management experience
        4. Technical depth and complexity of work
        5. Recent and duration of experience

        Generate the LaTeX resume entries for the most relevant experiences:
        """)

        experiences_text = json.dumps(data["experiences"], indent=2)

        messages = prompt.invoke({
            "job": state["job"],
            "experiences": experiences_text
        })

        response = self.llm.invoke(messages)

        # Extract only the LaTeX code from the response
        latex_content = self.extract_latex_experiences(response.content)

        return {"experiences": latex_content}

    def summarize_technical_skills(self, state: State):
        data = {}
        with open("./data/technical_skills.json", "r") as f:
            data = json.load(f)

        prompt = PromptTemplate.from_template("""
            You are an expert resume writer specializing in tailoring technical skills sections to specific job requirements.

            Your task is to analyze the job posting and remove only those skills from the candidate’s skill set that are clearly irrelevant, keeping a broad and well-rounded technical skills section. Start with the full list, then prune.

            JOB POSTING:
            {job}

            CANDIDATE'S TECHNICAL SKILLS:
            {skills}

            INSTRUCTIONS:
            1. Analyze the job posting to identify required/preferred technical skills, technologies, frameworks, and tools.
            2. Start with the full candidate skill set, and remove only those skills that are clearly irrelevant to the job.
            3. Within each category, prioritize:
            - Direct matches from the job posting
            - High expertise (score ≥ 6)
            - Industry-relevant and complementary skills
            4. Ensure **at least 4–5 skills per category** (unless fewer exist in the candidate’s set).
            5. Cap each category at **8–10 skills maximum** to keep it concise.

            OUTPUT FORMAT:
            Generate a LaTeX technical skills section in this exact format:

            \\begin{{itemize}}[leftmargin=0.15in, label={{}}]
            \\small{{\\item{{
                \\textbf{{AI / Machine Learning}}{{: [Selected AI/ML skills]}} \\\\
                \\textbf{{Languages}}{{: [Selected programming languages]}} \\\\
                \\textbf{{Cloud \\& DevOps}}{{: [Selected cloud/devops tools]}} \\\\
                \\textbf{{Databases}}{{: [Selected database technologies]}} \\\\
                \\textbf{{Web Frameworks}}{{: \\emph{{Back-end}}: [Backend frameworks]. \\emph{{Front-end}}: [Frontend frameworks]}} \\\\
                \\textbf{{Tools \\& Methodologies}}{{: [Selected tools and methodologies]}}
            }}}}
            \\end{{itemize}}

            FORMATTING RULES:
            - Only omit a category if the candidate truly has no relevant skills there.
            - Within categories, sort skills by relevance to the job posting.
            - Use LaTeX escaping (\\& for ampersands, etc.).
            - Do not include expertise scores in the output.
            - Keep categories ordered according to relevance to the job description.
            - Output **only the LaTeX block**, nothing else.

            Now generate the LaTeX technical skills section:
        """)

        skills_text = json.dumps(data, indent=2)

        messages = prompt.invoke({
            "job": state["job"],
            "skills": skills_text
        })

        response = self.llm.invoke(messages)

        # Extract only the LaTeX code from the response
        latex_content = self.extract_latex_skills(response.content)

        return {"skills": latex_content}

    def select_projects(self, state: State):
        data = {}
        with open("./data/projects.json", "r") as f:
            data = json.load(f)

        prompt = PromptTemplate.from_template("""
        You are an expert resume strategist specializing in project selection for job applications.
        
        Your task is to analyze the job posting and select up to 4 most relevant projects from the candidate's portfolio that best demonstrate the skills and experience required for the position.

        JOB POSTING:
        {job}

        CANDIDATE'S PROJECTS:
        {projects}

        INSTRUCTIONS:
        1. Analyze the job posting to identify:
           - Required technical skills and technologies
           - Preferred experience areas
           - Industry domain and problem types
           - Project complexity and scale requirements
           - Key competencies (full-stack, AI/ML, backend, etc.)

        2. Evaluate each project based on:
           - Technology stack alignment with job requirements
           - Problem domain relevance to the job's industry
           - Complexity and scale that demonstrates required skill level
           - Unique value proposition that sets candidate apart
           - Recency and relevance to current tech trends

        3. Select up to 4 projects that collectively:
           - Cover the most important job requirements
           - Demonstrate progression and skill growth
           - Show diverse but relevant capabilities
           - Highlight unique expertise that differentiates the candidate

        SELECTION CRITERIA (in order of importance):
        1. Direct technology/framework matches (highest priority)
        2. Problem domain alignment with job industry
        3. Complexity level appropriate for the role
        4. Demonstrates end-to-end project ownership
        5. Shows innovation or unique technical solutions
        6. Covers complementary skills mentioned in job posting
        7. You are allowed to select even one project, as long as the selected projects are relevant to the job.

        OUTPUT FORMAT:
        Return ONLY a JSON list of the selected project titles, ordered by relevance to the job posting.
        
        Example format:
        ["Project Title 1", "Project Title 2", "Project Title 3", "Project Title 4"]

        Important: Return ONLY the JSON list, no additional text or explanation.
        """)

        projects_text = json.dumps(data["projects"], indent=2)

        messages = prompt.invoke({
            "job": state["job"],
            "projects": projects_text
        })

        response = self.llm.invoke(messages)

        # Extract JSON from the response using regex
        try:
            selected_projects = self.extract_json_from_response(
                response.content)
            if selected_projects:
                return {"project_names": selected_projects}
        except Exception:
            pass

        # Fallback: if regex extraction fails, try standard JSON parsing
        try:
            selected_projects = json.loads(response.content.strip())
            return {"project_names": selected_projects}
        except json.JSONDecodeError:
            # Ultimate fallback: extract project names from response text
            projects_list = [project["title"] for project in data["projects"]]
            # Return first 4 as fallback
            return {"project_names": projects_list[:4]}

    def summarize_projects(self, state: State):
        """Generate LaTeX project summaries for selected projects based on job requirements"""
        projects_data = {}
        with open("./data/projects.json", "r") as f:
            projects_data = json.load(f)

        selected_projects = state["project_names"]
        project_summaries = []

        for project_name in selected_projects:
            # Find project data
            project_info = None
            for project in projects_data["projects"]:
                if project["title"] == project_name:
                    project_info = project
                    break

            if not project_info:
                continue

            project_docs = ""
            try:
                # Use the readme path from projects.json
                readme_path = project_info.get("readme", "")
                if readme_path:
                    # Convert relative path to absolute path from data directory
                    file_path = f"./data/{readme_path}" if not readme_path.startswith(
                        "./data/") else readme_path
                    with open(file_path, "r") as f:
                        project_docs = f.read()

            except Exception:
                pass

            # Create comprehensive project context
            project_context = {
                "title": project_info["title"],
                "description": project_info["description"],
                "stack": project_info["stack"],
                "documentation": project_docs,
                "github": project_info["github"]
            }

            # Generate LaTeX summary for this project
            prompt = PromptTemplate.from_template("""
            You are an expert resume writer specializing in creating compelling project descriptions for technical resumes.
            
            Your task is to analyze the job posting and project details, then generate a LaTeX-formatted project entry that highlights the most relevant aspects for the target position.

            JOB POSTING:
            {job}

            PROJECT DETAILS:
            Title: {project_title}
            Description: {project_description}
            Tech Stack: {project_stack}
            
            Detailed Documentation:
            {project_docs}

            INSTRUCTIONS:
            1. Analyze the job posting to identify key requirements and preferred technologies
            2. From the project's tech stack, select 4-6 technologies that are MOST RELEVANT to the job requirements
            3. Extract the most relevant project achievements and technical details
            4. Be honest about the projects and do not hallucinate because something is need in the job description.
            5. Generate a LaTeX project entry following this EXACT format:

            \\resumeProjectHeading
                {{\\textbf{{{project_title}}} $|$ \\emph{{[Select 4-6 most job-relevant technologies from tech stack]}} $|$ \\href{{{github}}}{{\\underline{{Code}}}}}} {{}}
                \\resumeItemListStart
                    \\resumeItem{{Key achievement/feature highlighting relevant technology with \\textbf{{bold keywords}}}}
                    \\resumeItem{{Technical implementation detail showing relevant skills with \\textbf{{bold keywords}}}}
                    \\resumeItem{{Impact/result with quantified metrics and \\textbf{{bold keywords}} where possible}}
                \\resumeItemListEnd

            FORMATTING GUIDELINES:
            - For the \\emph{{}} section, intelligently select 4-6 technologies from the project stack that are most relevant to the job posting
            - Prioritize technologies explicitly mentioned in the job description
            - Include complementary technologies that demonstrate full-stack or specialized capabilities relevant to the role
            - Bold technical terms, frameworks, and methodologies mentioned in the job posting using \\textbf{{}}
            - Focus on achievements and impact, not just features
            - Include quantified results when available (percentages, time savings, performance improvements - use \\% for percentages in LaTeX)
            - Use strong action verbs (Built, Developed, Implemented, Integrated, Designed, etc.)
            - Tailor language to match job posting terminology
            - Keep each \\resumeItem concise but impactful (1-2 lines max)
            - Generate 3 \\resumeItem entries per project

            TECHNOLOGY SELECTION CRITERIA:
            1. Technologies explicitly mentioned in the job posting (highest priority)
            2. Technologies commonly required in the job's domain/industry
            3. Technologies that demonstrate relevant architectural capabilities
            4. Technologies that show full-stack or specialized expertise relevant to the role
            5. Avoid generic or less relevant technologies unless they're specifically mentioned in the job

            PRIORITIZATION:
            1. Technologies/frameworks mentioned in job posting
            2. Architecture and scalability achievements
            3. Performance improvements and metrics
            4. Innovation and problem-solving approach
            5. Integration with external services/APIs

            Generate the LaTeX project entry:
            """)

            messages = prompt.invoke({
                "job": state["job"],
                "project_title": project_context["title"],
                "project_description": project_context["description"],
                "project_stack": ", ".join(project_context["stack"]),
                # Limit docs length
                "project_docs": project_context["documentation"][:3000],
                "github": project_context["github"],
            })

            response = self.llm.invoke(messages)

            # Extract only the LaTeX code from the response
            latex_content = self.extract_latex_projects(response.content)
            project_summaries.append(latex_content)

        # Combine all project summaries
        combined_summaries = "\n\n".join(project_summaries)

        return {"project_summaries": combined_summaries}

    def generate_highlights(self, state: State):
        """Generate comprehensive highlight of qualifications based on experiences, skills, and projects"""

        prompt = PromptTemplate.from_template("""
        You are an expert resume writer specializing in creating compelling "Highlight of Qualifications" sections that synthesize a candidate's experiences, skills, and projects into powerful qualification statements.
        
        Your task is to analyze the job posting and all provided resume content, then generate a LaTeX-formatted highlights section that positions the candidate as the ideal fit for the role.

        JOB POSTING:
        {job}

        CANDIDATE'S EXPERIENCES:
        {experiences}

        CANDIDATE'S TECHNICAL SKILLS:
        {skills}

        CANDIDATE'S PROJECTS:
        {projects}

        INSTRUCTIONS:
        1. Analyze the job posting to identify the most critical qualifications and requirements
        2. Review all the candidate's content (experiences, skills, projects) to extract relevant strengths
        3. Synthesize this information into 5-7 compelling qualification highlights
        4. Generate a LaTeX highlights section following this EXACT format:

        \\resumeItem{{\\textbf{{Domain Area 1:}} Comprehensive statement showcasing relevant expertise with \\textbf{{key technologies}} and demonstrable outcomes.}}
        \\resumeItem{{\\textbf{{Domain Area 2:}} Comprehensive statement showcasing relevant expertise with \\textbf{{key technologies}} and demonstrable outcomes.}}
        \\resumeItem{{\\textbf{{Domain Area 3:}} Comprehensive statement showcasing relevant expertise with \\textbf{{key technologies}} and demonstrable outcomes.}}
        \\resumeItem{{\\textbf{{Domain Area 4:}} Comprehensive statement showcasing relevant expertise with \\textbf{{key technologies}} and demonstrable outcomes.}}
        \\resumeItem{{\\textbf{{Domain Area 5:}} Comprehensive statement showcasing relevant expertise with \\textbf{{key technologies}} and demonstrable outcomes.}}
        

        FORMATTING GUIDELINES:
        - Each highlight should start with a \\textbf{{domain area}} that matches job requirements
        - Bold all technical skills, technologies, frameworks, and methodologies using \\textbf{{}}
        - Include specific technologies and techniques mentioned in experiences and projects
        - Quantify achievements where possible (percentages, scale, impact - use \\% for percentages in LaTeX)
        - Use strong, confident language that demonstrates expertise
        - Each highlight should be 1-2 lines maximum for readability
        - Order highlights by importance to the job posting

        DOMAIN AREAS TO CONSIDER (select most relevant to job):
        - Generative AI \& LLMs
        - Machine Learning Engineering
        - Deep Learning \& Neural Networks
        - NLP \& Computer Vision
        - Full-Stack Development
        - Backend Development \& APIs
        - Cloud \& DevOps
        - Data Engineering \& Analytics
        - System Architecture \& Design
        - Research \& Innovation
        - Collaboration \& Leadership
        - Agile \& Project Management

        QUALIFICATION SYNTHESIS STRATEGY:
        1. Combine related skills and experiences into cohesive statements
        2. Highlight unique combinations that set the candidate apart
        3. Emphasize both technical depth and breadth
        4. Include evidence from projects and work experience
        5. Match the language and priorities of the job posting
        6. Show progression from research to production applications
        7. Demonstrate both individual expertise and team collaboration

        CONTENT EXTRACTION GUIDELINES:
        - Extract specific technologies from the technical skills section
        - Reference concrete achievements from experiences
        - Mention innovative approaches from projects
        - Include relevant methodologies and best practices
        - Highlight any quantified results or impacts
        - Show versatility across different domains when relevant

        Generate the LaTeX highlight of qualifications:
        """)

        messages = prompt.invoke({
            "job": state["job"],
            "experiences": state.get("experiences", ""),
            "skills": state.get("skills", ""),
            "projects": state.get("project_summaries", "")
        })

        response = self.llm.invoke(messages)

        # Extract only the LaTeX code from the response
        latex_content = self.extract_latex_highlights(response.content)

        return {"highlights": latex_content}

    def generate_resume(self, state: State):
        """Generate complete resume by combining all sections and compiling to PDF"""
        import subprocess
        import os
        
        # Extract content from state
        highlights = state.get("highlights", "")
        experiences = state.get("experiences", "")
        skills = state.get("skills", "")
        projects = state.get("project_summaries", "")
        
        # Generate the complete LaTeX resume using the formatting function
        resume_latex = format_resume(highlights, experiences, skills, projects)
        
        # Create output directory structure
        company = state.get("company", "Default")
        position = state.get("position", "Position")
        
        output_dir = f"./output/resumes/{company}"
        os.makedirs(output_dir, exist_ok=True)
        
        # Write LaTeX file
        tex_filename = f"{position}.tex"
        tex_filepath = os.path.join(output_dir, tex_filename)
        
        with open(tex_filepath, "w", encoding="utf-8") as f:
            f.write(resume_latex)
        
        # Compile LaTeX to PDF
        pdf_filepath = None
        try:
            # Change to output directory for compilation
            original_cwd = os.getcwd()
            os.chdir(output_dir)
            
            # Run pdflatex twice for proper references
            subprocess.run(["pdflatex", "-interaction=nonstopmode", tex_filename], 
                         check=True, capture_output=True, text=True)
            subprocess.run(["pdflatex", "-interaction=nonstopmode", tex_filename], 
                         check=True, capture_output=True, text=True)
            
            # Clean up auxiliary files
            base_name = os.path.splitext(tex_filename)[0]
            aux_extensions = ['.aux', '.log', '.out', '.fdb_latexmk', '.fls']
            for ext in aux_extensions:
                aux_file = base_name + ext
                if os.path.exists(aux_file):
                    os.remove(aux_file)
            
            pdf_filepath = os.path.join(output_dir, f"{base_name}.pdf")
            
        except subprocess.CalledProcessError as e:
            print(f"LaTeX compilation failed: {e}")
            print(f"Error output: {e.stderr}")
        except FileNotFoundError:
            print("pdflatex not found. Please install LaTeX (e.g., MacTeX on macOS)")
        finally:
            # Return to original directory
            os.chdir(original_cwd)
        
        return {
            "resume": resume_latex,
            "tex_file": tex_filepath,
            "pdf_file": pdf_filepath if pdf_filepath and os.path.exists(pdf_filepath) else None
        }

    def generate_cover_letter(self, state: State):
        pass


load_dotenv()


aria = Aria()

# Example usage
sample_job_posting = """
Skills and Responsibilities:

 
 •Seeking for a motivated Gen AI Engineer to work with our Global Advanced Customer Analytics team and develop & support solutions primarily focused on customer insight knowledge bot. 

 
Responsibilities: 



 •Gen AI use cases requirements understanding working with product owners, business and design LLM solutions aligned with Manulife approved RAG patterns· 

 •Drive data requirements conversations and work with data office to get required data for the use case· Design efficient chunking & indexing strategies to support answer generation as per expectations· Develop and deploy inference APIs using frameworks like Lang chain and deploy to AKS or function apps· 

 •Capable to pick up UI work as needed to support front end integration collaborating with UI team· 

 •Support Gen AI knowledge BOTs in production by monitoring user feedback and improve BOT response quality through enhancements as per feedback· 

 •Embrace best practices, processes related to ML Ops, Coding best practices· 

 •Experience in optimizing model accuracy by efficient prompt refinements· 

 •Collaborate with existing members in the team, contribute to reusable Gen AI code base What we are looking for: · 

 •Good years of experience solving high-impact business problems using Machine learning & latest advancements in LLMs· 

 •Proven experience as a ML Engineer, with a strong focus on generative AI, prompt engineering, and RAG applications. · 

 •Hands-on experience using Azure AI search, Lang chain, other Vector stores. 

 •Experience in Azure Open AI. Open-source LLMs is a plus. · 

 •Strong software development skills with proficiency in Python, Pyspark, preferably using Databricks Azure ML. 

 •Basic knowledge of React or equivalent UI frameworks is a plus. · 

 •Strong experience in supporting production applications post development and continuously improve response quality to increase benefits· 

 •Strong collaboration skills, ability to translate sophisticated requirements into technical backlog, presentation skills, and an ability to balance a sense.
 
Tata Consultancy Services Canada Inc. is committed to meeting the accessibility needs of all individuals in accordance with the Accessibility for Ontarians with Disabilities Act (AODA) and the Ontario Human Rights Code (OHRC). Should you require accommodations during the recruitment and selection process, please inform Human Resources.
 
Thank you for your interest in TCS. Candidates that meet the qualifications for this position will be contacted within a 2-week period. We invite you to continue to apply for other opportunities that match your profile.
"""

# Test the complete pipeline
print("RUNNING COMPLETE RESUME GENERATION PIPELINE...")
print("="*80 + "\n")

# Test the summarize_experiences method
experiences_result = aria.summarize_experiences({"job": sample_job_posting})
print("EXPERIENCES:")
print(experiences_result["experiences"])
print("\n" + "="*80 + "\n")

# Test the summarize_technical_skills method
skills_result = aria.summarize_technical_skills({"job": sample_job_posting})
print("TECHNICAL SKILLS:")
print(skills_result["skills"])
print("\n" + "="*80 + "\n")

# Test the select_projects method
projects_result = aria.select_projects({"job": sample_job_posting})
print("SELECTED PROJECTS:")
print(projects_result["project_names"])
print("\n" + "="*80 + "\n")

# Test the summarize_projects method
project_summaries_result = aria.summarize_projects({
    "job": sample_job_posting,
    "project_names": projects_result["project_names"]
})
print("PROJECT SUMMARIES:")
print(project_summaries_result["project_summaries"])
print("\n" + "="*80 + "\n")

# Test the generate_highlights method
highlights_result = aria.generate_highlights({
    "job": sample_job_posting,
    "experiences": experiences_result["experiences"],
    "skills": skills_result["skills"],
    "project_summaries": project_summaries_result["project_summaries"]
})
print("HIGHLIGHT OF QUALIFICATIONS:")
print(highlights_result["highlights"])

# Generate complete resume with PDF compilation
complete_state = {
    "job": sample_job_posting,
    "highlights": highlights_result["highlights"],
    "experiences": experiences_result["experiences"],
    "skills": skills_result["skills"],
    "project_summaries": project_summaries_result["project_summaries"],
    "company": "TCS",
    "position": "Gen AI Developer"
}

resume_result = aria.generate_resume(complete_state)
print("\n" + "="*80 + "\n")
print("RESUME GENERATION COMPLETE:")
print(f"LaTeX file: {resume_result['tex_file']}")
if resume_result['pdf_file']:
    print(f"PDF file: {resume_result['pdf_file']}")
else:
    print("PDF compilation failed or pdflatex not available")