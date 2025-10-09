import { 
  Box, 
  TextField, 
  Button, 
  Alert,
  Stack,
  Typography,
  Card,
  CardContent,
  // Chip,
  Divider
} from "@mui/material";
import { PersonalVideo, Work, Business, Assignment } from "@mui/icons-material";
import type { JobInputFormProps } from "../types";

export default function JobInputForm({ 
  formData, 
  error, 
  onInputChange, 
  onStartPersonalization 
}: JobInputFormProps) {
  return (
    <Stack spacing={4}>
      {/* Header Section */}
      <Box sx={{ textAlign: 'center', mb: 2 }}>
        <Typography variant="h5" sx={{ fontWeight: 600, mb: 1 }}>
          Let's Get Started
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Paste the job details below and we'll create a personalized resume for you
        </Typography>
      </Box>

      {/* Form Fields */}
      <Stack spacing={3}>
        {/* Job Description Card */}
        <Card variant="outlined" sx={{ borderRadius: 2 }}>
          <CardContent sx={{ p: 3 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <Assignment sx={{ mr: 1, color: 'primary.main' }} />
              <Typography variant="h6" sx={{ fontWeight: 600 }}>
                Job Description
              </Typography>
              {/* <Chip 
                label="Required" 
                size="small" 
                color="primary" 
                sx={{ ml: 'auto' }}
              /> */}
            </Box>
            <TextField
              fullWidth
              placeholder="Paste the complete job posting here..."
              multiline
              rows={8}
              value={formData.jobDescription}
              onChange={onInputChange('jobDescription')}
              variant="outlined"
              required
              sx={{
                '& .MuiOutlinedInput-root': {
                  borderRadius: 2,
                  '&:hover fieldset': {
                    borderColor: 'primary.main',
                  },
                }
              }}
            />
          </CardContent>
        </Card>

        {/* Company and Position Details */}
        <Box sx={{ display: 'flex', gap: 2, flexDirection: { xs: 'column', sm: 'row' } }}>
          {/* Company Name */}
          <Card variant="outlined" sx={{ flex: 1, borderRadius: 2 }}>
            <CardContent sx={{ p: 3 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Business sx={{ mr: 1, color: 'primary.main' }} />
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                  Company
                </Typography>
              </Box>
              <TextField
                fullWidth
                placeholder="e.g., Google, Microsoft, Startup Inc."
                value={formData.companyName}
                onChange={onInputChange('companyName')}
                variant="outlined"
                required
                sx={{
                  '& .MuiOutlinedInput-root': {
                    borderRadius: 2,
                    '&:hover fieldset': {
                      borderColor: 'primary.main',
                    },
                  }
                }}
              />
            </CardContent>
          </Card>

          {/* Position Title */}
          <Card variant="outlined" sx={{ flex: 1, borderRadius: 2 }}>
            <CardContent sx={{ p: 3 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Work sx={{ mr: 1, color: 'primary.main' }} />
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                  Position
                </Typography>
              </Box>
              <TextField
                fullWidth
                placeholder="e.g., Software Engineer, Data Scientist"
                value={formData.positionTitle}
                onChange={onInputChange('positionTitle')}
                variant="outlined"
                required
                sx={{
                  '& .MuiOutlinedInput-root': {
                    borderRadius: 2,
                    '&:hover fieldset': {
                      borderColor: 'primary.main',
                    },
                  }
                }}
              />
            </CardContent>
          </Card>
        </Box>
      </Stack>

      {/* Error Alert */}
      {error && (
        <Alert 
          severity="error" 
          sx={{ 
            borderRadius: 2,
            '& .MuiAlert-message': {
              width: '100%'
            }
          }}
        >
          {error}
        </Alert>
      )}

      <Divider sx={{ my: 2 }} />

      {/* Start Personalization Button */}
      <Button
        fullWidth
        variant="contained"
        size="large"
        onClick={onStartPersonalization}
        startIcon={<PersonalVideo />}
        sx={{ 
          py: 2,
          borderRadius: 2,
          fontSize: '1.1rem',
          fontWeight: 600,
          textTransform: 'none',
          background: 'linear-gradient(45deg, #1976d2, #42a5f5)',
          '&:hover': {
            background: 'linear-gradient(45deg, #1565c0, #1e88e5)',
            transform: 'translateY(-2px)',
            boxShadow: '0 8px 25px rgba(25, 118, 210, 0.3)',
          },
          transition: 'all 0.3s ease'
        }}
      >
        Start Creating Your Resume
      </Button>
    </Stack>
  );
}