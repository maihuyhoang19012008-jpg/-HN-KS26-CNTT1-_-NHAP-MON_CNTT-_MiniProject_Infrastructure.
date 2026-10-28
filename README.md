# GreenTech Infrastructure Management System

> Hệ thống quản lý hạ tầng cho Startup công nghệ GreenTech — 100 trạm cảm biến IoT ngoài trang trại.
> MiniProject: **Máy tính và Mạng máy tính** — Cơ sở CNTT.

---

## 1. Phân tích & Thiết kế hệ thống (40 điểm)

### 1.1 Mô hình xử lý thông tin IPO

| Giai đoạn | Đầu vào (Input) | Xử lý (Process) | Đầu ra (Output) |
|---|---|---|---|
| Log | `log-he-thong.log` (500MB/ngày) | `type \| findstr` lọc CRITICAL/ERROR | `bao-cao-su-co.txt` |
| Thiết bị | `ma_linh_kien`, `ma_tram` | VLOOKUP + TRIM đối soát | Bảng trang-thai-tram đầy đủ |
| Cấu hình | Biến môi trường `.env` | Nạp vào script | Kết nối DB/MQTT an toàn |

### 1.2 Tư duy hệ thống DIKW

- **Data (Dữ liệu thô):** Dòng log, mã linh kiện, thông số cảm biến.
- **Information (Thông tin):** Lọc được 4 CRITICAL + 8 ERROR; trạm nào dùng SSD/HDD.
- **Knowledge (Kiến thức):** Trạm TRAM-060 sắp hết pin; SSD chính cần thay thế.
- **Wisdom (Quản trị):** Quyết định thay thiết bị, phân bổ nhân viên bảo trì, lập báo cáo sếp.

### 1.3 Cây thư mục 3 cấp — 4 trụ cột (kebab-case, KHÔNG dấu/Khoảng trắng)

```
greentech-system/          ← Root (cấp 1)
├── docs/                  ← Trụ cột 1: Tài liệu (cấp 2)
│   ├── README.md          ← (cấp 3)
│   └── srs-he-thong.docx  ← (cấp 3)
├── scripts/               ← Trụ cột 2: Tự động hóa
│   ├── auto_report.bat    ← Windows
│   └── auto_report.sh     ← Linux/Mac
├── data/                  ← Trụ cột 3: Dữ liệu
│   ├── log-he-thong.log
│   └── quan-ly-thiet-bi.xlsx
└── backup/                ← Trụ cột 4: Sao lưu
    └── bao-cao-su-co.txt
.env                       ← File ẩn cấu hình (Root)
```

---

## 2. Module 1 — Thiết lập "Căn cứ số" (Terminal)

**Một dòng lệnh duy nhất** khởi tạo toàn bộ cây thư mục lồng nhau:

```bash
# Linux / Mac / Git-Bash
mkdir -p greentech-system/{docs,scripts,data,backup} && cd greentech-system && touch .env
```

```bat
:: Windows CMD (1 dong)
mkdir greentech-system\docs greentech-system\scripts greentech-system\data greentech-system\backup && cd greentech-system && type nul > .env
```

**Dùng Relative Path** di chuyển và tạo file cấu hình ẩn chứa mật khẩu:

```bash
cd greentech-system          # Relative path: vao thu muc du an
echo "DB_PASS=FakeP@ssw0rd_2024!" > .env   # Tao file an .env
cat .env                     # Kiem tra noi dung
```

---

## 3. Module 2 — Robot lọc Log tự động

### Hướng dẫn chạy script (Code Block)

```bat
:: Windows — mo CMD, cd vao thu muc goc du an, chay:
scripts\auto_report.bat
```

```bash
# Linux / Mac / Git-Bash
chmod +x scripts/auto_report.sh
bash scripts/auto_report.sh
# Ket qua noi (append >>) vao: backup/bao-cao-su-co.txt
```

### Nguyên lý không tràn RAM với file 500MB

- `type file.log | findstr "CRITICAL"` — đọc **theo dòng (streaming)**, không nạp toàn bộ file vào RAM.
- Toán tử `>>` **nối tiếp (append)** vào báo cáo, không ghi đè.
- **Bước Audit bắt buộc:** kiểm tra file log tồn tại trước khi xử lý; **tuyệt đối không dùng** `del /f /s /q` (lệnh xóa nguy hiểm AI hay gợi ý sai).

---

## 4. Module 3 — Tài liệu hướng dẫn vận hành

