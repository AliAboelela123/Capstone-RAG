import React from 'react';
import { Box, styled, GlobalStyles } from '@mui/material';

const MainContentBox = styled(Box)({
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'flex-end',
  overflowY: 'auto',
  overflowX: 'hidden',
  padding: '1rem',
  paddingTop: '60px',
  paddingBottom: '90px',
  width: '100%',
  boxSizing: 'border-box',
  maxHeight: 'calc(100vh - 100 - 100)', 
});

const MessageBox = styled(Box)(({ theme }) => ({
  marginBottom: '1rem',
  maxWidth: '70%',
  borderRadius: '10px',
}));

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

const MainContent = ({ messages }) => {
  return (
    <MainContentBox>
      <GlobalStyles styles={{
        '@global': {
          '@font-face': {
            fontFamily: 'Poppins',
            src: `url(https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap)`,
          }
        },
      }} />
      {messages.map((message, index) => (
        <MessageBox 
          key={index}
          component={message.type === 'response' ? ResponseBox : QueryBox}
        >
          {message.text}
        </MessageBox>
      ))}
    </MainContentBox>
  );
};

export default MainContent;
