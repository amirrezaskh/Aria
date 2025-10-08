import { 
  Typography, 
  CircularProgress,
  Stack
} from "@mui/material";
import type { GeneratingProps } from "../types";

export default function Generating({ 
  isLoading, 
  resumeStrategy, 
  selectedTemplate 
}: GeneratingProps) {
  return (
    <Stack spacing={3} alignItems="center" sx={{ py: 8 }}>
      <CircularProgress size={60} />
      <Typography variant="h5">Generating Your Documents...</Typography>
      <Typography variant="body1" color="text.secondary" align="center">
        Please wait while we create your personalized resume and cover letter.
        <br />
        This usually takes 30-60 seconds.
      </Typography>
      {isLoading && (
        <Typography variant="body2" color="text.secondary">
          {resumeStrategy === 'template' 
            ? `Using ${selectedTemplate.replace('-', ' ')} template...` 
            : 'Creating custom resume...'}
        </Typography>
      )}
    </Stack>
  );
}