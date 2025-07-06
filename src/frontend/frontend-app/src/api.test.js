import { describe, it, expect, vi } from 'vitest';
import { fetchData } from './api';

describe('fetchData', () => {
  // Mock the global fetch function
  const mockFetch = vi.fn();
  global.fetch = mockFetch;

  beforeEach(() => {
    mockFetch.mockReset();
    vi.spyOn(console, 'error').mockImplementation(() => {}); // Mock console.error
  });

  afterEach(() => {
    vi.restoreAllMocks(); // Restore all mocks after each test
  });

  it('should fetch data successfully', async () => {
    const mockData = { message: 'Success' };
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve(mockData),
    });

    const data = await fetchData('test-endpoint');

    expect(mockFetch).toHaveBeenCalledWith(
      'http://localhost:5000/api/test-endpoint',
      {}
    );
    expect(data).toEqual(mockData);
  });

  it('should throw an error if response is not ok', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: false,
      status: 404,
    });

    await expect(fetchData('test-endpoint')).rejects.toThrow('HTTP error! status: 404');
  });

  it('should throw an error if fetch fails', async () => {
    mockFetch.mockRejectedValueOnce(new Error('Network error'));

    await expect(fetchData('test-endpoint')).rejects.toThrow('Network error');
  });
});