import { describe, it, expect, beforeEach, vi } from 'vitest';
import { fetchApi } from '$lib/config';
import { mockApiResponse } from '../setup';

describe('API Configuration', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('makes successful API calls', async () => {
    const mockData = { id: 1, title: 'Test' };
    mockApiResponse(mockData);
    
    const result = await fetchApi('/api/test');
    
    expect(result).toEqual(mockData);
    expect(fetch).toHaveBeenCalledWith(
      'http://localhost:8000/api/test',
      expect.objectContaining({
        headers: {
          'Content-Type': 'application/json'
        }
      })
    );
  });

  it('handles API errors correctly', async () => {
    mockApiResponse({ detail: 'Not Found' }, false);
    
    await expect(fetchApi('/api/not-found')).rejects.toThrow('Not Found');
  });

  it('handles network errors gracefully', async () => {
    (fetch as any).mockRejectedValueOnce(new Error('Network Error'));
    
    await expect(fetchApi('/api/test')).rejects.toThrow('Network Error');
  });

  it('sends custom headers when provided', async () => {
    const mockData = { id: 1 };
    mockApiResponse(mockData);
    
    await fetchApi('/api/test', {
      headers: {
        'Authorization': 'Bearer token',
        'X-Custom': 'value'
      }
    });
    
    expect(fetch).toHaveBeenCalledWith(
      'http://localhost:8000/api/test',
      expect.objectContaining({
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer token',
          'X-Custom': 'value'
        }
      })
    );
  });

  it('handles FormData correctly', async () => {
    const mockData = { id: 1 };
    mockApiResponse(mockData);
    
    const formData = new FormData();
    formData.append('file', 'test');
    
    await fetchApi('/api/upload', {
      method: 'POST',
      body: formData
    });
    
    expect(fetch).toHaveBeenCalledWith(
      'http://localhost:8000/api/upload',
      expect.objectContaining({
        method: 'POST',
        body: formData,
        headers: expect.not.objectContaining({
          'Content-Type': 'application/json'
        })
      })
    );
  });

  it('handles POST requests', async () => {
    const mockData = { id: 1 };
    const postData = { title: 'Test' };
    mockApiResponse(mockData);
    
    await fetchApi('/api/create', {
      method: 'POST',
      body: JSON.stringify(postData)
    });
    
    expect(fetch).toHaveBeenCalledWith(
      'http://localhost:8000/api/create',
      expect.objectContaining({
        method: 'POST',
        body: JSON.stringify(postData),
        headers: {
          'Content-Type': 'application/json'
        }
      })
    );
  });

  it('handles empty error responses', async () => {
    (fetch as any).mockResolvedValueOnce({
      ok: false,
      json: async () => {
        throw new Error('Invalid JSON');
      },
      status: 500
    });
    
    await expect(fetchApi('/api/error')).rejects.toThrow('Error desconocido del servidor');
  });

  it('uses correct API base URL', async () => {
    const mockData = { id: 1 };
    mockApiResponse(mockData);
    
    await fetchApi('/api/test');
    
    expect(fetch).toHaveBeenCalledWith(
      'http://localhost:8000/api/test',
      expect.any(Object)
    );
  });
});