- `docs/README.md` — file này (Markdown, render chuẩn trên GitHub).
- `docs/srs-he-thong.docx` — Đặc tả yêu cầu phần mềm, gán **Heading 1/2/3** + **Auto TOC** ở trang đầu.

---

## 5. Module 4 — Đối soát tài nguyên (Excel)

File: `data/quan-ly-thiet-bi.xlsx` — 2 sheet:

| Sheet | Trường (Field) | Khoá |
|---|---|---|
| `danh-muc-linh-kien` | ma_linh_kien, ten_thiet_bi, don_gia, loai_storage | **PK**: ma_linh_kien |
| `trang-thai-tram` | ma_tram, ma_linh_kien, dung_luong_ram, ngay_lap_dat | **FK**: ma_linh_kien |

**Công thức đối soát** (cột E của sheet `trang-thai-tram`):

```excel
=IFERROR(VLOOKUP(TRIM(B2),'danh-muc-linh-kien'!$A$2:$D$11,2,FALSE),"Khong tim thay")
```

- `TRIM(B2)` — làm sạch khoảng trắng thừa → tránh lỗi `#N/A`.
- `$A$2:$D$11` — khoá tuyệt đối vùng tra cứu (kéo fill không bị lệch).
- `FALSE` — tra cứu chính xác tuyệt đối.
- `IFERROR(...)` — bắt lỗi #N/A, hiển thị "Khong tim thay".

---

## 6. Checklist kiểm tra thiết bị (Task List)

- [x] Cây thư mục đúng kebab-case, không dấu, không khoảng trắng
- [x] File `.env` ẩn chứa cấu hình giả định (không phải mật khẩu thật)
- [x] `auto_report.bat` chạy thành công, có bước Audit, không dùng `del /f /s /q`
- [x] Pipe `|` + `findstr` lọc CRITICAL/ERROR; `>>` nối vào `backup/bao-cao-su-co.txt`
- [x] README.md có H1, Code Block, Task List, Table (render chuẩn GitHub)
- [x] `srs-he-thong.docx` gán Heading 1/2/3 + Auto TOC ở trang đầu
- [x] Excel 2 sheet, VLOOKUP + TRIM + $ + FALSE, không lỗi #N/A
- [x] Vùng dữ liệu **không hàng trống, không Merge Cell** → AutoFilter chính xác
- [ ] Thay thế SSD chính báo lỗi sector (hành động bảo trì)
- [ ] Sạc/pin cho trạm TRAM-060 (dưới 5%)

---

## 7. Bảng thông số phần cứng (Table)

| Thiết bị | Mã linh kiện | Thông số | Loại storage | Đơn giá |
|---|---|---|---|---|
| CPU trung tâm | LK-CPU-01 | Intel Core i5-12400, 6 nhân 12 luồng | — | 4.500.000₫ |
| RAM máy chủ | LK-RAM-02 | DDR4 16GB Bus 3200 | — | 1.800.000₫ |
| SSD khởi động | LK-SSD-03 | Samsung 500GB NVMe, đọc 3500MB/s | SSD | 2.200.000₫ |
| HDD lưu trữ | LK-HDD-04 | Seagate 2TB, 7200rpm | HDD | 1.500.000₫ |
| Cảm biến IoT | LK-CPU-07 | Raspberry Pi Pico W, WiFi | — | 150.000₫ |

---

## 8. Xử lý bẫy dữ liệu (Data Traps)

| Bẫy | Giải pháp áp dụng |
|---|---|
| **Terminal:** Tên thư mục không được có dấu/khoảng trắng | Dùng kebab-case: `greentech-system`, `auto-report.bat` |
| **Script:** Tránh `del /f /s /q` do AI gợi ý | Có bước Audit; chỉ dùng `echo`, `type`, `findstr`, `>>` |
| **Excel:** Hàng trống/Merge Cell làm hỏng AutoFilter | Dữ liệu liền mạch, không merge, bật AutoFilter |
| **Hardware:** Tốc độ mạng Mbps → MB/s | Hệ số chia **8**: `100 Mbps = 100/8 = 12.5 MB/s`. Tải log 500MB mất ~40 giây. |

---

## 9. Cấu trúc Repository GitHub

```
[Tên Lớp]_[Môn Học]_MiniProject_GreenTech
├── docs/
│   ├── README.md
│   └── srs-he-thong.docx
├── scripts/
│   ├── auto_report.bat
│   └── auto_report.sh
├── data/
│   ├── log-he-thong.log
│   └── quan-ly-thiet-bi.xlsx
├── backup/
│   └── bao-cao-su-co.txt
└── .env
```

*Nộp đường dẫn repository lên hệ thống Portal theo quy định.*
