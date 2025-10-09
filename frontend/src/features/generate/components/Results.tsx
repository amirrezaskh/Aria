import { 
  Box, 
  Typography, 
  Button, 
  Stack,
  Alert
} from "@mui/material";
import { Download, Visibility } from "@mui/icons-material";
import type { ResultsProps } from "../types";

export default function Results({ 
  formData,
  paths,
  onDownload, 
  onCreateAnother 
}: ResultsProps) {
  const handlePreview = (type: 'resume' | 'coverLetter') => {
    const path = type === 'resume' ? paths.resumePath : paths.coverLetterPath;
    if (path) {
      window.open(path, '_blank');
    }
  };

  const isResumeAvailable = Boolean(paths.resumePath);
  const isCoverLetterAvailable = Boolean(paths.coverLetterPath);

  return (
    <Stack spacing={3}>
      <Typography variant="h5" align="center" gutterBottom color="success.main">
        ✅ Documents Generated Successfully!
      </Typography>
      
      <Typography variant="body1" color="text.secondary" align="center">
        Your personalized resume and cover letter for{' '}
        <strong>{formData.positionTitle}</strong> at{' '}
        <strong>{formData.companyName}</strong> are ready for download.
      </Typography>

      {/* Show warning if files are not available */}
      {(!isResumeAvailable || !isCoverLetterAvailable) && (
        <Alert severity="warning">
          Some documents may not be available. Please try generating again if needed.
        </Alert>
      )}

      <Box sx={{ 
        display: 'flex', 
        gap: 2, 
        justifyContent: 'center',
        flexDirection: { xs: 'column', sm: 'row' }
      }}>
        <Stack spacing={1} sx={{ minWidth: 200 }}>
          <Button
            variant="contained"
            size="large"
            startIcon={<Download />}
            onClick={() => onDownload('resume')}
            disabled={!isResumeAvailable}
            fullWidth
          >
            Download Resume
          </Button>
          {isResumeAvailable && (
            <Button
              variant="outlined"
              size="small"
              startIcon={<Visibility />}
              onClick={() => handlePreview('resume')}
              fullWidth
            >
              Preview Resume
            </Button>
          )}
        </Stack>
        
        <Stack spacing={1} sx={{ minWidth: 200 }}>
          <Button
            variant="outlined"
            size="large"
            startIcon={<Download />}
            onClick={() => onDownload('coverLetter')}
            disabled={!isCoverLetterAvailable}
            fullWidth
          >
            Download Cover Letter
          </Button>
          {isCoverLetterAvailable && (
            <Button
              variant="outlined"
              size="small"
              startIcon={<Visibility />}
              onClick={() => handlePreview('coverLetter')}
              fullWidth
            >
              Preview Cover Letter
            </Button>
          )}
        </Stack>
      </Box>

      <Button
        variant="text"
        onClick={onCreateAnother}
        sx={{ alignSelf: 'center', mt: 2 }}
      >
        Create Another Resume
      </Button>
    </Stack>
  );
}