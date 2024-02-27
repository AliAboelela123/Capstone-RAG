import React, { useState, useEffect, useRef } from 'react';
import { Box, Button, styled, GlobalStyles } from '@mui/material';
import PictureAsPdfIcon from '@mui/icons-material/PictureAsPdf';

const MainContentBox = styled(Box)(({ paddingBottom }) => ({
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'flex-end',
  overflowY: 'auto',
  overflowX: 'hidden',
  padding: '1rem',
  paddingTop: '60px',
  paddingBottom: paddingBottom,
  width: '100%',
  boxSizing: 'border-box',
}));

const MessageBox = styled(Box)(({ theme }) => ({
  marginBottom: '1rem',
  maxWidth: '70%',
  borderRadius: '10px',
}));

const StyledButton = styled(Button)({
  padding: '0.5rem 1rem',
  backgroundColor: '#DDDDDD',
  borderRadius: '50px',
  alignSelf: 'flex-end',
  color: 'black',
  fontFamily: 'Poppins, sans-serif',
  fontWeight: 400,
  maxWidth: '60%',
  marginTop: '-10px',
  marginBottom: '20px',
  '&:hover': {
    backgroundColor: '#BBBBBB',
  },
  '&:active': {
    backgroundColor: '#BBBBBB',
  },
});

const ResponseBox = styled(Box)({
  alignSelf: 'flex-start',
  backgroundColor: '#f3f3f3',
  padding: '0.5rem 1rem',
  maxWidth: '60%',
  borderRadius: '50px',
  fontFamily: 'Poppins, sans-serif',
});

const QueryBox = styled(Box)({
  alignSelf: 'flex-end',
  backgroundColor: '#007bff',
  color: 'white',
  margin: '0.5rem 0',
  padding: '0.5rem 1rem',
  maxWidth: '60%',
  borderRadius: '50px',
  fontFamily: 'Poppins, sans-serif',
});

function formatTextWithLineBreaks(text) {
  text.replace(/\\n/g, '\n');
  return text.split('\n').map((line, index, array) => (
    <React.Fragment key={index}>
      {line}
      {index !== array.length - 1 && <br />}
    </React.Fragment>
  ));
}

const MainContent = ({ messages, onOpenPdf }) => {
  const [queryBarHeight, setQueryBarHeight] = useState(0);
  const queryBarRef = useRef(null); 
  const endOfMessagesRef = useRef(null);

  useEffect(() => {
    const updateQueryBarHeight = () => {
      const height = queryBarRef.current ? queryBarRef.current.getBoundingClientRect().height : 120;
      setQueryBarHeight(height);
    };

    updateQueryBarHeight();
    window.addEventListener('resize', updateQueryBarHeight);
    return () => window.removeEventListener('resize', updateQueryBarHeight);
  }, [messages]);

  const scrollToBottom = () => {
    endOfMessagesRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleOpenPdf = (pdfFile) => {
    onOpenPdf(pdfFile);
  };

  return (
    <MainContentBox paddingBottom={`${queryBarHeight}px`}>
      <GlobalStyles styles={{
        '@global': {
          '@font-face': {
            fontFamily: 'Poppins',
            src: `url(https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap)`,
          }
        },
      }} />
      {messages.map((message, index) => (
        <React.Fragment key={index}>
          {message.type === 'response' && (
            <MessageBox 
              key={index}
              component={ResponseBox}
            >
              <div>{formatTextWithLineBreaks(message.text)}</div>
            </MessageBox>
          )}
          {message.type === 'query' && message.files && (
            <MessageBox 
              component={QueryBox}
            >
              <div>{formatTextWithLineBreaks(message.text)}</div>
            </MessageBox>
          )}
          {message.files && message.files.map((fileName, fileIndex) => (
            
              <StyledButton startIcon={<PictureAsPdfIcon />} 
                onClick={() => handleOpenPdf(fileName)}
              >
                {message.fileName}
              </StyledButton>
          ))}
        </React.Fragment>
      ))}
      <div ref={endOfMessagesRef} />
      
    </MainContentBox>
    
    
  );
};

export default MainContent;
