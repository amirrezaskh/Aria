import { 
  Box, 
  TextField, 
  Button, 
  Alert,
  Stack
} from "@mui/material";
import { PersonalVideo } from "@mui/icons-material";
import type { JobInputFormProps } from "../types";

export default function JobInputForm({ 
  formData, 
  error, 
  onInputChange, 
  onStartPersonalization 
}: JobInputFormProps) {
  return (
    <Stack spacing={3}>
      {/* Job Description */}
      <TextField
        fullWidth
        label="Job Description"
        placeholder="Paste the complete job posting here..."
        multiline
        rows={8}
        value={formData.jobDescription}
        onChange={onInputChange('jobDescription')}
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
          onChange={onInputChange('companyName')}
          variant="outlined"
          required
        />

        <TextField
          fullWidth
          label="Position Title"
          placeholder="e.g., Software Engineer, Data Scientist"
          value={formData.positionTitle}
          onChange={onInputChange('positionTitle')}
          variant="outlined"
          required
        />
      </Box>

      {/* Error Alert */}
      {error && (
        <Alert severity="error">{error}</Alert>
      )}

      {/* Start Personalization Button */}
      <Button
        fullWidth
        variant="contained"
        size="large"
        onClick={onStartPersonalization}
        startIcon={<PersonalVideo />}
        sx={{ py: 1.5 }}
      >
        Start Personalization
      </Button>
    </Stack>
  );
}