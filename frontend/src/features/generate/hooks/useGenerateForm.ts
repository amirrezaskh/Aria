import { useState } from "react";
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

export function useGenerateForm() {
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
        resumePath: result.resume_path,
        coverLetterPath: result.cover_letter_path
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
        resumePath: result.resume_path,
        coverLetterPath: result.cover_letter_path
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
        resumePath: result["resume_path"],
        coverLetterPath: result["cover_letter_path"]
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

  const handleDownload = (type: 'resume' | 'coverLetter') => {
    // TODO: Implement actual download logic
    console.log(`Downloading ${type}...`);
    
    // For now, create a dummy download
    const link = document.createElement('a');
    link.href = paths[`${type}Path`];
    console.log(link.href);
    link.download = `${formData.companyName}_${formData.positionTitle}_${type}.pdf`;
    link.click();
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