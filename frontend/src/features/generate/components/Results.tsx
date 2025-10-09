import { 
  Box, 
  Typography, 
  Button, 
  Stack,
  Alert,
  Card,
  CardContent,
  Divider
} from "@mui/material";
import { 
  Download, 
  Visibility, 
  CheckCircle,
  Description,
  Email,
  Add
} from "@mui/icons-material";
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
    <Stack spacing={4}>
      {/* Success Header */}
      <Box sx={{ textAlign: 'center' }}>
        <CheckCircle 
          sx={{ 
            fontSize: 64, 
            color: 'success.main',
            mb: 2
          }} 
        />
        <Typography 
          variant="h4" 
          sx={{ 
            fontWeight: 700, 
            color: 'success.main',
            mb: 1
          }}
        >
          🎉 Success!
        </Typography>
        <Typography variant="h6" color="text.secondary" sx={{ maxWidth: 500, mx: 'auto' }}>
          Your personalized documents for <br /> {formData.positionTitle} at {formData.companyName} are ready!
        </Typography>
      </Box>

      {/* Show warning if files are not available */}
      {(!isResumeAvailable || !isCoverLetterAvailable) && (
        <Alert 
          severity="warning"
          sx={{ 
            borderRadius: 2,
            '& .MuiAlert-message': { width: '100%' }
          }}
        >
          Some documents may not be available. Please try generating again if needed.
        </Alert>
      )}

      {/* Download Cards */}
      <Box sx={{ 
        display: 'flex', 
        flexDirection: { xs: 'column', sm: 'row' },
        gap: 4, 
        justifyContent: 'center',
        alignItems: 'center',
        width: '100%',
        px: 2
      }}>
        {/* Resume Card */}
        <Card 
          variant="outlined" 
          sx={{ 
            borderRadius: 3,
            border: isResumeAvailable ? '2px solid' : '1px solid',
            borderColor: 'primary.main',
            position: 'relative',
            overflow: 'visible',
            width: { xs: '100%', sm: 300 },
            flexShrink: 0
          }}
        >
          {/* {isResumeAvailable && (
            <Chip
              label="Ready"
              color="success"
              size="small"
              sx={{
                position: 'absolute',
                top: -8,
                right: 16,
                zIndex: 1
              }}
            />
          )} */}
          <CardContent sx={{ p: 3, textAlign: 'center' }}>
            <Description sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
            <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
              Resume
            </Typography>
            <Stack spacing={2}>
              <Button
                variant="contained"
                size="large"
                startIcon={<Download />}
                onClick={() => onDownload('resume')}
                disabled={!isResumeAvailable}
                fullWidth
                sx={{
                  borderRadius: 2,
                  fontWeight: 600,
                  '&:disabled': {
                    opacity: 0.6
                  }
                }}
              >
                Download Resume
              </Button>
              {isResumeAvailable && (
                <Button
                  variant="outlined"
                  size="medium"
                  startIcon={<Visibility />}
                  onClick={() => handlePreview('resume')}
                  fullWidth
                  sx={{ borderRadius: 2 }}
                >
                  Preview
                </Button>
              )}
            </Stack>
          </CardContent>
        </Card>
        
        {/* Cover Letter Card */}
        <Card 
          variant="outlined" 
          sx={{ 
            borderRadius: 3,
            border: isCoverLetterAvailable ? '2px solid' : '1px solid',
            borderColor: 'secondary.main',
            position: 'relative',
            overflow: 'visible',
            width: { xs: '100%', sm: 300 },
            flexShrink: 0
          }}
        >
          {/* {isCoverLetterAvailable && (
            <Chip
              label="Ready"
              color="success"
              size="small"
              sx={{
                position: 'absolute',
                top: -8,
                right: 16,
                zIndex: 1
              }}
            />
          )} */}
          <CardContent sx={{ p: 3, textAlign: 'center' }}>
            <Email sx={{ fontSize: 48, color: 'secondary.main', mb: 2 }} />
            <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
              Cover Letter
            </Typography>
            <Stack spacing={2}>
              <Button
                variant="contained"
                size="large"
                startIcon={<Download />}
                onClick={() => onDownload('coverLetter')}
                disabled={!isCoverLetterAvailable}
                fullWidth
                color="secondary"
                sx={{
                  borderRadius: 2,
                  fontWeight: 600,
                  '&:disabled': {
                    opacity: 0.6
                  }
                }}
              >
                Download Letter
              </Button>
              {isCoverLetterAvailable && (
                <Button
                  variant="outlined"
                  size="medium"
                  startIcon={<Visibility />}
                  onClick={() => handlePreview('coverLetter')}
                  fullWidth
                  color="secondary"
                  sx={{ borderRadius: 2 }}
                >
                  Preview
                </Button>
              )}
            </Stack>
          </CardContent>
        </Card>
      </Box>

      <Divider sx={{ my: 2 }} />

      {/* Create Another Button */}
      <Box sx={{ textAlign: 'center' }}>
        <Button
          variant="outlined"
          size="large"
          startIcon={<Add />}
          onClick={onCreateAnother}
          sx={{ 
            borderRadius: 2,
            px: 4,
            py: 1.5,
            fontWeight: 600,
            textTransform: 'none'
          }}
        >
          Create Another Resume
        </Button>
      </Box>
    </Stack>
  );
}