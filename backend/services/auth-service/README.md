# 璁よ瘉鍩熸湇鍔?(auth-service)

## 鏈嶅姟璇存槑

璁よ瘉鍩熸湇鍔¤礋璐ｅ鐞嗙敤鎴疯璇併€乀oken绠＄悊鍜岀敤鎴风櫥褰曠櫥鍑虹瓑鏍稿績璁よ瘉鍔熻兘銆?

## 鍔熻兘鐗规€?

- 鉁?鐢ㄦ埛鐧诲綍/鐧诲嚭
- 鉁?JWT Token鐢熸垚鍜岄獙璇?
- 鉁?Token鍒锋柊鏈哄埗
- 鉁?瀵嗙爜鍔犲瘑鍜岄獙璇?
- 鉁?鐢ㄦ埛鐘舵€佺鐞?
- 鉁?澶氱鎴锋敮鎸?
- 鉁?API Key璁よ瘉

## 鎶€鏈爤

- **妗嗘灦**: FastAPI 0.104+
- **ORM**: SQLAlchemy 2.0+
- **鏁版嵁搴?*: MySQL 8.0+
- **缂撳瓨**: Redis 7.0+
- **鏃ュ織**: loguru 0.7+

## 椤圭洰缁撴瀯

```
auth-service/
鈹溾攢鈹€ app/
鈹?  鈹溾攢鈹€ __init__.py
鈹?  鈹溾攢鈹€ main.py              # 搴旂敤鍏ュ彛
鈹?  鈹溾攢鈹€ api/                  # API璺敱
鈹?  鈹?  鈹斺攢鈹€ v1/
鈹?  鈹?      鈹斺攢鈹€ auth.py      # 璁よ瘉API
鈹?  鈹溾攢鈹€ core/                 # 鏍稿績閰嶇疆
鈹?  鈹?  鈹溾攢鈹€ config.py        # 閰嶇疆绫?
鈹?  鈹?  鈹斺攢鈹€ deps.py          # 渚濊禆娉ㄥ叆
鈹?  鈹溾攢鈹€ models/               # SQLAlchemy妯″瀷
鈹?  鈹?  鈹溾攢鈹€ __init__.py
鈹?  鈹?  鈹溾攢鈹€ user.py          # 鐢ㄦ埛妯″瀷
鈹?  鈹?  鈹斺攢鈹€ token.py         # Token妯″瀷
鈹?  鈹溾攢鈹€ schemas/              # Pydantic妯″瀷
鈹?  鈹?  鈹溾攢鈹€ __init__.py
鈹?  鈹?  鈹斺攢鈹€ auth.py          # 璁よ瘉Schema
鈹?  鈹溾攢鈹€ services/             # 涓氬姟閫昏緫灞?
鈹?  鈹?  鈹溾攢鈹€ __init__.py
鈹?  鈹?  鈹溾攢鈹€ auth_service.py  # 璁よ瘉鏈嶅姟
鈹?  鈹?  鈹斺攢鈹€ token_service.py # Token鏈嶅姟
鈹?  鈹斺攢鈹€ repositories/         # 鏁版嵁璁块棶灞?
鈹?      鈹溾攢鈹€ __init__.py
鈹?      鈹溾攢鈹€ user_repository.py    # 鐢ㄦ埛鏁版嵁璁块棶
鈹?      鈹斺攢鈹€ token_repository.py   # Token鏁版嵁璁块棶
鈹溾攢鈹€ tests/                     # 娴嬭瘯鐩綍
鈹?  鈹溾攢鈹€ unit/               # 鍗曞厓娴嬭瘯
鈹?  鈹斺攢鈹€ integration/        # 闆嗘垚娴嬭瘯
鈹溾攢鈹€ alembic/                   # 鏁版嵁搴撹縼绉?
鈹?  鈹溾攢鈹€ env.py              # 杩佺Щ鐜閰嶇疆
鈹?  鈹溾攢鈹€ script.py.mako      # 杩佺Щ鑴氭湰妯℃澘
鈹?  鈹斺攢鈹€ versions/           # 杩佺Щ鐗堟湰
鈹溾攢鈹€ scripts/                   # 鑴氭湰宸ュ叿
鈹溾攢鈹€ .env.development          # 寮€鍙戠幆澧冮厤缃?
鈹溾攢鈹€ .env.production           # 鐢熶骇鐜閰嶇疆
鈹溾攢鈹€ Dockerfile                # Docker閰嶇疆
鈹溾攢鈹€ docker-compose.yml        # Docker缂栨帓
鈹溾攢鈹€ requirements.txt          # Python渚濊禆
鈹斺攢鈹€ README.md                 # 鏈枃浠?
```

