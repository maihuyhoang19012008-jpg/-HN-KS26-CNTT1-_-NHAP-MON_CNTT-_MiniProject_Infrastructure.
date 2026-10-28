#!/usr/bin/env bash
# ============================================================
#  GreenTech - Auto Report Log Filter (Linux/Mac .sh)
#  Module 2: Shell Script + Pipe (|) + Redirect (>>)
#  Audit: KHONG dung rm -rf / del nguy hiem
# ============================================================
set -euo pipefail

LOG_FILE="data/log-he-thong.log"
REPORT="backup/bao-cao-su-co.txt"

# --- Buoc 0: AUDIT / THAM DINH ---
if [ ! -f "$LOG_FILE" ]; then
    echo "[AUDIT] LOI: Khong tim thay file log $LOG_FILE"
    exit 1
fi
echo "[AUDIT OK] File log ton tai. Khong co lenh xoa."

# --- Buoc 1: Tieu de bao cao ---
{
    echo "============================================================"
    echo "  BAO CAO SU CO HE THONG - GreenTech IoT Farm"
    echo "  Ngay tao: $(date)"
    echo "============================================================"
    echo
    echo "[I] Cac dong CRITICAL:"
    echo "------------------------------------------------------------"
} >> "$REPORT"

# --- Buoc 2: Loc bang Pipe (|) + grep (doc streaming, khong tran RAM) ---
grep "CRITICAL" "$LOG_FILE" >> "$REPORT"
{
    echo
    echo "[II] Cac dong ERROR:"
    echo "------------------------------------------------------------"
} >> "$REPORT"
grep "ERROR" "$LOG_FILE" >> "$REPORT"

# --- Buoc 3: Thong ke bang pipe nhieu pha ---
CRIT=$(grep "CRITICAL" "$LOG_FILE" | wc -l)
ERR=$(grep "ERROR" "$LOG_FILE" | wc -l)

{
    echo
    echo "---------- TONG KET SO LUONG SU CO ----------"
    echo "So dong CRITICAL : $CRIT"
    echo "So dong ERROR    : $ERR"
    echo "============================================================"
    echo
} >> "$REPORT"

echo "[DONE] Bao cao da duoc noi vao: $REPORT"
