import React, { useEffect } from 'react';
import './QueryBar.css';

const QueryBar = () => {
  useEffect(() => {
    const textarea = document.getElementById('dynamicTextarea');
    if (textarea) {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
    }
  }, []);

  return (
    <div className="query-bar">
      <textarea id="dynamicTextarea" placeholder="Type your Query here..."></textarea>
      <button>Upload PDF</button>
      <button>Send</button>
    </div>
  );
};

export default QueryBar;