import { Box, Typography, Paper } from "@mui/material";
import { 
  JobInputForm,
  PersonalizationChoice,
  TemplateSelection,
  Generating,
  Results,
  ProgressStepper
} from "./components";
import { useGenerateForm } from "./hooks/useGenerateForm";

export default function GenerateForm() {
  const {
    // State
    currentStep,
    formData,
    resumeStrategy,
    selectedTemplate,
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
  } = useGenerateForm();

  const renderCurrentStep = () => {
    switch (currentStep) {
      case 'input':
        return (
          <JobInputForm
            formData={formData}
            error={error}
            onInputChange={handleInputChange}
            onStartPersonalization={handleStartPersonalization}
          />
        );
      case 'personalization':
        return (
          <PersonalizationChoice
            onStrategySelection={handleStrategySelection}
            onBack={handleBack}
          />
        );
      case 'strategy':
        return (
          <TemplateSelection
            selectedTemplate={selectedTemplate}
            onTemplateSelection={handleTemplateSelection}
            onGenerate={handleGenerate}
            onBack={handleBack}
          />
        );
      case 'generating':
        return (
          <Generating
            isLoading={isLoading}
            resumeStrategy={resumeStrategy}
            selectedTemplate={selectedTemplate}
          />
        );
      case 'results':
        return (
          <Results
            onDownload={handleDownload}
            onCreateAnother={handleCreateAnother}
          />
        );
      default:
        return (
          <JobInputForm
            formData={formData}
            error={error}
            onInputChange={handleInputChange}
            onStartPersonalization={handleStartPersonalization}
          />
        );
    }
  };

  return (
    <Box sx={{ maxWidth: 900, mx: 'auto', p: 3 }}>
      <Typography variant="h4" gutterBottom align="center" sx={{ mb: 4 }}>
        🤖 Aria - AI Resume & Cover Letter Generator
      </Typography>
      
      {/* Progress Stepper */}
      <ProgressStepper currentStep={currentStep} />
      
      {/* Main Content */}
      <Paper elevation={3} sx={{ p: 4 }}>
        {renderCurrentStep()}
      </Paper>
    </Box>
  );
}
