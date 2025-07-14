// src/frontend/frontend-app/src/components/Navigation.jsx

import React from 'react';
import { List, ListItem, ListItemButton, ListItemIcon, ListItemText, Box, Typography } from '@mui/material';
import { Link } from 'react-router-dom';
import { Dashboard as DashboardIcon, Key, Lock, AccountTree, Science, Insights, Group, Settings } from '@mui/icons-material';

const Navigation = () => {
  return (
    <Box sx={{ width: 250, bgcolor: '#1A2027', color: '#E0E0E0', height: '100%' }}>
      <Box sx={{ p: 2, textAlign: 'center', borderBottom: '1px solid #424242' }}>
        <Typography variant="h6" sx={{ color: '#E0E0E0', fontWeight: 'bold' }}>
          MILITARY-GRADE
        </Typography>
        <Typography variant="subtitle2" sx={{ color: '#90CAF9' }}>
          QUANTUM ENCRYPTION
        </Typography>
      </Box>
      <List>
        <ListItem disablePadding>
          <ListItemButton component={Link} to="/dashboard" sx={{ '&:hover': { backgroundColor: '#2C333A' } }}>
            <ListItemIcon sx={{ color: '#E0E0E0' }}>
              <DashboardIcon />
            </ListItemIcon>
            <ListItemText primary="Dashboard" />
          </ListItemButton>
        </ListItem>
        <ListItem disablePadding>
          <ListItemButton component={Link} to="/key-management" sx={{ '&:hover': { backgroundColor: '#2C333A' } }}>
            <ListItemIcon sx={{ color: '#E0E0E0' }}>
              <Key />
            </ListItemIcon>
            <ListItemText primary="Key Management" />
          </ListItemButton>
        </ListItem>
        <ListItem disablePadding>
          <ListItemButton component={Link} to="/encryption-decryption" sx={{ '&:hover': { backgroundColor: '#2C333A' } }}>
            <ListItemIcon sx={{ color: '#E0E0E0' }}>
              <Lock />
            </ListItemIcon>
            <ListItemText primary="Encryption/Decryption" />
          </ListItemButton>
        </ListItem>
        <ListItem disablePadding>
          <ListItemButton component={Link} to="/automation-orchestration" sx={{ '&:hover': { backgroundColor: '#2C333A' } }}>
            <ListItemIcon sx={{ color: '#E0E0E0' }}>
              <AccountTree />
            </ListItemIcon>
            <ListItemText primary="Automation & Orchestration" />
          </ListItemButton>
        </ListItem>
        <ListItem disablePadding>
          <ListItemButton component={Link} to="/qkd-simulation-integration" sx={{ '&:hover': { backgroundColor: '#2C333A' } }}>
            <ListItemIcon sx={{ color: '#E0E0E0' }}>
              <Science />
            </ListItemIcon>
            <ListItemText primary="QKD Simulation & Integration" />
          </ListItemButton>
        </ListItem>
        <ListItem disablePadding>
          <ListItemButton component={Link} to="/threat-intelligence-analytics" sx={{ '&:hover': { backgroundColor: '#2C333A' } }}>
            <ListItemIcon sx={{ color: '#E0E0E0' }}>
              <Insights />
            </ListItemIcon>
            <ListItemText primary="Threat Intelligence & Analytics" />
          </ListItemButton>
        </ListItem>
        <ListItem disablePadding>
          <ListItemButton component={Link} to="/user-role-management" sx={{ '&:hover': { backgroundColor: '#2C333A' } }}>
            <ListItemIcon sx={{ color: '#E0E0E0' }}>
              <Group />
            </ListItemIcon>
            <ListItemText primary="User & Role Management" />
          </ListItemButton>
        </ListItem>
        <ListItem disablePadding>
          <ListItemButton component={Link} to="/system-configuration" sx={{ '&:hover': { backgroundColor: '#2C333A' } }}>
            <ListItemIcon sx={{ color: '#E0E0E0' }}>
              <Settings />
            </ListItemIcon>
            <ListItemText primary="System Configuration" />
          </ListItemButton>
        </ListItem>
        {/* Removed unused routes for brevity and focus on the image's content */}
      </List>
    </Box>
  );
};

export default Navigation;