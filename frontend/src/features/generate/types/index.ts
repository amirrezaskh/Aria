export interface FormData {
  jobDescription: string;
  companyName: string;
  positionTitle: string;
}

export type ResumeStrategy = 'generate' | 'template';
export type TemplateType = 'ml-engineering' | 'data-science' | 'software-engineering' | 'overall';

export interface ResumeTemplate {
  id: TemplateType;
  title: string;
  description: string;
  icon: React.ElementType;
  keywords: string[];
}

export type Step = 'input' | 'personalization' | 'strategy' | 'generating' | 'results';

export interface GeneratedPaths {
  resumePath: string;
  coverLetterPath: string;
}

// export interface GenerateFormProps {
//   // Props for the main form if needed
// }

export interface JobInputFormProps {
  formData: FormData;
  error: string | null;
  onInputChange: (field: keyof FormData) => (event: React.ChangeEvent<HTMLInputElement>) => void;
  onStartPersonalization: () => void;
}

export interface PersonalizationChoiceProps {
  onStrategySelection: (strategy: ResumeStrategy) => void;
  onBack: () => void;
}

export interface TemplateSelectionProps {
  selectedTemplate: TemplateType;
  onTemplateSelection: (templateId: TemplateType) => void;
  onGenerate: () => void;
  onBack: () => void;
}

export interface GeneratingProps {
  isLoading: boolean;
  resumeStrategy: ResumeStrategy;
  selectedTemplate: TemplateType;
}

export interface ResultsProps {
  formData: FormData;
  paths: GeneratedPaths;
  onDownload: (type: 'resume' | 'coverLetter') => void;
  onCreateAnother: () => void;
}

export interface ProgressStepperProps {
  currentStep: Step;
}