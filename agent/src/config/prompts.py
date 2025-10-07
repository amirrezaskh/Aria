"""Centralized prompt templates for Aria"""

from langchain.prompts import PromptTemplate


class PromptTemplates:
    """Container for all prompt templates used in the application"""
    
    EXPERIENCE_PROMPT = PromptTemplate.from_template("""
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

    PRIORITIZATION CRITERIA:
    1. Direct skill/technology matches with job requirements
    2. Relevant industry experience
    3. Leadership and project management experience
    4. Technical depth and complexity of work
    5. Recent and duration of experience

    Generate the LaTeX resume entries for the most relevant experiences:
    """)

    SKILLS_PROMPT = PromptTemplate.from_template("""
    You are an expert resume writer specializing in tailoring technical skills sections to specific job requirements.

    Your task is to analyze the job posting and remove only those skills from the candidate's skill set that are clearly irrelevant, keeping a broad and well-rounded technical skills section. Start with the full list, then prune.

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
    4. Ensure **at least 4–5 skills per category** (unless fewer exist in the candidate's set).
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

    PROJECT_SELECTION_PROMPT = PromptTemplate.from_template("""
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

    PROJECT_SUMMARY_PROMPT = PromptTemplate.from_template("""
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
    - Include quantified results when available (percentages, time savings, performance improvements)
    - IMPORTANT: Use proper LaTeX escaping - write \\% instead of percentage in text
    - Use strong action verbs (Built, Developed, Implemented, Integrated, Designed, etc.)
    - Tailor language to match job posting terminology
    - Keep each \\resumeItem concise but impactful (1-2 lines max)
    - Generate 3 \\resumeItem entries per project

    Generate the LaTeX project entry:
    """)

    HIGHLIGHTS_PROMPT = PromptTemplate.from_template("""
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

    EXAMPLE OUTPUT:
    \\resumeItem{{\\textbf{{Machine Learning \\& AI:}} 5+ years developing \\textbf{{deep learning}} models using \\textbf{{PyTorch}} \\& \\textbf{{TensorFlow}} with 95\\% accuracy improvements.}}

    Note: Always use \\& instead of & for ampersands in LaTeX text.

    FORMATTING GUIDELINES:
    - Each highlight should start with a \\textbf{{domain area}} that matches job requirements
    - Bold all technical skills, technologies, frameworks, and methodologies using \\textbf{{}}
    - Include specific technologies and techniques mentioned in experiences and projects
    - Quantify achievements where possible (percentages, scale, impact - use \\% for percentages in LaTeX)
    - Use strong, confident language that demonstrates expertise
    - Each highlight should be 1-2 lines maximum for readability
    - Order highlights by importance to the job posting
    - IMPORTANT: Use proper LaTeX escaping - write \\& instead of & for ampersands in text

    Generate the LaTeX highlight of qualifications:
    """)

    COVER_LETTER_PROMPT = PromptTemplate.from_template("""
    You are an expert cover letter writer specializing in creating compelling, personalized cover letters that effectively connect a candidate's background to specific job opportunities.

    Your task is to analyze the job posting, personalized resume, and retrieved context to generate ONLY the cover letter content paragraphs in plain LaTeX format.

    POSITION: {position}
    COMPANY: {company}
    JOB POSTING:
    {job_posting}

    PERSONALIZED RESUME CONTENT:
    Highlights: {resume_highlights}
    Experiences: {resume_experiences}
    Skills: {resume_skills}
    Projects: {resume_projects}

    RETRIEVED CONTEXT FROM KNOWLEDGE BASE:
    {retrieved_context}
                                                       
    INSTRUCTIONS:
    1. Analyze the job posting to identify:
       - Company mission, values, and culture
       - Key technical requirements and preferred technologies
       - Required experience level and responsibilities
       - Specific skills and qualifications sought

    2. Use the personalized resume content to:
       - Highlight the most relevant experiences and achievements
       - Showcase technical skills that match job requirements
       - Reference specific projects that demonstrate required capabilities
       - Quantify accomplishments where possible

    3. Leverage the retrieved context to:
       - Add depth and authenticity to your statements
       - Reference relevant research, projects, or experiences not in the resume
       - Demonstrate domain knowledge and passion for the field
       - Show progression and learning from past experiences

    4. Follow the template structure but adapt content to:
       - Match the company's tone and industry language
       - Create a narrative that connects past experiences to future contributions
       - Show genuine enthusiasm for the specific role and company
       - Address any potential gaps or explain career transitions


    CRITICAL OUTPUT REQUIREMENTS:
    - Generate ONLY the cover letter content paragraphs
    - DO NOT include any LaTeX document structure (\\documentclass, \\begin{{document}}, \\begin{{letter}}, \\end{{letter}}, \\end{{document}})
    - DO NOT include any explanations, introductions, or meta-commentary
    - DO NOT include salutations like "Dear Hiring Manager" or closings like "Sincerely"
    - Start directly with the first paragraph content
    - End with the last paragraph content
    - Use clean paragraph breaks (double newlines) between paragraphs

    CONTENT STRUCTURE:
    Write exactly 3-4 paragraphs of cover letter content:

    Paragraph 1: Express enthusiasm for the specific role and company, briefly state your relevant background and why you're applying.

    Paragraph 2: Highlight your most relevant technical experiences and projects with specific examples that match the job requirements.

    Paragraph 3: Demonstrate alignment with the company's mission and technology stack, referencing retrieved context to show deeper knowledge and genuine interest.

    Paragraph 4 (optional): Reiterate enthusiasm and mention specific contributions you can make to the team and company.

                                                       
    COVER LETTER STRUCTURE:
    1. Opening paragraph: Express enthusiasm for the specific role and company, briefly state your relevant background
    2. Body paragraph 1: Highlight relevant technical experience and projects with specific examples
    3. Body paragraph 2: Demonstrate alignment with company mission/technology stack, reference retrieved context for depth
    4. Closing paragraph: Reiterate enthusiasm, mention specific contributions you can make, professional closing

    TONE AND STYLE:
    - Professional yet enthusiastic
    - Confident but not boastful
    - Specific and detailed, not generic
    - Forward-looking and solution-oriented
    - Authentic and genuine
    LATEX FORMATTING REQUIREMENTS:
    - Use proper LaTeX escaping: \\& instead of & for ampersands
    - Use \\% for percentages in text  
    - Use \\textbf{{}} for emphasizing key technologies, company names, and achievements
    - Write in clean, readable paragraph format
    - Use standard paragraph separation (double newlines)

    CONTENT GUIDELINES:
    - Reference specific technologies, frameworks, and methodologies from the job posting
    - Use metrics and quantified achievements where available
    - Show understanding of the company's challenges and how you can help
    - Demonstrate continuous learning and adaptability
    - Connect past experiences to future potential contributions
    - Use retrieved context to add unique insights or relevant background
    - Be professional yet enthusiastic, confident but not boastful
    - Make it specific and detailed, not generic

    OUTPUT FORMAT EXAMPLE:
    I am excited to apply for the {{position}} position at \\textbf{{{{company name}}}}. With my background in \\textbf{{relevant technology}} and experience in \\textbf{{relevant domain}}, I am eager to contribute to your team's mission of advancing \\textbf{{company focus area}}.

    In my recent projects, I have built scalable applications using \\textbf{{specific technologies}} that align with your requirements. For example, in my \\textbf{{project name}} project, I developed \\textbf{{specific implementation}} that resulted in \\textbf{{quantified outcome}}. My experience with \\textbf{{relevant technology stack}} has prepared me to tackle the challenges outlined in your job posting.

    I am particularly drawn to \\textbf{{{{company name}}}}'s commitment to \\textbf{{company values/mission}}. My research in \\textbf{{relevant area from context}} has given me deep insights into \\textbf{{relevant domain knowledge}}, and I am excited about the opportunity to apply this knowledge in a production environment where I can help \\textbf{{specific company goals}}.

    Generate the cover letter content paragraphs following this exact format:
    """)