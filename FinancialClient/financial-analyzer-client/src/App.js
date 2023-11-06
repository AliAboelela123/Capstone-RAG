import React, { useState } from 'react';
import Header from './components/Header';
import MainContent from './components/MainContent';
import QueryBar from './components/QueryBar';
import { createTheme, ThemeProvider } from '@mui/material';
import './App.css';

const theme = createTheme({
  typography: {
    fontFamily: 'Poppins, sans-serif',
  },
});

const App = () => {
  const [messages, setMessages] = useState([]);
  const [uploadedPDFs, setUploadedPDFs] = useState([]);
  const [selectedLevel, setSelectedLevel] = useState('Beginner');

  const addMessage = (newMessage) => {
    setMessages((prevMessages) => {
      const updatedMessages = [...prevMessages, newMessage];
      console.log(updatedMessages);
      return updatedMessages;
    });
  };

  const uploadPDF = (file) => {
    setUploadedPDFs([...uploadedPDFs, file]);
  };

  const clearPDF = (index) => {
    setUploadedPDFs(uploadedPDFs.filter((_, i) => i !== index));
  };

  console.log('Rendering App Component with Messages:', messages);

  return (
    <ThemeProvider theme={theme}>
      <div className="app">
        <Header selectedLevel={selectedLevel} setSelectedLevel={setSelectedLevel} />
        <div className="content">
          <MainContent messages={messages} />
        </div>
        <QueryBar
          addMessage={addMessage}
          uploadPDF={uploadPDF}
          clearPDF={clearPDF}
          uploadedPDFs={uploadedPDFs}
          setUploadedPDFs={setUploadedPDFs}
          selectedLevel={selectedLevel}
        />
      </div>
    </ThemeProvider>
  );
};

export default App;