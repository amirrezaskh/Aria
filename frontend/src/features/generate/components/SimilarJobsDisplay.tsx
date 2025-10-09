import {
  Box,
  Typography,
  Card,
  CardContent,
  CardActions,
  Button,
  Chip,
  Alert,
  AlertTitle,
  Stack,
  LinearProgress,
  Divider
} from '@mui/material';
import { 
  CheckCircle, 
  Visibility, 
  Download,
  BusinessCenter,
  TrendingUp 
} from '@mui/icons-material';
import type { SimilarJob } from '../types';

interface SimilarJobsDisplayProps {
  similarJobs: SimilarJob[];
  isLoading: boolean;
  onUseSimilarResume: (job: SimilarJob) => void;
  onViewResume: (job: SimilarJob) => void;
  onProceedWithNew: () => void;
  onBack: () => void;
}

export function SimilarJobsDisplay({
  similarJobs,
  isLoading,
  onUseSimilarResume,
  onViewResume,
  onProceedWithNew,
  onBack
}: SimilarJobsDisplayProps) {
  
  const getSimilarityColor = (score: number) => {
    if (score >= 0.9) return 'success';
    if (score >= 0.8) return 'warning';
    return 'info';
  };

  const getSimilarityLabel = (score: number) => {
    if (score >= 0.9) return 'Excellent Match';
    if (score >= 0.8) return 'Good Match';
    return 'Similar';
  };

  if (isLoading) {
    return (
      <Box sx={{ textAlign: 'center', py: 4 }}>
        <TrendingUp sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
        <Typography variant="h6" gutterBottom>
          🔍 Searching for similar job applications...
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
          Analyzing your previous resumes using AI similarity matching
        </Typography>
        <LinearProgress sx={{ maxWidth: 300, mx: 'auto' }} />
      </Box>
    );
  }

  if (similarJobs.length === 0) {
    return (
      <Box sx={{ textAlign: 'center', py: 4 }}>
        <BusinessCenter sx={{ fontSize: 48, color: 'text.secondary', mb: 2 }} />
        <Typography variant="h6" gutterBottom>
          🆕 No Similar Applications Found
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
          This appears to be a unique position! We'll create a fresh resume for you.
        </Typography>
        <Button
          variant="contained"
          onClick={onProceedWithNew}
          sx={{ mt: 2 }}
        >
          Continue with New Resume
        </Button>
      </Box>
    );
  }

  return (
    <Box>
      <Alert severity="info" sx={{ mb: 3 }}>
        <AlertTitle>🎯 Similar Job Applications Found!</AlertTitle>
        We found {similarJobs.length} similar job application{similarJobs.length > 1 ? 's' : ''} in your history. 
        You can reuse an existing resume or create a new one.
      </Alert>

      <Typography variant="h6" gutterBottom sx={{ mb: 3 }}>
        Choose an option:
      </Typography>

      <Stack spacing={3}>
        {similarJobs.map((job) => (
          <Card 
            key={job.id}
            variant="outlined" 
            sx={{ 
              transition: 'all 0.2s',
              '&:hover': { 
                elevation: 3,
                transform: 'translateY(-2px)' 
              }
            }}
          >
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                  <Box>
                    <Typography variant="h6" component="h3" gutterBottom>
                      {job.position_title}
                    </Typography>
                    <Typography variant="subtitle1" color="primary" gutterBottom>
                      {job.company_name}
                    </Typography>
                  </Box>
                  
                  <Box sx={{ textAlign: 'right' }}>
                    <Chip
                      icon={<CheckCircle />}
                      label={`${Math.round(job.similarity_score * 100)}% similar`}
                      color={getSimilarityColor(job.similarity_score)}
                      variant="filled"
                      size="small"
                      sx={{ mb: 1 }}
                    />
                    <Typography variant="caption" display="block" color="text.secondary">
                      {getSimilarityLabel(job.similarity_score)}
                    </Typography>
                  </Box>
                </Box>

                <Divider sx={{ my: 2 }} />

                <Typography 
                  variant="body2" 
                  color="text.secondary" 
                  sx={{ 
                    display: '-webkit-box',
                    WebkitLineClamp: 3,
                    WebkitBoxOrient: 'vertical',
                    overflow: 'hidden',
                    mb: 2
                  }}
                >
                  {job.job_description}
                </Typography>

                <Typography variant="caption" color="text.secondary">
                  Applied on: {new Date(job.created_at).toLocaleDateString()}
                </Typography>
              </CardContent>

              <CardActions sx={{ p: 2, pt: 0 }}>
                <Button
                  variant="contained"
                  color="primary"
                  startIcon={<Download />}
                  onClick={() => onUseSimilarResume(job)}
                  sx={{ mr: 1 }}
                >
                  Use This Resume
                </Button>
                <Button
                  variant="outlined"
                  startIcon={<Visibility />}
                  onClick={() => onViewResume(job)}
                >
                  Preview
                </Button>
              </CardActions>
            </Card>
        ))}
      </Stack>

      <Divider sx={{ my: 4 }} />

      <Box sx={{ textAlign: 'center' }}>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
          Or create a completely new resume:
        </Typography>
        <Button
          variant="outlined"
          color="secondary"
          onClick={onProceedWithNew}
          sx={{ mr: 2 }}
        >
          Create New Resume
        </Button>
        <Button
          variant="text"
          onClick={onBack}
        >
          Back
        </Button>
      </Box>
    </Box>
  );
}