import React, { useEffect, useRef } from 'react';
import { Button, TextField, Box, styled, Typography, ThemeProvider, createTheme } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import PublishIcon from '@mui/icons-material/Publish';

const theme = createTheme({
  typography: {
    fontFamily: 'Poppins, sans-serif',
  },
  components: {
    MuiCssBaseline: {
      styleOverrides: {
        '@global': {
          '@font-face': {
            fontFamily: 'Poppins',
            src: `url(https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap)`,
          },
        },
      },
    },
  },
});

const StyledBox = styled(Box)({
  display: 'flex',
  justifyContent: 'space-between',
  padding: '1rem 0',
  backgroundColor: '#f3f3f3',
  borderTop: '1px solid #e0e0e0',
  position: 'fixed',
  width: '100%',
  bottom: 0,
  left: 0,
});

const StyledButton = styled(Button)({
  padding: '0.5rem 1rem',
  backgroundColor: '#B76E79',
  borderRadius: '0.5rem',
  color: 'white',
  marginRight: '1rem',
  fontFamily: 'Poppins, sans-serif',
  fontWeight: 600,
  '&:hover': {
    backgroundColor: '#0056b3',
  },
  '&:active': {
    backgroundColor: '#003d80',
  },
});

const StyledTextField = styled(TextField)({
  flex: 1,
  margin: '0 1rem',
  '& .MuiInputBase-root': {
    borderRadius: '0.5rem',
  },
});

const QueryBar = () => {
  const textareaRef = useRef(null);

  useEffect(() => {
    const currentRef = textareaRef.current;

    const handleInput = () => {
      if (currentRef) {
        currentRef.style.height = 'auto';
        currentRef.style.height = `${currentRef.scrollHeight}px`;
      }
    };

    if (currentRef) {
      currentRef.addEventListener('input', handleInput);
    }

    return () => {
      if (currentRef) {
        currentRef.removeEventListener('input', handleInput);
      }
    };
  }, []);

  return (
    <StyledBox>
      <StyledTextField
        multiline
        placeholder="Type your Query here..."
        inputRef={textareaRef}
        InputProps={{ disableUnderline: true }}
      />
      <StyledButton variant="contained" endIcon={<PublishIcon />}>
        <Typography variant="button">Upload PDF</Typography>
      </StyledButton>
      <StyledButton variant="contained" endIcon={<SendIcon />}>
        <Typography variant="button">Send</Typography>
      </StyledButton>
    </StyledBox>
  );
};

export default function App() {
  return (
    <ThemeProvider theme={theme}>
      <QueryBar />
    </ThemeProvider>
  );
}
