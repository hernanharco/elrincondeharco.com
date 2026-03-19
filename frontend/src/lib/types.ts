export interface HeroResponse {
  id: number;
  title: string;
  subtitle: string;
  description: string;
  background_image: string | null;
  contact_button_text: string;
  cv_button_text: string;
  image_url: string | null;
}

export interface AboutResponse {
  id: number;
  title: string;
  description: string;
  image_url: string | null;
  location: string;
  years_experience: string;
  team_name: string;
  leadership_title: string;
  leadership_desc: string;
  experience_title: string;
  experience_desc: string;
}

export interface StackResponse {
  id: number;
  name: string;
  category: string;
  icon: string;
  description: string;
  color: string;
  border: string;
  glow: string;
}

export interface ProjectResponse {
  id: number;
  title: string;
  description: string;
  image_url: string | null;
  tags: string[];
  icon_name: string;
  color: string;
  demo_url: string | null;
  github_url: string | null;
}

export interface PassionResponse {
  id: number;
  title: string;
  description: string;
  image_url: string | null;
  family_title: string;
  family_desc: string;
  games_title: string;
  games_desc: string;
  coding_title: string;
  coding_desc: string;
}

export interface FooterResponse {
  id: number;
  name: string;
  description: string;
  location: string;
  email: string;
  github_url: string | null;
  linkedin_url: string | null;
  twitter_url: string | null;
  quick_links: { text: string; href: string }[];
}
