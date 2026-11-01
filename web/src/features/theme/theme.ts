export type Theme = 'dark' | 'light';
export const THEME_KEY = 'nhipdung:theme';
export const parseTheme = (raw: unknown): Theme => (raw === 'light' ? 'light' : 'dark');
