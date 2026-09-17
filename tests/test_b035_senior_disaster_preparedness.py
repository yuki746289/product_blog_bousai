from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "content" / "articles" / "B035_senior_disaster_preparedness.md"
PREVIEW = ROOT / "preview" / "article_b035.html"


def source_text() -> str:
    return SOURCE.read_text(encoding="utf-8")


def preview_text() -> str:
    return PREVIEW.read_text(encoding="utf-8")


def test_source_keeps_medication_and_daily_function_boundaries():
    text = source_text()
    assert "自己判断で服用量を減らしたり中断したりしない" in text
    assert "本人以外も確認できる状態" in text
    assert "眼鏡・補聴器・入れ歯・杖" in text
    assert "本人が普段食べている形態" in text
    assert "高齢者だから全員おかゆ" in text


def test_level3_is_not_age_only_rule():
    text = source_text()
    assert "警戒レベル3" in text
    assert "高齢者等避難" in text
    assert "危険な場所" in text
    assert "避難を完了するまでに時間を要する" in text
    assert "年齢だけ" in text


def test_individual_evacuation_plan_does_not_guarantee_helper_arrival():
    text = source_text()
    assert "個別避難計画" in text
    assert "市町村の努力義務" in text
    assert "必ず到着できるとは限りません" in text
    assert "支援者と連絡がつかない場合" in text


def test_welfare_shelter_requires_local_confirmation():
    text = source_text()
    assert "福祉避難所" in text
    assert "高齢者なら行けば入れる場所" in text
    assert "直接避難" in text
    assert "市区町村" in text
    assert "受入対象" in text


def test_preview_contains_updated_decision_points_after_sync():
    html = preview_text()
    for phrase in (
        "警戒レベル3",
        "個別避難計画",
        "福祉避難所",
        "本人の生活機能と避難条件",
    ):
        assert phrase in html
