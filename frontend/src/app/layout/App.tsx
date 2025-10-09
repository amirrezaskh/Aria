import { Box, ThemeProvider, CssBaseline } from "@mui/material";
import { useEffect, useState } from "react";
import GenerateForm from "../../features/generate/GenerateForm";
import { ariaTheme } from "../../theme";
import "./styles.css";

interface ExtensionJobData {
  title?: string;
  company?: string;
  description?: string;
  location?: string;
  salary?: string;
  type?: string;
  remote?: string;
  requirements?: string[] | string;
}

export default function App() {
  const [extensionJobData, setExtensionJobData] = useState<ExtensionJobData | null>(null);

  useEffect(() => {
    // Chrome extension message listener
    const handleMessage = (event: MessageEvent) => {
      // Verify the message is from the Chrome extension
      if (event.data.type === 'JOB_DATA_FROM_EXTENSION') {
        console.log('Received job data from Chrome extension:', event.data.jobData);
        setExtensionJobData(event.data.jobData);
      }
    };

    // Add the message listener
    window.addEventListener('message', handleMessage);

    // Send ready signal to Chrome extension
    window.parent.postMessage({ type: 'REACT_APP_READY' }, '*');

    // Cleanup listener on unmount
    return () => {
      window.removeEventListener('message', handleMessage);
    };
  }, []);

  return (
    <ThemeProvider theme={ariaTheme}>
      <CssBaseline />
      <Box
        sx={{
          minHeight: '100vh',
          background: `linear-gradient(135deg, ${ariaTheme.palette.primary.main}08 0%, ${ariaTheme.palette.secondary.main}05 100%)`,
        }}
      >
        <GenerateForm extensionJobData={extensionJobData} />
      </Box>
    </ThemeProvider>
  );
}
