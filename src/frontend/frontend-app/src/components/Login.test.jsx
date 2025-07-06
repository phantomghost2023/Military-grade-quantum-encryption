import { render, screen, fireEvent, act, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import Login from './Login';
import { useStore } from '../store';
import { fetchData } from '../api';

// Mock the useStore hook
vi.mock('../store', () => ({
  useStore: vi.fn(),
}));

// Mock the fetchData function
vi.mock('../api', () => ({
  fetchData: vi.fn(),
}));

describe('Login Component', () => {
  let setAuthMock;

  beforeEach(() => {
    setAuthMock = vi.fn();
    useStore.mockImplementation((selector) => selector({
      isAuthenticated: false,
      setAuth: setAuthMock,
    }));
    fetchData.mockReset();
  });

  it('renders correctly', () => {
    render(<Login />);
    expect(screen.getByLabelText(/username/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /login/i })).toBeInTheDocument();
  });

  it('handles input changes', () => {
    render(<Login />);
    const usernameInput = screen.getByLabelText(/username/i);
    const passwordInput = screen.getByLabelText(/password/i);

    fireEvent.change(usernameInput, { target: { value: 'testuser' } });
    fireEvent.change(passwordInput, { target: { value: 'testpass' } });

    expect(usernameInput.value).toBe('testuser');
    expect(passwordInput.value).toBe('testpass');
  });

  it('shows error message on failed login', async () => {
    fetchData.mockRejectedValueOnce(new Error('Invalid credentials'));

    render(<Login />);
    const loginButton = screen.getByRole('button', { name: /login/i });

    await act(async () => {
      fireEvent.click(loginButton);
    });

    await waitFor(() => {
      expect(screen.getByText(/invalid credentials/i)).toBeInTheDocument();
    });
    expect(setAuthMock).not.toHaveBeenCalled();
  });

  it('calls setAuth on successful login', async () => {
    fetchData.mockResolvedValueOnce({ token: 'mock-token' });

    render(<Login />);
    const usernameInput = screen.getByLabelText(/username/i);
    const passwordInput = screen.getByLabelText(/password/i);
    const loginButton = screen.getByRole('button', { name: /login/i });

    await act(async () => {
      fireEvent.change(usernameInput, { target: { value: 'testuser' } });
      fireEvent.change(passwordInput, { target: { value: 'testpass' } });
      fireEvent.click(loginButton);
    });

    await waitFor(() => {
      expect(setAuthMock).toHaveBeenCalledWith(true, 'mock-token');
    });
  });
});