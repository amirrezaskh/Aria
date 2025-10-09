import { useState, useEffect } from "react";
import type { 
  FormData, 
  ResumeStrategy, 
  TemplateType, 
  Step, 
  GeneratedPaths,
  SimilarJob,
  SimilarJobsResponse
} from "../types";
import { API_ENDPOINTS, RESUME_PREVIEW_MAPPING } from "../constants";

// Utility function to convert absolute file paths to proper URLs for serving
const convertPathToUrl = (filePath: string): string => {
  if (!filePath) return "";
  if (filePath.startsWith('http://') || filePath.startsWith('https://')) {
    return filePath; // Already a URL
  }
  
  // Extract the relative path from the absolute path
  // Backend expects: output/resumes/CompanyName/Position.pdf or output/cover_letters/CompanyName/Position.pdf
  // We need to extract: resumes/CompanyName/Position.pdf or cover_letters/CompanyName/Position.pdf
  const pathParts = filePath.split('/');
  const outputIndex = pathParts.lastIndexOf('output');
  
  if (outputIndex !== -1 && outputIndex < pathParts.length - 2) {
    // Get everything after 'output' folder (includes resumes/cover_letters directory)
    const relativePath = pathParts.slice(outputIndex + 1).join('/');
    return `${API_ENDPOINTS.GENERATED_RESUMES}/${encodeURIComponent(relativePath)}`;
  }
  
  // Fallback: just use filename
  const filename = pathParts[pathParts.length - 1] || '';
  return `${API_ENDPOINTS.GENERATED_RESUMES}/${encodeURIComponent(filename)}`;
};

interface ExtensionJobData {
  title?: string;
  company?: string;
  description?: string;
  location?: string;
  salary?: string;
  type?: string;
  remote?: string;
  requirements?: string[] | string;
}

