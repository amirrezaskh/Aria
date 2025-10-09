import { Box, Typography, Paper, Container, Fade, useTheme } from "@mui/material";
import { 
  JobInputForm,
  PersonalizationChoice,
  TemplateSelection,
  Generating,
  Results,
  ProgressStepper
} from "./components";
import { SimilarJobsDisplay } from "./components/SimilarJobsDisplay";
import { useGenerateForm } from "./hooks/useGenerateForm";

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

interface GenerateFormProps {
  extensionJobData?: ExtensionJobData | null;
}

export default function GenerateForm({ extensionJobData }: GenerateFormProps) {
  const theme = useTheme();
  const {
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
    handleUseSimilarResume,
    handleViewResume,
    handleProceedWithNew,
    handleStrategySelection,
    handleTemplateSelection,
    handleGenerateWithTemplate,
    handleDownload,
    handleBack,
    handleCreateAnother
  } = useGenerateForm(extensionJobData);

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
      case 'similarity':
        return (
          <SimilarJobsDisplay
            similarJobs={similarJobs}
            isLoading={isLoadingSimilarJobs}
            onUseSimilarResume={handleUseSimilarResume}
            onViewResume={handleViewResume}
            onProceedWithNew={handleProceedWithNew}
            onBack={handleBack}
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
            onGenerate={handleGenerateWithTemplate}
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
            formData={formData}
            paths={paths}
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
    <Box 
      sx={{ 
        minHeight: '100vh',
        background: `linear-gradient(135deg, ${theme.palette.primary.main}15 0%, ${theme.palette.secondary.main}10 100%)`,
        py: 4
      }}
    >
      <Container maxWidth="lg">
        <Fade in timeout={800}>
          <Box sx={{ maxWidth: 900, mx: 'auto' }}>
            {/* Header Section */}
            <Box sx={{ textAlign: 'center', mb: 6 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', mb: 2 }}>
                <img 
                  src="/agent.png" 
                  alt="Aria Agent" 
                  style={{ 
                    width: '48px', 
                    height: '48px', 
                    marginRight: '12px' 
                  }} 
                />
                <Typography 
                  variant="h3" 
                  component="h1"
                  sx={{ 
                    fontWeight: 700,
                    background: `linear-gradient(45deg, ${theme.palette.primary.main}, ${theme.palette.secondary.main})`,
                    backgroundClip: 'text',
                    WebkitBackgroundClip: 'text',
                    WebkitTextFillColor: 'transparent',
                    textAlign: 'center'
                  }}
                >
                  Aria
                </Typography>
              </Box>
              <Typography 
                variant="h5" 
                color="text.secondary"
                sx={{ 
                  fontWeight: 400,
                  maxWidth: 600,
                  mx: 'auto',
                  lineHeight: 1.6
                }}
              >
                AI-Powered Resume & Cover Letter Generator
              </Typography>
              {/* <Typography 
                variant="body1" 
                color="text.secondary"
                sx={{ 
                  mt: 2,
                  opacity: 0.8,
                  maxWidth: 500,
                  mx: 'auto'
                }}
              >
                Transform job descriptions into personalized, professional resumes in minutes
              </Typography> */}
            </Box>
            
            {/* Progress Stepper */}
            <ProgressStepper currentStep={currentStep} />
            
            {/* Main Content */}
            <Paper 
              elevation={0}
              sx={{ 
                borderRadius: 3,
                border: `1px solid ${theme.palette.divider}`,
                background: 'rgba(255, 255, 255, 0.95)',
                backdropFilter: 'blur(10px)',
                p: { xs: 3, sm: 4, md: 5 },
                position: 'relative',
                overflow: 'hidden',
                '&::before': {
                  content: '""',
                  position: 'absolute',
                  top: 0,
                  left: 0,
                  right: 0,
                  height: 4,
                  background: `linear-gradient(90deg, ${theme.palette.primary.main}, ${theme.palette.secondary.main})`,
                  borderRadius: '12px 12px 0 0'
                }
              }}
            >
              <Fade in key={currentStep} timeout={600}>
                <Box>
                  {renderCurrentStep()}
                </Box>
              </Fade>
            </Paper>
          </Box>
        </Fade>
      </Container>
    </Box>
  );
}
