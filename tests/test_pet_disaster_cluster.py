# Created: 2026-09-18
import unittest
from pathlib import Path

from bousai_blog.registry import load_registry
from scripts.audit_article_content_metrics import audit

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "content_registry.json"


class PetDisasterClusterTests(unittest.TestCase):
    def test_pet_articles_are_registered_under_b033(self):
        registry = load_registry(REGISTRY)
        by_id = {a["article_id"]: a for a in registry["articles"]}
        for article_id in ("B078", "B079", "B080", "B081"):
            self.assertIn(article_id, by_id)
            self.assertEqual("evacuation", by_id[article_id]["category"])
            self.assertEqual("B033", by_id[article_id]["parent_article_id"])
            self.assertEqual("READY_TO_PUBLISH", by_id[article_id]["status"])

    def test_pet_article_length_rules_pass(self):
        rows = {row.article_id: row for row in audit()}
        for article_id in ("B078", "B079", "B080", "B081"):
            self.assertEqual("PASS", rows[article_id].length_status, article_id)

    def test_shelter_article_distinguishes_accompanied_and_same_room_evacuation(self):
        text = (ROOT / "content/articles/B078_shelter_pet_evacuation.md").read_text(encoding="utf-8")
        self.assertIn("同じ室内で生活できるとは限りません", text)
        self.assertIn("災害時の実際の開設状況を再確認", text)
        self.assertIn("危険な場所へ戻らない", text)

    def test_vehicle_article_keeps_human_and_pet_risks_and_alternatives(self):
        text = (ROOT / "content/articles/B079_pet_vehicle_overnight.md").read_text(encoding="utf-8")
        self.assertIn("エコノミークラス症候群", text)
        self.assertIn("車中泊を選ぶ前に確認したい代替策", text)
        self.assertIn("ペット側でも「車内温度」を最優先", text)
        self.assertNotIn("何度までなら安全", text.replace("「何度までなら安全」という固定値は設けません", ""))

    def test_evacuation_category_links_pet_cluster_articles(self):
        html = (ROOT / "preview/category_evacuation.html").read_text(encoding="utf-8")
        for article_id in ("B033", "B078", "B079", "B080", "B081"):
            self.assertIn(f'data-article-id="{article_id}"', html)

    def test_dog_and_cat_articles_link_pet_goods_guide(self):
        for filename in ("B080_dog_disaster_preparedness.md", "B081_cat_disaster_preparedness.md"):
            text = (ROOT / "content/articles" / filename).read_text(encoding="utf-8")
            self.assertIn("(goods_pet_evacuation.html)", text, filename)

    def test_pet_goods_guide_keeps_transport_and_stay_roles_separate(self):
        html = (ROOT / "preview/goods_pet_evacuation.html").read_text(encoding="utf-8")
        self.assertIn("移動用", html)
        self.assertIn("滞在用", html)
        self.assertIn("B079MD6JMN", html)
        self.assertNotIn("amazon.co.jp/s?k=", html)
        self.assertIn("商品情報より", html)

    def test_pet_hub_links_all_cluster_articles(self):
        html = (ROOT / "preview/category_pet.html").read_text(encoding="utf-8")
        for article_id in ("B033", "B078", "B079", "B080", "B081"):
            self.assertIn(f'data-article-id="{article_id}"', html)

    def test_b033_summary_table_is_detailed_and_actionable(self):
        md = (ROOT / "content/articles/B033_pet_disaster_preparedness.md").read_text(encoding="utf-8")
        html = (ROOT / "preview/article_b033.html").read_text(encoding="utf-8")
        for wording in (
            "主に準備するもの",
            "ここまで確認する",
            "玄関・階段・避難経路まで実際に移動",
            "家族や第三者が短時間で確認",
            "飼養場所・ケージ条件・移動経路・第二候補",
        ):
            self.assertIn(wording, md)
            self.assertIn(wording, html)
        self.assertIn('class="preparedness-summary-table"', html)
        self.assertNotIn("平常時に確認すること", html)
        self.assertNotIn("災害時に困らないためのポイント", html)

    def test_saved_checklist_supports_persistence_progress_and_share(self):
        html = (ROOT / "preview/article_b033.html").read_text(encoding="utf-8")
        js = (ROOT / "preview/bousai_common.js").read_text(encoding="utf-8")
        css = (ROOT / "preview/bousai_common.css").read_text(encoding="utf-8")
        self.assertIn("この端末のブラウザに自動保存", html)
        for token in (
            "enhancePersistentChecklists",
            "window.localStorage",
            "navigator.share",
            "copyTextFallback",
            "未完了:",
            "checklist_share",
            "最終更新:",
        ):
            self.assertIn(token, js)
        self.assertIn(".interactive-checklist", css)
        self.assertIn(".checklist-tools", css)
        self.assertIn('type="checkbox"', html)
        self.assertIn('data-persistent-checklist="1"', html)
        self.assertIn("bousai-checklist:v2:", js)

    def test_b033_links_to_pet_hub_and_children(self):
        md = (ROOT / "content/articles/B033_pet_disaster_preparedness.md").read_text(encoding="utf-8")
        for target in (
            "/pet/index.html",
            "/pet/shelter-pet-evacuation.html",
            "/pet/pet-vehicle-overnight.html",
            "/pet/dog-disaster-preparedness.html",
            "/pet/cat-disaster-preparedness.html",
        ):
            self.assertIn(target, md)


if __name__ == "__main__":
    unittest.main()
