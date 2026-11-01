"""Vietnamese text keeps every letter: font fallbacks, scene companions, and template widths stay consistent."""
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / 'skills/nhipdung/engine'
VISUALS = ROOT / 'skills/nhipdung/visuals'
TEMPLATE = ENGINE / 'project-template'
VIETNAMESE = [chr(c) for c in range(0x1EA0, 0x1EFA)] + list('ăâđêôơưĂÂĐÊÔƠƯ')
FACE = re.compile(r'@font-face\{font-family:"?([^";]+)"?;src:url\("([^"]+)"\)[^;]*;font-weight:([^;]+);font-display:block(?:;unicode-range:([^}]+))?\}')


def faces(text):
    return [dict(zip(('family', 'src', 'weight', 'range'), match)) for match in FACE.findall(text)]


def covers(unicode_range, char):
    for part in unicode_range.split(','):
        low, _, high = part.strip()[2:].partition('-')
        if int(low, 16) <= ord(char) <= int(high or low, 16):
            return True
    return False


class FontManifestTests(unittest.TestCase):
    def test_fallbacks_point_to_bundled_licensed_fonts(self):
        manifest = json.loads((ENGINE / 'assets/fonts/fonts.json').read_text(encoding='utf-8'))
        fallbacks = {key: entry['fallback'] for key, entry in manifest.items() if 'fallback' in entry}
        self.assertEqual(set(fallbacks), {'text_bold', 'text_semibold', 'marker', 'hand'})
        for key, fallback in fallbacks.items():
            with self.subTest(key=key):
                self.assertIn(fallback, manifest)
                self.assertNotIn('fallback', manifest[fallback])
                self.assertTrue((ENGINE / 'assets/fonts' / manifest[fallback]['file']).is_file())
                self.assertTrue((ENGINE / 'assets/fonts' / manifest[fallback]['license']).is_file())

    def test_new_fonts_are_listed_in_the_notices(self):
        notices = (ENGINE / 'THIRD_PARTY_NOTICES.md').read_text(encoding='utf-8')
        for name in ('Plus Jakarta Sans', 'Sriracha', 'Sedgwick Ave Display', 'Inter', 'Sora', 'Playfair Display'):
            self.assertIn(name, notices)


class SceneCompanionTests(unittest.TestCase):
    def test_every_scene_face_without_vietnamese_has_a_matching_companion(self):
        # Chrome only combines unicode-range faces whose weight descriptors are identical.
        primaries = {'Inter': 'assets/visuals/fonts/inter-var-latin.woff2', 'Caveat': 'assets/fonts/Caveat.ttf',
                     'Sora': 'assets/visuals/fonts/Sora.ttf', 'SoraV': 'assets/visuals/fonts/Sora.ttf'}
        companions = {'Inter': 'assets/visuals/fonts/inter-var-vietnamese.woff2',
                      'Caveat': 'assets/fonts/Sriracha-vietnamese.ttf',
                      'Sora': 'assets/visuals/fonts/plusjakartasans-vietnamese.woff2',
                      'SoraV': 'assets/visuals/fonts/plusjakartasans-vietnamese.woff2'}
        checked = 0
        for path in sorted((VISUALS / 'scenes').glob('*.html')):
            declared = faces(path.read_text(encoding='utf-8'))
            for family, primary in primaries.items():
                base = [f for f in declared if f['family'] == family and f['src'] == primary]
                if not base:
                    continue
                checked += 1
                with self.subTest(scene=path.name, family=family):
                    companion = [f for f in declared if f['family'] == family and f['src'] == companions[family]]
                    self.assertEqual(len(companion), 1)
                    self.assertEqual(companion[0]['weight'], base[0]['weight'])
                    self.assertTrue(all(covers(companion[0]['range'], ch) for ch in 'ạệờựơư'))
                    self.assertGreater(declared.index(companion[0]), declared.index(base[-1]))
        self.assertGreaterEqual(checked, 135 + 19 + 14)

    def test_companion_files_exist_where_projects_receive_them(self):
        self.assertTrue((VISUALS / 'assets/visuals/fonts/inter-var-vietnamese.woff2').is_file())
        self.assertTrue((VISUALS / 'assets/visuals/fonts/plusjakartasans-vietnamese.woff2').is_file())
        self.assertTrue((TEMPLATE / 'assets/fonts/Sriracha-vietnamese.ttf').is_file())
        for name in ('OFL-Inter.txt', 'OFL-PlusJakartaSans.txt', 'OFL-Sora.txt', 'OFL-PlayfairDisplay.txt'):
            self.assertTrue((VISUALS / 'assets/visuals/fonts' / name).is_file(), name)
        self.assertTrue((TEMPLATE / 'assets/fonts/OFL-Sriracha.txt').is_file())


class TemplateTests(unittest.TestCase):
    def test_template_declares_the_caveat_companion(self):
        build = (TEMPLATE / 'build.py').read_text(encoding='utf-8')
        line = re.search(r"^FONTS_CSS = '(.*)'$", build, re.M).group(1).replace('\\n', '\n')
        caveat = [f for f in faces(line.replace('font-family:Caveat', 'font-family:"Caveat"')) if f['family'] == 'Caveat']
        self.assertEqual([f['src'] for f in caveat], ['assets/fonts/Caveat.ttf', 'assets/fonts/Sriracha-vietnamese.ttf'])
        self.assertEqual(caveat[0]['weight'], caveat[1]['weight'])

    def test_widths_cover_vietnamese_letters(self):
        widths = json.loads((TEMPLATE / 'assets/fonts/widths.json').read_text(encoding='utf-8'))
        for family, entry in widths['fonts'].items():
            for weight, table in entry['weights'].items():
                with self.subTest(family=family, weight=weight):
                    self.assertFalse([ch for ch in VIETNAMESE if ch not in table])
                    self.assertGreater(table['Ệ'], table['n'] * 0.5)


if __name__ == '__main__':
    unittest.main()
