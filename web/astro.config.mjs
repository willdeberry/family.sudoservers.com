// @ts-check
import { defineConfig } from 'astro/config';
import node from '@astrojs/node';
import tailwindcss from '@tailwindcss/vite';

// Server mode with per-page prerender. The tree viewer (index.astro)
// opts into prerender:true so it ships as a static HTML file; the
// /api/submit endpoint runs on the Node server (Google ID-token verify
// + GitHub issue creation). Standalone Node listens on 127.0.0.1:4321
// and is proxied by nginx — see deploy/family.sudoservers.com.conf.
export default defineConfig({
  site: 'https://family.sudoservers.com',
  output: 'server',
  adapter: node({ mode: 'standalone' }),

  build: {
    assets: '_assets',
  },

  vite: {
    plugins: [tailwindcss()],
  },
});
