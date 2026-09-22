#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "beautifulsoup4>=4.12.0",
# ]
# ///
"""
Event Information Extractor & Normalizer
イベント・特典会公式告知ページからの情報抽出・構造化ツール

Web URL またはローカル HTML/テキストファイルから、
アイドルのリリースイベント・特典会ドメインに必要な情報を網羅的・決定論的に抽出し、
構造化 JSON (`event_data.json`) および 整理された Markdown (`event_summary.md`) として出力します。
"""

import argparse
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional

# beautifulsoup4 のインポートと uv run による動的自己解決
try:
    from bs4 import BeautifulSoup
except ImportError:
    if os.environ.get("_EXTRACT_REEXEC") != "1" and shutil.which("uv"):
        env = os.environ.copy()
        env["_EXTRACT_REEXEC"] = "1"
        cmd = [
            "uv",
            "run",
            "--with",
            "beautifulsoup4>=4.12.0",
            "python",
            os.path.abspath(__file__),
            *sys.argv[1:],
        ]
        res = subprocess.run(cmd, env=env)
        sys.exit(res.returncode)
    else:
        print("Error: Missing required dependency (beautifulsoup4). Run with 'uv run extract_event.py'.", file=sys.stderr)
        sys.exit(1)


class EventExtractor:
    def __init__(self, source: str):
        self.source = source
        self.raw_html = ""
        self.lines: List[str] = []
        self.cleaned_text = ""
        self.page_title = ""

    def fetch_or_read(self) -> None:
        """URL またはファイルからコンテンツを取得"""
        if self.source.startswith("http://") or self.source.startswith("https://"):
            req = urllib.request.Request(
                self.source,
                headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"},
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                charset = resp.headers.get_content_charset() or "utf-8"
                self.raw_html = resp.read().decode(charset, errors="replace")
        else:
            p = Path(self.source)
            if not p.exists():
                raise FileNotFoundError(f"File not found: {self.source}")
            self.raw_html = p.read_text(encoding="utf-8", errors="replace")

    def parse_content(self) -> None:
        """HTML をブロック要素境界で適切に改行分割して行リストを構築"""
        soup = BeautifulSoup(self.raw_html, "html.parser")

        if soup.title and soup.title.string:
            self.page_title = soup.title.string.strip()

        # 不要タグの除去
        for tag in soup(["script", "style", "nav", "footer", "header", "noscript", "aside"]):
            tag.decompose()

        # 改行・ブロック要素の前後に改行を明示的に挿入
        block_tags = ["br", "p", "div", "li", "tr", "th", "td", "h1", "h2", "h3", "h4", "h5", "h6", "section", "article"]
        for tag in soup.find_all(block_tags):
            tag.insert_before("\n")
            tag.insert_after("\n")

        # コンテンツ抽出
        content_elem = (
            soup.find(class_=re.compile(r"entry-content|post-content", re.I))
            or soup.find("article")
            or soup.find("main")
            or soup.find(class_=re.compile(r"schedule|detail|entry|post|event|content", re.I))
            or soup.body
        )
        if not content_elem:
            content_elem = soup

        raw_text = content_elem.get_text()
        self.lines = [re.sub(r"\s+", " ", l).strip() for l in raw_text.splitlines() if l.strip()]
        self.cleaned_text = "\n".join(self.lines)

    def dump_text(self, selector: Optional[str] = None) -> str:
        """指定セレクタまたは本文全体のテキストを抽出して返す"""
        self.fetch_or_read()
        soup = BeautifulSoup(self.raw_html, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header", "noscript", "aside"]):
            tag.decompose()

        block_tags = ["br", "p", "div", "li", "tr", "th", "td", "h1", "h2", "h3", "h4", "h5", "h6", "section", "article"]
        for tag in soup.find_all(block_tags):
            tag.insert_before("\n")
            tag.insert_after("\n")

        if selector:
            target = soup.select_one(selector)
        else:
            target = (
                soup.find(class_=re.compile(r"entry-content|post-content", re.I))
                or soup.find("article")
                or soup.find("main")
                or soup.find(class_=re.compile(r"schedule|detail|entry|post|event|content", re.I))
                or soup.body
                or soup
            )
        if not target:
            target = soup

        raw_text = target.get_text()
        lines = [re.sub(r"[ \t]+", " ", l).strip() for l in raw_text.splitlines() if l.strip()]
        return "\n".join(lines)

    def extract(self) -> Dict[str, Any]:
        """構造化イベントデータを抽出"""
        self.fetch_or_read()
        self.parse_content()

        data: Dict[str, Any] = {
            "meta": {
                "source_url": self.source,
                "extracted_at": datetime.datetime.now().isoformat(),
                "page_title": self.page_title,
            },
            "overview": self._extract_overview(),
            "cast": self._extract_cast(),
            "timetable": self._extract_timetable(),
            "products": self._extract_products(),
            "admission": self._extract_admission(),
            "tokutenkai": self._extract_tokutenkai(),
            "photo_time": self._extract_photo_time(),
            "regulations_and_notes": self._extract_notes(),
            "style_and_typography": self._extract_style_and_typography(),
        }
        return data

    def _extract_overview(self) -> Dict[str, Any]:
        """公演名、日時、会場、アクセスの抽出"""
        res: Dict[str, Any] = {
            "event_name": "",
            "date": "",
            "day_of_week": "",
            "venue_name": "",
            "venue_floor": "",
            "venue_address": "",
            "access_notes": [],
        }

        for idx, line in enumerate(self.lines):
            # タイトル
            if not res["event_name"]:
                m = re.search(r"(?:【?(?:タイトル|イベント名)】?)[：:]\s*[「『\"]?([^\n」』\"]+)[」』\"]?", line)
                if m:
                    res["event_name"] = m.group(1).strip()
                elif "「" in line and "」" in line and any(k in line for k in ["Live", "LIVE", "Party", "リリース", "ツアー", "フェス", "公演"]):
                    m_title = re.search(r"「([^」]+)」", line)
                    if m_title:
                        res["event_name"] = m_title.group(1).strip()

            # 日程 (例: 2026年9月27日(日), 2026.09.27(日), 2026年9月23日(水・祝))
            m_day = re.search(r"(\d{4})[年\.\-/](\d{1,2})[月\.\-/](\d{1,2})日?\s*[\(（]([日月火水木金土祝・\s]+)[\)）]", line)
            if m_day:
                y, m_val, d = int(m_day.group(1)), int(m_day.group(2)), int(m_day.group(3))
                res["date"] = f"{y:04d}-{m_val:02d}-{d:02d}"
                res["day_of_week"] = m_day.group(4).strip()
            elif not res["date"]:
                m_plain = re.search(r"(\d{4})[年\.\-/](\d{1,2})[月\.\-/](\d{1,2})", line)
                if m_plain:
                    y, m_val, d = int(m_plain.group(1)), int(m_plain.group(2)), int(m_plain.group(3))
                    res["date"] = f"{y:04d}-{m_val:02d}-{d:02d}"

            # 会場
            if not res["venue_name"]:
                m = re.search(r"^(?:【?(?:会場|場所)】?)[：:]\s*(.+)", line)
                if not m and line.strip() in ["【会場】", "【場所】", "会場", "場所"]:
                    # 次の行を会場とする
                    if idx + 1 < len(self.lines):
                        v_next = self.lines[idx + 1].strip()
                        m = re.match(r"^(.+)", v_next)
                if m:
                    v_raw = m.group(1).strip()
                    # 住所分離
                    m_addr = re.search(r"[\(（]〒?(\d{3}-\d{4})?\s*([^\)）]+)[\)）]", v_raw)
                    if m_addr:
                        res["venue_address"] = m_addr.group(2).strip()
                        v_raw = v_raw[: m_addr.start()].strip()
                    
                    # 施設名とフロアの分離
                    m_fl = re.search(r"^(.+?(?:パルコ|ビル|タワー|プラザ|モール|会館|劇場|ホール|LOFT|STUDIO|店))\s*(.*)$", v_raw)
                    if m_fl:
                        res["venue_name"] = m_fl.group(1).strip()
                        res["venue_floor"] = m_fl.group(2).strip()
                    else:
                        res["venue_name"] = v_raw

            # 住所単独行
            if not res["venue_address"] and ("〒" in line or "東京都" in line or "市" in line or "区" in line):
                if any(k in self.lines[max(0, idx - 1)] for k in ["会場", "場所"]):
                    res["venue_address"] = line.strip("（）() ")

            # アクセス注意
            if any(k in line for k in ["エレベーター", "エスカレーター", "階段で", "来場方法", "7Fまで"]):
                clean_l = line.lstrip("※・- ")
                if clean_l not in res["access_notes"]:
                    res["access_notes"].append(clean_l)

        # ページタイトルからのフォールバック
        clean_title = self.page_title
        # サイト名（例: - Straight Angeli）を末尾から削除
        clean_title = re.sub(r"\s+[-–—|｜]\s+[^|–—\-]+$", "", clean_title).strip()
        # 更新プレフィックス（例: 9/22更新）を削除
        clean_title = re.sub(r"^\d{1,2}/\d{1,2}更新\s*", "", clean_title).strip()

        # タイトルから会場（＠会場）を抽出
        if not res["venue_name"] and "＠" in clean_title:
            t_part, v_part = clean_title.split("＠", 1)
            v_part = v_part.strip()
            m_fl = re.search(r"^(.+?(?:パルコ|ビル|タワー|プラザ|モール|会館|劇場|ホール|LOFT|店))\s*(.*)$", v_part)
            if m_fl:
                res["venue_name"] = m_fl.group(1).strip()
                res["venue_floor"] = m_fl.group(2).strip()
            else:
                res["venue_name"] = v_part

        if not res["event_name"] and clean_title:
            m_quote = re.search(r"「([^」]+)」", clean_title)
            if m_quote:
                res["event_name"] = m_quote.group(1).strip()
            else:
                # ＠より前
                if "＠" in clean_title:
                    res["event_name"] = clean_title.split("＠", 1)[0].strip()
                else:
                    res["event_name"] = clean_title

        return res

    def _extract_cast(self) -> Dict[str, Any]:
        """出演者、組分け・チーム分けの抽出およびメンバーカラー調査指示"""
        res: Dict[str, Any] = {
            "group_name": "",
            "members": [],
            "teams": [],
            "color_research_required": True,
            "member_color_guidance": "公式サイト・SNS・プロフィールを能動的に調査し、各メンバーのイメージカラー（背景色・文字色・枠線）を特定して.member-chipに反映してください（※スタプラ研究生等未設定グループを除く）。",
        }

        # グループ名判定
        full_text = self.cleaned_text
        if "スタープラネットアイドルアカデミー" in full_text or "スタアカ" in full_text:
            res["group_name"] = "スタープラネットアイドルアカデミー (スタアカ)"
            res["color_research_required"] = False
            res["member_color_guidance"] = "スタプラ研究生/スタアカは個人メンバーカラー未設定のため、公式組分け（松ぼっくり組・どんぐり組）の.team-chipを使用してください。"
        elif "ばってん少女隊" in full_text:
            res["group_name"] = "ばってん少女隊"
        elif "RE-GE" in full_text:
            res["group_name"] = "RE-GE"
        elif "Straight Angeli" in full_text:
            res["group_name"] = "Straight Angeli"
        elif "ukka" in full_text:
            res["group_name"] = "ukka"
        elif "TEAM SHACHI" in full_text:
            res["group_name"] = "TEAM SHACHI"
        elif "私立恵比寿中学" in full_text:
            res["group_name"] = "私立恵比寿中学"
        elif "超ときめき♡宣伝部" in full_text:
            res["group_name"] = "超ときめき♡宣伝部"

        # 組分け・チーム分けパターン (例: 【松ぼっくり組】原田麻衣・ゆめ・香月りおな・沖名むぎ)
        team_pattern = re.compile(r"^[【\[]([🍂🌰🌸🌻🍁☘️]*[^\n】\]]+(?:組|チーム|ユニット))[】\]]\s*(.+)")
        for line in self.lines:
            m = team_pattern.match(line)
            if m:
                t_name = m.group(1).strip()
                t_members_raw = m.group(2).strip()
                m_list = [mem.strip() for mem in re.split(r"[・,、/／\s]+", t_members_raw) if mem.strip()]
                res["teams"].append({
                    "team_name": t_name,
                    "members": m_list,
                })
                for mem in m_list:
                    if mem not in res["members"]:
                        res["members"].append(mem)

        # 出演者行パターン (例: 出演：メンバー1, メンバー2 または 出演\nStraight Angeli\n(メンバー1・メンバー2))
        if not res["members"]:
            for idx, line in enumerate(self.lines):
                if line.strip() in ["出演", "出演者", "MEMBERS", "【出演】", "【出演者】"]:
                    for offset in range(1, 4):
                        if idx + offset < len(self.lines):
                            next_l = self.lines[idx + offset].strip()
                            if "(" in next_l or "（" in next_l:
                                m_inner = re.search(r"[\(（]([^\)）]+)[\)）]", next_l)
                                if m_inner:
                                    res["members"] = [mem.strip() for mem in re.split(r"[・,、/／\s]+", m_inner.group(1)) if mem.strip()]
                                    break
                    if res["members"]:
                        break
                m = re.match(r"^(?:出演|出演者|MEMBERS)[：:]\s*(.+)", line)
                if m:
                    m_list = [mem.strip() for mem in re.split(r"[・,、/／\s]+", m.group(1)) if mem.strip()]
                    res["members"] = m_list
                    break

        return res

    def _extract_timetable(self) -> Dict[str, Any]:
        """タイムテーブルの抽出（時系列順の厳格保持 ＆ 2部制並記集約対応）"""
        items: List[Dict[str, Any]] = []
        # 時刻パターン: 10:30〜物販開始, 12:25〜(予定) 優先観覧エリア...
        tt_pattern = re.compile(r"^(\d{1,2}:\d{2})\s*(?:〜|~|-)?\s*(\d{1,2}:\d{2})?\s*(?:\(予定\))?\s*(.+)")

        full_text = self.cleaned_text
        has_part1 = "1部" in full_text or "第1部" in full_text
        has_part2 = "2部" in full_text or "第2部" in full_text
        is_multi_part = has_part1 and has_part2

        for line in self.lines:
            m = tt_pattern.match(line)
            if m:
                st = m.group(1)
                et = m.group(2) or ""
                content = m.group(3).strip()

                # 補足（例: （約45分））の切り出し
                note = ""
                m_note = re.search(r"[\(（]([^\)）]+)[\)）]", content)
                if m_note:
                    note = m_note.group(1).strip()
                    content = content[: m_note.start()] + content[m_note.end() :]
                    content = content.strip()

                items.append({
                    "time": st,
                    "end_time": et,
                    "title": content,
                    "detail": note,
                })

        # 重複除去 & ソート
        seen = set()
        dedup_items = []
        for it in items:
            key = (it["time"], it["title"])
            if key not in seen:
                seen.add(key)
                dedup_items.append(it)

        dedup_items.sort(key=lambda x: x["time"])

        # 2部制の場合の共通タイムライン並記集約案の生成
        consolidated_items = []
        if is_multi_part:
            # 優先入場、ミニライブ等のペアリング探索
            p1_entry = next((it for it in dedup_items if any(k in it["title"] for k in ["優先", "入場", "開場"]) and "1部" in (it["title"] + it["detail"])), None)
            p2_entry = next((it for it in dedup_items if any(k in it["title"] for k in ["優先", "入場", "開場"]) and "2部" in (it["title"] + it["detail"])), None)
            
            p1_live = next((it for it in dedup_items if any(k in it["title"] for k in ["ライブ", "LIVE", "開演"]) and "1部" in (it["title"] + it["detail"])), None)
            p2_live = next((it for it in dedup_items if any(k in it["title"] for k in ["ライブ", "LIVE", "開演"]) and "2部" in (it["title"] + it["detail"])), None)

            # 物販等、部共通のアイテム
            for it in dedup_items:
                if any(k in it["title"] for k in ["販売", "予約", "グッズ", "CD", "物販"]):
                    consolidated_items.append(it)
                    break

            if p1_entry and p2_entry:
                consolidated_items.append({
                    "time": f"{p1_entry['time']} / {p2_entry['time']}",
                    "end_time": "",
                    "title": "観覧エリアご案内 ＆ 会場レイアウト（優先入場）",
                    "detail": "各部開演15分前集合・整理番号順入場",
                })
            
            if p1_live and p2_live:
                consolidated_items.append({
                    "time": f"{p1_live['time']} / {p2_live['time']}",
                    "end_time": "",
                    "title": "ミニライブ開演（観覧無料）",
                    "detail": f"1部 {p1_live['time']}〜 / 2部 {p2_live['time']}〜",
                })

        return {
            "items": dedup_items,
            "is_multi_part": is_multi_part,
            "consolidated_items": consolidated_items,
        }

    def _extract_products(self) -> Dict[str, Any]:
        """CD・グッズ・対象商品、購入上限、ループルールの抽出"""
        res: Dict[str, Any] = {
            "items": [],
            "purchase_limit": "",
            "loop_rule": "",
            "payment_methods": [],
            "payment_exclusions": [],
        }

        # 商品行の走査 (例: ・生写真第2シリーズ ¥1,000(税込), 対象商品(BTRC-1055))
        for line in self.lines:
            # 品番
            m_code = re.search(r"([A-Z]{3,5}-\d{3,5})", line)
            # 価格
            m_price = re.search(r"([0-9,]+円(?:\(税込\))?|¥[0-9,]+(?:\(税込\))?)", line)

            if m_price and any(k in line for k in ["生写真", "CD", "エムカード", "グッズ", "写真", "盤"]):
                clean_name = re.sub(r"^[・※\-\s]+", "", line)
                price_str = m_price.group(1)
                # 商品名から価格部分を除去
                clean_name = clean_name.replace(price_str, "").strip(" 　/／")
                code_str = m_code.group(1) if m_code else ""
                
                # 盤種（集合盤、ユニット盤など）
                disc_type = ""
                m_disc = re.search(r"【([^】]+)】", clean_name)
                if m_disc:
                    disc_type = m_disc.group(1)
                    clean_name = clean_name[: m_disc.start()].strip()

                res["items"].append({
                    "name": clean_name,
                    "disc_type": disc_type,
                    "code": code_str,
                    "price": price_str,
                })

            # 1会計上限
            if any(k in line for k in ["1会計", "一会計"]) and any(k in line for k in ["上限", "点まで", "枚まで", "個まで", "制限"]):
                res["purchase_limit"] = line.lstrip("※・- ")

            # ループ
            if any(k in line for k in ["ループ", "並び直し", "買い増し"]):
                if not any(k in line for k in ["：", ":"]) or "個" not in line:
                    res["loop_rule"] = line.lstrip("※・- ")

            # 決済方法
            if "支払い方法" in line or "支払方法" in line or any(k in line for k in ["クレジットカード", "QRコード決済", "電子マネー", "現金"]):
                if not any(k in line for k in ["禁止", "不可", "対象外"]):
                    clean_p = line.lstrip("※・- ")
                    if clean_p not in res["payment_methods"]:
                        res["payment_methods"].append(clean_p)

            # 対象外事項
            if any(k in line for k in ["対象外", "ご利用いただけません", "発行は全て対象外"]):
                clean_e = line.lstrip("※・- ")
                if clean_e not in res["payment_exclusions"]:
                    res["payment_exclusions"].append(clean_e)

        return res

    def _extract_admission(self) -> Dict[str, Any]:
        """入場・観覧エリアルールおよび会場フロアマップ要否の抽出"""
        res: Dict[str, Any] = {
            "has_priority_area": False,
            "meeting_time": "",
            "meeting_place": "",
            "ticket_rule": "",
            "free_viewing": "",
            "female_area": False,
            "handicap_area": False,
            "floor_map_required": False,
            "floor_map_guidance": "",
        }

        full_text = self.cleaned_text
        res["has_priority_area"] = "優先観覧エリア" in full_text
        res["female_area"] = "女性専用" in full_text or "女性優先" in full_text or "女性限定" in full_text
        res["handicap_area"] = "車椅子" in full_text or "お身体の不自由" in full_text

        # エリア図の要否判定（優先エリア、女性専用、車椅子、入場順等の記述がある場合は必須）
        if res["has_priority_area"] or res["female_area"] or res["handicap_area"] or "ファミリー" in full_text or "入場順" in full_text or "レイアウト" in full_text:
            res["floor_map_required"] = True
            res["floor_map_guidance"] = "ステージ、優先観覧エリア、女性専用エリア、入場導線等を含む縦長ベクターフロアマップ（floor_map.svg）を作成し、入場案内枠の右側（.entry-layout-row > .entry-map-col）に配置してください。"

        for line in self.lines:
            if "集合" in line or "整列" in line or "入場開始" in line:
                m_t = re.search(r"(\d{1,2}:\d{2})", line)
                if m_t and not res["meeting_time"]:
                    res["meeting_time"] = m_t.group(1)

            if any(k in line for k in ["整理番号付き優先観覧エリア券", "優先観覧エリア券"]):
                if any(k in line for k in ["ランダム", "先着", "1枚まで", "ご購入の方", "配布"]):
                    clean_t = line.lstrip("※・- ")
                    clean_t = re.sub(r"[\(（※]?定員に達し次第[、,\s]*終了[いたしますとなります]*[\)）]?", "", clean_t)
                    clean_t = re.sub(r"[\(（※]?無?なくなり次第[、,\s]*終了[いたしますとなります]*[\)）]?", "", clean_t)
                    clean_t = clean_t.strip("・- 　/※")
                    if clean_t and not any(clean_t.startswith(p) for p in ["「整理番号付き優先観覧エリア券」の配布は", "配布は定員", "配布は無くなり"]):
                        if not res["ticket_rule"] or len(clean_t) > len(res["ticket_rule"]):
                            res["ticket_rule"] = clean_t

            if "一般観覧" in line or "フリー観覧" in line or "観覧は無料" in line:
                res["free_viewing"] = line.lstrip("※・- ")

            if "集合場所" in line or "整列場所" in line:
                res["meeting_place"] = line.lstrip("※・- ")

        return res

    def _extract_tokutenkai(self) -> Dict[str, Any]:
        """特典会メニュー、くじ内訳、実施順、および1部/2部差分ダブルテーブル判定の抽出"""
        full_text = self.cleaned_text
        has_part1 = "1部" in full_text or "第1部" in full_text
        has_part2 = "2部" in full_text or "第2部" in full_text
        
        # 特典会内で1部・2部の書き分けがあるか
        is_multi_part_tokutenkai = has_part1 and has_part2 and any(k in full_text for k in ["【1部】", "【2部】", "1部特典会", "2部特典会", "第1部 特典会", "第2部 特典会"])

        res: Dict[str, Any] = {
            "execution_order": "",
            "is_multi_part": is_multi_part_tokutenkai,
            "menus": [],
            "part1_menus": [],
            "part2_menus": [],
            "kuji_items": [],
            "general_rules": [],
            "tokutenkai_guidance": "特典会の枠が空きすぎないよう、参加手順（呼び出し順、録画開始タイミング、足元マーク、交代制、まとめ出し制限等）の具体的情報を隙間なく記述してください。",
        }

        in_kuji_section = False
        for line in self.lines:
            # 実施順序 (例: 推し運検定→帰りの会)
            if "→" in line and any(k in line for k in ["会", "検定", "撮影", "ショット", "お話し"]):
                res["execution_order"] = line.strip()

            # 特典券N枚パターン (例: 特典券1枚：お見送り会, 特典券3枚：2ショット撮影会)
            m_ticket = re.match(r"^(?:特典券|参加券)\s*(\d+)枚\s*[：:]\s*(.+)", line)
            if m_ticket:
                t_count = m_ticket.group(1)
                t_title = m_ticket.group(2).strip()
                res["menus"].append({
                    "order": str(len(res["menus"]) + 1),
                    "name": t_title,
                    "description": f"特典券{t_count}枚",
                    "required_sets": f"{t_count}枚",
                })

            # 特典会大メニュー (例: ①帰りの会(お見送り会), ②推し運検定(ランダムくじ特典会))
            m_menu = re.match(r"^([①②③④⑤⑥⑦⑧⑨⑩\d]+[\.\)]?)\s*([^\n：:]{3,30}?)(?:[：:]\s*(.+))?$", line)
            if m_menu:
                order_raw = m_menu.group(1).strip()
                title = m_menu.group(2).strip()
                desc = m_menu.group(3) or ""
                # 数字への正規化
                order_num = ""
                for circ_ch, d_num in zip("①②③④⑤⑥⑦⑧⑨⑩", "12345678910"):
                    if circ_ch in order_raw:
                        order_num = d_num
                        break
                if not order_num:
                    m_d = re.search(r"\d+", order_raw)
                    if m_d:
                        order_num = m_d.group(0)

                if any(k in title for k in ["帰りの会", "お見送り", "推し運検定", "撮影", "shot", "ショット", "お話し", "サイン"]):
                    res["menus"].append({
                        "order": order_num,
                        "name": title,
                        "description": desc,
                        "required_sets": "",
                    })

            # 特典券必要セット数 (例: 対象商品1セットご購入で...)
            if res["menus"] and ("セットご購入" in line or "特典券をお渡し" in line):
                res["menus"][-1]["required_sets"] = line.lstrip("※・- ")

            # くじ賞品セクション (例: ◼︎グループショット(お客様＋メンバー全員))
            if any(k in line for k in ["推し運検定特典会内容", "くじ内訳", "賞品内容"]):
                in_kuji_section = True
                continue

            # 個数行 (例: ・グループショット：1個, ・推し2shot：2個)
            m_qty = re.search(r"^[・※\-\s]*([^\n：:]+)[：:]\s*(\d+個)", line)
            if m_qty:
                prize_name = m_qty.group(1).strip()
                qty_val = m_qty.group(2).strip()
                # 既存賞品に個数を付与
                matched = False
                for item in res["kuji_items"]:
                    if prize_name in item["name"]:
                        item["quantity"] = qty_val
                        matched = True
                        break
                if not matched and any(k in prize_name for k in ["ショット", "shot", "ソロ"]):
                    res["kuji_items"].append({"name": prize_name, "quantity": qty_val, "rules": []})
                continue

            if in_kuji_section:
                if line.startswith("■") or line.startswith("▼") or line.startswith("【商品販売"):
                    in_kuji_section = False
                elif any(line.startswith(p) for p in ["◼︎", "■", "・", "- "]):
                    clean_item = line.lstrip("◼︎■・- ")
                    if any(k in clean_item for k in ["ショット", "shot", "ソロ", "2shot", "3shot", "グループ"]):
                        # 重複追加の回避
                        if not any(it["name"] == clean_item for it in res["kuji_items"]):
                            res["kuji_items"].append({"name": clean_item, "quantity": "", "rules": []})
                    elif res["kuji_items"] and ("指名" in line or "撮影" in line or "メンバー" in line):
                        clean_rule = line.lstrip("※・- ")
                        if clean_rule not in res["kuji_items"][-1]["rules"]:
                            res["kuji_items"][-1]["rules"].append(clean_rule)

            # 特典会禁止事項・現場ルール
            if any(k in line for k in ["ふれる行為", "座らせる行為", "小道具", "画面録画", "Live Photos", "BeReal", "加工アプリ"]):
                clean_r = line.lstrip("※・- ★")
                if clean_r not in res["general_rules"]:
                    res["general_rules"].append(clean_r)
            if any(k in line for k in ["スマートフォンで行います", "スマホ限定", "手ぶら", "荷物置き場"]):
                clean_r = line.lstrip("※・- ★")
                if clean_r not in res["general_rules"]:
                    res["general_rules"].append(clean_r)

        return res

    def _extract_photo_time(self) -> Dict[str, Any]:
        """撮可TIMEの厳格抽出"""
        res: Dict[str, Any] = {
            "has_photo_time": False,
            "condition": "",
            "allowed_devices": "",
            "prohibited": [],
        }

        full_text = self.cleaned_text
        if "撮可" in full_text or "撮影可能タイム" in full_text:
            res["has_photo_time"] = True
            for line in self.lines:
                if any(k in line for k in ["撮可", "撮影可能"]):
                    clean_c = line.lstrip("※・- 〇★")
                    if "撮影可能タイムについて" not in clean_c and not res["condition"]:
                        res["condition"] = clean_c
                if any(k in line for k in ["スマートフォンのみ", "スマホ限定", "一眼レフ可", "一眼レフなど", "動画・写真"]):
                    clean_dev = line.lstrip("※・- 〇★")
                    if clean_dev not in res["allowed_devices"]:
                        res["allowed_devices"] = (res["allowed_devices"] + " / " + clean_dev).strip(" / ")
                if any(k in line for k in ["三脚", "一脚", "フラッシュ", "セルカ棒", "脚立", "自撮り棒", "頭上"]):
                    clean_p = line.lstrip("※・- 〇★")
                    if clean_p not in res["prohibited"]:
                        res["prohibited"].append(clean_p)
        elif "指示がない場合" in full_text:
            # メンバー・スタッフの指示がある場合は撮影可（指示時のみ可・原則禁止）
            res["has_photo_time"] = "conditional"
            for line in self.lines:
                if "指示がない場合" in line:
                    res["condition"] = line.lstrip("※・- ")
        else:
            # 撮影禁止の明記
            res["has_photo_time"] = False
            for line in self.lines:
                if "写真撮影、動画撮影、録音行為は固く禁止" in line or "撮影は禁止" in line:
                    res["condition"] = line.lstrip("※・- ")

        return res

    def _extract_notes(self) -> Dict[str, List[str]]:
        """注意事項・安全管理・禁止事項の整理"""
        notes: Dict[str, List[str]] = {
            "facility_and_safety": [],
            "baggage": [],
            "prohibited_actions": [],
            "contact": [],
        }

        for line in self.lines:
            clean_l = line.lstrip("※・- ")
            if not clean_l:
                continue

            # 屋上・施設安全
            if any(k in clean_l for k in ["傘の使用", "雨具", "カッパ", "危険防止", "屋上内", "オープンスペース", "一般のお客様"]):
                notes["facility_and_safety"].append(clean_l)
            # 通路・待機
            elif any(k in clean_l for k in ["立ち止まり", "階段など", "観覧エリア外", "徹夜", "早朝からの待機"]):
                notes["facility_and_safety"].append(clean_l)
            # 手荷物
            elif any(k in clean_l for k in ["手荷物", "貴重品", "ロッカー", "クローク", "故障"]):
                notes["baggage"].append(clean_l)
            # 禁止行為
            elif any(k in clean_l for k in ["座り込み", "迷惑行為", "三脚や一脚", "脚立", "台の上"]):
                notes["prohibited_actions"].append(clean_l)
            # 問い合わせ
            elif any(k in clean_l for k in ["お問い合わせ", "お問合せ", "contact", "株式会社スターダスト"]):
                notes["contact"].append(clean_l)

        # 重複除外
        for k in notes:
            seen = set()
            dedup = []
            for item in notes[k]:
                if item not in seen:
                    seen.add(item)
                    dedup.append(item)
            notes[k] = dedup

        return notes

    def _extract_style_and_typography(self) -> Dict[str, Any]:
        """公式ページやイベント内容から、推奨スタイル・配色テーマおよびタイポグラフィ（フォント選定）を分析"""
        detected_fonts: List[str] = []
        soup = BeautifulSoup(self.raw_html, "html.parser")
        for link in soup.find_all("link", rel=re.compile(r"stylesheet", re.I)):
            href = link.get("href", "")
            if "fonts.googleapis.com" in href:
                m_f = re.findall(r"family=([^&:]+)", href)
                for f in m_f:
                    clean_name = f.replace("+", " ")
                    if clean_name not in detected_fonts:
                        detected_fonts.append(clean_name)

        title_raw = (self.page_title + " " + self.cleaned_text)

        recommended_font_pattern = "1_modern_geometric"
        font_reason = "Mac/Win標準フォント（Hiragino Sans / Yu Gothic）とJost欧文によるクリーンで洗練された視認性"

        if any(k in title_raw for k in ["天使", "気品", "クラシック", "エレガント", "透明感", "クラシカル", "愛"]):
            recommended_font_pattern = "2_elegant_mincho"
            font_reason = "優美な明朝体（Shippori Mincho / Hiragino Mincho / Yu Mincho）とクラシカルセリフ欧文による幻想的な世界観"
        elif any(k in title_raw for k in ["ROCK", "ロック", "FES", "フェス", "激闘", "爆音", "タワーレコード", "熱気"]):
            recommended_font_pattern = "3_heavy_condensed"
            font_reason = "迫力の極太角ゴシック（Hiragino Sans / Yu Gothic / Noto Sans 900）とコンデンスド欧文（Impact / Oswald）"
        elif any(k in title_raw for k in ["キュート", "放課後", "学園", "アカデミー", "ポップ", "かわいい"]):
            recommended_font_pattern = "1_modern_geometric"
            font_reason = "親しみやすい標準角ゴシック（Hiragino Sans / Yu Gothic）とスクール感のあるJost欧文の組み合わせ"

        theme_presets = [
            {
                "id": "pattern_a",
                "name": "シーズン・イベント連動テーマ（例: オータム・ウォーム）",
                "concept": "ツアー名や開催季節（秋の放課後、松ぼっくり、どんぐり）を象徴する暖色系配色",
                "primary_color": "#b45309 (アンバー・テラコッタ)",
                "bg_accent": "秋の葉・どんぐりベクターパターン (bg-autumn.svg)",
                "font_stack": "Jost + Hiragino Sans / Yu Gothic / Noto Sans JP",
            },
            {
                "id": "pattern_b",
                "name": "公式ブランド・アイデンティティテーマ（例: アカデミー・ネイビー＆ゴールド）",
                "concept": "スタープラネット・アイドルアカデミーの制服とエンブレムを意識した端正なスクール配色",
                "primary_color": "#1e3a8a (スクールディープネイビー)",
                "bg_accent": "スクールチェック・幾何学パターン (bg-academy.svg)",
                "font_stack": "Jost + Hiragino Sans / Yu Gothic / Noto Sans JP",
            },
            {
                "id": "pattern_c",
                "name": "会場・ロケーション連動テーマ（例: パルコ・ポップ＆ルーフトップ）",
                "concept": "吉祥寺パルコの屋上オープンスペースの青空とモダンストリート感を表現したポップ配色",
                "primary_color": "#ea580c (パルコビビッドオレンジ)",
                "bg_accent": "青空ルーフトップ・ポップドットパターン (bg-parco.svg)",
                "font_stack": "Jost + Hiragino Sans / Yu Gothic / Noto Sans JP",
            },
        ]

        return {
            "detected_fonts": detected_fonts,
            "recommended_font_pattern": recommended_font_pattern,
            "font_selection_reason": font_reason,
            "theme_patterns": theme_presets,
        }


    def to_markdown(self, data: Dict[str, Any]) -> str:
        """決定論的に整理された構造化Markdown（情報要約シート）を生成"""
        meta = data["meta"]
        ov = data["overview"]
        cast = data["cast"]
        tt = data["timetable"]
        prod = data["products"]
        adm = data["admission"]
        tokuten = data["tokutenkai"]
        photo = data["photo_time"]
        notes = data["regulations_and_notes"]

        md = []
        md.append(f"# 【情報構造化シート】{ov.get('event_name') or meta.get('page_title')}")
        md.append("")
        md.append(f"- **元URL**: {meta.get('source_url')}")
        md.append(f"- **抽出日時**: {meta.get('extracted_at')}")
        md.append("")

        md.append("## 1. 公演概要")
        md.append(f"- **イベント名**: {ov.get('event_name')}")
        md.append(f"- **開催日程**: {ov.get('date')} ({ov.get('day_of_week')})")
        md.append(f"- **会場**: {ov.get('venue_name')} {ov.get('venue_floor')}")
        if ov.get("venue_address"):
            md.append(f"- **所在地**: {ov.get('venue_address')}")
        if ov.get("access_notes"):
            md.append("- **来場・アクセス方法**:")
            for an in ov.get("access_notes"):
                md.append(f"  - {an}")
        md.append("")

        md.append("## 2. 出演者・組分け・メンバーカラー（ヘッダー用データ）")
        if cast.get("group_name"):
            md.append(f"- **グループ**: {cast.get('group_name')}")
        if cast.get("teams"):
            md.append("- **組分け・チーム一覧**:")
            for tm in cast.get("teams"):
                m_str = "、".join(tm.get("members", []))
                md.append(f"  - **{tm.get('team_name')}**: {m_str}")
        elif cast.get("members"):
            md.append(f"- **出演メンバー一覧**: {'、'.join(cast.get('members'))}")

        if cast.get("color_research_required"):
            md.append("")
            md.append(f"> [!IMPORTANT]\n> **【要能動的調査】公式メンバーカラーの調査と反映**:\n> {cast.get('member_color_guidance')}\n> 公式サイト・プロフィール・公式SNS等を調査し、各メンバー固有のカラーコード（背景色・文字色・枠線）を特定して `.member-chip` に反映してください。")
        else:
            md.append("")
            md.append(f"> [!NOTE]\n> {cast.get('member_color_guidance')}")
        md.append("")

        md.append("## 3. タイムテーブル（時系列順 ＆ 2部制集約）")
        tt_items = tt.get("items", []) if isinstance(tt, dict) else tt
        is_multi = tt.get("is_multi_part", False) if isinstance(tt, dict) else False
        cons_items = tt.get("consolidated_items", []) if isinstance(tt, dict) else []

        if is_multi and cons_items:
            md.append("> [!TIP]\n> **【2部制集約推奨】紙面縦スペースの最大活用**:\n> 1部・2部共通のタイムライン（優先入場、ミニライブ等）は時刻を並記（例: `13:15 / 16:15 優先エリア入場`）して1つのカードに集約してください。貴重な縦スペースを節約し、特典会枠を最大化できます。")
            md.append("")
            md.append("### 推奨：並記集約タイムライン案")
            md.append("| 時刻 | 内容 | 補足 |")
            md.append("| :--- | :--- | :--- |")
            for it in cons_items:
                t_str = it["time"]
                if it.get("end_time"):
                    t_str += f"〜{it['end_time']}"
                md.append(f"| {t_str} | {it['title']} | {it.get('detail', '')} |")
            md.append("")
            md.append("### 全時系列タイムライン（詳細）")

        if tt_items:
            md.append("| 時刻 | 内容 | 補足 |")
            md.append("| :--- | :--- | :--- |")
            for it in tt_items:
                t_str = it["time"]
                if it.get("end_time"):
                    t_str += f"〜{it['end_time']}"
                md.append(f"| {t_str} | {it['title']} | {it.get('detail', '')} |")
        else:
            md.append("（タイムテーブル明記なし）")
        md.append("")

        md.append("## 4. CD・対象商品＆購入レギュレーション")
        if prod.get("items"):
            md.append("### 対象商品")
            md.append("| 商品名 / 盤種 | 品番 | 価格 |")
            md.append("| :--- | :--- | :--- |")
            for it in prod.get("items"):
                d_type = f"【{it['disc_type']}】" if it.get("disc_type") else ""
                md.append(f"| {it.get('name')} {d_type} | {it.get('code', '-')} | {it.get('price', '-')} |")
        if prod.get("purchase_limit"):
            md.append(f"- **購入点数上限**: {prod.get('purchase_limit')}")
        if prod.get("loop_rule"):
            md.append(f"- **ループ（並び直し）可否**: {prod.get('loop_rule')}")
        if prod.get("payment_methods"):
            md.append("- **決済方法**:")
            for pm in prod.get("payment_methods"):
                md.append(f"  - {pm}")
        if prod.get("payment_exclusions"):
            md.append("- **決済対象外・注意事項**:")
            for pe in prod.get("payment_exclusions"):
                md.append(f"  - {pe}")
        md.append("")

        md.append("## 5. 入場＆優先観覧エリア案内 ＆ 会場フロアマップ")
        md.append(f"- **優先観覧エリア**: {'あり' if adm.get('has_priority_area') else 'なし'}")
        if adm.get("meeting_time"):
            md.append(f"- **整列・入場開始**: {adm.get('meeting_time')}")
        if adm.get("ticket_rule"):
            md.append(f"- **入場券配布方法**: {adm.get('ticket_rule')}")
        if adm.get("free_viewing"):
            md.append(f"- **フリー観覧**: {adm.get('free_viewing')}")
        md.append(f"- **女性専用エリア**: {'あり' if adm.get('female_area') else 'なし / 記載なし'}")
        md.append(f"- **車椅子エリア**: {'あり' if adm.get('handicap_area') else 'なし / 記載なし'}")

        if adm.get("floor_map_required"):
            md.append("")
            md.append(f"> [!IMPORTANT]\n> **【エリア図必須】会場フロアマップ（縦長ベクターSVG `floor_map.svg`）の配置**:\n> {adm.get('floor_map_guidance')}")
        md.append("")

        md.append("## 6. 特典会メニュー・レギュレーション・実施順")
        if tokuten.get("is_multi_part"):
            md.append("> [!TIP]\n> **【1部・2部差分ダブルテーブル適用推奨】**:\n> 1部と2部で特典会メニューやレーン分けに差分があるため、左右2カラムのダブルテーブル（`.tokutenkai-double-table` > `.session-box`）で書き分けてください。")
            md.append("")
        
        md.append(f"> [!NOTE]\n> **【特典会情報密度最大化原則】**:\n> {tokuten.get('tokutenkai_guidance', '')}")
        md.append("")

        if tokuten.get("execution_order"):
            md.append(f"- **実施順序**: {tokuten.get('execution_order')}")
        if tokuten.get("menus"):
            md.append("### 特典会メニュー")
            for m in tokuten.get("menus"):
                req = f"（{m['required_sets']}）" if m.get("required_sets") else ""
                ord_badge = f"[#{m['order']}] " if m.get("order") else ""
                md.append(f"- **{ord_badge}{m.get('name')}** {req}")
        if tokuten.get("kuji_items"):
            md.append("### くじ賞品内訳（推し運検定等）")
            md.append("| 賞品内容 | 当選個数 | レギュレーション・指名条件 |")
            md.append("| :--- | :--- | :--- |")
            for k in tokuten.get("kuji_items"):
                rule_str = " / ".join(k.get("rules", [])) or "-"
                qty = k.get("quantity") or "-"
                md.append(f"| {k.get('name')} | {qty} | {rule_str} |")
        if tokuten.get("general_rules"):
            md.append("### 特典会共通ルール・禁止事項")
            for gr in tokuten.get("general_rules"):
                md.append(f"- {gr}")
        md.append("")

        md.append("## 7. 撮可（撮影可能）TIME")
        if photo.get("has_photo_time") is True:
            md.append("- **撮可TIME**: あり")
            if photo.get("condition"):
                md.append(f"  - 条件: {photo.get('condition')}")
            if photo.get("allowed_devices"):
                md.append(f"  - 機材: {photo.get('allowed_devices')}")
            if photo.get("prohibited"):
                md.append(f"  - 禁止事項: {', '.join(photo.get('prohibited'))}")
        elif photo.get("has_photo_time") == "conditional":
            md.append("- **撮可TIME**: 指示時のみ可（原則禁止）")
            if photo.get("condition"):
                md.append(f"  - 公式記述: {photo.get('condition')}")
        else:
            md.append("- **撮可TIME**: なし（ライブ・イベント中の撮影・録画・録音は全面禁止）")
            if photo.get("condition"):
                md.append(f"  - 公式記述: {photo.get('condition')}")
        md.append("")

        md.append("## 8. 注意事項・安全管理・お問い合わせ（紙面下部集約用）")
        if notes.get("facility_and_safety"):
            md.append("### 施設利用・屋上安全管理")
            for s in notes.get("facility_and_safety"):
                md.append(f"- {s}")
        if notes.get("baggage"):
            md.append("### 手荷物・クローク")
            for b in notes.get("baggage"):
                md.append(f"- {b}")
        if notes.get("prohibited_actions"):
            md.append("### 禁止事項（観覧マナー・迷惑行為）")
            for p in notes.get("prohibited_actions"):
                md.append(f"- {p}")
        if notes.get("contact"):
            md.append("### お問い合わせ先")
            for c in notes.get("contact"):
                md.append(f"- {c}")
        md.append("")

        # 9. スタイル選定＆フォント選定ガイド
        style = data.get("style_and_typography", {})
        if style:
            md.append("## 9. スタイル選定＆フォント選定ガイド（推奨タイポグラフィ）")
            if style.get("detected_fonts"):
                md.append(f"- **検出された公式Webフォント**: {', '.join(style['detected_fonts'])}")
            md.append(f"- **推奨フォント選定パターン**: `{style.get('recommended_font_pattern')}`")
            md.append(f"- **選定理由**: {style.get('font_selection_reason')}")
            md.append("")
            md.append("### 推奨デザインスタイル・テーマ案（3パターン提示）")
            for tp in style.get("theme_patterns", []):
                md.append(f"- **{tp.get('name')}** (`{tp.get('id')}`)")
                md.append(f"  - コンセプト: {tp.get('concept')}")
                md.append(f"  - 推奨カラー: {tp.get('primary_color')}")
                md.append(f"  - 推奨背景: {tp.get('bg_accent')}")
                md.append(f"  - フォントスタック: `{tp.get('font_stack')}`")
            md.append("")

        return "\n".join(md)


def main():
    parser = argparse.ArgumentParser(
        description="Event & Tokutenkai Information Extractor CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # 1. URL から情報を抽出し、Markdown と JSON を同時に保存 (推奨)
  uv run python extract_event.py "https://starplanet-academy.com/schedule/item-359/" -o event_summary.md --json event_data.json

  # 2. 抽出結果を標準出力に表示
  uv run python extract_event.py "https://starplanet-academy.com/schedule/item-359/"
""",
    )
    parser.add_argument("source", help="抽出元の URL または ローカル HTML/テキストファイル")
    parser.add_argument("-o", "--output", help="出力先ファイルパス (省略時: 標準出力)")
    parser.add_argument("--json", help="出力先 JSON ファイルパス")
    parser.add_argument("-q", "--quiet", action="store_true", help="進捗メッセージを抑制")
    parser.add_argument("--dump", "--dump-text", action="store_true", help="HTMLから本文テキストを整形ダンプする")
    parser.add_argument("-s", "--selector", help="ダンプ時の CSS セレクタ指定 (省略時: 本文自動判定)")

    args = parser.parse_args()

    extractor = EventExtractor(args.source)

    if args.dump:
        text = extractor.dump_text(selector=args.selector)
        if args.output:
            out_path = Path(args.output)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(text, encoding="utf-8")
            if not args.quiet:
                print(f"📄 Dumped text saved to: {out_path}")
        else:
            print(text)
        return 0

    if not args.quiet:
        print(f"==> Extracting event information from: {args.source}")

    data = extractor.extract()
    md_content = extractor.to_markdown(data)

    if args.json:
        json_path = Path(args.json)
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        if not args.quiet:
            print(f"💾 Structured JSON saved to: {json_path}")

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(md_content, encoding="utf-8")
        if not args.quiet:
            print(f"📝 Structured Markdown summary saved to: {out_path}")
    elif not args.json:
        print(md_content)

    return 0


if __name__ == "__main__":
    sys.exit(main())