## 蹇€熷紑濮?

### 鏈湴寮€鍙?

```bash
# 瀹夎渚濊禆
pip install -r requirements.txt

# 閰嶇疆鐜鍙橀噺
cp .env.development .env

# 鍚姩鏈嶅姟
python -m uvicorn app.main:app --host 0.0.0.0 --port 28001 --reload
```

### Docker閮ㄧ讲

```bash
# 鏋勫缓闀滃儚
docker build -t auth-service:latest .

# 鍚姩鏈嶅姟
docker-compose up -d

# 鏌ョ湅鏃ュ織
docker-compose logs -f auth-service
```

## API鎺ュ彛

### 鍋ュ悍妫€鏌?

- `GET /health` - 鍋ュ悍妫€鏌ユ帴鍙?

### 璁よ瘉鎺ュ彛

- `POST /api/v1/auth/login` - 鐢ㄦ埛鐧诲綍
- `POST /api/v1/auth/refresh` - 鍒锋柊Token
- `POST /api/v1/auth/logout` - 鐢ㄦ埛鐧诲嚭

## 鐜鍙橀噺

| 鍙橀噺鍚?| 璇存槑 | 榛樿鍊?|
|--------|------|--------|
| APP_NAME | 搴旂敤鍚嶇О | 璁よ瘉鍩熸湇鍔?|
| APP_ENV | 鐜绫诲瀷 | development |
| APP_DEBUG | 璋冭瘯妯″紡 | True |
| APP_PORT | 鏈嶅姟绔彛 | 28001 |
| DATABASE_URL | 鏁版嵁搴撹繛鎺RL | - |
| REDIS_HOST | Redis涓绘満 | 127.0.0.1 |
| REDIS_PORT | Redis绔彛 | 6379 |
| JWT_SECRET | JWT瀵嗛挜 | - |
| JWT_EXPIRE_MINUTES | Token杩囨湡鏃堕棿锛堝垎閽燂級 | 1440 |
| REFRESH_TOKEN_EXPIRE_DAYS | 鍒锋柊Token杩囨湡鏃堕棿锛堝ぉ锛?| 30 |

## 鏁版嵁搴撹縼绉?

```bash
# 鐢熸垚杩佺Щ鑴氭湰
alembic revision --autogenerate -m "鍒涘缓鐢ㄦ埛琛?

# 鎵ц杩佺Щ
alembic upgrade head

# 鍥炴粴杩佺Щ
alembic downgrade -1
```

## 娴嬭瘯

```bash
# 杩愯鎵€鏈夋祴璇?
pytest

# 杩愯鍗曞厓娴嬭瘯
pytest tests/unit

# 杩愯闆嗘垚娴嬭瘯
pytest tests/integration

# 鐢熸垚娴嬭瘯鎶ュ憡
pytest --html=reports/test-report.html
```

## 寮€鍙戣鑼?

- 閬靛惊 PEP 8 浠ｇ爜瑙勮寖
- 浣跨敤绫诲瀷娉ㄨВ
- 缂栧啓鍗曞厓娴嬭瘯
- 娣诲姞鏃ュ織璁板綍
- 缂栧啓鏂囨。娉ㄩ噴

## 甯歌闂

### 鏁版嵁搴撹繛鎺ュけ璐?

妫€鏌?MySQL 鏈嶅姟鏄惁鍚姩锛屾暟鎹簱閰嶇疆鏄惁姝ｇ‘銆?

### Token楠岃瘉澶辫触

妫€鏌?JWT_SECRET 閰嶇疆鏄惁姝ｇ‘锛孴oken鏄惁杩囨湡銆?

### 渚濊禆瀹夎澶辫触

灏濊瘯浣跨敤铏氭嫙鐜锛屾垨鑰呭崌绾?pip 鐗堟湰銆?

## 鑱旂郴鏂瑰紡

- 椤圭洰鍦板潃: https://github.com/klpk961224/mcp-platform
- 闂鍙嶉: 鎻愪氦 Issue

---

**鏈€鍚庢洿鏂?*: 2026-01-15
