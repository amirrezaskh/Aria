import { Box } from "@mui/material";
import GenerateForm from "../../features/generate/GenerateForm";
import "./styles.css";

export default function App() {
  return (
    <Box
      sx={{
        maxWidth: {
          xl: "lg",
          lg: "md",
        },
        mx: "auto",
      }}
    >
      <GenerateForm />
    </Box>
  );
}
