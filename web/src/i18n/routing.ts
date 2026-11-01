import { defineRouting } from 'next-intl/routing';

export const routing = defineRouting({
  locales: ['en-US', 'pt-BR', 'es', 'vi'],
  defaultLocale: 'en-US',
  // Short, lowercase URL prefixes; the [locale] segment still receives the full locale code.
  localePrefix: { mode: 'always', prefixes: { 'en-US': '/en', 'pt-BR': '/pt-br', es: '/es', vi: '/vi' } },
  localeDetection: true,
  // next-intl defaults to a session cookie; a manual language choice should survive closing the browser.
  localeCookie: { maxAge: 60 * 60 * 24 * 365 },
  pathnames: {
    '/': '/',
    '/create': { 'en-US': '/create', 'pt-BR': '/criar', es: '/crear', vi: '/tao-yeu-cau' },
    '/catalog': { 'en-US': '/catalog', 'pt-BR': '/catalogo', es: '/catalogo', vi: '/danh-muc' },
    '/examples': { 'en-US': '/examples', 'pt-BR': '/exemplos', es: '/ejemplos', vi: '/vi-du' },
    '/install': { 'en-US': '/install', 'pt-BR': '/instalacao', es: '/instalacion', vi: '/cai-dat' },
  },
});

export type AppLocale = (typeof routing.locales)[number];
export type AppPathname = keyof typeof routing.pathnames;
