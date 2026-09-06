# Created: 2026-09-03
import unittest

from scripts.update_realtime import (
    apply_warning_updates,
    parse_atom,
    parse_earthquake,
    parse_typhoon_update,
    parse_warning_json,
    process_extra,
    parse_warning_updates,
)


ATOM = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <title>震源・震度情報</title>
    <id>urn:test:1</id>
    <updated>2026-09-03T09:00:00+09:00</updated>
    <link href="https://example.test/quake.xml"/>
  </entry>
</feed>
"""

QUAKE = """<?xml version="1.0" encoding="UTF-8"?>
<Report xmlns="http://xml.kishou.go.jp/jmaxml1/">
  <Head xmlns="http://xml.kishou.go.jp/jmaxml1/informationBasis1/">
    <Title>震源・震度情報</Title>
    <ReportDateTime>2026-09-03T09:02:00+09:00</ReportDateTime>
    <TargetDateTime>2026-09-03T09:00:00+09:00</TargetDateTime>
    <EventID>20260903090000</EventID>
    <Headline><Text>最大震度３を観測しました。</Text></Headline>
  </Head>
  <Body xmlns="http://xml.kishou.go.jp/jmaxml1/body/seismology1/">
    <Earthquake>
      <Hypocenter><Area><Name>日向灘</Name></Area></Hypocenter>
      <Magnitude xmlns="http://xml.kishou.go.jp/jmaxml1/elementBasis1/">4.2</Magnitude>
    </Earthquake>
    <Intensity><Observation><MaxInt>3</MaxInt></Observation></Intensity>
  </Body>
</Report>
""".encode()

WARNING = """<?xml version="1.0" encoding="UTF-8"?>
<Report xmlns="http://xml.kishou.go.jp/jmaxml1/">
  <Head xmlns="http://xml.kishou.go.jp/jmaxml1/informationBasis1/">
    <Title>気象特別警報・警報・注意報</Title>
    <ReportDateTime>2026-09-03T09:05:00+09:00</ReportDateTime>
    <Headline>
      <Information type="気象警報・注意報（府県予報区等）">
        <Item>
          <Kind><Name>大雨警報</Name><Status>発表</Status></Kind>
          <Kind><Name>雷注意報</Name><Status>発表</Status></Kind>
          <Areas><Area><Name>佐賀県</Name></Area></Areas>
        </Item>
      </Information>
    </Headline>
  </Head>
</Report>
""".encode()

WARNING_CANCEL = WARNING.replace(b"<Status>\xe7\x99\xba\xe8\xa1\xa8</Status>", b"<Status>\xe8\xa7\xa3\xe9\x99\xa4</Status>", 1)

WARNING_MAP = """[
  {
    "reportDatetime": "2026-09-03T09:05:00+09:00",
    "warning": {
      "class10Items": [
        {
          "areaCode": "410010",
          "kinds": [
            {"code": "03", "status": "発表"},
            {"code": "14", "status": "発表"}
          ]
        }
      ]
    }
  }
]""".encode()

AREA_MAP = """{
  "class10s": {
    "410010": {"name": "佐賀県南部"}
  }
}""".encode()

TYPHOON_ACTIVE = """<?xml version="1.0" encoding="UTF-8"?>
<Report xmlns="http://xml.kishou.go.jp/jmaxml1/">
  <Head xmlns="http://xml.kishou.go.jp/jmaxml1/informationBasis1/">
    <Title>台風解析・予報情報（5日予報）（H30）</Title>
    <ReportDateTime>2026-09-03T09:10:00+09:00</ReportDateTime>
    <TargetDateTime>2026-09-03T09:00:00+09:00</TargetDateTime>
    <EventID>TY202623</EventID>
    <Headline><Text></Text></Headline>
  </Head>
</Report>
""".encode()

TYPHOON_END = """<?xml version="1.0" encoding="UTF-8"?>
<Report xmlns="http://xml.kishou.go.jp/jmaxml1/">
  <Head xmlns="http://xml.kishou.go.jp/jmaxml1/informationBasis1/">
    <Title>全般台風情報</Title>
    <ReportDateTime>2026-09-03T09:10:00+09:00</ReportDateTime>
    <TargetDateTime>2026-09-03T09:00:00+09:00</TargetDateTime>
    <EventID>TY202601</EventID>
    <Headline><Text>台風第1号は温帯低気圧に変わりました。</Text></Headline>
  </Head>
</Report>
""".encode()


class RealtimeJmaTests(unittest.TestCase):
    def test_atom_feed_entry(self):
        entries = parse_atom(ATOM)
        self.assertEqual(1, len(entries))
        self.assertEqual("震源・震度情報", entries[0]["title"])
        self.assertEqual("https://example.test/quake.xml", entries[0]["link"])

    def test_earthquake_summary(self):
        result = parse_earthquake(QUAKE)
        self.assertEqual("日向灘", result["area"])
        self.assertEqual("4.2", result["magnitude"])
        self.assertEqual("3", result["max_intensity"])
        self.assertEqual("2026-09-03T09:00:00+09:00", result["time"])

    def test_warning_filters_out_advisories(self):
        updates = parse_warning_updates(WARNING)
        self.assertEqual(1, len(updates))
        self.assertEqual("佐賀県", updates[0]["area"])
        self.assertEqual("大雨警報", updates[0]["kind"])

    def test_warning_json_keeps_only_warning_codes(self):
        state = parse_warning_json(WARNING_MAP, AREA_MAP)
        self.assertEqual(1, len(state))
        item = next(iter(state.values()))
        self.assertEqual("佐賀県南部", item["area"])
        self.assertEqual("大雨警報", item["kind"])

    def test_warning_cancel_removes_state(self):
        state = {}
        apply_warning_updates(state, parse_warning_updates(WARNING))
        self.assertIn(("佐賀県", "大雨警報"), state)
        apply_warning_updates(state, parse_warning_updates(WARNING_CANCEL))
        self.assertNotIn(("佐賀県", "大雨警報"), state)

    def test_typhoon_probability_product_is_not_counted(self):
        entries = [
            {
                "title": "台風解析・予報情報（5日予報）（H30）",
                "link": "https://example.test/analysis.xml",
            },
            {
                "title": "台風の暴風域に入る確率",
                "link": "https://example.test/probability.xml",
            },
        ]

        def fetcher(url):
            self.assertEqual("https://example.test/analysis.xml", url)
            return TYPHOON_ACTIVE

        state = {}
        process_extra(entries, state, fetcher)
        self.assertEqual(["TY202623"], list(state))

    def test_typhoon_end_is_inactive(self):
        result = parse_typhoon_update(TYPHOON_END)
        self.assertFalse(result["active"])
        self.assertEqual("TY202601", result["event_id"])


if __name__ == "__main__":
    unittest.main()
