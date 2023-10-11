import React from 'react';
import './MainContent.css';

const MainContent = ({ messages }) => {
  return (
    <div className="main-content">
      {messages.map((message, index) => (
        <div 
            key={index} 
            className={`message ${message.type}`}
        >
          {message.text}
        </div>
      ))}
    </div>
  );
};

export default MainContent;
