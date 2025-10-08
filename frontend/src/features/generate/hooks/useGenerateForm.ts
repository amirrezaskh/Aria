import { useState } from "react";
import type { 
  FormData, 
  ResumeStrategy, 
  TemplateType, 
  Step, 
  GeneratedPaths 
} from "../types";
import { API_ENDPOINTS } from "../constants";

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

  const handleStrategySelection = (strategy: ResumeStrategy) => {
    setResumeStrategy(strategy);
    if (strategy === 'template') {
      setCurrentStep('strategy');
    } else {
      // Generate new resume
      handleGenerate();
    }
  };

  const handleTemplateSelection = (templateId: TemplateType) => {
    setSelectedTemplate(templateId);
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
    isLoading,
    error,
    
    // Handlers
    handleInputChange,
    handleStartPersonalization,
    handleStrategySelection,
    handleTemplateSelection,
    handleGenerate,
    handleDownload,
    handleBack,
    handleCreateAnother
  };
}