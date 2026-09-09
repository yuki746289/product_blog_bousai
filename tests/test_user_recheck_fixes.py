# Created: 2026-09-09 14:58 JST
import unittest

from scripts.article_diagrams import DIAGRAMS, inject_article_diagram, inject_article_image_zoom
from scripts.sync_previews_from_markdown import EXTRA_SYNC_ARTICLE_IDS, SYNC_ARTICLE_IDS


class UserRecheckFixTests(unittest.TestCase):
    def test_missing_markdown_articles_are_now_synchronized(self):
        self.assertEqual({"B003", "B008", "B010"}, EXTRA_SYNC_ARTICLE_IDS)
        self.assertTrue(EXTRA_SYNC_ARTICLE_IDS.issubset(SYNC_ARTICLE_IDS))

    def test_article_images_receive_one_accessible_zoom_behavior(self):
        source = (
            '<html><head></head><body><main class="article-shell"><article>'
            '<figure class="article-feature-image"><img src="hero.jpg" alt="防災画像">'
            '<figcaption>説明</figcaption></figure></article></main></body></html>'
        )
        once = inject_article_image_zoom(source)
        twice = inject_article_image_zoom(once)
        self.assertEqual(once, twice)
        self.assertEqual(1, once.count("data-article-image-zoom-style"))
        self.assertEqual(1, once.count("data-article-image-zoom-script"))
        self.assertIn("article-image-zoom-dialog", once)
        self.assertIn("HTMLDialogElement", once)
        self.assertIn("window.open(src,'_blank','noopener')", once)
        self.assertIn("event.key==='Enter'||event.key===' '", once)
        self.assertIn(".article-inline-image img", once)
        self.assertIn(".article-explainer--image img", once)

    def test_product_card_image_alone_does_not_enable_zoom(self):
        source = (
            '<html><head></head><body><main class="article-shell">'
            '<div class="product-recommendation__image"><img src="product.jpg" alt="商品"></div>'
            '</main></body></html>'
        )
        self.assertEqual(source, inject_article_image_zoom(source))

    def test_inserted_diagram_is_zoomable_even_without_existing_article_image(self):
        output_path, spec = next(iter(DIAGRAMS.items()))
        source = (
            '<html><head></head><body><main class="article-shell"><article>'
            f'<h2>{spec["heading"]}</h2><p>本文</p></article></main></body></html>'
        )
        result = inject_article_diagram(source, output_path)
        self.assertIn(f'data-article-diagram="{spec["article_id"]}"', result)
        self.assertIn("data-article-image-zoom-script", result)
        self.assertIn("data-article-image-zoom-style", result)


if __name__ == "__main__":
    unittest.main()
