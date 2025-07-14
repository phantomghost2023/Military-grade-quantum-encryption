import React from 'react';
import { Box, Typography, Grid, Paper, IconButton, FormControl, InputLabel, Select, MenuItem, LinearProgress, Avatar, Stack, Divider } from '@mui/material';
import { User as UserIcon, CheckCircleOutline, WarningAmberOutlined, LockOutlined, AccountCircleOutlined, SettingsOutlined, SecurityOutlined, NetworkCheckOutlined, IntegrationInstructionsOutlined } from '@mui/icons-material';

function Dashboard() {
  return (
    <Box sx={{ flexGrow: 1, p: 3, backgroundColor: '#1A2027', minHeight: '100vh' }}>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
        <Typography variant="h4" sx={{ color: '#E0E0E0' }}>
          Dashboard
        </Typography>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <IconButton sx={{ color: '#E0E0E0' }}>
            <UserIcon />
          </IconButton>
          <Typography variant="body1" sx={{ color: '#E0E0E0', ml: 1 }}>
            User
          </Typography>
        </Box>
      </Box>

      <Grid container spacing={3}>
        {/* System Status */}
        <Grid item xs={12} md={6} lg={4}>
          <Paper sx={{ p: 3, backgroundColor: '#2C333A', color: '#E0E0E0', borderRadius: '8px' }}>
            <Typography variant="h6" gutterBottom sx={{ color: '#90CAF9' }}>System Status</Typography>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
              <CheckCircleOutline sx={{ color: '#81C784', mr: 1 }} />
              <Typography>Operational</Typography>
              <Typography sx={{ ml: 'auto' }}>5</Typography>
            </Box>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
              <Typography sx={{ mr: 1 }}>||</Typography>
              <Typography>Active Encryption Sessions</Typography>
              <Typography sx={{ ml: 'auto' }}>12</Typography>
            </Box>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <WarningAmberOutlined sx={{ color: '#FFD54F', mr: 1 }} />
              <Typography>Key Management Alerts</Typography>
              <Typography sx={{ ml: 'auto' }}>13</Typography>
            </Box>
            <Stack direction="row" spacing={1} sx={{ mt: 2 }}>
              <Typography variant="body2" sx={{ color: '#90CAF9' }}>Generate</Typography>
              <Typography variant="body2" sx={{ color: '#90CAF9' }}>Store</Typography>
              <Typography variant="body2" sx={{ color: '#90CAF9' }}>Distribute</Typography>
              <Typography variant="body2" sx={{ color: '#90CAF9' }}>Revoke</Typography>
            </Stack>
          </Paper>
        </Grid>

        {/* Encryption/Decryption */}
        <Grid item xs={12} md={6} lg={4}>
          <Paper sx={{ p: 3, backgroundColor: '#2C333A', color: '#E0E0E0', borderRadius: '8px' }}>
            <Typography variant="h6" gutterBottom sx={{ color: '#90CAF9' }}>Encryption/Decryption</Typography>
            <FormControl fullWidth variant="outlined" size="small" sx={{ mb: 2 }}>
              <InputLabel sx={{ color: '#E0E0E0' }}>Algorithm</InputLabel>
              <Select label="Algorithm" defaultValue="PQC" sx={{ color: '#E0E0E0', '.MuiOutlinedInput-notchedOutline': { borderColor: '#424242' }, '&.Mui-focused .MuiOutlinedInput-notchedOutline': { borderColor: '#90CAF9' }, '.MuiSvgIcon-root': { color: '#E0E0E0' } }}>
                <MenuItem value="PQC">PQC</MenuItem>
              </Select>
            </FormControl>
            <Typography variant="subtitle2" sx={{ color: '#B0B0B0' }}>Endpoints</Typography>
            <Box sx={{ display: 'flex', mb: 2 }}>
              <Paper sx={{ p: 1, backgroundColor: '#424242', color: '#E0E0E0', borderRadius: '4px', mr: 1 }}>Endpoint A</Paper>
              <Paper sx={{ p: 1, backgroundColor: '#424242', color: '#E0E0E0', borderRadius: '4px' }}>Endpoint B</Paper>
            </Box>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <Typography variant="subtitle2" sx={{ color: '#B0B0B0', mr: 1 }}>Status:</Typography>
              <LockOutlined sx={{ color: '#81C784', mr: 0.5 }} />
              <Typography sx={{ color: '#81C784' }}>Secure</Typography>
            </Box>
            <Typography variant="subtitle2" sx={{ color: '#B0B0B0' }}>Communication Logs</Typography>
            <Typography variant="body2">2 02:11 20:28:12:25</Typography>
            <LinearProgress variant="determinate" value={70} sx={{ height: 5, borderRadius: 5, backgroundColor: '#424242', '& .MuiLinearProgress-bar': { backgroundColor: '#90CAF9' }, mb: 0.5 }} />
            <Typography variant="body2">3 00:11 20:26:12:95</Typography>
            <LinearProgress variant="determinate" value={50} sx={{ height: 5, borderRadius: 5, backgroundColor: '#424242', '& .MuiLinearProgress-bar': { backgroundColor: '#90CAF9' } }} />
          </Paper>
        </Grid>

        {/* Automation & Orchestration */}
        <Grid item xs={12} md={6} lg={4}>
          <Paper sx={{ p: 3, backgroundColor: '#2C333A', color: '#E0E0E0', borderRadius: '8px' }}>
            <Typography variant="h6" gutterBottom sx={{ color: '#90CAF9' }}>Automation & Orchestration</Typography>
            <Typography variant="body2" sx={{ mb: 2 }}>Workflow Builder: Trigger → Condition → Action</Typography>
            {/* Placeholder for workflow builder diagram */}
            <Box sx={{ width: '100%', height: 100, backgroundColor: '#424242', display: 'flex', alignItems: 'center', justifyContent: 'center', borderRadius: '4px', mb: 2 }}>
              <Typography variant="caption" sx={{ color: '#B0B0B0' }}>Workflow Diagram Placeholder</Typography>
            </Box>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <Typography variant="subtitle2" sx={{ color: '#B0B0B0', mr: 1 }}>Status:</Typography>
              <LockOutlined sx={{ color: '#81C784', mr: 0.5 }} />
              <Typography sx={{ color: '#81C784' }}>Secure</Typography>
            </Box>
            <Typography variant="subtitle2" sx={{ color: '#B0B0B0' }}>Communication Logs</Typography>
            {/* Placeholder for communication logs graph */}
            <Box sx={{ width: '100%', height: 50, backgroundColor: '#424242', display: 'flex', alignItems: 'center', justifyContent: 'center', borderRadius: '4px' }}>
              <Typography variant="caption" sx={{ color: '#B0B0B0' }}>Graph Placeholder</Typography>
            </Box>
          </Paper>
        </Grid>

        {/* QKD Simulation & Integration */}
        <Grid item xs={12} md={6} lg={4}>
          <Paper sx={{ p: 3, backgroundColor: '#2C333A', color: '#E0E0E0', borderRadius: '8px' }}>
            <Typography variant="h6" gutterBottom sx={{ color: '#90CAF9' }}>QKD Simulation & Integration</Typography>
            <Typography variant="subtitle2" sx={{ color: '#B0B0B0' }}>Key Generation Rate</Typography>
            {/* Placeholder for Key Generation Rate Graph */}
            <Box sx={{ width: '100%', height: 80, backgroundColor: '#424242', display: 'flex', alignItems: 'center', justifyContent: 'center', borderRadius: '4px', mb: 2 }}>
              <Typography variant="caption" sx={{ color: '#B0B0B0' }}>Graph Placeholder</Typography>
            </Box>
            <Typography variant="subtitle2" sx={{ color: '#B0B0B0' }}>Error Rate</Typography>
            {/* Placeholder for Error Rate Graph */}
            <Box sx={{ width: '100%', height: 80, backgroundColor: '#424242', display: 'flex', alignItems: 'center', justifyContent: 'center', borderRadius: '4px', mb: 2 }}>
              <Typography variant="caption" sx={{ color: '#B0B0B0' }}>Graph Placeholder</Typography>
            </Box>
            <Typography variant="subtitle2" sx={{ color: '#B0B0B0' }}>Quantum Channel Parameters</Typography>
            <Stack direction="row" justifyContent="space-around" sx={{ mt: 1 }}>
              <Box textAlign="center">
                <Typography variant="h6" sx={{ color: '#81C784' }}>0.6+</Typography>
                <Typography variant="caption" sx={{ color: '#B0B0B0' }}>Key Sustainabilit</Typography>
              </Box>
              <Box textAlign="center">
                <Typography variant="h6" sx={{ color: '#FFD54F' }}>-6.0</Typography>
                <Typography variant="caption" sx={{ color: '#B0B0B0' }}>Communic Channel</Typography>
              </Box>
              <Box textAlign="center">
                <Typography variant="h6" sx={{ color: '#90CAF9' }}>8.2 VA</Typography>
                <Typography variant="caption" sx={{ color: '#B0B0B0' }}>Security Unobod</Typography>
              </Box>
            </Stack>
          </Paper>
        </Grid>

        {/* Threat Intelligence & Analytics */}
        <Grid item xs={12} md={6} lg={4}>
          <Paper sx={{ p: 3, backgroundColor: '#2C333A', color: '#E0E0E0', borderRadius: '8px' }}>
            <Typography variant="h6" gutterBottom sx={{ color: '#90CAF9' }}>Threat Intelligence & Analytics</Typography>
            {/* Placeholder for world map */}
            <Box sx={{ width: '100%', height: 120, backgroundColor: '#424242', display: 'flex', alignItems: 'center', justifyContent: 'center', borderRadius: '4px', mb: 2 }}>
              <Typography variant="caption" sx={{ color: '#B0B0B0' }}>World Map Placeholder</Typography>
            </Box>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
              <Typography>Timed Data:</Typography>
              <Typography>92%</Typography>
            </Box>
            <LinearProgress variant="determinate" value={92} sx={{ height: 5, borderRadius: 5, backgroundColor: '#424242', '& .MuiLinearProgress-bar': { backgroundColor: '#81C784' }, mb: 1 }} />
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
              <Typography>Security Events:</Typography>
              <Typography>92%</Typography>
            </Box>
            <LinearProgress variant="determinate" value={92} sx={{ height: 5, borderRadius: 5, backgroundColor: '#424242', '& .MuiLinearProgress-bar': { backgroundColor: '#81C784' }, mb: 1 }} />
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
              <Typography>Anomaly Detection:</Typography>
              <Typography>87%</Typography>
            </Box>
            <LinearProgress variant="determinate" value={87} sx={{ height: 5, borderRadius: 5, backgroundColor: '#424242', '& .MuiLinearProgress-bar': { backgroundColor: '#81C784' } }} />
          </Paper>
        </Grid>

        {/* User & Role Management */}
        <Grid item xs={12} md={6} lg={4}>
          <Paper sx={{ p: 3, backgroundColor: '#2C333A', color: '#E0E0E0', borderRadius: '8px' }}>
            <Typography variant="h6" gutterBottom sx={{ color: '#90CAF9' }}>User & Role Management</Typography>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
              <Typography variant="subtitle2" sx={{ color: '#B0B0B0' }}>User Role</Typography>
              <Typography variant="subtitle2" sx={{ color: '#B0B0B0' }}>MFA</Typography>
            </Box>
            <Divider sx={{ backgroundColor: '#424242', mb: 1 }} />
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
              <Typography>Admin</Typography>
              <CheckCircleOutline sx={{ color: '#81C784' }} />
            </Box>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
              <Typography>Analyst</Typography>
              <CheckCircleOutline sx={{ color: '#81C784' }} />
            </Box>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
              <Typography>Operator</Typography>
              <CheckCircleOutline sx={{ color: '#81C784' }} />
            </Box>
          </Paper>
        </Grid>

        {/* System Configuration */}
        <Grid item xs={12} md={6} lg={4}>
          <Paper sx={{ p: 3, backgroundColor: '#2C333A', color: '#E0E0E0', borderRadius: '8px' }}>
            <Typography variant="h6" gutterBottom sx={{ color: '#90CAF9' }}>System Configuration</Typography>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
              <NetworkCheckOutlined sx={{ color: '#B0B0B0', mr: 1 }} />
              <Typography>Network Settings</Typography>
            </Box>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
              <IntegrationInstructionsOutlined sx={{ color: '#B0B0B0', mr: 1 }} />
              <Typography>Integration</Typography>
            </Box>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
              <SecurityOutlined sx={{ color: '#B0B0B0', mr: 1 }} />
              <Typography>Security Policies</Typography>
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}

export default Dashboard;