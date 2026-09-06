# Created: 2026-09-03
import unittest

from scripts.localize_commons_images import (
    add_image_attributes,
    add_responsive_attributes,
    commons_description_url,
    ensure_source_link,
    is_commons_source,
    is_eligible_figure,
    stable_asset_name,
)


class CommonsImageLocalizationTests(unittest.TestCase):
    def test_special_redirect_description_url(self):
        source = (
            "https://commons.wikimedia.org/wiki/Special:Redirect/file/"
            "Earthquake%20Kit%20in%20Japan%202008.jpg?width=960"
        )
        self.assertEqual(
            "https://commons.wikimedia.org/wiki/File:Earthquake%20Kit%20in%20Japan%202008.jpg",
            commons_description_url(source),
        )

    def test_commons_source_detection_for_card_images(self):
        self.assertTrue(
            is_commons_source(
                "https://commons.wikimedia.org/wiki/Special:Redirect/file/Test.jpg?width=640"
            )
        )
        self.assertTrue(
            is_commons_source(
                "https://upload.wikimedia.org/wikipedia/commons/thumb/a/aa/Test.jpg/640px-Test.jpg"
            )
        )
        self.assertFalse(
            is_commons_source("https://example.com/product.jpg")
        )

    def test_only_attributed_article_figures_are_eligible(self):
        attrs = ' class="article-feature-image"'
        body = (
            '<img src="https://commons.wikimedia.org/wiki/Special:Redirect/file/Test.jpg?width=960" '
            'alt="test" loading="eager">'
            "<figcaption>Photo / Wikimedia Commons (CC BY 4.0)</figcaption>"
        )
        self.assertTrue(is_eligible_figure(attrs, body))
        self.assertFalse(is_eligible_figure(' class="card-thumb"', body))
        self.assertFalse(is_eligible_figure(attrs, body.replace("Wikimedia Commons", "External source")))

    def test_image_attributes_reduce_layout_shift_and_prioritize_feature(self):
        tag = (
            '<img src="assets/images/commons/example.webp" '
            'alt="test" loading="eager">'
        )
        updated = add_image_attributes(tag, 960, 720, feature=True)
        self.assertIn('width="960"', updated)
        self.assertIn('height="720"', updated)
        self.assertIn('decoding="async"', updated)
        self.assertIn('fetchpriority="high"', updated)

    def test_responsive_srcset_is_added_for_mobile_variant(self):
        tag = '<img src="../assets/images/commons/full.webp" alt="test" width="960" height="960">'
        updated = add_responsive_attributes(
            tag,
            "../assets/images/commons/mobile.webp",
            720,
            "../assets/images/commons/full.webp",
            960,
        )
        self.assertIn('srcset="../assets/images/commons/mobile.webp 720w, ../assets/images/commons/full.webp 960w"', updated)
        self.assertIn('sizes="(max-width: 760px) calc(100vw - 32px), 900px"', updated)

    def test_source_link_is_added_when_missing(self):
        body = (
            '<img src="https://commons.wikimedia.org/wiki/Special:Redirect/file/Test.jpg?width=960" '
            'alt="test">'
            "<figcaption>Photo / Wikimedia Commons (CC BY 4.0)</figcaption>"
        )
        updated = ensure_source_link(
            body,
            "https://commons.wikimedia.org/wiki/Special:Redirect/file/Test.jpg?width=960",
        )
        self.assertIn("Wikimedia Commonsの元画像", updated)
        self.assertIn("https://commons.wikimedia.org/wiki/File:Test.jpg", updated)

    def test_asset_name_is_stable_and_webp(self):
        source = "https://commons.wikimedia.org/wiki/Special:Redirect/file/Test.jpg?width=960"
        self.assertEqual(stable_asset_name(source), stable_asset_name(source))
        self.assertTrue(stable_asset_name(source).endswith(".webp"))


if __name__ == "__main__":
    unittest.main()
