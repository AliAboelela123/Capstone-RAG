import React, { useState } from 'react';
import { Button, Menu, MenuItem, Typography, styled } from '@mui/material';
import ArrowDropDownIcon from '@mui/icons-material/ArrowDropDown';
import { GlobalStyles } from '@mui/system';

const StyledButton = styled(Button)({
  color: '#FFFFFF',
  borderColor: '#007BFF',
  fontWeight: 600,
  marginRight: 10,
});

function Dropdown({ selectedLevel, setSelectedLevel }) {
  const [anchorEl, setAnchorEl] = useState(null);

  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = (level) => {
    if (level) setSelectedLevel(level);
    setAnchorEl(null);
  };

  return (
    <div>
      <GlobalStyles styles={{
        '@global': {
          '@font-face': {
            fontFamily: 'Poppins',
            src: `url(https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap)`,
          },
          body: {
            fontFamily: 'Poppins, sans-serif',
          },
        },
      }} />

      <StyledButton 
        endIcon={<ArrowDropDownIcon />}
        onClick={handleClick}
      >
        Level: {selectedLevel}
      </StyledButton>

      <Menu
        anchorEl={anchorEl}
        keepMounted
        open={Boolean(anchorEl)}
        onClose={handleClose}
        PaperProps={{
          style: {
            borderRadius: 6,
            boxShadow: '0px 4px 20px rgba(0, 0, 0, 0.1)',
          }
        }}
      >
        <MenuItem onClick={() => handleClose('Beginner')}>
          <Typography variant="body1">Beginner</Typography>
        </MenuItem>
        <MenuItem onClick={() => handleClose('Intermediate')}>
          <Typography variant="body1">Intermediate</Typography>
        </MenuItem>
        <MenuItem onClick={() => handleClose('Expert')}>
          <Typography variant="body1">Expert</Typography>
        </MenuItem>
      </Menu>
    </div>
  );
}

export default Dropdown;
