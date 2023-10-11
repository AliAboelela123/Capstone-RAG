import React from 'react';
import Header from './components/Header';
import MainContent from './components/MainContent';
import QueryBar from './components/QueryBar';
import './App.css';

const App = () => {
  const exampleMessages = [
    { type: 'response', text: "This is Apple's revenue in 2024: $123." },
    { type: 'query', text: "What are Apple's projected sales for 2025?" },
    { type: 'response', text: "This is Apple's revenue in 2024: $123." },
    { type: 'query', text: "What are Apple's projected sales for 2025?" },
    { type: 'response', text: "This is Apple's revenue in 2024: $123." },
    { type: 'query', text: "What are Apple's projected sales for 2025?" },
    { type: 'response', text: "This is Apple's revenue in 2024: $123." },
    { type: 'query', text: "What are Apple's projected sales for 2025?" },
    { type: 'response', text: "This is Apple's revenue in 2024: $123." },
    { type: 'query', text: "What are Apple's projected sales for 2025?" },
    { type: 'response', text: "This is Apple's revenue in 2024: $123." },
    { type: 'query', text: "What are Apple's projected sales for 2025?" },
    { type: 'response', text: "This is Apple's revenue in 2024: $123." },
    { type: 'query', text: "What are Apple's projected sales for 2025?" },
    { type: 'response', text: "This is Apple's revenue in 2024: $123." },
    { type: 'query', text: "What are Apple's projected sales for 2025?" },
  ];

  return (
    <div className="app">
      <Header />
      <div className="content">
        <MainContent messages={exampleMessages} />
      </div>
      <QueryBar />
    </div>
  );
};

export default App;