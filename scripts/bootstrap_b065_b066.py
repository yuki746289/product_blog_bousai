from __future__ import annotations

import re
from pathlib import Path

from bousai_blog.registry import load_registry
import sync_previews_core as core

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "content_registry.json"

ARTICLES = {
    "B065": {
        "description": "女性の防災で準備したい生理用品・下着・衛生用品、持ち出しと自宅備蓄の分け方、避難所でのプライバシーや安全面を整理します。",
        "title": "女性の防災は何を準備する？生理用品・衛生・避難所のプライバシー",
        "crumb": "女性の防災",
        "label": "防災入門 / 女性の防災",
        "official": "個人用品は必要な人・種類・量がそれぞれ異なります。避難所の物資や相談方法は自治体・施設の最新案内を確認してください。",
    },
    "B066": {
        "description": "認知症の人と家族向けに、災害前の避難準備、持ち物、本人情報の共有、避難所で伝えたいこと、福祉・介護の相談先を整理します。",
        "title": "認知症の人の防災｜避難前の準備・持ち物・避難所で伝えたいこと",
        "crumb": "認知症の人の防災",
        "label": "防災入門 / 認知症",
        "official": "認知症の人の医療・介護上の個別対応は、平時から関わる医療・介護職、自治体等の案内を優先してください。",
    },
}


def replace_once(text: str, pattern: str, replacement: str, *, flags: int = 0) -> str:
    updated, count = re.subn(pattern, replacement, text, count=1, flags=flags)
    if count != 1:
        raise RuntimeError(f"replacement count {count} for {pattern[:60]!r}")
    return updated


def create_shell(article_id: str, preview_path: Path) -> None:
    if preview_path.exists():
        return
    cfg = ARTICLES[article_id]
    html = (ROOT / "preview" / "article_b064.html").read_text(encoding="utf-8")
    html = replace_once(html, r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{cfg["description"]}">')
    html = replace_once(html, r'<title>.*?</title>', f'<title>{cfg["title"]}｜防災くらしガイド</title>', flags=re.DOTALL)
    html = replace_once(html, r'<div class="official-bar__inner">.*?</div>', f'<div class="official-bar__inner">{cfg["official"]}</div>', flags=re.DOTALL)
    html = replace_once(
        html,
        r'(<nav class="breadcrumb" aria-label="パンくずリスト"><a href="index\.html">トップ</a> &gt; <a href="category_guide\.html">防災入門</a> &gt; ).*?(</nav>)',
        rf'\1{cfg["crumb"]}\2',
        flags=re.DOTALL,
    )
    html = replace_once(html, r'<span class="label">防災入門 / 食物アレルギー</span>', f'<span class="label">{cfg["label"]}</span>')
    html = replace_once(html, r'<h1>.*?</h1>', f'<h1>{cfg["title"]}</h1>', flags=re.DOTALL)
    html = replace_once(html, r'<p class="article-lead">.*?</p>', '<p class="article-lead">本文正本から同期します。</p>', flags=re.DOTALL)
    html = replace_once(
        html,
        r'<div class="article-meta"><span>記事ID: B064</span><span>公的情報確認: 2026年9月12日</span><span>要安全確認</span></div>',
        f'<div class="article-meta"><span>記事ID: {article_id}</span><span>公的情報確認: 2026年9月12日</span><span>要安全確認</span></div>',
    )
    preview_path.write_text(html, encoding="utf-8")


def update_category() -> None:
    path = ROOT / "preview" / "category_guide.html"
    text = path.read_text(encoding="utf-8")
    if 'data-article-id="B065"' not in text:
        marker = '<a class="category-article-link" href="article_b062.html" data-article-id="B062"><span>妊婦・妊産婦の防災｜避難時の持ち物・母子健康手帳・健診をどう備える？</span></a>'
        addition = (
            marker
            + '<a class="category-article-link" href="article_b065.html" data-article-id="B065"><span>女性の防災は何を準備する？生理用品・衛生・避難所のプライバシー</span></a>'
            + '<a class="category-article-link" href="article_b066.html" data-article-id="B066"><span>認知症の人の防災｜避難前の準備・持ち物・避難所で伝えたいこと</span></a>'
        )
        if marker not in text:
            raise RuntimeError("B062 category marker not found")
        text = text.replace(marker, addition, 1)
        text = text.replace(
            'ペット・乳幼児・高齢者・常用薬・妊産婦など、家庭ごとに追加したい備えを整理します。',
            'ペット・乳幼児・高齢者・常用薬・妊産婦・女性の衛生・認知症など、家庭ごとに追加したい備えを整理します。',
            1,
        )
        path.write_text(text, encoding="utf-8")


def main() -> None:
    registry = load_registry(REGISTRY)
    aliases = core.preview_aliases(registry)
    by_id = {article["article_id"]: article for article in registry["articles"]}

    for article_id in ARTICLES:
        article = by_id[article_id]
        preview_path = ROOT / article["preview_path"]
        create_shell(article_id, preview_path)
        core.sync_generic(article, aliases)

    update_category()
    print("Generated B065/B066 previews and category links")


if __name__ == "__main__":
    main()
