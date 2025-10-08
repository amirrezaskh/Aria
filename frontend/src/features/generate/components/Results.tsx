import { 
  Box, 
  Typography, 
  Button, 
  Stack
} from "@mui/material";
import { Download } from "@mui/icons-material";
import type { ResultsProps } from "../types";

export default function Results({ 
  onDownload, 
  onCreateAnother 
}: Pick<ResultsProps, 'onDownload' | 'onCreateAnother'>) {
  return (
    <Stack spacing={3}>
      <Typography variant="h5" align="center" gutterBottom color="success.main">
        ✅ Documents Generated Successfully!
      </Typography>
      
      <Typography variant="body1" color="text.secondary" align="center">
        Your personalized resume and cover letter are ready for download.
      </Typography>

      <Box sx={{ 
        display: 'flex', 
        gap: 2, 
        justifyContent: 'center',
        flexDirection: { xs: 'column', sm: 'row' }
      }}>
        <Button
          variant="contained"
          size="large"
          startIcon={<Download />}
          onClick={() => onDownload('resume')}
          sx={{ minWidth: 200 }}
        >
          Download Resume
        </Button>
        
        <Button
          variant="outlined"
          size="large"
          startIcon={<Download />}
          onClick={() => onDownload('coverLetter')}
          sx={{ minWidth: 200 }}
        >
          Download Cover Letter
        </Button>
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