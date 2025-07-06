
// src/frontend/frontend-app/src/App.jsx

import React from 'react';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { Box, AppBar, Toolbar, Typography, Container, Drawer, useMediaQuery, useTheme } from '@mui/material';
import { theme } from './theme';
import Navigation from './components/Navigation';
import Login from './components/Login';
import { useStore } from './store';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import AgentManagement from './pages/AgentManagement';
import PolicyConfiguration from './pages/PolicyConfiguration';
import EventMonitoring from './pages/EventMonitoring';
import KMSIntegration from './pages/KMSIntegration';
import PQCResearch from './pages/PQCResearch';

function App() {
  const isAuthenticated = useStore((state) => state.isAuthenticated);

  if (!isAuthenticated) {
    return (
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Login />
      </ThemeProvider>
    );
  }

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Box sx={{ display: 'flex' }}>
          <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
            <Toolbar>
              <Typography variant="h6" noWrap component="div">
                Quantum Encryption Dashboard
              </Typography>
            </Toolbar>
          </AppBar>
          <Drawer
            variant="permanent"
            sx={{
              width: 240,
              flexShrink: 0,
              [`& .MuiDrawer-paper`]: { width: 240, boxSizing: 'border-box' },
            }}
          >
            <Toolbar />
            <Box sx={{ overflow: 'auto' }}>
              <Navigation />
            </Box>
          </Drawer>
          <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
            <Toolbar />
            <Container sx={{ mt: 4, mb: 4 }}>
              <Routes>
                <Route path="/agent-management" element={<AgentManagement />} />
                <Route path="/policy-configuration" element={<PolicyConfiguration />} />
                <Route path="/event-monitoring" element={<EventMonitoring />} />
                <Route path="/kms-integration" element={<KMSIntegration />} />
                <Route path="/pqc-research" element={<PQCResearch />} />
                {/* Add other routes here */}
                <Route path="/" element={
                  <Typography variant="h4" gutterBottom>
                    Welcome to the Dashboard
                  </Typography>
                } />
              </Routes>
            </Container>
          </Box>
        </Box>
      </Router>
    </ThemeProvider>
  );
}

function App() {
  const isAuthenticated = useStore((state) => state.isAuthenticated);
  const theme = useTheme();
  const isSmallScreen = useMediaQuery(theme.breakpoints.down('sm'));

  if (!isAuthenticated) {
    return (
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Login />
      </ThemeProvider>
    );
  }

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Box sx={{ display: 'flex' }}>
          <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
            <Toolbar>
              <Typography variant="h6" noWrap component="div">
                Quantum Encryption Dashboard
              </Typography>
            </Toolbar>
          </AppBar>
          <Drawer
            variant={isSmallScreen ? "temporary" : "permanent"}
            sx={{
              width: isSmallScreen ? 0 : 240,
              flexShrink: 0,
              [`& .MuiDrawer-paper`]: { width: isSmallScreen ? 0 : 240, boxSizing: 'border-box' },
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
              p: 3,
              ml: isSmallScreen ? 0 : '240px', // Adjust margin for drawer
              width: isSmallScreen ? '100%' : `calc(100% - 240px)`, // Adjust width for drawer
            }}
          >
            <Toolbar />
            <Container sx={{ mt: 4, mb: 4 }}>
              <Routes>
                <Route path="/agent-management" element={<AgentManagement />} />
                <Route path="/policy-configuration" element={<PolicyConfiguration />} />
                <Route path="/event-monitoring" element={<EventMonitoring />} />
                <Route path="/kms-integration" element={<KMSIntegration />} />
                <Route path="/pqc-research" element={<PQCResearch />} />
                {/* Add other routes here */}
                <Route path="/" element={
                  <Typography variant="h4" gutterBottom>
                    Welcome to the Dashboard
                  </Typography>
                } />
              </Routes>
            </Container>
          </Box>
        </Box>
      </Router>
    </ThemeProvider>
  );
}

export default App;
