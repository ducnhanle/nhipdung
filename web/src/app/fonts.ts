import localFont from 'next/font/local';
import type { AppLocale } from '@/i18n/routing';

// Latin WOFF2 subsets of the engine's licensed fonts (see ./fonts/README.md). Each loader exposes a --font-*-face
// variable that design-system/tokens/typography.css maps onto the font tokens; only Figtree is preloaded.
const figtree = localFont({ src: './fonts/figtree-latin.woff2', weight: '300 900', variable: '--font-figtree-face', display: 'swap' });
const anton = localFont({ src: './fonts/anton-latin.woff2', weight: '400', variable: '--font-anton-face', display: 'swap', preload: false });
const montserrat = localFont({ src: './fonts/montserrat-latin.woff2', weight: '100 900', variable: '--font-montserrat-face', display: 'swap', preload: false });
const caveat = localFont({ src: './fonts/caveat-latin.woff2', weight: '400 700', variable: '--font-caveat-face', display: 'swap', preload: false });
const marker = localFont({ src: './fonts/permanent-marker-latin.woff2', weight: '400', variable: '--font-marker-face', display: 'swap', preload: false });

// Vietnamese pages fill the same variables with Latin + Vietnamese subsets. Figtree, Caveat, and Permanent Marker draw
// no Vietnamese letters, so their roles go to the engine's extended-coverage fonts: Plus Jakarta Sans, Sriracha, and
// Sedgwick Ave Display. Anton and Montserrat keep their design with the Vietnamese glyphs they already have.
const sansVi = localFont({ src: './fonts/plus-jakarta-sans-latin-vietnamese.woff2', weight: '200 800', variable: '--font-figtree-face', display: 'swap', preload: false });
const antonVi = localFont({ src: './fonts/anton-latin-vietnamese.woff2', weight: '400', variable: '--font-anton-face', display: 'swap', preload: false });
const montserratVi = localFont({ src: './fonts/montserrat-latin-vietnamese.woff2', weight: '100 900', variable: '--font-montserrat-face', display: 'swap', preload: false });
const handVi = localFont({ src: './fonts/sriracha-latin-vietnamese.woff2', weight: '400', variable: '--font-caveat-face', display: 'swap', preload: false });
const markerVi = localFont({ src: './fonts/sedgwick-ave-display-latin-vietnamese.woff2', weight: '400', variable: '--font-marker-face', display: 'swap', preload: false });

const join = (fonts: Array<{ variable: string }>) => fonts.map(font => font.variable).join(' ');

/** Class names that define every font variable; put them on `<html>`. */
export const fontVariables = join([figtree, anton, montserrat, caveat, marker]);
const vietnameseVariables = join([sansVi, antonVi, montserratVi, handVi, markerVi]);

/** The font variables for a locale: Vietnamese needs fonts that draw its letters. */
export const fontVariablesFor = (locale: AppLocale): string => (locale === 'vi' ? vietnameseVariables : fontVariables);
