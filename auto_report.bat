@echo off
REM ============================================================
REM  GreenTech - Auto Report Log Filter (Windows .bat)
REM  Module 2: Robot loc log tu dong
REM  Audit (BAO MAT): Tuyet doi KHONG dung lenh xoa nguy hiem
REM                   del /f /s /q (AI hay goi y sai)
REM ============================================================
setlocal enabledelayedexpansion

REM --- Buoc 0: AUDIT / THAM DINH (bat buoc) ---
set "LOG_FILE=data\log-he-thong.log"
set "REPORT=backup\bao-cao-su-co.txt"

if not exist "%LOG_FILE%" (
    echo [AUDIT] LOI: Khong tim thay file log "%LOG_FILE%"
    echo [AUDIT] Dung chuong trinh de tranh ghi sai.
    exit /b 1
)
echo [AUDIT OK] File log ton tai. Khong co lenh xoa (del) nao duoc su dung.

REM --- Buoc 1: Tao tieu de bao cao chuyen nghiep bang lenh echo ---
echo ============================================================  >> "%REPORT%"
echo   BAO CAO SU CO HE THONG - GreenTech IoT Farm                 >> "%REPORT%"
echo   Ngay tao: %date% %time%                                     >> "%REPORT%"
echo ============================================================  >> "%REPORT%"
echo. >> "%REPORT%"
echo [I] Cac dong muc do CRITICAL:                                 >> "%REPORT%"
echo ------------------------------------------------------------  >> "%REPORT%"

REM --- Buoc 2: Loc log bang Pipe (|) ket hop findstr ---
REM type doc file theo dong (streaming) + pipe sang findstr loc
REM =^> khong nap toan bo file 500MB vao RAM, khong bi tran bo nho
type "%LOG_FILE%" | findstr /C:"CRITICAL" >> "%REPORT%"

echo. >> "%REPORT%"
echo [II] Cac dong muc do ERROR:                                   >> "%REPORT%"
echo ------------------------------------------------------------  >> "%REPORT%"
type "%LOG_FILE%" | findstr /C:"ERROR" >> "%REPORT%"

REM --- Buoc 3: Thong ke su dung Pipe nhieu pha (| ... |) ---
for /f %%a in ('type "%LOG_FILE%" ^| findstr /C:"CRITICAL" ^| find /c /v ""') do set CRIT=%%a
for /f %%a in ('type "%LOG_FILE%" ^| findstr /C:"ERROR" ^| find /c /v ""') do set ERR=%%a

echo. >> "%REPORT%"
echo ---------- TONG KET SO LUONG SU CO ---------- >> "%REPORT%"
echo So dong CRITICAL : !CRIT! >> "%REPORT%"
echo So dong ERROR    : !ERR! >> "%REPORT%"
echo ============================================================ >> "%REPORT%"
echo. >> "%REPORT%"

echo [DONE] Bao cao da duoc NOI (append ^>^>) vao: %REPORT%
endlocal
