import { 
  Box, 
  Typography, 
  Button, 
  Stack,
  Card,
  CardContent
} from "@mui/material";
import { 
  PersonalVideo, 
  Computer, 
  ArrowBack
} from "@mui/icons-material";
import type { PersonalizationChoiceProps } from "../types";

export default function PersonalizationChoice({ 
  onStrategySelection, 
  onBack 
}: PersonalizationChoiceProps) {
  return (
    <Stack spacing={3}>
      <Typography variant="h5" align="center" gutterBottom>
        Choose Your Resume Strategy
      </Typography>
      
      <Typography variant="body1" color="text.secondary" align="center">
        How would you like to create your resume for this position?
      </Typography>

      <Box sx={{ display: 'flex', gap: 3, justifyContent: 'center', flexDirection: { xs: 'column', md: 'row' } }}>
        {/* Generate New Resume Card */}
        <Card 
          sx={{ 
            flex: 1, 
            cursor: 'pointer', 
            '&:hover': { transform: 'translateY(-4px)' },
            transition: 'transform 0.2s ease-in-out'
          }}
          onClick={() => onStrategySelection('generate')}
        >
          <CardContent sx={{ textAlign: 'center', py: 4 }}>
            <PersonalVideo sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
            <Typography variant="h6" gutterBottom>
              Generate New Resume
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Create a completely customized resume tailored specifically to this job posting using AI
            </Typography>
          </CardContent>
        </Card>

        {/* Use Template Card */}
        <Card 
          sx={{ 
            flex: 1, 
            cursor: 'pointer', 
            '&:hover': { transform: 'translateY(-4px)' },
            transition: 'transform 0.2s ease-in-out'
          }}
          onClick={() => onStrategySelection('template')}
        >
          <CardContent sx={{ textAlign: 'center', py: 4 }}>
            <Computer sx={{ fontSize: 48, color: 'secondary.main', mb: 2 }} />
            <Typography variant="h6" gutterBottom>
              Use Template Resume
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Choose from pre-built resume templates optimized for specific roles and industries
            </Typography>
          </CardContent>
        </Card>
      </Box>

      <Button
        variant="outlined"
        startIcon={<ArrowBack />}
        onClick={onBack}
        sx={{ alignSelf: 'flex-start' }}
      >
        Back to Job Details
      </Button>
    </Stack>
  );
}