import React from 'react';
import './Header.css';
import Dropdown from './Dropdown';

const Header = () => {
  return (
    <header className="header">
      Financial LLM Analyzer
      <Dropdown className="button"/>
    </header>
  );
};

export default Header;