export function useGenerateForm(extensionJobData?: ExtensionJobData | null) {
  const [currentStep, setCurrentStep] = useState<Step>('input');
  const [formData, setFormData] = useState<FormData>({
    jobDescription: "",
    companyName: "",
    positionTitle: ""
  });

  const [resumeStrategy, setResumeStrategy] = useState<ResumeStrategy>('generate');
  const [selectedTemplate, setSelectedTemplate] = useState<TemplateType>('overall');

  const [paths, setPaths] = useState<GeneratedPaths>({
    resumePath: "",
    coverLetterPath: ""
  });
  
  const [similarJobs, setSimilarJobs] = useState<SimilarJob[]>([]);
  const [isLoadingSimilarJobs, setIsLoadingSimilarJobs] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Handle Chrome extension job data
  useEffect(() => {
    if (extensionJobData) {
      // Auto-populate form with extension data
      const newFormData: FormData = {
        jobDescription: extensionJobData.description || "",
        companyName: extensionJobData.company || "",
        positionTitle: extensionJobData.title || ""
      };
      
      // Only update if the form is empty or different
      if (!formData.jobDescription && !formData.companyName && !formData.positionTitle) {
        setFormData(newFormData);
        console.log('Auto-populated form with extension data:', newFormData);
      }
    }
  }, [extensionJobData, formData.jobDescription, formData.companyName, formData.positionTitle]);

  const handleInputChange = (field: keyof FormData) => (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    setFormData(prev => ({
      ...prev,
      [field]: event.target.value
    }));
  };

  const handleStartPersonalization = () => {
    // Basic validation
    if (!formData.jobDescription.trim() || !formData.companyName.trim() || !formData.positionTitle.trim()) {
      setError("Please fill in all fields before starting personalization");
      return;
    }
    setError(null);
    setCurrentStep('personalization');
  };

  const handleSearchSimilarJobs = async () => {
    setIsLoadingSimilarJobs(true);
    setCurrentStep('similarity');
    
    try {
      const response = await fetch(API_ENDPOINTS.SIMILAR_JOBS, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          job_description: formData.jobDescription,
          company_name: formData.companyName,
          position_title: formData.positionTitle
        })
      });

      if (!response.ok) {
        throw new Error(`Failed to search similar jobs: ${response.status}`);
      }

      const result: SimilarJobsResponse = await response.json();
      setSimilarJobs(result.similar_jobs);
      
      // If no similar jobs found, proceed directly to generation
      if (result.similar_jobs.length === 0) {
        handleGenerate();
      }
    } catch (error) {
      console.error('Error searching similar jobs:', error);
      setError(error instanceof Error ? error.message : "Failed to search for similar jobs");
      // Continue to generation even if similarity search fails
      handleGenerate();
    } finally {
      setIsLoadingSimilarJobs(false);
    }
  };

  const handleUseSimilarResume = async (job: SimilarJob) => {
    setError(null);
    setCurrentStep('generating');
    setIsLoading(true);
    
    try {
      // Generate a cover letter using the existing resume
      const payload = {
        jobDescription: formData.jobDescription,
        companyName: formData.companyName,
        positionTitle: formData.positionTitle,
        resumePdfFile: job.resume_path
      };

      const response = await fetch(API_ENDPOINTS.GENERATE_COVER_LETTER, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ message: 'Unknown error' }));
        throw new Error(errorData.message || `HTTP ${response.status}`);
      }
      
      const result = await response.json();

      setPaths({
        resumePath: convertPathToUrl(result.resume_path),
        coverLetterPath: convertPathToUrl(result.cover_letter_path)
      });
      
      setCurrentStep('results');
    } catch (error) {
      console.error('Cover letter generation error:', error);
      setError(error instanceof Error ? error.message : "Failed to generate cover letter. Please try again.");
      setCurrentStep('similarity');
    } finally {
      setIsLoading(false);
    }
  };

  const handleViewResume = (job: SimilarJob) => {
    // Open resume in new tab/window for preview
    if (job.resume_path) {
      window.open(job.resume_path, '_blank');
    }
  };

  const handleProceedWithNew = () => {
    // Continue with generation
    handleGenerate();
  };

  const handleStrategySelection = async (strategy: ResumeStrategy) => {
    setResumeStrategy(strategy);
    if (strategy === 'template') {
      setCurrentStep('strategy');
    } else {
      // Generate new resume - first check for similar jobs
      await handleSearchSimilarJobs();
    }
  };

  const handleTemplateSelection = (templateId: TemplateType) => {
    setSelectedTemplate(templateId);
  };

  const handleGenerateWithTemplate = async () => {
    setError(null);
    setCurrentStep('generating');
    setIsLoading(true);
    
    try {
      // Get the template resume path from constants
      const templateResumeUrl = RESUME_PREVIEW_MAPPING[selectedTemplate];
      
      if (!templateResumeUrl) {
        throw new Error("Template resume not found");
      }

      const payload = {
        jobDescription: formData.jobDescription,
        companyName: formData.companyName,
        positionTitle: formData.positionTitle,
        resumePdfFile: templateResumeUrl
      };

      const response = await fetch(API_ENDPOINTS.GENERATE_COVER_LETTER, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ message: 'Unknown error' }));
        throw new Error(errorData.message || `HTTP ${response.status}`);
      }
      
      const result = await response.json();

      setPaths({
        resumePath: convertPathToUrl(result.resume_path),
        coverLetterPath: convertPathToUrl(result.cover_letter_path)
      });
      
      setCurrentStep('results');
    } catch (error) {
      console.error('Template cover letter generation error:', error);
      setError(error instanceof Error ? error.message : "Failed to generate cover letter with template. Please try again.");
      setCurrentStep('strategy');
    } finally {
      setIsLoading(false);
    }
  };

  const handleGenerate = async () => {
    setError(null);
    setCurrentStep('generating');
    setIsLoading(true);
    
    try {
      const payload = {
        ...formData,
        strategy: resumeStrategy,
        template: resumeStrategy === 'template' ? selectedTemplate : undefined
      };

      const response = await fetch(API_ENDPOINTS.GENERATE, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ message: 'Unknown error' }));
        throw new Error(errorData.message || `HTTP ${response.status}`);
      }
      
      const result = await response.json();

      setPaths({
        resumePath: convertPathToUrl(result["resume_path"]),
        coverLetterPath: convertPathToUrl(result["cover_letter_path"])
      });
      console.log('Generation result:', result);
      
      setCurrentStep('results');
    } catch (error) {
      console.error('Generation error:', error);
      setError(error instanceof Error ? error.message : "Failed to generate documents. Please try again.");
      setCurrentStep('input');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDownload = async (type: 'resume' | 'coverLetter') => {
    try {
      const path = type === 'resume' ? paths.resumePath : paths.coverLetterPath;
      
      if (!path) {
        console.error(`No ${type} path available for download`);
        setError(`${type} file not available for download`);
        return;
      }

      console.log(`Downloading ${type} from:`, path);

      // Create a descriptive filename
      const timestamp = new Date().toISOString().split('T')[0]; // YYYY-MM-DD format
      const sanitizedCompany = formData.companyName.replace(/[^a-zA-Z0-9]/g, '_');
      const sanitizedPosition = formData.positionTitle.replace(/[^a-zA-Z0-9]/g, '_');
      const filename = `${sanitizedCompany}_${sanitizedPosition}_${type}_${timestamp}.pdf`;

      // For URLs (which is what our API returns), fetch and download
      if (path.startsWith('http://') || path.startsWith('https://')) {
        const response = await fetch(path);
        if (!response.ok) {
          throw new Error(`Failed to fetch ${type}: ${response.statusText}`);
        }
        
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        link.style.display = 'none';
        
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        // Clean up the object URL
        window.URL.revokeObjectURL(url);
      } else {
        // For local file paths (fallback)
        const link = document.createElement('a');
        link.href = path;
        link.download = filename;
        link.style.display = 'none';
        
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      }

      console.log(`${type} download initiated successfully`);
    } catch (error) {
      console.error(`Error downloading ${type}:`, error);
      setError(`Failed to download ${type}. Please try again.`);
    }
  };

  const handleBack = () => {
    if (currentStep === 'strategy') {
      setCurrentStep('personalization');
    } else if (currentStep === 'similarity') {
      setCurrentStep('personalization');
    } else if (currentStep === 'personalization') {
      setCurrentStep('input');
    } else if (currentStep === 'results') {
      setCurrentStep('input');
    }
  };

  const handleCreateAnother = () => {
    setCurrentStep('input');
    setFormData({ jobDescription: "", companyName: "", positionTitle: "" });
    setPaths({ resumePath: "", coverLetterPath: "" });
    setError(null);
  };

  return {
    // State
    currentStep,
    formData,
    resumeStrategy,
    selectedTemplate,
    paths,
    similarJobs,
    isLoading,
    isLoadingSimilarJobs,
    error,
    
    // Handlers
    handleInputChange,
    handleStartPersonalization,
    handleSearchSimilarJobs,
    handleUseSimilarResume,
    handleViewResume,
    handleProceedWithNew,
    handleStrategySelection,
    handleTemplateSelection,
    handleGenerateWithTemplate,
    handleGenerate,
    handleDownload,
    handleBack,
    handleCreateAnother
  };
}