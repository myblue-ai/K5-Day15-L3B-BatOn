"""Công cụ của bài toán — NHÓM VIẾT. Điền ở guide bước 2.2 (thiết kế) và 3.2 (code).

Mỗi công cụ là một hàm Python có @tool. Docstring ghi đúng 4 ý như sơ đồ ở spec.md §4:
    tên · input · output · có tác động ra ngoài không (gửi tin, sửa dữ liệu, chấm điểm…)
Khung tự ghi mỗi lần gọi công cụ vào trace (tên, input, output rút gọn, thời gian, lỗi).

Số công cụ, kiểu công cụ do thiết kế của nhóm quyết định — có bài chỉ cần một công cụ tra cứu.
Công cụ có tác động ra ngoài: KHÔNG tự làm. Trả về bản nháp chờ người duyệt (guide bước 2.2, "chỗ người duyệt").
Dữ liệu công cụ đọc (bài mẫu, thông báo mẫu, lịch…): để trong data/ và mô tả ở data/DATA_CARD.md.
"""
import json
from pathlib import Path

from tracing import tool


DEMO_LESSON = Path(__file__).resolve().parents[1] / "data" / "a1_demo_lesson.json"


@tool
def read_lesson_segments() -> list[dict[str, str]]:
    """Đọc các đoạn của video Day01 mô phỏng đang mở.
    Input: không có. Output: danh sách đoạn {"code", "text"}.
    Chỉ đọc tệp cục bộ, không tác động ra ngoài.
    """
    with DEMO_LESSON.open(encoding="utf-8") as file:
        return json.load(file)
