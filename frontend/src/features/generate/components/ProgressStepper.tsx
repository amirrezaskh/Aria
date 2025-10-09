import { 
  Paper,
  Stepper,
  Step,
  StepLabel
} from "@mui/material";
import type { ProgressStepperProps } from "../types";
import { STEPPER_STEPS } from "../constants";

export default function ProgressStepper({ currentStep }: ProgressStepperProps) {
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
    <Paper elevation={1} sx={{ p: 2, mb: 4 }}>
      <Stepper activeStep={getActiveStep()} alternativeLabel>
        {STEPPER_STEPS.map((label) => (
          <Step key={label}>
            <StepLabel>{label}</StepLabel>
          </Step>
        ))}
      </Stepper>
    </Paper>
  );
}