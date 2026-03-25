import { render, screen, waitFor } from '@testing-library/svelte';
import { describe, it, expect, beforeEach, vi } from 'vitest';
import Hero from '$lib/components/sections/Hero.svelte';
import type { HeroResponse } from '$lib/types';
import { mockApiResponse } from '../setup';

// Mock dataEvents
vi.mock('$lib/dataEvents', () => ({
  listenForDataChange: vi.fn(() => vi.fn())
}));

describe('Hero Component', () => {
  const mockHeroData: HeroResponse = {
    id: 1,
    title: 'Test Hero Title',
    subtitle: 'Test Subtitle',
    description: 'Test description for hero section',
    background_image: null,
    contact_button_text: 'Contact Me',
    cv_button_text: 'Download CV',
    image_url: null,
    cv_url: 'https://example.com/cv.pdf'
  };

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders loading state initially', () => {
    render(Hero);
    
    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });

  it('renders hero data when API call succeeds', async () => {
    mockApiResponse(mockHeroData);
    
    render(Hero);
    
    await waitFor(() => {
      expect(screen.getByText('Test Hero Title')).toBeInTheDocument();
      expect(screen.getByText('Test Subtitle')).toBeInTheDocument();
      expect(screen.getByText('Test description for hero section')).toBeInTheDocument();
    });
  });

  it('renders contact and CV buttons when data is loaded', async () => {
    mockApiResponse(mockHeroData);
    
    render(Hero);
    
    await waitFor(() => {
      expect(screen.getByText('Contact Me')).toBeInTheDocument();
      expect(screen.getByText('Download CV')).toBeInTheDocument();
    });
  });

  it('handles API error gracefully', async () => {
    mockApiResponse({ detail: 'API Error' }, false);
    
    render(Hero);
    
    await waitFor(() => {
      expect(screen.queryByText('Loading...')).not.toBeInTheDocument();
      expect(screen.queryByText('Test Hero Title')).not.toBeInTheDocument();
    });
  });

  it('processes Cloudinary URLs correctly for download', async () => {
    const heroWithCloudinary: HeroResponse = {
      ...mockHeroData,
      cv_url: 'https://res.cloudinary.com/test/upload/v123/file.pdf'
    };
    
    mockApiResponse(heroWithCloudinary);
    
    render(Hero);
    
    await waitFor(() => {
      const cvLink = screen.getByText('Download CV');
      expect(cvLink).toHaveAttribute('href', expect.stringContaining('fl_attachment'));
    });
  });

  it('handles null CV URL gracefully', async () => {
    const heroWithoutCV: HeroResponse = {
      ...mockHeroData,
      cv_url: null
    };
    
    mockApiResponse(heroWithoutCV);
    
    render(Hero);
    
    await waitFor(() => {
      const cvLink = screen.getByText('Download CV');
      expect(cvLink).toHaveAttribute('href', '#');
    });
  });

  it('has correct accessibility attributes', async () => {
    mockApiResponse(mockHeroData);
    
    render(Hero);
    
    await waitFor(() => {
      const section = screen.getByRole('region');
      expect(section).toHaveAttribute('id', 'inicio');
      expect(section).toHaveClass('relative', 'min-h-screen', 'flex', 'items-center', 'justify-center');
    });
  });

  it('calls API on mount', async () => {
    mockApiResponse(mockHeroData);
    
    render(Hero);
    
    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining('/api/v1/heroes/latest/'),
      expect.objectContaining({
        headers: expect.objectContaining({
          'Content-Type': 'application/json'
        })
      })
    );
  });

  it('handles array response from API', async () => {
    mockApiResponse([mockHeroData]);
    
    render(Hero);
    
    await waitFor(() => {
      expect(screen.getByText('Test Hero Title')).toBeInTheDocument();
    });
  });

  it('sets up data change listener on mount', async () => {
    const { listenForDataChange } = await import('$lib/dataEvents');
    
    render(Hero);
    
    expect(listenForDataChange).toHaveBeenCalledWith('hero', expect.any(Function));
  });
});
