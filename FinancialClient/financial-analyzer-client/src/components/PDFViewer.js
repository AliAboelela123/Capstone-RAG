import React, { useState, useEffect, useRef } from 'react';
import { IconButton } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';

const PDFViewer = ({ pdfFile, onClose }) => {
    const [queryBarHeight, setQueryBarHeight] = useState(0);
    const queryBarRef = useRef(null);

    useEffect(() => {
        const updateQueryBarHeight = () => {
            const height = queryBarRef.current ? queryBarRef.current.getBoundingClientRect().height : 0;
            setQueryBarHeight(height);
        };

        updateQueryBarHeight();
        window.addEventListener('resize', updateQueryBarHeight);
        return () => window.removeEventListener('resize', updateQueryBarHeight);
    }, []);

    return (
        <div style={{ 
            display: 'flex', 
            flexDirection: 'row', 
            height: '100%', 
            marginTop: '50px', 
            position: 'relative', 
            paddingBottom: `${queryBarHeight}px`, 
            backgroundColor: '#323639' 
        }}>
            <IconButton onClick={onClose} style={{ color: 'white', display: 'flex', alignItems: 'flex-start' }}>
                <CloseIcon />
            </IconButton>
            <iframe
                src={pdfFile}
                style={{ width: '100%', height: '100%' }}
                frameBorder="0"
                title="PDF Viewer"
            ></iframe>
        </div>
    );
};

export default PDFViewer;
