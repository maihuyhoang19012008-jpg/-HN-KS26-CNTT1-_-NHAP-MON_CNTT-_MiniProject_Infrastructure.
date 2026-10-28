#!/usr/bin/env python3
"""Tao srs-he-thong.docx: Heading 1/2/3 + Auto TOC o trang dau."""
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUT = "/home/user/.dola/agent_mode/workspace/.sessions/38418469310528785/agents/m_0cLCXU5UjFZ/MiniProject_GreenTech/docs/srs-he-thong.docx"

doc = Document()

# --- Cai dat trang A4, margin 2.5cm ---
for section in doc.sections:
    section.page_height = Cm(29.7)
    section.page_width = Cm(21.0)
    section.top_margin = Cm(2.5)
    section.bottom_margin = Cm(2.5)
    section.left_margin = Cm(2.5)
    section.right_margin = Cm(2.5)

# --- Style mac dinh ---
normal = doc.styles["Normal"]
normal.font.name = "Times New Roman"
normal.font.size = Pt(12)
normal._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")

# Heading styles (override font/size)
for lvl, size in [(1, 16), (2, 14), (3, 13)]:
    h = doc.styles[f"Heading {lvl}"]
    h.font.name = "Arial"
    h.font.size = Pt(size)
    h.font.bold = True
    h.font.color.rgb = RGBColor(0x1B, 0x5E, 0x20)
    h._element.rPr.rFonts.set(qn("w:eastAsia"), "Arial")

# --- Trang bia ---
t = doc.add_paragraph()
t.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = t.add_run("TÀI LIỆU ĐẶC TẢ YÊU CẦU PHẦN MỀM\n(SRS - Software Requirements Specification)")
r.bold = True
r.font.size = Pt(18)

sub = doc.add_paragraph()
sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
sub.add_run("\nHỆ THỐNG QUẢN LÝ HẠ TẦNG GREEN TECH\nGreenTech Infrastructure Management System").bold = True

info = doc.add_paragraph()
info.alignment = WD_ALIGN_PARAGRAPH.CENTER
info.add_run("\n\nMôn học: Máy tính và Mạng máy tính\nMiniProject: Cơ sở CNTT\nPhiên bản: 1.0\nNgày: 28/10/2026").font.size = Pt(12)

doc.add_page_break()

# --- Trang Mục lục (Auto TOC) ---
toc_title = doc.add_paragraph()
toc_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
tr = toc_title.add_run("MỤC LỤC")
tr.bold = True
tr.font.size = Pt(16)

# Chen truong TOC (Auto TOC) — trong Word bam F9 hoac right-click > Update Field
p = doc.add_paragraph()
run = p.add_run()
fldChar1 = OxmlElement("w:fldChar"); fldChar1.set(qn("w:fldCharType"), "begin")
instrText = OxmlElement("w:instrText"); instrText.set(qn("xml:space"), "preserve")
instrText.text = ' TOC \\o "1-3" \\h \\z \\u '
fldChar2 = OxmlElement("w:fldChar"); fldChar2.set(qn("w:fldCharType"), "separate")
fldChar3 = OxmlElement("w:t"); fldChar3.text = "Mở file trong Word, bấm F9 hoặc chuột phải > Update Field để tạo mục lục tự động."
fldChar4 = OxmlElement("w:fldChar"); fldChar4.set(qn("w:fldCharType"), "end")
run._r.append(fldChar1); run._r.append(instrText); run._r.append(fldChar2)
run._r.append(fldChar3); run._r.append(fldChar4)

doc.add_page_break()

# --- Noi dung chuong (Heading 1/2/3) ---
doc.add_heading("1. Giới thiệu", level=1)
doc.add_heading("1.1 Mục đích", level=2)
doc.add_paragraph("Tài liệu này mô tả yêu cầu chức năng và phi chức năng của hệ thống quản lý hạ tầng GreenTech, phục vụ 100 trạm cảm biến IoT ngoài trang trại. Hệ thống tự động lọc log sự cố và đối soát danh mục thiết bị phần cứng.")
doc.add_heading("1.2 Phạm vi", level=2)
doc.add_paragraph("Phạm vi bao gồm 4 module: (1) Thiết lập cấu trúc lưu trữ, (2) Robot lọc log tự động, (3) Tài liệu vận hành, (4) Đối soát tài nguyên thiết bị.")
doc.add_heading("1.3 Định nghĩa, từ viết tắt", level=2)
doc.add_heading("1.3.1 Thuật ngữ", level=3)
doc.add_paragraph("IPO: Input – Process – Output. DIKW: Data – Information – Knowledge – Wisdom. PK: Khoá chính. FK: Khoá ngoại.")

doc.add_heading("2. Mô tả tổng thể", level=1)
doc.add_heading("2.1 Giao diện người dùng", level=2)
doc.add_paragraph("Người vận hành thao tác qua Terminal (CMD/Bash) và Microsoft Excel. Báo cáo sự cố xuất ra file text trong thư mục backup/.")
doc.add_heading("2.2 Ràng buộc thiết kế", level=2)
doc.add_paragraph("Tên thư mục dùng kebab-case, không dấu, không khoảng trắng. Script phải có bước Audit, tuyệt đối không dùng lệnh xóa nguy hiểm del /f /s /q.")

doc.add_heading("3. Yêu cầu chức năng", level=1)
doc.add_heading("3.1 Module lọc log tự động", level=2)
doc.add_heading("3.1.1 Chức năng lọc CRITICAL/ERROR", level=3)
doc.add_paragraph("Sử dụng Pipe (|) kết hợp findstr/grep lọc các dòng chứa CRITICAL và ERROR từ file log 500MB theo cơ chế streaming, không làm tràn RAM. Kết quả nối tiếp (>>) vào backup/bao-cao-su-co.txt.")
doc.add_heading("3.1.2 Bước Audit", level=3)
doc.add_paragraph("Kiểm tra file log tồn tại trước khi xử lý; ngừng chương trình nếu không tìm thấy để tránh ghi sai.")
doc.add_heading("3.2 Module đối soát thiết bị", level=2)
doc.add_paragraph("Sử dụng VLOOKUP (FALSE + $) kết hợp TRIM để tự động điền ten_thiet_bi, don_gia, loai_storage từ sheet danh-muc-linh-kien sang sheet trang-thai-tram dựa trên ma_linh_kien. IFERROR bắt lỗi #N/A.")

doc.add_heading("4. Yêu cầu phi chức năng", level=1)
doc.add_heading("4.1 Hiệu năng", level=2)
doc.add_paragraph("Xử lý file log 500MB trong thời gian hợp lý. Tốc độ tải log tính theo MB/s = Mbps / 8. Ví dụ 100 Mbps tương đương 12.5 MB/s.")
doc.add_heading("4.2 Bảo mật", level=2)
doc.add_paragraph("Mật khẩu và cấu hình nhạy cảm lưu trong file ẩn .env với giá trị giả định, không dùng thông tin thật.")

doc.add_heading("5. Ràng buộc dữ liệu & bẫy", level=1)
doc.add_paragraph("Vùng dữ liệu Excel không chứa hàng trống hay Merge Cell để AutoFilter hoạt động chính xác. Mã linh kiện có thể có khoảng trắng thừa, phải làm sạch bằng TRIM trước khi tra cứu.")

doc.add_heading("6. Tài liệu tham khảo", level=1)
doc.add_paragraph("[1] Tài liệu học phần Máy tính và Mạng máy tính. [2] Microsoft Excel VLOOKUP function documentation. [3] Windows Batch findstr / Linux grep manual.")

doc.save(OUT)
print("Saved:", OUT)
