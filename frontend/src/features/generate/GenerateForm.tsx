import { 
  Box, 
  TextField, 
  Typography, 
  Button, 
  Paper,
  CircularProgress,
  Alert,
  Stack
} from "@mui/material";
import { Download, Send } from "@mui/icons-material";
import { useState } from "react";

interface FormData {
  jobDescription: string;
  companyName: string;
  positionTitle: string;
}

export default function GenerateForm() {
  const [formData, setFormData] = useState<FormData>({
    jobDescription: "",
    companyName: "",
    positionTitle: ""
  });

  const [paths, setPaths] = useState({
    resumePath: "",
    coverLetterPath: ""
  })
  
  const [isLoading, setIsLoading] = useState(false);
  const [isGenerated, setIsGenerated] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleInputChange = (field: keyof FormData) => (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    setFormData(prev => ({
      ...prev,
      [field]: event.target.value
    }));
  };

  const handleSubmit = async () => {
    setError(null);
    
    // Basic validation
    if (!formData.jobDescription.trim() || !formData.companyName.trim() || !formData.positionTitle.trim()) {
      setError("Please fill in all fields");
      return;
    }

    setIsLoading(true);
    
    try {
      const response = await fetch('http://localhost:8080/api/generate/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ message: 'Unknown error' }));
        throw new Error(errorData.message || `HTTP ${response.status}`);
      }
      
      const result = await response.json();

      setPaths({
        resumePath: result["resume_path"],
        coverLetterPath: result["cover_letter_path"]
      })
      console.log('Generation result:', result);
      
      setIsGenerated(true);
    } catch (error) {
      console.error('Generation error:', error);
      setError(error instanceof Error ? error.message : "Failed to generate documents. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleDownload = (type: 'resume' | 'coverLetter') => {
    // TODO: Implement actual download logic
    console.log(`Downloading ${type}...`);
    
    // For now, create a dummy download
    const link = document.createElement('a');
    link.href = paths[`${type}Path`];
    console.log(link.href);
    link.download = `${formData.companyName}_${formData.positionTitle}_${type}.pdf`;
    link.click();
  };

  return (
    <Box sx={{ maxWidth: 800, mx: 'auto', p: 3 }}>
      <Typography variant="h4" gutterBottom align="center" sx={{ mb: 4 }}>
        🤖 Aria - AI Resume & Cover Letter Generator
      </Typography>
      
      <Paper elevation={3} sx={{ p: 4 }}>
        <Stack spacing={3}>
          {/* Job Description */}
          <TextField
            fullWidth
            label="Job Description"
            placeholder="Paste the complete job posting here..."
            multiline
            rows={8}
            value={formData.jobDescription}
            onChange={handleInputChange('jobDescription')}
            variant="outlined"
            required
          />

          {/* Company Name and Position Title */}
          <Box sx={{ display: 'flex', gap: 2, flexDirection: { xs: 'column', sm: 'row' } }}>
            <TextField
              fullWidth
              label="Company Name"
              placeholder="e.g., Google, Microsoft, Startup Inc."
              value={formData.companyName}
              onChange={handleInputChange('companyName')}
              variant="outlined"
              required
            />

            <TextField
              fullWidth
              label="Position Title"
              placeholder="e.g., Software Engineer, Data Scientist"
              value={formData.positionTitle}
              onChange={handleInputChange('positionTitle')}
              variant="outlined"
              required
            />
          </Box>

          {/* Error Alert */}
          {error && (
            <Alert severity="error">{error}</Alert>
          )}

          {/* Submit Button */}
          <Button
            fullWidth
            variant="contained"
            size="large"
            onClick={handleSubmit}
            disabled={isLoading}
            startIcon={isLoading ? <CircularProgress size={20} /> : <Send />}
            sx={{ py: 1.5 }}
          >
            {isLoading ? 'Generating Documents...' : 'Generate Resume & Cover Letter'}
          </Button>

          {/* Download Links */}
          {isGenerated && (
            <Box>
              <Box sx={{ 
                display: 'flex', 
                gap: 2, 
                justifyContent: 'center',
                flexDirection: { xs: 'column', sm: 'row' }
              }}>
                <Button
                  variant="outlined"
                  startIcon={<Download />}
                  onClick={() => handleDownload('resume')}
                  sx={{ minWidth: 200 }}
                >
                  Download Resume
                </Button>
                
                <Button
                  variant="outlined"
                  startIcon={<Download />}
                  onClick={() => handleDownload('coverLetter')}
                  sx={{ minWidth: 200 }}
                >
                  Download Cover Letter
                </Button>
              </Box>
              
              <Typography 
                variant="body2" 
                color="text.secondary" 
                align="center" 
                sx={{ mt: 2 }}
              >
                ✅ Documents generated successfully! Click the buttons above to download.
              </Typography>
            </Box>
          )}
        </Stack>
      </Paper>
    </Box>
  );
}
