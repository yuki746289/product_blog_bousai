# Created: 2026-09-09 09:12 JST
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

EXPECTED = {
    'B001': 'ai_b001_hazardmap_flow_20260909.webp',
    'B003': 'ai_b003_toilet_difference_20260909.webp',
    'B004': 'ai_b004_outage_five_roles_20260909.webp',
    'B012': 'ai_b012_sandbag_placement_20260909.webp',
    'B015': 'ai_b015_damage_photo_steps_20260909.webp',
    'B021': 'ai_b021_typhoon_timeline_20260909.webp',
    'B022': 'ai_b022_apartment_flood_points_20260909.webp',
    'B028': 'ai_b028_wh_w_guide_20260909.webp',
    'B041': 'ai_b041_tsunami_evacuation_20260909.webp',
}


class ArticleDiagramTests(unittest.TestCase):
    def test_shared_head_loads_article_diagram_script(self):
        partial = (ROOT / 'templates/partials/google_analytics.html').read_text(encoding='utf-8')
        self.assertIn('/assets/article_diagrams.js', partial)

    def test_diagram_script_contains_all_article_routes_and_accessibility_text(self):
        script = (ROOT / 'preview/assets/article_diagrams.js').read_text(encoding='utf-8')
        for article_id, filename in EXPECTED.items():
            with self.subTest(article_id=article_id):
                self.assertIn("id: '%s'" % article_id, script)
                self.assertIn(filename, script)
        self.assertIn('image.alt = config.alt', script)
        self.assertIn('figcaption', script)
        self.assertIn('data-article-diagram', script)

    def test_all_diagram_assets_exist_and_are_reasonably_sized(self):
        image_dir = ROOT / 'preview/assets/images'
        for article_id, filename in EXPECTED.items():
            with self.subTest(article_id=article_id):
                path = image_dir / filename
                self.assertTrue(path.is_file(), filename)
                self.assertGreater(path.stat().st_size, 50_000, filename)
                self.assertLess(path.stat().st_size, 500_000, filename)


if __name__ == '__main__':
    unittest.main()
