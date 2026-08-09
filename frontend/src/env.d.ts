/// <reference types="astro/client" />

declare namespace App {
  interface Locals {
    user?: {
      id: string;
      username: string;
      role: string;
      [key: string]: any;
    };
  }
}
