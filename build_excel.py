#!/usr/bin/env python3
"""Tao file quan-ly-thiet-bi.xlsx voi 2 sheet + VLOOKUP + TRIM + IFERROR."""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.table import Table, TableStyleInfo
from datetime import date

OUT = "/home/user/.dola/agent_mode/workspace/.sessions/38418469310528785/agents/m_0cLCXU5UjFZ/MiniProject_GreenTech/data/quan-ly-thiet-bi.xlsx"

wb = Workbook()

# ---------- Sheet 1: danh-muc-linh-kien ----------
ws1 = wb.active
ws1.title = "danh-muc-linh-kien"
header1 = ["ma_linh_kien", "ten_thiet_bi", "don_gia", "loai_storage"]
components = [
    ("LK-CPU-01", "CPU Intel Core i5-12400", 4500000, "SSD"),
    ("LK-RAM-02", "RAM DDR4 16GB Bus 3200", 1800000, "SSD"),
    ("LK-SSD-03", "SSD Samsung 500GB NVMe", 2200000, "SSD"),
    ("LK-HDD-04", "HDD Seagate 2TB Barracuda", 1500000, "HDD"),
    ("LK-SSD-05", "SSD Kingston 240GB SATA", 900000, "SSD"),
    ("LK-RAM-06", "RAM DDR4 8GB Bus 2666", 950000, "SSD"),
    ("LK-CPU-07", "CPU Raspberry Pi Pico W", 150000, "SSD"),
    ("LK-SSD-08", "SSD Western Digital 1TB", 3100000, "SSD"),
    ("LK-HDD-09", "HDD Toshiba 4TB Enterprise", 5200000, "HDD"),
    ("LK-RAM-10", "RAM DDR5 32GB Bus 4800", 3500000, "SSD"),
]

# ---------- Sheet 2: trang-thai-tram ----------
ws2 = wb.create_sheet("trang-thai-tram")
header2 = ["ma_tram", "ma_linh_kien", "dung_luong_ram", "ngay_lap_dat", "ten_thiet_bi (VLOOKUP)", "don_gia (VLOOKUP)", "loai_storage (VLOOKUP)"]
# Co dinh them 1-2 dong co khoang trang thua o ma_linh_kien de TRIM sua loi #N/A
stations = [
    ("TRAM-001", "LK-CPU-01", 16, date(2025, 1, 15)),
    ("TRAM-002", "LK-RAM-02", 16, date(2025, 1, 15)),
    ("TRAM-003", "  LK-SSD-03", 8, date(2025, 2, 10)),   # co khoang trang thua TRIM se xu ly
    ("TRAM-004", "LK-HDD-04  ", 32, date(2025, 2, 20)),  # co khoang trang thua
    ("TRAM-005", "LK-SSD-05", 8, date(2025, 3, 5)),
    ("TRAM-006", "LK-RAM-06", 8, date(2025, 3, 18)),
    ("TRAM-007", "LK-CPU-07", 4, date(2025, 4, 2)),
    ("TRAM-008", " LK-SSD-08 ", 16, date(2025, 4, 22)),  # co khoang trang ca 2 dau
    ("TRAM-009", "LK-HDD-09", 64, date(2025, 5, 1)),
    ("TRAM-010", "LK-RAM-10", 32, date(2025, 5, 14)),
    ("TRAM-011", "LK-CPU-01", 16, date(2025, 6, 3)),
    ("TRAM-012", "LK-SSD-03", 8, date(2025, 6, 25)),
]

# Styles
header_font = Font(bold=True, color="FFFFFF", size=11)
header_fill = PatternFill("solid", fgColor="2E7D32")
thin = Side(style="thin", color="BBBBBB")
border = Border(left=thin, right=thin, top=thin, bottom=thin)
center = Alignment(horizontal="center", vertical="center")

def write_header(ws, header, ncols):
    for c, h in enumerate(header, 1):
        cell = ws.cell(row=1, column=c, value=h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center
        cell.border = border

# Sheet 1 data
write_header(ws1, header1, len(header1))
for r, row in enumerate(components, 2):
    for c, val in enumerate(row, 1):
        cell = ws1.cell(row=r, column=c, value=val)
        cell.border = border
        if c == 3:
            cell.number_format = '#,##0" VND"'
ws1.column_dimensions["A"].width = 16
ws1.column_dimensions["B"].width = 32
ws1.column_dimensions["C"].width = 16
ws1.column_dimensions["D"].width = 14
last1 = len(components) + 1  # 11

# Sheet 2 data + cong thuc VLOOKUP
write_header(ws2, header2, len(header2))
for r, (ma_tram, ma_lk, ram, ngay) in enumerate(stations, 2):
    ws2.cell(row=r, column=1, value=ma_tram).border = border
    ws2.cell(row=r, column=2, value=ma_lk).border = border
    ws2.cell(row=r, column=3, value=ram).border = border
    c4 = ws2.cell(row=r, column=4, value=ngay)
    c4.number_format = "dd/mm/yyyy"
    c4.border = border
    # Cong thuc: TRIM lam sach ma_linh_kien (cot B) -> VLOOKUP exact (FALSE) vao bang danh muc
    # Su dung $ de khoa vung, IFERROR tranh #N/A
    f_ten = f"=IFERROR(VLOOKUP(TRIM(B{r}),'danh-muc-linh-kien'!$A$2:$D${last1},2,FALSE),\"Khong tim thay\")"
    f_gia = f"=IFERROR(VLOOKUP(TRIM(B{r}),'danh-muc-linh-kien'!$A$2:$D${last1},3,FALSE),0)"
    f_loai = f"=IFERROR(VLOOKUP(TRIM(B{r}),'danh-muc-linh-kien'!$A$2:$D${last1},4,FALSE),\"Khong tim thay\")"
    c5 = ws2.cell(row=r, column=5, value=f_ten); c5.border = border
    c6 = ws2.cell(row=r, column=6, value=f_gia); c6.border = border; c6.number_format = '#,##0" VND"'
    c7 = ws2.cell(row=r, column=7, value=f_loai); c7.border = border

ws2.column_dimensions["A"].width = 12
ws2.column_dimensions["B"].width = 16
ws2.column_dimensions["C"].width = 16
ws2.column_dimensions["D"].width = 14
ws2.column_dimensions["E"].width = 30
ws2.column_dimensions["F"].width = 16
ws2.column_dimensions["G"].width = 18

# AutoFilter (khong Merge Cell, khong hang trong -> chay chinh xac)
ws1.auto_filter.ref = f"A1:D{last1}"
ws2.auto_filter.ref = f"A1:G{len(stations)+1}"

wb.save(OUT)
print("Saved:", OUT)
print("Sheet1 rows:", last1, " Sheet2 rows:", len(stations)+1)
