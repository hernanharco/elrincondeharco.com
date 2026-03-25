import { describe, it, expect } from 'vitest';
import type { 
  HeroResponse, 
  AboutResponse, 
  StackResponse, 
  ProjectResponse, 
  PassionResponse, 
  FooterResponse,
  SiteSettingsResponse,
  SocialNetworks 
} from '$lib/types';

describe('TypeScript Interfaces', () => {
  describe('HeroResponse', () => {
    it('accepts valid hero data', () => {
      const hero: HeroResponse = {
        id: 1,
        title: 'Test Hero',
        subtitle: 'Test Subtitle',
        description: 'Test Description',
        background_image: null,
        contact_button_text: 'Contact',
        cv_button_text: 'Download CV',
        image_url: null,
        cv_url: 'https://example.com/cv.pdf'
      };
      
      expect(hero.id).toBe(1);
      expect(hero.title).toBe('Test Hero');
    });
    
    it('allows null values for optional fields', () => {
      const hero: HeroResponse = {
        id: 1,
        title: 'Test Hero',
        subtitle: 'Test Subtitle',
        description: 'Test Description',
        background_image: null,
        contact_button_text: 'Contact',
        cv_button_text: 'Download CV',
        image_url: null,
        cv_url: null
      };
      
      expect(hero.cv_url).toBeNull();
    });
  });

  describe('ProjectResponse', () => {
    it('accepts valid project data', () => {
      const project: ProjectResponse = {
        id: 1,
        title: 'Test Project',
        description: 'Test Description',
        image_url: null,
        tags: ['React', 'TypeScript'],
        icon_name: 'Code',
        color: 'from-blue-500/20',
        demo_url: 'https://demo.com',
        github_url: 'https://github.com'
      };
      
      expect(project.tags).toHaveLength(2);
      expect(project.tags[0]).toBe('React');
    });
    
    it('allows empty tags array', () => {
      const project: ProjectResponse = {
        id: 1,
        title: 'Test Project',
        description: 'Test Description',
        image_url: null,
        tags: [],
        icon_name: 'Code',
        color: 'from-blue-500/20',
        demo_url: null,
        github_url: null
      };
      
      expect(project.tags).toHaveLength(0);
    });
  });

  describe('StackResponse', () => {
    it('accepts valid stack data', () => {
      const stack: StackResponse = {
        id: 1,
        name: 'React',
        category: 'Frontend',
        icon: 'Globe',
        description: 'JavaScript library',
        color: 'text-cyan-500',
        border: 'group-hover:border-cyan-500/50',
        glow: 'group-hover:shadow-[0_0_30px_-5px_rgba(6,182,212,0.3)]'
      };
      
      expect(stack.category).toBe('Frontend');
      expect(stack.name).toBe('React');
    });
  });

  describe('SocialNetworks', () => {
    it('accepts valid social networks data', () => {
      const socials: SocialNetworks = {
        github: 'https://github.com/user',
        linkedin: 'https://linkedin.com/in/user',
        twitter: null
      };
      
      expect(socials.github).toBe('https://github.com/user');
      expect(socials.twitter).toBeNull();
    });
    
    it('allows all null values', () => {
      const socials: SocialNetworks = {
        github: null,
        linkedin: null,
        twitter: null
      };
      
      expect(socials.github).toBeNull();
      expect(socials.linkedin).toBeNull();
      expect(socials.twitter).toBeNull();
    });
  });

  describe('SiteSettingsResponse', () => {
    it('accepts valid site settings', () => {
      const settings: SiteSettingsResponse = {
        id: 1,
        brand_name: 'Test Brand',
        site_url: 'https://test.com',
        legal_name: 'Test Legal',
        slogan: 'Test Slogan',
        copyright_notice: '© 2024 Test',
        contact_email: 'test@example.com',
        social_networks: {
          github: 'https://github.com',
          linkedin: null,
          twitter: null
        },
        is_active: true
      };
      
      expect(settings.brand_name).toBe('Test Brand');
      expect(settings.is_active).toBe(true);
    });
    
    it('allows null social_networks', () => {
      const settings: SiteSettingsResponse = {
        id: 1,
        brand_name: 'Test Brand',
        site_url: 'https://test.com',
        legal_name: 'Test Legal',
        slogan: null,
        copyright_notice: '© 2024 Test',
        contact_email: 'test@example.com',
        social_networks: null,
        is_active: true
      };
      
      expect(settings.social_networks).toBeNull();
      expect(settings.slogan).toBeNull();
    });
  });

  describe('Type Validation', () => {
    it('validates URL patterns in interface types', () => {
      const project: ProjectResponse = {
        id: 1,
        title: 'Test',
        description: 'Test',
        image_url: 'https://example.com/image.jpg',
        tags: [],
        icon_name: 'Code',
        color: 'from-blue-500/20',
        demo_url: 'https://demo.com',
        github_url: 'https://github.com'
      };
      
      expect(project.image_url).toMatch(/^https?:\/\//);
      expect(project.demo_url).toMatch(/^https?:\/\//);
      expect(project.github_url).toMatch(/^https?:\/\//);
    });
    
    it('validates email format in site settings', () => {
      const settings: SiteSettingsResponse = {
        id: 1,
        brand_name: 'Test',
        site_url: 'https://test.com',
        legal_name: 'Test',
        slogan: null,
        copyright_notice: '© 2024',
        contact_email: 'test@example.com',
        social_networks: null,
        is_active: true
      };
      
      expect(settings.contact_email).toMatch(/@.*\./);
    });
  });
});
