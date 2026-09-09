# Created: 2026-09-09 14:58 JST
# Updated: 2026-09-09 15:10 JST
import unittest
from pathlib import Path

from scripts.article_diagrams import DIAGRAMS, inject_article_diagram, inject_article_image_zoom
from scripts.sync_previews_from_markdown import EXTRA_SYNC_ARTICLE_IDS, SYNC_ARTICLE_IDS

ROOT = Path(__file__).resolve().parents[1]


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

    def test_b008_intro_maps_the_main_decisions(self):
        text = (ROOT / "content/articles/B008_car_flood_submersion.md").read_text(encoding="utf-8")
        self.assertIn("①冠水路へ入らない判断", text)
        self.assertIn("③脱出用ハンマーと破砕できるガラス", text)
        self.assertIn("④水が引いた後にやってはいけないこと", text)
        self.assertIn("冠水を見つけた段階で停止・迂回できるなら、それが最優先", text)

    def test_b020_intro_contains_concrete_time_and_action_map(self):
        text = (ROOT / "content/articles/B020_home_heavy_rain_checklist.md").read_text(encoding="utf-8")
        self.assertIn("3〜7日前にハザードマップ・排水口・1階の家財を確認", text)
        self.assertIn("①浸水リスクの確認", text)
        self.assertIn("⑤当日の中止条件と避難判断", text)
        self.assertIn("家の対策が未完成でも、危険が高まったら中止する", text)

    def test_b034_has_contextual_internal_product_guides(self):
        text = (ROOT / "content/articles/B034_baby_disaster_stockpile.md").read_text(encoding="utf-8")
        self.assertIn("調乳用の水や、家族全体の保存水・非常食を追加する場合", text)
        self.assertIn("[水・非常食の選び方と商品紹介](goods_water_food.html)", text)
        self.assertIn("家族共通で使う衛生用品", text)
        self.assertIn("[携帯トイレ・衛生用品の商品例を見る](goods_toilet_hygiene.html)", text)
        self.assertIn("紙おむつや乳児専用品の選択はこの商品記事の対象外", text)


if __name__ == "__main__":
    unittest.main()
