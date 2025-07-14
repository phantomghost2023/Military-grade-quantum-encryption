
// src/frontend/frontend-app/src/App.jsx

import React from 'react';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { Box, AppBar, Toolbar, Typography, Container, Drawer, useMediaQuery, useTheme } from '@mui/material';
import { theme as muiTheme } from './theme';
import Navigation from './components/Navigation';
import Login from './components/Login';
import { useStore } from './store';
import { Routes, Route } from 'react-router-dom';
// import AgentManagement from './pages/AgentManagement';
// import PolicyConfiguration from './pages/PolicyConfiguration';
// import EventMonitoring from './pages/EventMonitoring';
// import KMSIntegration from './pages/KMSIntegration';
// import PQCResearch from './pages/PQCResearch';
import Dashboard from './pages/Dashboard';
// import KeyManagement from './pages/KeyManagement';
// import EncryptionDecryption from './pages/EncryptionDecryption';
// import AutomationOrchestration from './pages/AutomationOrchestration';
// import QKDSimulationIntegration from './pages/QKDSimulationIntegration';
// import ThreatIntelligenceAnalytics from './pages/ThreatIntelligenceAnalytics';
// import UserRoleManagement from './pages/UserRoleManagement';
// import SystemConfiguration from './pages/SystemConfiguration';

function App() {
  const isAuthenticated = useStore((state) => state.isAuthenticated);
  const theme = useTheme();
  const isSmallScreen = useMediaQuery(theme.breakpoints.down('sm'));

  if (!isAuthenticated) {
    return (
      <ThemeProvider theme={muiTheme}>
        <CssBaseline />
        <Login />
      </ThemeProvider>
    );
  }

  return (
    <ThemeProvider theme={muiTheme}>
      <CssBaseline />
        <Box sx={{ display: 'flex' }}>
          <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1, backgroundColor: '#1A2027', boxShadow: 'none' }}>
            <Toolbar>
              {/* Placeholder for logo/title if needed, currently empty to match image */}
            </Toolbar>
          </AppBar>
          <Drawer
            variant={isSmallScreen ? "temporary" : "permanent"}
            sx={{
              width: isSmallScreen ? 0 : 240,
              flexShrink: 0,
              [`& .MuiDrawer-paper`]: { width: isSmallScreen ? 0 : 240, boxSizing: 'border-box', backgroundColor: '#1A2027', color: '#E0E0E0' },
            }}
          >
            <Toolbar />
            <Box sx={{ overflow: 'auto' }}>
              <Navigation />
            </Box>
          </Drawer>
          <Box
            component="main"
            sx={{
              flexGrow: 1,
              ml: isSmallScreen ? 0 : '240px', // Adjust margin for drawer
              width: isSmallScreen ? '100%' : `calc(100% - 240px)`, // Adjust width for drawer
              backgroundColor: '#1A2027',
              minHeight: '100vh'
            }}
          >
            <Toolbar />
              {/* <Routes>
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/key-management" element={<KeyManagement />} />
                <Route path="/encryption-decryption" element={<EncryptionDecryption />} />
                <Route path="/automation-orchestration" element={<AutomationOrchestration />} />
                <Route path="/qkd-simulation-integration" element={<QKDSimulationIntegration />} />
                <Route path="/threat-intelligence-analytics" element={<ThreatIntelligenceAnalytics />} />
                <Route path="/user-role-management" element={<UserRoleManagement />} />
                <Route path="/system-configuration" element={<SystemConfiguration />} />
                <Route path="/agent-management" element={<AgentManagement />} />
                <Route path="/policy-configuration" element={<PolicyConfiguration />} />
                <Route path="/event-monitoring" element={<EventMonitoring />} />
                <Route path="/kms-integration" element={<KMSIntegration />} />
                <Route path="/pqc-research" element={<PQCResearch />} />
                <Route path="/" element={<Dashboard />} />
              </Routes> */}

          </Box>
        </Box>
    </ThemeProvider>
  );
}

export default App;
