"""Offline checks of retained Markdown/HTML; never downloads or retries a page."""
import hashlib
import html
import re
from html.parser import HTMLParser


class TableRows(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.rows, self.row, self.cell = [], None, None

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self.row = []
        elif tag in ("td", "th") and self.row is not None:
            self.cell = []

    def handle_data(self, data):
        if self.cell is not None:
            self.cell.append(data)

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self.cell is not None:
            self.row.append(" ".join("".join(self.cell).split())); self.cell = None
        elif tag == "tr" and self.row is not None:
            self.rows.append(self.row); self.row = None


def plain_cell(value):
    value = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", value)
    value = re.sub(r"\*\*(.*?)\*\*", r"\1", value).replace("`", "")
    return " ".join(html.unescape(value.replace(r"\|", "|")).split())


def change_rows(brief):
    section = brief.split("## 已确认合并/发布的变更", 1)[1].split("\n## ", 1)[0]
    rows = []
    for line in section.splitlines():
        if not line.startswith("|"):
            continue
        cells = [plain_cell(x.strip()) for x in re.split(r"(?<!\\)\|", line.strip("|"))]
        if len(cells) != 4 or cells[2] == "状态" or all(re.fullmatch(r"[: -]+", x) for x in cells):
            continue
        rows.append(cells)
    return rows


def check_bytes(core, raw, brief, assertions, name, run_id):
    text = " ".join(html.unescape(re.sub(r"<[^>]+>", " ", raw.decode("utf-8"))).split())
    core.require(all(value in text for value in assertions), "webpage title/key-content/run identity mismatch")
    rows = []
    if name != "homepage":
        expected = change_rows(brief)
        core.require(expected, "actual Data brief has no change/status rows")
        parser = TableRows(); parser.feed(raw.decode("utf-8"))
        for row in expected:
            core.require(row in parser.rows, "published change/status row differs: " + row[0])
        rows = expected
    return dict(status="Passed", run_id=run_id, body_sha256=hashlib.sha256(raw).hexdigest(),
                checks=assertions, change_status_rows=len(rows))
