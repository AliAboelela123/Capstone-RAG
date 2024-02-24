import React, { useState, useEffect, useRef } from 'react';
import { Box, styled, GlobalStyles } from '@mui/material';

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

const MainContent = ({ messages, addMessage }) => {
  const [queryBarHeight, setQueryBarHeight] = useState(0);
  const queryBarRef = useRef(null); 

  useEffect(() => {
    const updateQueryBarHeight = () => {
      const height = queryBarRef.current ? queryBarRef.current.getBoundingClientRect().height : 120;
      setQueryBarHeight(height);
    };

    updateQueryBarHeight();
    window.addEventListener('resize', updateQueryBarHeight);
    return () => window.removeEventListener('resize', updateQueryBarHeight);
  }, [messages]);

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
        <MessageBox 
          key={index}
          component={message.type === 'response' ? ResponseBox : QueryBox}
        >
          <div>{formatTextWithLineBreaks(message.text)}</div>
        </MessageBox>
      ))}
    </MainContentBox>
  );
};

export default MainContent;
