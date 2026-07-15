import { describe, it, expect } from 'vitest';
import type {
  TechItem,
  RecruiterProject,
  ServerSpec,
  RecruiterData,
} from '$lib/recruiter-data';
import {
  recruiterData,
  RECRUITER_TECH_STACK,
  RECRUITER_PROJECTS,
  RECRUITER_SERVERS,
  RECRUITER_METRICS,
} from '$lib/recruiter-data';

describe('RecruiterData Types', () => {
  it('accepts valid TechItem', () => {
    const item: TechItem = {
      name: 'Python',
      category: 'Backend',
      icon: 'Code',
      description: 'Programming language',
    };
    expect(item.name).toBe('Python');
    expect(item.category).toBe('Backend');
  });

  it('accepts valid RecruiterProject', () => {
    const project: RecruiterProject = {
      title: 'AuthCore',
      description: 'Auth system',
      tags: ['Python', 'FastAPI'],
      github: 'https://github.com/test',
      type: 'personal',
    };
    expect(project.title).toBe('AuthCore');
    expect(project.github).toBeDefined();
  });

  it('accepts valid ServerSpec', () => {
    const server: ServerSpec = {
      name: 'Hetzner',
      provider: 'Hetzner',
      specs: 'CX22, 2 cores, 4GB RAM',
      services: ['Docker', 'Traefik'],
      os: 'Ubuntu 24.04',
    };
    expect(server.name).toBe('Hetzner');
  });

  it('accepts valid RecruiterData', () => {
    const data: RecruiterData = {
      name: 'Hernan Arango',
      role: 'Ingeniero de Sistemas',
      location: 'Aviles, Asturias',
      email: 'test@test.com',
      github: 'https://github.com/test',
      linkedin: 'https://linkedin.com/in/test',
      summary: 'Test summary',
      stack: [],
      projects: [],
      servers: [],
      metrics: [],
    };
    expect(data.name).toBe('Hernan Arango');
  });
});

describe('RecruiterData Content', () => {
  it('exports recruiterData with correct name', () => {
    expect(recruiterData.name).toBe('Hernan Arango Cortes');
    expect(recruiterData.role).toContain('Ingeniero');
    expect(recruiterData.location).toContain('Aviles');
  });

  it('has contact links', () => {
    expect(recruiterData.github).toContain('github.com');
    expect(recruiterData.linkedin).toContain('linkedin.com');
    expect(recruiterData.email).toContain('@');
  });

  it('has a non-empty summary', () => {
    expect(recruiterData.summary.length).toBeGreaterThan(50);
  });
});

describe('RECRUITER_TECH_STACK', () => {
  it('has stack items with all required fields', () => {
    RECRUITER_TECH_STACK.forEach((item) => {
      expect(item.name).toBeTruthy();
      expect(item.category).toBeTruthy();
      expect(item.icon).toBeTruthy();
      expect(item.description).toBeTruthy();
    });
  });

  it('includes key backend technologies', () => {
    const names = RECRUITER_TECH_STACK.map((t) => t.name);
    expect(names).toContain('Python');
    expect(names).toContain('Go');
    expect(names).toContain('Docker');
  });

  it('has multiple categories', () => {
    const categories = new Set(RECRUITER_TECH_STACK.map((t) => t.category));
    expect(categories.size).toBeGreaterThanOrEqual(3);
  });
});

describe('RECRUITER_PROJECTS', () => {
  it('has projects with required fields', () => {
    RECRUITER_PROJECTS.forEach((p) => {
      expect(p.title).toBeTruthy();
      expect(p.description).toBeTruthy();
      expect(p.tags.length).toBeGreaterThan(0);
    });
  });

  it('includes key projects', () => {
    const titles = RECRUITER_PROJECTS.map((p) => p.title);
    expect(titles).toContain('AuthCore');
    expect(titles).toContain('Portfolio elRincondeHarco');
  });
});

describe('RECRUITER_SERVERS', () => {
  it('has server entries with specs', () => {
    RECRUITER_SERVERS.forEach((s) => {
      expect(s.name).toBeTruthy();
      expect(s.specs).toBeTruthy();
      expect(s.services.length).toBeGreaterThan(0);
    });
  });

  it('includes Hetzner and Netcup', () => {
    const names = RECRUITER_SERVERS.map((s) => s.name);
    expect(names).toContain('Hetzner');
  });
});

describe('RECRUITER_METRICS', () => {
  it('has metics with label and value', () => {
    RECRUITER_METRICS.forEach((m) => {
      expect(m.label).toBeTruthy();
      expect(m.value).toBeTruthy();
    });
  });

  it('includes key metrics', () => {
    const labels = RECRUITER_METRICS.map((m) => m.label);
    expect(labels).toContain('Años de experiencia');
  });
});
