import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EXPECTED = {
    "article_b067.html": {
        "linear-rainband-overview.jpg",
        "unsafe-actions.jpg",
    },
    "article_b012.html": {"home-flooding.jpg"},
    "article_b009.html": {"flooded-road-car.jpg"},
    "article_b036.html": {"landslide.jpg"},
}


class DisasterIllustrationEmbeddingTests(unittest.TestCase):
    def test_all_generated_images_exist_as_real_assets(self):
        asset_dir = ROOT / "preview" / "assets" / "images" / "disaster"
        for names in EXPECTED.values():
            for name in names:
                path = asset_dir / name
                self.assertTrue(path.is_file(), f"missing generated image asset: {path}")
                self.assertGreater(path.stat().st_size, 20_000, f"image asset too small: {path}")

    def test_expected_pages_embed_actual_img_files(self):
        for page, names in EXPECTED.items():
            html = (ROOT / "preview" / page).read_text(encoding="utf-8")
            for name in names:
                self.assertIn(f'src="assets/images/disaster/{name}"', html, page)
            self.assertIn("article-generated-illustration", html, page)
            self.assertIn("AI生成による", html, page)

    def test_generated_images_have_accessibility_and_intrinsic_dimensions(self):
        for page in EXPECTED:
            html = (ROOT / "preview" / page).read_text(encoding="utf-8")
            self.assertIn('loading="lazy"', html, page)
            self.assertIn('decoding="async"', html, page)
            self.assertRegex(html, r'<img src="assets/images/disaster/[^"]+\.jpg" alt="[^"]+" width="\d+" height="\d+"')

    def test_car_and_home_depths_are_not_presented_as_safe_thresholds(self):
        car = (ROOT / "preview" / "article_b009.html").read_text(encoding="utf-8")
        home = (ROOT / "preview" / "article_b012.html").read_text(encoding="utf-8")
        self.assertIn("「ここまでなら走行できる」という安全基準ではありません", car)
        self.assertIn("冠水した道路には進入しないでください", car)
        self.assertIn("避難開始や安全を判断する境界ではありません", home)
        self.assertIn("ハザードマップ・キキクル・自治体の避難情報を優先", home)

    def test_b067_no_longer_uses_old_lr_scene_substitute(self):
        html = (ROOT / "preview" / "article_b067.html").read_text(encoding="utf-8")
        self.assertNotIn("article-inline-image lr-scene", html)
        self.assertNotIn("lr-scene--overview", html)
        self.assertNotIn("lr-scene--home", html)
        self.assertNotIn("lr-scene--car", html)
        self.assertNotIn("lr-scene--landslide", html)
        self.assertNotIn("lr-scene--unsafe", html)

    def test_generated_illustration_css_never_crops_the_diagram(self):
        css = (ROOT / "preview" / "bousai_common.css").read_text(encoding="utf-8")
        self.assertIn(".article-generated-illustration img", css)
        self.assertIn("max-height: none", css)
        self.assertIn("object-fit: contain", css)


if __name__ == "__main__":
    unittest.main()
