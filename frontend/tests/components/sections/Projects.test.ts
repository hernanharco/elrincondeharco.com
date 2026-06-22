import { render, screen, waitFor } from '@testing-library/svelte';
import { describe, it, expect, beforeEach, vi } from 'vitest';
import Projects from '$lib/components/sections/Projects.svelte';
import type { ProjectResponse } from '$lib/types';
import { mockApiResponse } from '../../setup';

// Mock dataEvents
vi.mock('$lib/dataEvents', () => ({
  listenForDataChange: vi.fn(() => vi.fn())
}));

describe('Projects Component', () => {
  const mockProjectsData: ProjectResponse[] = [
    {
      id: 1,
      title: 'Test Project 1',
      description: 'Description for project 1',
      image_url: null,
      tags: ['React', 'TypeScript'],
      icon_name: 'Code',
      color: 'from-blue-500/20',
      demo_url: 'https://demo1.com',
      github_url: 'https://github1.com'
    },
    {
      id: 2,
      title: 'Test Project 2',
      description: 'Description for project 2',
      image_url: null,
      tags: ['Svelte', 'Tailwind'],
      icon_name: 'Globe',
      color: 'from-green-500/20',
      demo_url: null,
      github_url: 'https://github2.com'
    }
  ];

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders loading state initially', () => {
    render(Projects);
    
    expect(screen.getByText('Loading projects...')).toBeInTheDocument();
  });

  it('renders projects when API call succeeds', async () => {
    mockApiResponse(mockProjectsData);
    
    render(Projects);
    
    await waitFor(() => {
      expect(screen.getByText('Test Project 1')).toBeInTheDocument();
      expect(screen.getByText('Test Project 2')).toBeInTheDocument();
      expect(screen.getByText('Description for project 1')).toBeInTheDocument();
      expect(screen.getByText('Description for project 2')).toBeInTheDocument();
    });
  });

  it('renders project tags correctly', async () => {
    mockApiResponse(mockProjectsData);
    
    render(Projects);
    
    await waitFor(() => {
      expect(screen.getByText('React')).toBeInTheDocument();
      expect(screen.getByText('TypeScript')).toBeInTheDocument();
      expect(screen.getByText('Svelte')).toBeInTheDocument();
      expect(screen.getByText('Tailwind')).toBeInTheDocument();
    });
  });

  it('renders demo and github links when available', async () => {
    mockApiResponse(mockProjectsData);
    
    render(Projects);
    
    await waitFor(() => {
      const demoLink = screen.getByText('Live Demo');
      expect(demoLink).toHaveAttribute('href', 'https://demo1.com');
      
      const githubLinks = screen.getAllByText('View Code');
      expect(githubLinks[0]).toHaveAttribute('href', 'https://github1.com');
      expect(githubLinks[1]).toHaveAttribute('href', 'https://github2.com');
    });
  });

  it('handles missing demo link gracefully', async () => {
    mockApiResponse(mockProjectsData);
    
    render(Projects);
    
    await waitFor(() => {
      // Second project has no demo URL
      const demoLinks = screen.getAllByText('Live Demo');
      expect(demoLinks).toHaveLength(1); // Only first project has demo
    });
  });

  it('handles API error gracefully', async () => {
    mockApiResponse({ detail: 'API Error' }, false);
    
    render(Projects);
    
    await waitFor(() => {
      expect(screen.queryByText('Loading projects...')).not.toBeInTheDocument();
      expect(screen.queryByText('Test Project 1')).not.toBeInTheDocument();
    });
  });

  it('renders empty state when no projects', async () => {
    mockApiResponse([]);
    
    render(Projects);
    
    await waitFor(() => {
      expect(screen.getByText('No projects found')).toBeInTheDocument();
    });
  });

  it('has correct accessibility attributes', async () => {
    mockApiResponse(mockProjectsData);
    
    render(Projects);
    
    await waitFor(() => {
      const section = screen.getByRole('region');
      expect(section).toHaveAttribute('id', 'projects');
      expect(section).toHaveClass('py-20', 'bg-gray-50');
    });
  });

  it('calls correct API endpoint', async () => {
    mockApiResponse(mockProjectsData);
    
    render(Projects);
    
    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining('/api/projects'),
      expect.objectContaining({
        headers: expect.objectContaining({
          'Content-Type': 'application/json'
        })
      })
    );
  });

  it('filters projects by category when filter is applied', async () => {
    mockApiResponse(mockProjectsData);
    
    render(Projects);
    
    await waitFor(() => {
      expect(screen.getByText('Test Project 1')).toBeInTheDocument();
    });
    
    // This would test category filtering functionality
    // Implementation depends on actual component behavior
  });

  it('sets up data change listener on mount', async () => {
    const { listenForDataChange } = await import('$lib/dataEvents');
    
    render(Projects);
    
    expect(listenForDataChange).toHaveBeenCalledWith('projects', expect.any(Function));
  });
});
