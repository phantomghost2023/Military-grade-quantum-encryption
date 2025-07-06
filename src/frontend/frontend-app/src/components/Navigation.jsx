// src/frontend/frontend-app/src/components/Navigation.jsx

import React from 'react';
import { List, ListItem, ListItemButton, ListItemText, Box } from '@mui/material';
import { Link } from 'react-router-dom';

const Navigation = () => {
  return (
    <Box sx={{ width: 250, bgcolor: 'background.paper' }}>
      <List>
        <ListItem disablePadding>
          <ListItemButton component={Link} to="/agent-management">
            <ListItemText primary="Agent Management" />
          </ListItemButton>
        </ListItem>
        <ListItem disablePadding>
          <ListItemButton component={Link} to="/policy-configuration">
            <ListItemText primary="Policy Configuration" />
          </ListItemButton>
        </ListItem>
        <ListItem disablePadding>
          <ListItemButton component={Link} to="/event-monitoring">
            <ListItemText primary="Event Monitoring" />
          </ListItemButton>
        </ListItem>
        <ListItem disablePadding>
          <ListItemButton component={Link} to="/kms-integration">
            <ListItemText primary="KMS Integration" />
          </ListItemButton>
        </ListItem>
        <ListItem disablePadding>
          <ListItemButton component={Link} to="/pqc-research">
            <ListItemText primary="PQC Research" />
          </ListItemButton>
        </ListItem>
      </List>
    </Box>
  );
};

export default Navigation;