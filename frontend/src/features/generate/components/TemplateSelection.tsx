import { 
  Box, 
  Typography, 
  Button, 
  Stack,
  Card,
  CardContent,
  CardActions,
  Chip,
  RadioGroup,
  FormControlLabel,
  Radio,
  FormControl,
  IconButton,
  Tooltip
} from "@mui/material";
import { ArrowBack, ArrowForward, Visibility } from "@mui/icons-material";
import type { TemplateSelectionProps, TemplateType } from "../types";
import { RESUME_TEMPLATES, RESUME_PREVIEW_MAPPING } from "../constants";

export default function TemplateSelection({ 
  selectedTemplate, 
  onTemplateSelection, 
  onGenerate, 
  onBack 
}: TemplateSelectionProps) {
  
  const handlePreviewResume = (templateId: TemplateType) => {
    const resumeUrl = RESUME_PREVIEW_MAPPING[templateId];
    if (resumeUrl) {
      // Open the resume PDF in a new window/tab
      window.open(resumeUrl, '_blank');
    }
  };
  return (
    <Stack spacing={3}>
      <Typography variant="h5" align="center" gutterBottom>
        Select Resume Template
      </Typography>
      
      <Typography variant="body1" color="text.secondary" align="center">
        Choose the template that best matches your target role
      </Typography>

      <FormControl component="fieldset">
        <RadioGroup
          value={selectedTemplate}
          onChange={(e) => onTemplateSelection(e.target.value as TemplateType)}
        >
          <Stack spacing={2}>
            {RESUME_TEMPLATES.map((template) => {
              const IconComponent = template.icon;
              return (
                <Card 
                  key={template.id}
                  sx={{ 
                    cursor: 'pointer',
                    border: selectedTemplate === template.id ? 2 : 1,
                    borderColor: selectedTemplate === template.id ? 'primary.main' : 'divider',
                    '&:hover': { borderColor: 'primary.main' }
                  }}
                  onClick={() => onTemplateSelection(template.id)}
                >
                  <CardContent>
                    <FormControlLabel
                      value={template.id}
                      control={<Radio />}
                      label={
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, width: '100%' }}>
                          <IconComponent sx={{ fontSize: 32, color: 'primary.main' }} />
                          <Box sx={{ flex: 1 }}>
                            <Typography variant="h6">{template.title}</Typography>
                            <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                              {template.description}
                            </Typography>
                            <Box sx={{ display: 'flex', gap: 0.5, flexWrap: 'wrap' }}>
                              {template.keywords.map((keyword) => (
                                <Chip key={keyword} label={keyword} size="small" variant="outlined" />
                              ))}
                            </Box>
                          </Box>
                        </Box>
                      }
                      sx={{ margin: 0, width: '100%' }}
                    />
                  </CardContent>
                  <CardActions sx={{ justifyContent: 'flex-end', pt: 0 }}>
                    <Tooltip title="Preview Resume Template">
                      <IconButton 
                        onClick={(e) => {
                          e.stopPropagation(); // Prevent card selection when clicking preview
                          handlePreviewResume(template.id);
                        }}
                        size="small"
                        color="primary"
                      >
                        <Visibility />
                      </IconButton>
                    </Tooltip>
                  </CardActions>
                </Card>
              );
            })}
          </Stack>
        </RadioGroup>
      </FormControl>

      <Box sx={{ display: 'flex', gap: 2, justifyContent: 'space-between' }}>
        <Button
          variant="outlined"
          startIcon={<ArrowBack />}
          onClick={onBack}
        >
          Back
        </Button>
        
        <Button
          variant="contained"
          endIcon={<ArrowForward />}
          onClick={onGenerate}
          disabled={!selectedTemplate}
        >
          Generate Resume
        </Button>
      </Box>
    </Stack>
  );
}