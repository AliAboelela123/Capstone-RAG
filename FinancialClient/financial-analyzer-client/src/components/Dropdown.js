import React from 'react';
import './Dropdown.css';

function Dropdown() {
  return (
    <div className="dropdown">
      <button className="dropbtn">Level: Expert</button>
      <div className="dropdown-content">
        <h1>Beginner</h1>
        <h1>Intermediate</h1>
        <h1>Expert</h1>
      </div>
    </div>
  );
}

export default Dropdown;