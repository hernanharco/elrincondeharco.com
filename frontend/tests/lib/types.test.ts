import { describe, it, expect } from 'vitest';
import type {
  HeroResponse,
  ProjectResponse,
  SiteSettingsResponse,
  SocialNetworks,
  ExperienceSectionResponse,
} from '$lib/types';
import {
  fallbackHero,
  fallbackProjects,
  fallbackSectors,
  fallbackSiteSettings,
  fallbackExperienceSection,
} from '$lib/fallback-data';

// ── Type Validation ─────────────────────────────────────────

describe('TypeScript Interfaces', () => {
  describe('HeroResponse', () => {
    it('accepts valid hero data with primary_button_text', () => {
      const hero: HeroResponse = {
        id: 1,
        title: 'Test',
        subtitle: 'Test Sub',
        description: 'Test Desc',
        background_image: null,
        primary_button_text: 'Ver mi rubro',
        contact_button_text: 'Contacto',
        cv_button_text: 'Descargar CV',
        image_url: null,
        cv_url: null,
      };
      expect(hero.primary_button_text).toBe('Ver mi rubro');
    });
  });

  describe('ProjectResponse', () => {
    it('accepts valid project with image_urls array', () => {
      const project: ProjectResponse = {
        id: 1,
        title: 'Test',
        description: 'Test',
        image_urls: ['https://img1.com', 'https://img2.com'],
        tags: ['React'],
        icon_name: 'Code',
        color: 'from-blue-500/20',
        demo_url: null,
        github_url: null,
      };
      expect(project.image_urls).toHaveLength(2);
      expect(Array.isArray(project.image_urls)).toBe(true);
    });

    it('allows empty image_urls', () => {
      const project: ProjectResponse = {
        id: 1,
        title: 'Test',
        description: 'Test',
        image_urls: [],
        tags: [],
        icon_name: 'Code',
        color: 'from-blue-500/20',
        demo_url: null,
        github_url: null,
      };
      expect(project.image_urls).toEqual([]);
    });
  });

  describe('SiteSettingsResponse', () => {
    it('accepts valid site settings with CTA fields', () => {
      const settings: SiteSettingsResponse = {
        id: 1,
        brand_name: 'Test',
        site_url: 'https://test.com',
        legal_name: 'Test',
        slogan: null,
        copyright_notice: '©',
        contact_email: 'test@test.com',
        social_networks: null,
        is_active: true,
        cta_title: 'Test <span>CTA</span>',
        cta_description: 'Test description',
        cta_features: ['Feature 1', 'Feature 2'],
        cta_primary_text: 'Contacto',
        cta_secondary_text: 'LinkedIn',
      };
      expect(settings.cta_title).toContain('<span>');
      expect(settings.cta_features).toHaveLength(2);
      expect(settings.cta_primary_text).toBe('Contacto');
    });

    it('allows null CTA fields', () => {
      const settings: SiteSettingsResponse = {
        id: 1,
        brand_name: 'Test',
        site_url: 'https://test.com',
        legal_name: 'Test',
        slogan: null,
        copyright_notice: '©',
        contact_email: 'test@test.com',
        social_networks: null,
        is_active: true,
        cta_title: null,
        cta_description: null,
        cta_features: null,
        cta_primary_text: null,
        cta_secondary_text: null,
      };
      expect(settings.cta_title).toBeNull();
      expect(settings.cta_features).toBeNull();
    });
  });

  describe('ExperienceSectionResponse', () => {
    it('accepts valid experience section data', () => {
      const exp: ExperienceSectionResponse = {
        id: 1,
        tagline: 'Experiencia',
        title: 'Title <span>HTML</span>',
        description: 'Description text',
      };
      expect(exp.tagline).toBe('Experiencia');
      expect(exp.title).toContain('<span>');
    });
  });
});

// ── Fallback Data Validation ────────────────────────────────

describe('Fallback Data', () => {
  describe('fallbackHero', () => {
    it('has all required fields', () => {
      expect(fallbackHero.title).toBeTruthy();
      expect(fallbackHero.subtitle).toContain('<span');
      expect(fallbackHero.description).toBeTruthy();
      expect(fallbackHero.primary_button_text).toBe('Ver mi rubro');
      expect(fallbackHero.contact_button_text).toBe('Contacto');
    });
  });

  describe('fallbackProjects', () => {
    it('has 7 projects including new prototypes', () => {
      expect(fallbackProjects.length).toBeGreaterThanOrEqual(7);
      const titles = fallbackProjects.map(p => p.title);
      expect(titles).toContain('Tapicería Moderna');
      expect(titles).toContain('Landing Page Barbería');
      expect(titles).toContain('Gestión Gastronómica Inteligente');
    });

    it('all projects have image_urls array', () => {
      fallbackProjects.forEach(p => {
        expect(Array.isArray(p.image_urls)).toBe(true);
      });
    });

    it('projects with images have them in image_urls', () => {
      const withImages = fallbackProjects.filter(p => p.image_urls.length > 0);
      expect(withImages.length).toBeGreaterThanOrEqual(3);
    });
  });

  describe('fallbackSectors', () => {
    it('has 8 sectors including new ones', () => {
      expect(fallbackSectors.length).toBe(8);
      const names = fallbackSectors.map(s => s.name);
      expect(names).toContain('Educación');
      expect(names).toContain('Comercio');
    });

    it('sectors with projects have non-empty project_ids', () => {
      const withProjects = fallbackSectors.filter(s => s.project_ids.length > 0);
      expect(withProjects.length).toBeGreaterThanOrEqual(6);
    });
  });

  describe('fallbackSiteSettings', () => {
    it('has CTA fields with default values', () => {
      expect(fallbackSiteSettings.cta_title).toContain('algo grande');
      expect(fallbackSiteSettings.cta_description).toBeTruthy();
      expect(fallbackSiteSettings.cta_features).toHaveLength(3);
      expect(fallbackSiteSettings.cta_features).toContain('Respuesta en 24h');
      expect(fallbackSiteSettings.cta_primary_text).toBe('Enviar Correo');
      expect(fallbackSiteSettings.cta_secondary_text).toBe('LinkedIn');
    });
  });

  describe('fallbackExperienceSection', () => {
    it('has valid header content', () => {
      expect(fallbackExperienceSection.tagline).toBe('Experiencia');
      expect(fallbackExperienceSection.title).toContain('rubro');
      expect(fallbackExperienceSection.description).toBeTruthy();
    });
  });
});
