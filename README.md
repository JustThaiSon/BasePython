# BasePython Project - Quick Start & Usage Guide

## 1. Cài đặt môi trường

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Cấu hình môi trường

- Sửa file `.env` với thông tin kết nối database, ngôn ngữ mặc định, v.v.

Ví dụ:
```
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/DbPy
PROJECT_NAME=FASTAPI BASE
SECRET_KEY=your_secret_key
DEFAULT_LANG=vi
```

## 3. Migration database (với Alembic)

- Tạo migration mới:
```bash
alembic revision --autogenerate -m "your message"
```
- Áp dụng migration:
```bash
alembic upgrade head
```

## 4. Chạy server FastAPI

```bash
uvicorn main:app --reload
```
- Truy cập docs: http://localhost:8000/docs

## 5. Thêm model mới
- Tạo file model trong `app/models/` và kế thừa `Base`.
- Tạo migration mới và upgrade như hướng dẫn trên.

## 6. Đa ngôn ngữ cho message
- Sửa file `app/resources/messages.json` để thêm/chỉnh message cho từng code và ngôn ngữ.
- Đổi ngôn ngữ mặc định bằng cách sửa `DEFAULT_LANG` trong `.env`.

## 7. Đẩy code lên GitHub
```bash
git add .
git commit -m "your message"
git push origin master
```

## 8. Một số lệnh hữu ích
- Kiểm tra trạng thái git: `git status`
- Tạo migration rollback: `alembic downgrade -1`

---

**Mọi thắc mắc hoặc lỗi phát sinh, hãy kiểm tra lại file README này hoặc liên hệ quản trị dự án.**

