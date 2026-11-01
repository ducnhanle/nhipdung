import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('package', ROOT / 'scripts/package.py')
package = importlib.util.module_from_spec(spec)
spec.loader.exec_module(package)


class PackageTests(unittest.TestCase):
    def test_plugin_release_metadata_matches_the_portable_skill(self):
        version = (ROOT / 'skills/nhipdung/VERSION').read_text().strip()
        for name in ('.codex-plugin/plugin.json', '.claude-plugin/plugin.json'):
            self.assertEqual(json.loads((ROOT / name).read_text())['version'], version, name)
        marketplace = json.loads((ROOT / '.claude-plugin/marketplace.json').read_text())
        self.assertEqual(marketplace['plugins'][0]['version'], version)

    def test_packages_reject_symlinked_source_roots(self):
        with tempfile.TemporaryDirectory(prefix='nhipdung package roots ') as temporary:
            base = Path(temporary)
            root, outside = base / 'project', base / 'private'
            root.mkdir()
            (outside / 'nhipdung').mkdir(parents=True)
            (outside / 'nhipdung/VERSION').write_text('1.0.0')
            (outside / 'private-notes.txt').write_text('Private content must stay outside the package')
            (root / 'skills').symlink_to(outside, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, 'symlink'):
                package.build(root, root / 'dist', 'plugin')
            self.assertFalse(list((root / 'dist').glob('*.zip')))

    def test_plugin_rejects_symlinked_readme_art(self):
        with tempfile.TemporaryDirectory(prefix='nhipdung readme package ') as temporary:
            root = Path(temporary) / 'project'
            source = root / 'skills/nhipdung'
            source.mkdir(parents=True)
            (source / 'VERSION').write_text('1.0.0')
            outside = Path(temporary) / 'private'
            outside.mkdir()
            (outside / 'note.txt').write_text('Must not enter the public package')
            assets = root / 'docs/assets'
            assets.mkdir(parents=True)
            (assets / 'readme').symlink_to(outside, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, 'symlink'):
                package.build(root, root / 'dist', 'plugin')
            self.assertFalse(list((root / 'dist').glob('*.zip')))

    def test_site_archives_are_no_longer_built(self):
        with tempfile.TemporaryDirectory(prefix='nhipdung package kinds ') as temp:
            root = Path(temp)
            (root / 'skills/nhipdung').mkdir(parents=True)
            (root / 'skills/nhipdung/VERSION').write_text('1.0.0')
            with self.assertRaisesRegex(ValueError, 'plugin'):
                package.build(root, root / 'dist', 'site')

    def test_plugin_excludes_nested_secrets_and_development_artifacts(self):
        excluded = ['private.pem', 'private.key', 'private.p12', '.env', '.env.local',
                    'debug.log', 'venv/private.txt', '.venv/private.txt', '.pytest_cache/state',
                    '.ruff_cache/state', '__pycache__/module.pyc', 'module.pyo', '.DS_Store',
                    'node_modules/package/index.js', '.work/private.txt']
        with tempfile.TemporaryDirectory(prefix='nhipdung package exclusions ') as temp:
            root = Path(temp)
            source = root / 'skills/nhipdung'
            source.mkdir(parents=True)
            (source / 'VERSION').write_text('1.0.0')
            included = ['skills/nhipdung/SKILL.md', 'skills/nhipdung/engine/main.py', 'skills/nhipdung/.env.example',
                        '.codex-plugin/plugin.json', '.claude-plugin/plugin.json',
                        '.agents/plugins/marketplace.json', 'docs/assets/readme/hero.svg']
            rejected = [f'{folder}/nested/{name}' for folder in
                        ['skills/nhipdung', '.codex-plugin', '.claude-plugin', '.agents/plugins', 'docs/assets/readme']
                        for name in excluded]
            for name in included + rejected:
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text('fixture')
            with zipfile.ZipFile(package.build(root, root / 'dist', 'plugin')) as archive:
                self.assertEqual(set(archive.namelist()), {*included, 'skills/nhipdung/VERSION'})

    def test_plugin_package_contents_exclude_the_web_app_and_local_secrets(self):
        with tempfile.TemporaryDirectory(prefix='nhipdung package ') as temp:
            root = Path(temp)
            for name in ['web/package.json', 'web/src/app/[locale]/page.tsx', 'web/messages/en-US.json', 'web/.env', 'web/.next/server.js',
                         'skills/nhipdung/SKILL.md', 'skills/nhipdung/VERSION',
                         'skills/nhipdung/engine/.env', 'skills/nhipdung/engine/.venv/private',
                         'skills/nhipdung/old-prompts.pdf', 'skills/nhipdung/clip.MP4',
                         'skills/nhipdung/visuals/clip.webm', 'skills/nhipdung/visuals/still.png',
                         '.codex-plugin/plugin.json', '.claude-plugin/plugin.json',
                         'install.py', 'nhipdung.py', 'README.md', 'README.pt-BR.md', 'README.es.md', 'README.vi.md', 'LICENSE.md',
                         'PRODUCT.md', 'DESIGN.md', 'design-system/README.md', 'docs/architecture.md', 'docs/design.md', 'docs/setup.md',
                         'docs/installation.md', 'docs/archive/private.pdf',
                         'docs/assets/readme/hero.svg', 'docs/assets/readme/captions.gif',
                         'docs/assets/readme/.env', 'docs/assets/private.txt']:
                p = root / name
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text('1.0.0' if p.name == 'VERSION' else 'fixture')
            plugin = package.build(root, root / 'dist', 'plugin')
            with zipfile.ZipFile(plugin) as archive:
                self.assertIn('skills/nhipdung/SKILL.md', archive.namelist())
                self.assertIn('install.py', archive.namelist())
                self.assertIn('DESIGN.md', archive.namelist())
                self.assertTrue(all(not p.startswith('design-system/') for p in archive.namelist()))
                self.assertIn('README.pt-BR.md', archive.namelist())
                self.assertIn('README.es.md', archive.namelist())
                self.assertIn('README.vi.md', archive.namelist())
                self.assertIn('PRODUCT.md', archive.namelist())
                self.assertIn('docs/architecture.md', archive.namelist())
                self.assertIn('docs/assets/readme/hero.svg', archive.namelist())
                self.assertIn('docs/assets/readme/captions.gif', archive.namelist())
                self.assertNotIn('docs/assets/private.txt', archive.namelist())
                self.assertTrue(all(not p.startswith('web/') for p in archive.namelist()))
                self.assertIn('skills/nhipdung/visuals/still.png', archive.namelist())
                self.assertIn('skills/nhipdung/clip.MP4', archive.namelist())
                self.assertIn('skills/nhipdung/visuals/clip.webm', archive.namelist())
                self.assertTrue(all(not p.lower().endswith('.pdf') for p in archive.namelist()))
                self.assertTrue(all('.env' not in p and '.venv' not in p and 'archive/' not in p for p in archive.namelist()))


if __name__ == '__main__':
    unittest.main()
