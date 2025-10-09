import { Science, Code, Computer, Psychology } from "@mui/icons-material";
import type { ResumeTemplate } from "../types";

export const RESUME_TEMPLATES: ResumeTemplate[] = [
  {
    id: 'ml-engineering',
    title: 'ML Engineering',
    description: 'Machine Learning Engineer roles focusing on ML systems, MLOps, and production ML',
    icon: Psychology,
    keywords: ['TensorFlow', 'PyTorch', 'MLOps', 'Kubernetes', 'Python']
  },
  {
    id: 'data-science',
    title: 'Data Science',
    description: 'Data Scientist positions emphasizing analytics, modeling, and insights',
    icon: Science,
    keywords: ['Python', 'R', 'SQL', 'Statistics', 'Visualization']
  },
  {
    id: 'software-engineering',
    title: 'Software Engineering',
    description: 'Software Developer roles focusing on full-stack and backend development',
    icon: Code,
    keywords: ['React', 'Node.js', 'APIs', 'Databases', 'Cloud']
  },
  {
    id: 'overall',
    title: 'Overall',
    description: 'General-purpose resume highlighting diverse technical skills and experiences',
    icon: Computer,
    keywords: ['Versatile', 'Cross-functional', 'Leadership', 'Innovation']
  }
];

export const STEPPER_STEPS = ['Job Details', 'Personalization', 'Similar Jobs', 'Generation', 'Results'];

export const API_ENDPOINTS = {
  GENERATE: 'http://localhost:8080/api/generate/',
  GENERATE_COVER_LETTER: 'http://localhost:8080/api/generate/cover-letter/',
  SIMILAR_JOBS: 'http://localhost:8080/api/jobs/similar',
  RESUME_PREVIEW: 'http://localhost:8080/api/resumes/preview',
  GENERATED_RESUMES: 'http://localhost:8080/api/resumes/generated'
} as const;

// Resume preview URL mapping
export const RESUME_PREVIEW_MAPPING: Record<string, string> = {
  'ml-engineering': `${API_ENDPOINTS.RESUME_PREVIEW}/ml-engineering`,
  'data-science': `${API_ENDPOINTS.RESUME_PREVIEW}/data-science`,
  'software-engineering': `${API_ENDPOINTS.RESUME_PREVIEW}/software-engineering`,
  'overall': `${API_ENDPOINTS.RESUME_PREVIEW}/overall`
};