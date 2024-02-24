import React, { useState, useEffect, useRef } from 'react';
import {
  Button, TextField, Box, styled, Typography, IconButton, Paper
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import PublishIcon from '@mui/icons-material/Publish';
import CloseIcon from '@mui/icons-material/Close';
import CircularProgress from '@mui/material/CircularProgress';

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
  backgroundColor: 'white',
  margin: '0 1rem',
  '& .MuiInputBase-root': {
    borderRadius: '0.5rem',
  },
});

const StyledIconButton = styled(IconButton)({
  color: '#B76E79',
  '&:hover': {
    backgroundColor: '#f4f4f4',
  },
});

const StyledPaper = styled(Paper)({
  marginTop: '1rem',
  padding: '0.5rem',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'space-between',
  maxWidth: '100%',
  overflow: 'hidden',
  whiteSpace: 'nowrap',
  textOverflow: 'ellipsis',
});

const StyledFileName = styled(Typography)({
  overflow: 'hidden',
  textOverflow: 'ellipsis',
  whiteSpace: 'nowrap',
});

const QueryBar = ({ addMessage, appendMessage, uploadPDF, clearPDF, uploadedPDFs, setUploadedPDFs, selectedLevel }) => {
  const [isLoading, setIsLoading] = useState(false);
  const textareaRef = useRef(null);
  const fileInputRef = useRef(null);
  const queryBarRef = useRef(null);

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

  const handleUploadClick = () => {
    fileInputRef.current.click();
  };

  const handleFileChange = (event) => {
    const files = event.target.files;
    if (files.length > 0) {
      uploadPDF(files[0]);
    }
  };

  const handleSendClick = async () => {
    if (textareaRef.current.value.trim() === '') {
      alert('Please Enter a Query.');
      return;
    }


    const queryMessage = {
      type: 'query',
      text: `${textareaRef.current.value}`,
    };

    addMessage(queryMessage);
  
    setIsLoading(true);
    let isFirstChunk = true;

    try {
      // FormData to hold Text Query and PDF Files
      const formData = new FormData();
  
      // Append Text Query and complexity to formData
      formData.append('query', textareaRef.current.value.trim());
      formData.append('complexity', selectedLevel || 'Expert');
  
      // Append PDF Files to formData
      uploadedPDFs.forEach((file) => {
        formData.append('pdfFiles', file, file.name);
      });
  
      // Fetch request with signal for aborting if needed
      const controller = new AbortController();
      const signal = controller.signal;
      const response = await fetch('http://127.0.0.1:5001/query', {
        method: 'POST',
        body: formData,
        signal: signal,
      });
      
      if (response.ok) {

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let result = '';
  
        const read = async () => {
          const { done, value } = await reader.read();
          if (done) {
            console.log("Stream Complete");
            setIsLoading(false);
            return;
          }
          result += decoder.decode(value, { stream: true });
  
          // Process each chunk
          try {
            // Here we check if we have a complete JSON chunk to process
            if (result.endsWith('\n\n')) {
              const jsons = result.trim().split('\n\n');
              jsons.forEach(json => {
                const parsed = JSON.parse(json);

                // Check if either 'data' or 'error' has a valid value
                if (parsed.data || parsed.error) {
                  if (isFirstChunk || parsed.error) {
                    // Use parsed.error if parsed.data is undefined, else use parsed.data
                    const messageText = parsed.error || parsed.data;

                    addMessage({ type: 'response', text: messageText });
                    isFirstChunk = false; // After the first chunk, switch off the flag
                  } else {
                    appendMessage(parsed.data);
                  }
                }
              });
              result = ''; // Clear the buffer after processing
            }
          } catch (e) {
            console.error(e); // Error handling for JSON parsing
          }
  
          // Recursively read the next chunk
          read();
        };
  
        read(); // Start reading
      } else {
        throw new Error('Server Responded with an Error.');
      }
    } catch (error) {
      console.error(`Error: ${error.message}`);
    } finally {
      textareaRef.current.value = '';
      setUploadedPDFs([]);
      setIsLoading(false); // Ensure loading is set to false even if an error occurs
    }
  };

  return (
    <Box ref={queryBarRef}>
      <StyledBox>
        <Box sx={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
          <StyledTextField
            multiline
            placeholder="Type your Query here..."
            inputRef={textareaRef}
            disabled={isLoading}
          />
          <Box display="flex" flexDirection="column" alignItems="start" pl={2} mt={1}>
            {uploadedPDFs.map((file, index) => (
              <StyledPaper key={index}>
                <StyledFileName variant="body2" title={file.name}>
                  {file.name}
                </StyledFileName>
                <StyledIconButton size="small" onClick={() => clearPDF(index)} disabled={isLoading}>
                  <CloseIcon />
                </StyledIconButton>
              </StyledPaper>
            ))}
          </Box>
        </Box>
        <StyledButton variant="contained" endIcon={<PublishIcon />} onClick={handleUploadClick} disabled={isLoading}>
          <Typography variant="button">Upload PDF</Typography>
        </StyledButton>
        <StyledButton
          variant="contained"
          endIcon={isLoading ? <CircularProgress size={20} /> : <SendIcon />}
          onClick={handleSendClick}
          disabled={isLoading}
        >
          <Typography variant="button">{isLoading ? 'Sending...' : 'Send'}</Typography>
        </StyledButton>
      </StyledBox>
      <input
        type="file"
        accept="application/pdf"
        style={{ display: 'none' }}
        ref={fileInputRef}
        onChange={handleFileChange}
        multiple
        disabled={isLoading}
      />
    </Box>
  );
};

export default QueryBar;