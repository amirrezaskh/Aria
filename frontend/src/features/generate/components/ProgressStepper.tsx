import { 
  Paper,
  Stepper,
  Step,
  StepLabel,
  useTheme,
  Box
} from "@mui/material";
import type { ProgressStepperProps } from "../types";
import { STEPPER_STEPS } from "../constants";

export default function ProgressStepper({ currentStep }: ProgressStepperProps) {
  const theme = useTheme();
  
  const getActiveStep = () => {
    switch (currentStep) {
      case 'input': return 0;
      case 'personalization': return 1;
      case 'strategy': return 1; // Template selection is still part of personalization
      case 'similarity': return 2;
      case 'generating': return 3;
      case 'results': return 4;
      default: return 0;
    }
  };

  if (currentStep === 'input') {
    return null;
  }

  return (
    <Box sx={{ mb: 4 }}>
      <Paper 
        elevation={0} 
        sx={{ 
          p: 3,
          borderRadius: 3,
          border: `1px solid ${theme.palette.divider}`,
          background: 'rgba(255, 255, 255, 0.9)',
          backdropFilter: 'blur(5px)'
        }}
      >
        <Stepper 
          activeStep={getActiveStep()} 
          alternativeLabel
          sx={{
            '& .MuiStepLabel-root .Mui-completed': {
              color: theme.palette.success.main,
            },
            '& .MuiStepLabel-root .Mui-active': {
              color: theme.palette.primary.main,
            },
            '& .MuiStepLabel-label': {
              fontSize: '0.875rem',
              fontWeight: 500,
            },
            '& .MuiStepLabel-label.Mui-active': {
              fontWeight: 600,
            },
            '& .MuiStepConnector-line': {
              borderTopWidth: 2,
            }
          }}
        >
          {STEPPER_STEPS.map((label) => (
            <Step key={label}>
              <StepLabel>{label}</StepLabel>
            </Step>
          ))}
        </Stepper>
      </Paper>
    </Box>
  );
}