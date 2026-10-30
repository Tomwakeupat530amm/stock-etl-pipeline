# stock-etl-pipeline

**Tiếng Việt** | [English](README.en.md)

Pipeline ETL dữ liệu chứng khoán từ đầu đến cuối. Pipeline lấy giá hằng ngày của một hoặc nhiều mã cổ phiếu từ Alpha Vantage API, làm sạch và bổ sung chỉ số bằng Pandas, upsert vào PostgreSQL, vẽ biểu đồ, và được Apache Airflow chạy trong Docker lập lịch.

## Tính năng

- **Nhiều mã cổ phiếu**: cấu hình tùy ý (`STOCK_SYMBOLS=IBM,AAPL,MSFT`).
- **Dữ liệu bổ sung**: tính lợi suất ngày (%) và đường trung bình động 20 ngày ngay ở bước transform.
- **Kiểm tra dữ liệu**: loại bỏ giá trị không hợp lệ, giá không dương, dòng có `high < low` và ngày trùng.
- **Upsert idempotent**: `INSERT ... ON CONFLICT (symbol, trade_date) DO UPDATE` theo lô. Chạy lại không tạo bản ghi trùng, và dữ liệu đã được sửa sẽ ghi đè giá trị cũ.
- **Tự tạo bảng**: bảng đích được tạo tự động ở lần chạy đầu.
- **Mỗi mã một task Airflow**, chạy tuần tự để không vượt giới hạn của API. Một mã lỗi không làm dừng các mã còn lại.
- **Biểu đồ theo từng mã** lưu tại `visualization/output/<MÃ>/`: giá đóng cửa, khối lượng, trung bình động, histogram lợi suất ngày, box plot, heatmap tương quan.

## Kiến trúc

```text
Alpha Vantage API -> extract.py -> transform.py -> load.py (PostgreSQL)
                                        |
                                        +-> visualization/charts.py (PNG)

Airflow DAG (22:00 hằng ngày, Asia/Ho_Chi_Minh): etl_ibm >> etl_aapl >> ...
   mỗi task chạy: python -m src.main --symbol <MÃ>
```

## Cấu trúc thư mục

```text
stock-etl-pipeline/
├── airflow/dags/financial_etl_dag.py   # DAG: mỗi mã một task
├── src/
│   ├── config.py      # cấu hình từ biến môi trường
│   ├── database.py    # SQLAlchemy engine
│   ├── extract.py     # gọi Alpha Vantage
│   ├── transform.py   # làm sạch, kiểm tra, lợi suất & MA20
│   ├── load.py        # tạo bảng + upsert theo lô
│   ├── logger.py
│   └── main.py        # điểm vào dòng lệnh
├── visualization/charts.py
├── sql/create_tables.sql
├── Dockerfile
├── docker-compose.yaml
├── requirements.txt
└── .env.example
```

## Cấu hình

Sao chép `.env.example` thành `.env`:

```env
ALPHA_VANTAGE_API_KEY=your_api_key
STOCK_SYMBOLS=IBM,AAPL,MSFT
OUTPUT_SIZE=compact          # compact = ~100 ngày, full = hơn 20 năm

DB_HOST=host.docker.internal
DB_PORT=5432
DB_NAME=stock_market
DB_USER=postgres
DB_PASSWORD=your_password

AIRFLOW_UID=50000
FERNET_KEY=                  # python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Gói miễn phí của Alpha Vantage bị giới hạn (khoảng 5 request/phút và hạn mức nhỏ mỗi ngày), nên hãy giữ danh sách mã ngắn. Biến `API_DELAY_SECONDS` (mặc định 13) điều chỉnh thời gian nghỉ giữa các mã.

## Cách sử dụng

### Chạy với Airflow (Docker)

```bash
docker compose up airflow-init
docker compose up -d
```

Mở http://localhost:8080 (tài khoản mặc định `airflow` / `airflow`), bật DAG `financial_etl_pipeline` rồi Trigger, hoặc chờ đến lịch 22:00. Hãy tạo sẵn database `stock_market` trong PostgreSQL, còn bảng sẽ được tạo tự động.

Dừng bằng `docker compose down`.

### Chạy không cần Airflow

```bash
pip install -r requirements.txt
python -m src.main                      # dùng STOCK_SYMBOLS
python -m src.main --symbol NVDA TSLA   # ghi đè danh sách mã
```

### Truy vấn dữ liệu

```sql
SELECT symbol, trade_date, close_price, daily_return
FROM daily_stock_prices
WHERE symbol = 'IBM'
ORDER BY trade_date DESC
LIMIT 10;
```

## Lưu ý

- Dự án phục vụ học tập. Dữ liệu thị trường có thể bị trễ và không phải lời khuyên đầu tư.
- Các file `airflow.cfg` do Airflow sinh ra chứa secret và đã được thêm vào `.gitignore`.
- Mật khẩu Airflow và JWT secret mặc định trong `docker-compose.yaml` chỉ dùng cho môi trường local.
