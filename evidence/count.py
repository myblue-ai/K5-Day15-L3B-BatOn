"""Đếm bằng chứng pain từ data/preclass/ của BTC (evidence/data-mining.md, spec.md §2).

Chạy:  python evidence/count.py <đường-dẫn-tới-data/preclass>
Mặc định đọc data-btc/preclass (thư mục này đã nằm trong .gitignore, không commit data gốc).
Chỉ dùng thư viện chuẩn. In ra số đã tổng hợp + vài mã dòng ví dụ, không in nội dung cá nhân.
"""
import collections as C
import csv
import json
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")  # để PowerShell / cmd in được tiếng Việt

D = sys.argv[1] if len(sys.argv) > 1 else os.path.join("data-btc", "preclass")


def rd(name):
    with open(os.path.join(D, name), encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def js(s):
    try:
        return json.loads(s or "{}")
    except ValueError:
        return {}


def pct(x, n):
    return f"{x}/{n} ({100 * x / n:.1f}%)" if n else f"{x}/0"


ev = rd("events.csv")
chat = rd("chat.csv")

# Mẫu số: học viên có ít nhất 1 hành động
active = {e["hv"] for e in ev if e["actor"] == "learner"}

# D1 — câu hỏi dưới video
vq = [c for c in chat if c["channel"] == "video_question"]
vq_ids = {c["id"] for c in vq}
print("D1 học viên hỏi dưới video:", pct(len({c["hv"] for c in vq}), len(active)))
print("D1 số câu hỏi dưới video:", len(vq), "· khoảng", min(c["asked_at"][:10] for c in vq), "→", max(c["asked_at"][:10] for c in vq))

# D2 — câu trả lời của trợ giảng có dẫn mốc trong bài không (khoá moc_trich_dan chỉ có từ 13/11)
rep = {e["ref_id"]: js(e["data"]) for e in ev if e["type"] == "agent_replied"}
ta = [c for c in vq if c["agent_id"] == "teaching_assistant" and c["id"] in rep]
ta_k = [c for c in ta if "moc_trich_dan" in rep[c["id"]]]
no_cite = [c for c in ta_k if not rep[c["id"]]["moc_trich_dan"]]
print("D2 câu trả lời trợ giảng KHÔNG dẫn mốc bài:", pct(len(no_cite), len(ta_k)))
print("D2 ví dụ (mã chat):", [c["id"] for c in sorted(no_cite, key=lambda c: c["asked_at"])[:5]])
mc = [c for c in ta if rep[c["id"]].get("missing_context") is True]
print("D2b trợ giảng tự báo thiếu ngữ cảnh (missing_context):", pct(len(mc), len(ta)))

# D3 — tua lùi video
def is_back(d):
    return isinstance(d.get("from"), (int, float)) and isinstance(d.get("to"), (int, float)) and d["to"] < d["from"]

seek_back = [e for e in ev if e["type"] == "video_seeked" and is_back(js(e["data"]))]
viewers = {e["hv"] for e in ev if e["type"] == "video_opened"}
print("D3 người xem video có tua lùi:", pct(len({e["hv"] for e in seek_back}), len(viewers)), "· số lần tua lùi:", len(seek_back))

# D4, D5 — hướng A4 (bạn học AI)
shown = sum(e["type"] == "agent_message_shown" for e in ev)
replies = sum(c["channel"] == "video_discussion_reply" for c in chat)
print("D4/D5 lời bạn học AI hiện ra / học viên đáp lại:", shown, "/", replies)

# D6 — phân bố số câu hỏi mỗi học viên (persona)
per = C.Counter(c["hv"] for c in vq).values()
low = [v for v in per if v <= 2]
mid = [v for v in per if 3 <= v <= 9]
high = [v for v in per if v >= 10]
n = len(per)
print("D6 hỏi ít 1–2:", pct(len(low), n), "· vừa 3–9:", pct(len(mid), n), "· nhiều ≥10:", pct(len(high), n),
      "· câu của nhóm ≥10:", pct(sum(high), len(vq)))

# Giờ hỏi (giờ Việt Nam = UTC+7)
late = [c for c in vq if (int(c["asked_at"][11:13]) + 7) % 24 in (22, 23, 0, 1)]
print("Giờ hỏi 22:00–01:59 (giờ VN):", pct(len(late), len(vq)))
