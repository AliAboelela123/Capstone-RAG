import React from 'react';
import Header from './components/Header';
import MainContent from './components/MainContent';
import QueryBar from './components/QueryBar';
import './App.css';

const App = () => {
  const exampleMessages = [
    { type: 'query', text: "What's the current Market Capitilization of Apple?" },
    { type: 'response', text: "As of our last update, Apple's Market Capitalization stands at $2.4 trillion." },

    { type: 'query', text: "How did the S&P 500 Index perform last Quarter?" },
    { type: 'response', text: "The S&P 500 Index rose by 4.5% last Quarter, marking a positive trend in the Market." },

    { type: 'query', text: "Are there any updates on Federal Reserve Interest Rate policies?" },
    { type: 'response', text: "The Federal Reserve recently announced a 25 basis point hike in Interest Rates, aiming to curb inflation." },

    { type: 'query', text: "How are Tech stocks performing compared to the energy sector?" },
    { type: 'response', text: "Tech stocks have seen a growth of 6% this year, while the energy sector surged by 11% due to rising oil prices." },

    { type: 'query', text: "Has Berkshire Hathaway released its annual report?" },
    { type: 'response', text: "Yes, Berkshire Hathaway's annual report was released last week. Key highlights include a 9% increase in operating income and notable investments in the tech sector." },

    { type: 'query', text: "Are there any emerging markets worth investing in currently?" },
    { type: 'response', text: "Many analysts are currently bullish on Southeast Asian markets, especially Vietnam and Indonesia, given their growing middle class and digital transformation." },

    { type: 'query', text: "What's the latest on the bond yield curve in the US?" },
    { type: 'response', text: "The yield curve has steepened recently, with 10-year Treasury yields rising faster than 2-year yields, indicating positive economic outlook in the US." },

    { type: 'query', text: "Any recommendations for dividend-paying stocks?" },
    { type: 'response', text: "Some popular dividend-paying stocks include Procter & Gamble, Johnson & Johnson, and Coca-Cola, known for their consistent payouts and stable business models." }
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