// @ts-check
import { defineConfig, fontProviders } from "astro/config";

import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  vite: {
    plugins: [tailwindcss()]
  },
  fonts: [{
    provider: fontProviders.fontsource(),
    name: "Source Sans 3",
    cssVariable: "--font-source-sans",
    weights: ["200 900"],
  }],
});
