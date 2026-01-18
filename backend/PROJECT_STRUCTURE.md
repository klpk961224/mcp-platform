# 浼佷笟绾I缁煎悎绠＄悊骞冲彴 - 椤圭洰缁撴瀯璇存槑

## 馃搵 鏂囨。淇℃伅

- **椤圭洰鍚嶇О**锛氫紒涓氱骇AI缁煎悎绠＄悊骞冲彴
- **鏂囨。鐗堟湰**锛歷1.1
- **鍒涘缓鏃ユ湡**锛?026-01-15
- **鏈€鍚庢洿鏂?*锛?026-01-18
- **鏂囨。绫诲瀷**锛氶」鐩粨鏋勮鏄庢枃妗?
---

## 1. 姒傝堪

鏈」鐩噰鐢?*浼佷笟绾astAPI寰湇鍔℃鏋?*锛岄伒寰爣鍑嗙殑鍒嗗眰鏋舵瀯璁捐锛岀‘淇濅唬鐮佺殑鍙淮鎶ゆ€с€佸彲鎵╁睍鎬у拰鍙祴璇曟€с€?
### 1.1 鏋舵瀯鐗圭偣

- 鉁?**寰湇鍔℃灦鏋?*锛?涓嫭绔嬬殑寰湇鍔★紝姣忎釜鏈嶅姟璐熻矗鐗瑰畾鐨勪笟鍔″姛鑳?- 鉁?**鍒嗗眰鏋舵瀯**锛欰PI璺敱灞傘€佷笟鍔￠€昏緫灞傘€佹暟鎹闂眰銆佹暟鎹ā鍨嬪眰
- 鉁?**Repository妯″紡**锛氬皝瑁呮暟鎹闂€昏緫锛屾彁楂樹唬鐮佸鐢ㄦ€?- 鉁?**Service妯″紡**锛氬皝瑁呬笟鍔￠€昏緫锛屾彁楂樹唬鐮佸彲缁存姢鎬?- 鉁?**渚濊禆娉ㄥ叆**锛氫娇鐢‵astAPI鐨勪緷璧栨敞鍏ョ郴缁燂紝鎻愰珮浠ｇ爜鍙祴璇曟€?- 鉁?**缁熶竴閰嶇疆**锛氫娇鐢≒ydantic杩涜閰嶇疆绠＄悊锛屾敮鎸佸鐜閰嶇疆
- 鉁?**鏁版嵁搴撹縼绉?*锛氫娇鐢ˋlembic杩涜鏁版嵁搴撶増鏈鐞?- 鉁?**瀹瑰櫒鍖栭儴缃?*锛氭敮鎸丏ocker鍜孌ocker Compose閮ㄧ讲

### 1.2 鎶€鏈爤

| 鎶€鏈粍浠?| 鐗堟湰 | 鐢ㄩ€?|
|---------|------|------|
| **Python** | 3.13+ | 缂栫▼璇█ |
| **FastAPI** | 0.104+ | Web妗嗘灦 |
| **SQLAlchemy** | 2.0+ | ORM妗嗘灦 |
| **Pydantic** | 2.0+ | 鏁版嵁楠岃瘉 |
| **Alembic** | 1.12+ | 鏁版嵁搴撹縼绉?|
| **MySQL** | 8.0+ | 涓绘暟鎹簱 |
| **Redis** | 7.0+ | 缂撳瓨 |
| **RabbitMQ** | 3.12+ | 娑堟伅闃熷垪 |
| **Docker** | 24.0+ | 瀹瑰櫒鍖?|

---

## 2. 鏁翠綋鐩綍缁撴瀯

```
backend/
鈹溾攢鈹€ common/                          # 鍏变韩浠ｇ爜搴擄紙鎵€鏈夋湇鍔″叡鐢級
鈹?  鈹溾攢鈹€ cache/                       # 缂撳瓨妯″潡
鈹?  鈹溾攢鈹€ config/                      # 閰嶇疆妯″潡
鈹?  鈹溾攢鈹€ database/                    # 鏁版嵁搴撴ā鍧?鈹?  鈹溾攢鈹€ decorators/                  # 瑁呴グ鍣?鈹?  鈹溾攢鈹€ exceptions/                  # 寮傚父绫?鈹?  鈹溾攢鈹€ middleware/                  # 涓棿浠?鈹?  鈹溾攢鈹€ responses/                   # 鍝嶅簲妯″潡
鈹?  鈹溾攢鈹€ security/                    # 瀹夊叏妯″潡
鈹?  鈹斺攢鈹€ utils/                       # 宸ュ叿妯″潡
鈹?鈹溾攢鈹€ services/                        # 寰湇鍔＄洰褰?鈹?  鈹溾攢鈹€ auth-service/                # 璁よ瘉鍩熸湇鍔★紙28001锛?鈹?  鈹溾攢鈹€ user-service/                # 鐢ㄦ埛鍩熸湇鍔★紙28002锛?鈹?  鈹溾攢鈹€ permission-service/          # 鏉冮檺鍩熸湇鍔★紙28003锛?鈹?  鈹溾攢鈹€ system-service/              # 绯荤粺鍩熸湇鍔★紙28004锛?鈹?  鈹溾攢鈹€ support-service/             # 鏀拺鍩熸湇鍔★紙28005锛?鈹?  鈹斺攢鈹€ business-service/            # 涓氬姟鍩熸湇鍔★紙28006锛?鈹?鈹溾攢鈹€ tests/                           # 闆嗘垚娴嬭瘯
鈹溾攢鈹€ scripts/                         # 宸ュ叿鑴氭湰
鈹?  鈹溾攢鈹€ init_db.sql                 # 鏁版嵁搴撹〃缁撴瀯鍒濆鍖栬剼鏈?鈹?  鈹溾攢鈹€ execute_init_db.py          # 鎵ц鏁版嵁搴撹〃缁撴瀯鍒濆鍖?鈹?  鈹溾攢鈹€ init_data.py                # 鍒濆鍖栭粯璁ゆ暟鎹紙瓒呯骇绠＄悊鍛樸€佽鑹叉潈闄愮瓑锛?鈹?  鈹斺攢鈹€ ...                         # 鍏朵粬宸ュ叿鑴氭湰
鈹溾攢鈹€ alembic.ini                      # Alembic鍏ㄥ眬閰嶇疆
鈹溾攢鈹€ docker-compose.yml               # Docker缂栨帓閰嶇疆锛?涓井鏈嶅姟锛?鈹溾攢鈹€ start_services.bat               # 鍚姩鎵€鏈夋湇鍔?鈹溾攢鈹€ stop_services.bat                # 鍋滄鎵€鏈夋湇鍔?鈹溾攢鈹€ run_tests.bat                    # 杩愯娴嬭瘯
鈹斺攢鈹€ __init__.py                      # 鍖呭垵濮嬪寲鏂囦欢
```

---

## 3. 鍏变韩浠ｇ爜搴擄紙common/锛?
鍏变韩浠ｇ爜搴撳寘鍚墍鏈夊井鏈嶅姟鍏辩敤鐨勪唬鐮侊紝閬垮厤閲嶅寮€鍙戯紝鎻愰珮浠ｇ爜澶嶇敤鎬с€?
### 3.1 鐩綍缁撴瀯

```
common/
鈹溾攢鈹€ cache/                           # 缂撳瓨妯″潡
鈹?  鈹溾攢鈹€ local.py                     # 鏈湴缂撳瓨瀹炵幇
鈹?  鈹斺攢鈹€ redis.py                     # Redis缂撳瓨瀹炵幇
鈹?鈹溾攢鈹€ config/                          # 閰嶇疆妯″潡
鈹?  鈹溾攢鈹€ __init__.py
鈹?  鈹溾攢鈹€ constants.py                 # 甯搁噺瀹氫箟
鈹?  鈹斺攢鈹€ settings.py                  # 閰嶇疆绫伙紙Pydantic锛?鈹?鈹溾攢鈹€ database/                        # 鏁版嵁搴撴ā鍧?鈹?  鈹溾攢鈹€ __init__.py
鈹?  鈹溾攢鈹€ base.py                      # 鍩虹妯″瀷绫伙紙BaseModel锛?鈹?  鈹溾攢鈹€ connection.py                # 澶氭暟鎹簮绠＄悊鍣?鈹?  鈹溾攢鈹€ pandas_helper.py             # Pandas鏁版嵁鍒嗘瀽鍔╂墜
鈹?  鈹溾攢鈹€ session.py                   # 鏁版嵁搴撲細璇濈鐞?鈹?  鈹溾攢鈹€ transaction.py               # 璺ㄦ暟鎹簮浜嬪姟绠＄悊锛圫aga妯″紡锛?鈹?  鈹斺攢鈹€ models/                      # 鍏变韩鏁版嵁妯″瀷
鈹?      鈹溾攢鈹€ __init__.py
鈹?      鈹溾攢鈹€ permission.py            # 鏉冮檺鐩稿叧妯″瀷
鈹?      鈹溾攢鈹€ system.py                # 绯荤粺鐩稿叧妯″瀷
鈹?      鈹溾攢鈹€ tenant.py                # 绉熸埛鐩稿叧妯″瀷
鈹?      鈹溾攢鈹€ todo.py                  # 寰呭姙浠诲姟妯″瀷
鈹?      鈹溾攢鈹€ user.py                  # 鐢ㄦ埛鐩稿叧妯″瀷
鈹?      鈹斺攢鈹€ workflow.py              # 宸ヤ綔娴佺浉鍏虫ā鍨?鈹?鈹溾攢鈹€ decorators/                      # 瑁呴グ鍣?鈹?  鈹溾攢鈹€ __init__.py
鈹?  鈹溾攢鈹€ cache.py                     # 缂撳瓨瑁呴グ鍣?鈹?  鈹斺攢鈹€ permission.py                # 鏉冮檺瑁呴グ鍣?鈹?鈹溾攢鈹€ exceptions/                      # 寮傚父绫?鈹?  鈹溾攢鈹€ __init__.py
鈹?  鈹斺攢鈹€ base.py                      # 鍩虹寮傚父绫?鈹?鈹溾攢鈹€ middleware/                      # 涓棿浠?鈹?  鈹溾攢鈹€ __init__.py
鈹?  鈹溾攢鈹€ auth.py                      # 璁よ瘉涓棿浠?鈹?  鈹溾攢鈹€ exception.py                 # 寮傚父澶勭悊涓棿浠?鈹?  鈹斺攢鈹€ logging.py                   # 鏃ュ織涓棿浠?鈹?鈹溾攢鈹€ responses/                       # 鍝嶅簲妯″潡
鈹?  鈹溾攢鈹€ __init__.py
鈹?  鈹斺攢鈹€ base.py                      # 缁熶竴鍝嶅簲鏍煎紡
鈹?鈹溾攢鈹€ security/                        # 瀹夊叏妯″潡
鈹?  鈹溾攢鈹€ __init__.py
鈹?  鈹溾攢鈹€ api_key.py                   # API Key绠＄悊
鈹?  鈹溾攢鈹€ jwt.py                       # JWT宸ュ叿
鈹?  鈹斺攢鈹€ password.py                  # 瀵嗙爜鍔犲瘑
鈹?鈹斺攢鈹€ utils/                           # 宸ュ叿妯″潡
    鈹溾攢鈹€ __init__.py
    鈹溾攢鈹€ datetime.py                  # 鏃ユ湡鏃堕棿宸ュ叿
    鈹溾攢鈹€ helpers.py                   # 杈呭姪鍑芥暟
    鈹斺攢鈹€ validators.py                # 楠岃瘉鍣?```

### 3.2 鏍稿績妯″潡璇存槑

#### 3.2.1 鏁版嵁搴撴ā鍧楋紙database/锛?
**base.py** - 鍩虹妯″瀷绫诲拰Mixin绫?```python
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

BaseModel = declarative_base()

# Mixin绫诲畾涔?class TimestampMixin:
    """鏃堕棿鎴虫贩鍏ョ被 - 鎻愪緵created_at鍜寀pdated_at瀛楁"""
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False, comment='鍒涘缓鏃堕棿')
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False, comment='鏇存柊鏃堕棿')

class SoftDeleteMixin:
    """杞垹闄ゆ贩鍏ョ被 - 鎻愪緵is_deleted鍜宒eleted_at瀛楁"""
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, comment='鏄惁鍒犻櫎')
    deleted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True, comment='鍒犻櫎鏃堕棿')

class AuditMixin:
    """瀹¤娣峰叆绫?- 鎻愪緵created_by銆乽pdated_by銆乨eleted_by瀛楁"""
    created_by: Mapped[str] = mapped_column(String(50), nullable=True, comment='鍒涘缓浜?)
    updated_by: Mapped[str] = mapped_column(String(50), nullable=True, comment='鏇存柊浜?)
    deleted_by: Mapped[str] = mapped_column(String(50), nullable=True, comment='鍒犻櫎浜?)

class FullModelMixin(TimestampMixin, SoftDeleteMixin, AuditMixin):
    """瀹屾暣妯″瀷娣峰叆绫?- 缁勫悎浠ヤ笂涓変釜Mixin锛屾彁渚涘畬鏁寸殑瀹¤鍜屾椂闂存埑鍔熻兘"""
    pass

class CreatedAtMixin:
    """浠呭垱寤烘椂闂存贩鍏ョ被 - 浠呮彁渚沜reated_at瀛楁锛堢敤浜庢棩蹇楄〃锛?""
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False, comment='鍒涘缓鏃堕棿')

class BaseModel(BaseModel):
    """鎵€鏈夋暟鎹ā鍨嬬殑鍩虹被锛堝凡寮冪敤锛屼粎鐢ㄤ簬鍏煎锛?""
    
    __abstract__ = True
    
    id = Column(String(64), primary_key=True, comment="涓婚敭ID")
```

**Mixin绫荤户鎵垮叧绯?*锛?- **FullModelMixin**: 缁ф壙TimestampMixin銆丼oftDeleteMixin銆丄uditMixin锛堢敤浜庢牳蹇冧笟鍔″疄浣擄級
- **TimestampMixin**: 浠呮彁渚沜reated_at鍜寀pdated_at瀛楁锛堢敤浜庨厤缃被瀹炰綋锛?- **CreatedAtMixin**: 浠呮彁渚沜reated_at瀛楁锛堢敤浜庢棩蹇楃被瀹炰綋锛?
**浣跨敤绀轰緥**锛?```python
# 鏍稿績涓氬姟瀹炰綋浣跨敤FullModelMixin
class User(BaseModel, FullModelMixin):
    """鐢ㄦ埛琛?""
    __tablename__ = 'users'
    # ... 鍏朵粬瀛楁

# 閰嶇疆绫诲疄浣撲娇鐢═imestampMixin
class Dict(BaseModel, TimestampMixin):
    """瀛楀吀琛?""
    __tablename__ = 'dicts'
    # ... 鍏朵粬瀛楁

# 鏃ュ織绫诲疄浣撲娇鐢–reatedAtMixin
class LoginLog(BaseModel, CreatedAtMixin):
    """鐧诲綍鏃ュ織琛?""
    __tablename__ = 'login_logs'
    # ... 鍏朵粬瀛楁
```

**connection.py** - 澶氭暟鎹簮绠＄悊鍣?```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Dict, Optional

class DatasourceManager:
    """澶氭暟鎹簮绠＄悊鍣?""
    
    def __init__(self):
        self.engines: Dict[str, Any] = {}
        self.session_makers: Dict[str, Any] = {}
    
    def register_datasource(
        self,
        name: str,
        db_type: str,
        host: str,
        port: int,
        username: str,
        password: str,
        database: str,
        pool_size: int = 10,
        max_overflow: int = 20,
        echo: bool = False
    ):
        """娉ㄥ唽鏁版嵁婧?""
        # 鍒涘缓鏁版嵁搴撹繛鎺RL
        if db_type == "mysql":
            url = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
        elif db_type == "postgresql":
            url = f"postgresql://{username}:{password}@{host}:{port}/{database}"
        elif db_type == "oracle":
            url = f"oracle+cx_oracle://{username}:{password}@{host}:{port}/{database}"
        else:
            raise ValueError(f"涓嶆敮鎸佺殑鏁版嵁搴撶被鍨? {db_type}")
        
        # 鍒涘缓寮曟搸
        engine = create_engine(
            url,
            pool_size=pool_size,
            max_overflow=max_overflow,
            echo=echo
        )
        
        # 鍒涘缓浼氳瘽宸ュ巶
        session_maker = sessionmaker(bind=engine)
        
        # 淇濆瓨
        self.engines[name] = engine
        self.session_makers[name] = session_maker
    
    def get_session(self, name: str) -> Session:
        """鑾峰彇鏁版嵁搴撲細璇?""
        if name not in self.session_makers:
            raise ValueError(f"鏈壘鍒版暟鎹簮: {name}")
        return self.session_makers[name]()
    
    def close_all(self):
        """鍏抽棴鎵€鏈夎繛鎺?""
        for engine in self.engines.values():
            engine.dispose()

# 鍏ㄥ眬鏁版嵁婧愮鐞嗗櫒瀹炰緥
datasource_manager = DatasourceManager()
```

#### 3.2.2 閰嶇疆妯″潡锛坈onfig/锛?
**settings.py** - 閰嶇疆绫?```python
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """搴旂敤閰嶇疆绫?""
    
    # 搴旂敤閰嶇疆
    APP_NAME: str = "MCP Platform"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # 鏁版嵁搴撻厤缃?    DATABASE_URL: str = "mysql+pymysql://root:password@localhost:3306/mcp_platform"
    
    # Redis閰嶇疆
    REDIS_URL: str = "redis://localhost:6379/0"
    CACHE_ENABLED: bool = False
    CACHE_TYPE: str = "local"  # local or redis
    
    # JWT閰嶇疆
    JWT_SECRET_KEY: str = "your-secret-key"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # RabbitMQ閰嶇疆
    RABBITMQ_URL: str = "amqp://guest:guest@localhost:5672/"
    USE_RABBITMQ: bool = False
    
    # Nacos閰嶇疆
    NACOS_SERVER: str = "localhost:8848"
    USE_NACOS: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# 鍏ㄥ眬閰嶇疆瀹炰緥
settings = Settings()
```

#### 3.2.3 瀹夊叏妯″潡锛坰ecurity/锛?
**jwt.py** - JWT宸ュ叿
```python
from datetime import datetime, timedelta
from typing import Dict, Optional
import jwt
from common.config.settings import settings

def create_access_token(data: Dict, expires_delta: Optional[timedelta] = None) -> str:
    """鍒涘缓璁块棶浠ょ墝"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: Dict) -> str:
    """鍒涘缓鍒锋柊浠ょ墝"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[Dict]:
    """楠岃瘉浠ょ墝"""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None
```

---

## 4. 寰湇鍔＄粨鏋?
姣忎釜寰湇鍔￠兘閬靛惊缁熶竴鐨勭洰褰曠粨鏋勶紝纭繚浠ｇ爜鐨勪竴鑷存€у拰鍙淮鎶ゆ€с€?
### 4.1 鏍囧噯鐩綍缁撴瀯

```
{service-name}/
鈹溾攢鈹€ app/                             # 搴旂敤涓荤洰褰?鈹?  鈹溾攢鈹€ api/                         # API璺敱灞?鈹?  鈹?  鈹斺攢鈹€ v1/                      # API鐗堟湰1
鈹?  鈹?      鈹斺攢鈹€ {module}.py          # 妯″潡API
鈹?  鈹溾攢鈹€ core/                        # 鏍稿績閰嶇疆
鈹?  鈹?  鈹溾攢鈹€ config.py                # 鏈嶅姟閰嶇疆
鈹?  鈹?  鈹溾攢鈹€ deps.py                  # 渚濊禆娉ㄥ叆
鈹?  鈹?  鈹斺攢鈹€ security.py              # 瀹夊叏閰嶇疆
鈹?  鈹溾攢鈹€ models/                      # 鏁版嵁妯″瀷灞傦紙SQLAlchemy ORM锛?鈹?  鈹?  鈹溾攢鈹€ __init__.py
鈹?  鈹?  鈹斺攢鈹€ {module}.py              # 妯″潡妯″瀷
鈹?  鈹溾攢鈹€ repositories/                # 鏁版嵁璁块棶灞?鈹?  鈹?  鈹溾攢鈹€ __init__.py
鈹?  鈹?  鈹斺攢鈹€ {module}_repository.py   # 妯″潡鏁版嵁璁块棶
鈹?  鈹溾攢鈹€ schemas/                     # Pydantic妯″瀷锛堣姹?鍝嶅簲楠岃瘉锛?鈹?  鈹?  鈹溾攢鈹€ __init__.py
鈹?  鈹?  鈹斺攢鈹€ {module}.py              # 妯″潡Schema
鈹?  鈹溾攢鈹€ services/                    # 涓氬姟閫昏緫灞?鈹?  鈹?  鈹溾攢鈹€ __init__.py
鈹?  鈹?  鈹斺攢鈹€ {module}_service.py      # 妯″潡涓氬姟閫昏緫
鈹?  鈹斺攢鈹€ main.py                      # FastAPI搴旂敤鍏ュ彛
鈹?鈹溾攢鈹€ alembic/                         # 鏁版嵁搴撹縼绉?鈹?  鈹溾攢鈹€ env.py                       # 杩佺Щ鐜閰嶇疆
鈹?  鈹溾攢鈹€ script.py.mako               # 杩佺Щ妯℃澘
鈹?  鈹斺攢鈹€ versions/                    # 杩佺Щ鐗堟湰鏂囦欢
鈹?鈹溾攢鈹€ scripts/                         # 宸ュ叿鑴氭湰
鈹溾攢鈹€ tests/                           # 娴嬭瘯鐩綍
鈹?  鈹溾攢鈹€ unit/                        # 鍗曞厓娴嬭瘯
鈹?  鈹?  鈹斺攢鈹€ __init__.py
鈹?  鈹斺攢鈹€ integration/                 # 闆嗘垚娴嬭瘯
鈹?      鈹斺攢鈹€ __init__.py
鈹?鈹溾攢鈹€ .env.development                 # 寮€鍙戠幆澧冮厤缃?鈹溾攢鈹€ .env.production                  # 鐢熶骇鐜閰嶇疆
鈹溾攢鈹€ docker-compose.yml               # Docker缂栨帓
鈹溾攢鈹€ Dockerfile                       # Docker闀滃儚鏋勫缓
鈹溾攢鈹€ requirements.txt                 # Python渚濊禆
鈹斺攢鈹€ README.md                        # 鏈嶅姟鏂囨。
```

### 4.2 鍒嗗眰鏋舵瀯璇﹁В

#### 4.2.1 API璺敱灞傦紙api/锛?
**鑱岃矗**锛?- 鎺ユ敹HTTP璇锋眰
- 鍙傛暟楠岃瘉锛圥ydantic Schema锛?- 璋冪敤涓氬姟閫昏緫灞?- 杩斿洖HTTP鍝嶅簲

**绀轰緥浠ｇ爜**锛?```python
# app/api/v1/users.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import UserService
from app.core.deps import get_db

router = APIRouter(prefix="/users", tags=["鐢ㄦ埛绠＄悊"])

@router.post("/", response_model=UserResponse, summary="鍒涘缓鐢ㄦ埛")
async def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """鍒涘缓鏂扮敤鎴?""
    user_service = UserService(db)
    user = user_service.create(user_data)
    return user

@router.get("/{user_id}", response_model=UserResponse, summary="鑾峰彇鐢ㄦ埛")
async def get_user(
    user_id: str,
    db: Session = Depends(get_db)
):
    """鑾峰彇鐢ㄦ埛璇︽儏"""
    user_service = UserService(db)
    user = user_service.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="鐢ㄦ埛涓嶅瓨鍦?)
    return user
```

#### 4.2.2 涓氬姟閫昏緫灞傦紙services/锛?
**鑱岃矗**锛?- 瀹炵幇涓氬姟閫昏緫
- 鍗忚皟澶氫釜Repository
- 瀹炵幇浜嬪姟绠＄悊
- 涓氬姟瑙勫垯楠岃瘉

**绀轰緥浠ｇ爜**锛?```python
# app/services/user_service.py
from typing import Optional, List
from app.repositories.user_repository import UserRepository
from app.repositories.department_repository import DepartmentRepository
from app.schemas.user import UserCreate

class UserService:
    """鐢ㄦ埛涓氬姟閫昏緫鏈嶅姟"""
    
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
        self.dept_repo = DepartmentRepository(db)
    
    def create(self, user_data: UserCreate) -> User:
        """鍒涘缓鐢ㄦ埛
        
        涓氬姟閫昏緫锛?        1. 楠岃瘉閮ㄩ棬鏄惁瀛樺湪
        2. 鍒涘缓鐢ㄦ埛
        3. 鍒嗛厤榛樿瑙掕壊
        """
        # 楠岃瘉閮ㄩ棬
        if user_data.department_id:
            dept = self.dept_repo.get_by_id(user_data.department_id)
            if not dept:
                raise ValueError("閮ㄩ棬涓嶅瓨鍦?)
        
        # 鍒涘缓鐢ㄦ埛
        user = self.user_repo.create(user_data)
        
        # 鍒嗛厤榛樿瑙掕壊锛堝彲閫夛級
        # self.role_repo.assign_default_role(user.id)
        
        return user
    
    def get_by_id(self, user_id: str) -> Optional[User]:
        """鏍规嵁ID鑾峰彇鐢ㄦ埛"""
        return self.user_repo.get_by_id(user_id)
```

#### 4.2.3 鏁版嵁璁块棶灞傦紙repositories/锛?
**鑱岃矗**锛?- 灏佽鏁版嵁搴撴搷浣?- 鎻愪緵CRUD鏂规硶
- 瀹炵幇鏌ヨ閫昏緫
- 鏁版嵁缂撳瓨锛堝彲閫夛級

**绀轰緥浠ｇ爜**锛?```python
# app/repositories/user_repository.py
from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.user import User

class UserRepository:
    """鐢ㄦ埛鏁版嵁璁块棶灞?""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, user_id: str) -> Optional[User]:
        """鏍规嵁ID鑾峰彇鐢ㄦ埛"""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_by_username(self, username: str) -> Optional[User]:
        """鏍规嵁鐢ㄦ埛鍚嶈幏鍙栫敤鎴?""
        return self.db.query(User).filter(User.username == username).first()
    
    def create(self, user_data: dict) -> User:
        """鍒涘缓鐢ㄦ埛"""
        user = User(**user_data)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def update(self, user_id: str, user_data: dict) -> Optional[User]:
        """鏇存柊鐢ㄦ埛"""
        user = self.get_by_id(user_id)
        if not user:
            return None
        
        for key, value in user_data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def delete(self, user_id: str) -> bool:
        """鍒犻櫎鐢ㄦ埛"""
        user = self.get_by_id(user_id)
        if not user:
            return False
        
        self.db.delete(user)
        self.db.commit()
        return True
    
    def list(self, skip: int = 0, limit: int = 100) -> List[User]:
        """鑾峰彇鐢ㄦ埛鍒楄〃"""
        return self.db.query(User).offset(skip).limit(limit).all()
```

#### 4.2.4 鏁版嵁妯″瀷灞傦紙models/锛?
**鑱岃矗**锛?- 瀹氫箟鏁版嵁搴撹〃缁撴瀯
- 瀹炵幇ORM鏄犲皠
- 瀹氫箟琛ㄥ叧绯?- 鏁版嵁楠岃瘉

**绀轰緥浠ｇ爜**锛?```python
# app/models/user.py
from sqlalchemy import Column, String, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from common.database.base import BaseModel

class User(BaseModel):
    """鐢ㄦ埛妯″瀷"""
    
    __tablename__ = "users"
    
    # 鍩烘湰淇℃伅
    tenant_id = Column(String(64), nullable=False, index=True, comment="绉熸埛ID")
    username = Column(String(50), nullable=False, unique=True, index=True, comment="鐢ㄦ埛鍚?)
    email = Column(String(100), nullable=False, index=True, comment="閭")
    password_hash = Column(String(255), nullable=False, comment="瀵嗙爜鍝堝笇")
    
    # 鐢ㄦ埛淇℃伅
    full_name = Column(String(100), nullable=True, comment="鍏ㄥ悕")
    phone = Column(String(20), nullable=True, comment="鎵嬫満鍙?)
    avatar = Column(String(255), nullable=True, comment="澶村儚URL")
    
    # 鐘舵€佷俊鎭?    status = Column(String(20), nullable=False, default="active", comment="鐘舵€侊紙active/disabled锛?)
    is_superuser = Column(Boolean, default=False, comment="鏄惁瓒呯骇绠＄悊鍛?)
    
    # 閮ㄩ棬鍜屽矖浣?    department_id = Column(String(64), nullable=True, comment="閮ㄩ棬ID")
    position_id = Column(String(64), nullable=True, comment="宀椾綅ID")
    
    # 鎵╁睍淇℃伅
    bio = Column(Text, nullable=True, comment="涓汉绠€浠?)
    preferences = Column(Text, nullable=True, comment="鐢ㄦ埛鍋忓ソ璁剧疆锛圝SON锛?)
    
    # 鍏崇郴
    tokens = relationship("Token", back_populates="user", cascade="all, delete-orphan")
    roles = relationship("Role", secondary="user_roles", back_populates="users")
    
    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"
```

### 4.3 渚濊禆娉ㄥ叆锛坉eps.py锛?
**鑱岃矗**锛?- 鎻愪緵鏁版嵁搴撲細璇?- 鎻愪緵璁よ瘉淇℃伅
- 鎻愪緵鍏朵粬渚濊禆椤?
**绀轰緥浠ｇ爜**锛?```python
# app/core/deps.py
from typing import Optional, Generator
from sqlalchemy.orm import Session
from common.database.connection import datasource_manager
from app.core.security import verify_token

def get_db() -> Generator[Session, None, None]:
    """鑾峰彇鏁版嵁搴撲細璇?""
    session = None
    try:
        session = datasource_manager.get_session('mysql')
        yield session
        session.commit()
    except Exception as e:
        if session:
            session.rollback()
        raise
    finally:
        if session:
            session.close()

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """鑾峰彇褰撳墠鐢ㄦ埛"""
    credentials_exception = HTTPException(
        status_code=401,
        detail="鏃犳硶楠岃瘉鍑嵁",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = verify_token(token)
    if payload is None:
        raise credentials_exception
    
    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    
    user_repo = UserRepository(db)
    user = user_repo.get_by_id(user_id)
    if user is None:
        raise credentials_exception
    
    return user
```

### 4.4 搴旂敤鍏ュ彛锛坢ain.py锛?
**鑱岃矗**锛?- 鍒涘缓FastAPI搴旂敤
- 娉ㄥ唽璺敱
- 閰嶇疆涓棿浠?- 閰嶇疆浜嬩欢澶勭悊

**绀轰緥浠ｇ爜**锛?```python
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from common.config.settings import settings
from common.database.connection import datasource_manager
from app.api.v1 import auth

# 鍒涘缓FastAPI搴旂敤
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="浼佷笟绾I缁煎悎绠＄悊骞冲彴 - 璁よ瘉鍩熸湇鍔?
)

# 閰嶇疆CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 娉ㄥ唽璺敱
app.include_router(auth.router, prefix="/api/v1")

# 鍚姩浜嬩欢
@app.on_event("startup")
async def startup_event():
    """搴旂敤鍚姩浜嬩欢"""
    logger.info(f"鍚姩 {settings.APP_NAME} v{settings.APP_VERSION}")
    
    # 娉ㄥ唽鏁版嵁婧?    try:
        db_url = settings.DATABASE_URL
        if db_url.startswith("mysql+pymysql://"):
            # 瑙ｆ瀽杩炴帴瀛楃涓?            url_without_prefix = db_url.replace("mysql+pymysql://", "")
            auth_part, host_port_db = url_without_prefix.split("@")
            username, password = auth_part.split(":")
            host_port, database = host_port_db.split("/")
            host, port = host_port.split(":")
            
            datasource_manager.register_datasource(
                name='mysql',
                db_type='mysql',
                host=host,
                port=int(port),
                username=username,
                password=password,
                database=database,
                pool_size=10,
                max_overflow=20,
                echo=False
            )
            logger.info("鏁版嵁婧愭敞鍐屾垚鍔?)
    except Exception as e:
        logger.error(f"鏁版嵁婧愭敞鍐屽け璐? {e}")
        raise

# 鍏抽棴浜嬩欢
@app.on_event("shutdown")
async def shutdown_event():
    """搴旂敤鍏抽棴浜嬩欢"""
    logger.info("鍏抽棴搴旂敤")
    datasource_manager.close_all()

# 鍋ュ悍妫€鏌?@app.get("/health")
async def health_check():
    """鍋ュ悍妫€鏌?""
    return {"status": "healthy", "service": "auth-service"}
```

---

## 5. 寰湇鍔″垪琛?
| 鏈嶅姟鍚嶇О | 绔彛 | 鑱岃矗 | 涓昏鍔熻兘 |
|---------|------|------|---------|
| **auth-service** | 28001 | 璁よ瘉鍩熸湇鍔?| JWT璁よ瘉銆丄PI Key璁よ瘉銆佹潈闄愭牎楠屻€乀oken绠＄悊 |
| **user-service** | 28002 | 鐢ㄦ埛鍩熸湇鍔?| 鐢ㄦ埛CRUD銆侀儴闂ㄧ鐞嗐€佺鎴风鐞嗐€佺敤鎴蜂笌閮ㄩ棬/瑙掕壊鍏宠仈 |
| **permission-service** | 28003 | 鏉冮檺鍩熸湇鍔?| 瑙掕壊绠＄悊銆佹潈闄愬垎閰嶃€佽彍鍗曠鐞嗐€佸姩鎬佽彍鍗曞姞杞?|
| **system-service** | 28004 | 绯荤粺鍩熸湇鍔?| MCP宸ュ叿娉ㄥ唽/璋冪敤銆佸鏁版嵁婧愮鐞嗐€佸瓧鍏哥鐞嗐€佺郴缁熼厤缃?|
| **support-service** | 28005 | 鏀拺鍩熸湇鍔?| 鐧诲綍鏃ュ織銆佹搷浣滄棩蹇椼€佺珯鍐呬俊銆侀€氱煡鍏憡銆佸緟鍔炰换鍔＄鐞?|
| **business-service** | 28006 | 涓氬姟鍩熸湇鍔?| 宸ヤ綔娴佺鐞嗭紙瀹℃壒娴佺▼銆佸彲瑙嗗寲璁捐鍣ㄣ€佸鎵逛换鍔＄鐞嗭級 |

---

## 6. 鏁版嵁搴撹縼绉伙紙Alembic锛?
### 6.1 Alembic閰嶇疆

**alembic/env.py** - 杩佺Щ鐜閰嶇疆
```python
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from common.database.base import BaseModel
from app.models import *  # 瀵煎叆鎵€鏈夋ā鍨?
# Alembic Config瀵硅薄
config = context.config

# 璁剧疆鏃ュ織
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 鐩爣鍏冩暟鎹?target_metadata = BaseModel.metadata

def run_migrations_offline() -> None:
    """绂荤嚎杩愯杩佺Щ"""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """鍦ㄧ嚎杩愯杩佺Щ"""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

### 6.2 鍒涘缓杩佺Щ

```bash
# 鍒涘缓杩佺Щ鑴氭湰
alembic revision --autogenerate -m "create users table"

# 鎵ц杩佺Щ
alembic upgrade head

# 鍥炴粴杩佺Щ
alembic downgrade -1
```

---

## 7. 娴嬭瘯

### 7.1 娴嬭瘯鐩綍缁撴瀯

```
tests/
鈹溾攢鈹€ unit/                           # 鍗曞厓娴嬭瘯
鈹?  鈹溾攢鈹€ __init__.py
鈹?  鈹溾攢鈹€ test_user_service.py
鈹?  鈹斺攢鈹€ test_user_repository.py
鈹?鈹斺攢鈹€ integration/                    # 闆嗘垚娴嬭瘯
    鈹溾攢鈹€ __init__.py
    鈹溾攢鈹€ test_user_api.py
    鈹斺攢鈹€ test_auth_api.py
```

### 7.2 娴嬭瘯绀轰緥

**鍗曞厓娴嬭瘯**锛?```python
# tests/unit/test_user_service.py
import pytest
from app.services.user_service import UserService
from app.schemas.user import UserCreate

def test_create_user(db_session):
    """娴嬭瘯鍒涘缓鐢ㄦ埛"""
    user_service = UserService(db_session)
    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        password_hash="hashed_password"
    )
    
    user = user_service.create(user_data)
    
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.id is not None
```

**闆嗘垚娴嬭瘯**锛?```python
# tests/integration/test_user_api.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user():
    """娴嬭瘯鍒涘缓鐢ㄦ埛API"""
    response = client.post(
        "/api/v1/users/",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
```

---

## 8. 閮ㄧ讲

### 8.1 Docker閮ㄧ讲

**Dockerfile**锛?```dockerfile
FROM python:3.13-slim

WORKDIR /app

# 瀹夎渚濊禆
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 澶嶅埗浠ｇ爜
COPY . .

# 鏆撮湶绔彛
EXPOSE 28001

# 鍚姩鍛戒护
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "28001"]
```

**docker-compose.yml**锛?```yaml
version: '3.8'

services:
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: mcp_platform
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql

  redis:
    image: redis:7.0
    ports:
      - "6379:6379"

  auth-service:
    build: ./services/auth-service
    ports:
      - "28001:28001"
    depends_on:
      - mysql
      - redis
    environment:
      - DATABASE_URL=mysql+pymysql://root:root@mysql:3306/mcp_platform
      - REDIS_URL=redis://redis:6379/0

volumes:
  mysql_data:
```

### 8.2 鍚姩鏈嶅姟

```bash
# 鍚姩鎵€鏈夋湇鍔?docker-compose up -d

# 鏌ョ湅鏃ュ織
docker-compose logs -f

# 鍋滄鏈嶅姟
docker-compose down
```

---

## 9. 鏈€浣冲疄璺?
### 9.1 浠ｇ爜瑙勮寖

- 鉁?閬靛惊PEP 8瑙勮寖
- 鉁?浣跨敤绫诲瀷鎻愮ず锛圱ype Hints锛?- 鉁?缂栧啓鏂囨。瀛楃涓诧紙Docstrings锛?- 鉁?浣跨敤鏈夋剰涔夌殑鍙橀噺鍚嶅拰鍑芥暟鍚?- 鉁?閬垮厤杩囧害宓屽

### 9.2 閿欒澶勭悊

- 鉁?浣跨敤鑷畾涔夊紓甯哥被
- 鉁?缁熶竴鐨勫紓甯稿鐞嗕腑闂翠欢
- 鉁?璇︾粏鐨勯敊璇棩蹇?- 鉁?鍙嬪ソ鐨勯敊璇秷鎭?
### 9.3 鎬ц兘浼樺寲

- 鉁?浣跨敤鏁版嵁搴撹繛鎺ユ睜
- 鉁?浣跨敤缂撳瓨锛圧edis锛?- 鉁?寮傛澶勭悊锛圧abbitMQ锛?- 鉁?鏁版嵁搴撶储寮曚紭鍖?
### 9.4 瀹夊叏鎬?
- 鉁?浣跨敤JWT璁よ瘉
- 鉁?瀵嗙爜鍔犲瘑瀛樺偍
- 鉁?SQL娉ㄥ叆闃叉姢
- 鉁?XSS闃叉姢
- 鉁?CSRF闃叉姢

### 9.5 鏃ュ織璁板綍

- 鉁?浣跨敤缁撴瀯鍖栨棩蹇楋紙loguru锛?- 鉁?璁板綍鍏抽敭鎿嶄綔
- 鉁?璁板綍寮傚父淇℃伅
- 鉁?鏃ュ織鍒嗙骇绠＄悊

---

## 10. 甯歌闂

### Q1: 濡備綍娣诲姞鏂扮殑寰湇鍔★紵

1. 鍦?`backend/services/` 涓嬪垱寤烘柊鐨勬湇鍔＄洰褰?2. 鎸夌収鏍囧噯鐩綍缁撴瀯鍒涘缓瀛愮洰褰曞拰鏂囦欢
3. 瀹炵幇 `app/main.py` 浣滀负搴旂敤鍏ュ彛
4. 鍒涘缓 `requirements.txt` 鍜岄厤缃枃浠?5. 鍒涘缓 `Dockerfile` 鍜?`docker-compose.yml`
6. 缂栧啓娴嬭瘯鐢ㄤ緥

### Q2: 濡備綍娣诲姞鏂扮殑API鎺ュ彛锛?
1. 鍦?`app/api/v1/` 涓嬪垱寤烘垨淇敼璺敱鏂囦欢
2. 浣跨敤FastAPI Router瀹氫箟璺敱
3. 浣跨敤Pydantic Schema瀹氫箟璇锋眰/鍝嶅簲妯″瀷
4. 鍦⊿ervice灞傚疄鐜颁笟鍔￠€昏緫
5. 鍦≧epository灞傚疄鐜版暟鎹闂?6. 缂栧啓娴嬭瘯鐢ㄤ緥

### Q3: 濡備綍娣诲姞鏂扮殑鏁版嵁搴撹〃锛?
1. 鍦?`app/models/` 涓嬪垱寤烘柊鐨勬ā鍨嬫枃浠?2. 缁ф壙 `BaseModel` 绫?3. 瀹氫箟琛ㄧ粨鏋勫拰瀛楁
4. 鍒涘缓Alembic杩佺Щ鑴氭湰
5. 鎵ц杩佺Щ
6. 缂栧啓娴嬭瘯鐢ㄤ緥

### Q4: 濡備綍璋冭瘯浠ｇ爜锛?
1. 浣跨敤 `print()` 鎴?`logger.info()` 杈撳嚭璋冭瘯淇℃伅
2. 浣跨敤IDE鐨勮皟璇曞姛鑳斤紙鏂偣璋冭瘯锛?3. 鏌ョ湅鏃ュ織鏂囦欢
4. 浣跨敤FastAPI鐨勮嚜鍔ㄦ枃妗ｏ紙Swagger UI锛?5. 浣跨敤Postman鎴朿url娴嬭瘯API

---

## 馃敆 鐩稿叧鏂囨。

- [鎶€鏈灦鏋勮璁℃枃妗(../doc/2-鎶€鏈灦鏋勮璁℃枃妗?md)
- [鏁版嵁搴撹璁℃枃妗(../doc/3-鏁版嵁搴撹璁℃枃妗?md)
- [API鎺ュ彛璁捐鏂囨。](../doc/4-API鎺ュ彛璁捐鏂囨。.md)
- [寮€鍙戣鑼冩枃妗(../doc/6-寮€鍙戣鑼冩枃妗?md)
- [鐜閰嶇疆鏂囨。](../doc/7-鐜閰嶇疆鏂囨。.md)

---

## 馃挕 娉ㄦ剰浜嬮」

1. **浠ｇ爜澶嶇敤**锛氫紭鍏堜娇鐢?`common/` 涓殑鍏变韩浠ｇ爜锛岄伩鍏嶉噸澶嶅紑鍙?2. **鍒嗗眰娓呮櫚**锛氫弗鏍奸伒瀹堝垎灞傛灦鏋勶紝涓嶈璺ㄥ眰璋冪敤
3. **渚濊禆娉ㄥ叆**锛氫娇鐢‵astAPI鐨勪緷璧栨敞鍏ョ郴缁燂紝鎻愰珮浠ｇ爜鍙祴璇曟€?4. **鏁版嵁搴撲細璇?*锛氫娇鐢?`get_db()` 渚濊禆娉ㄥ叆鑾峰彇鏁版嵁搴撲細璇濓紝涓嶈鎵嬪姩鍒涘缓
5. **浜嬪姟绠＄悊**锛氬湪Service灞傜鐞嗕簨鍔★紝涓嶈鍦≧epository灞傜鐞?6. **寮傚父澶勭悊**锛氫娇鐢ㄨ嚜瀹氫箟寮傚父绫伙紝缁熶竴寮傚父澶勭悊
7. **鏃ュ織璁板綍**锛氫娇鐢?`loguru` 璁板綍鏃ュ織锛屼笉瑕佷娇鐢?`print()`
8. **娴嬭瘯瑕嗙洊**锛氱紪鍐欏崟鍏冩祴璇曞拰闆嗘垚娴嬭瘯锛屼繚璇佷唬鐮佽川閲?9. **鏂囨。鏇存柊**锛氫唬鐮佸彉鏇存椂鍙婃椂鏇存柊鏂囨。锛屼繚鎸佹枃妗ｄ笌浠ｇ爜鍚屾
10. **鐗堟湰鎺у埗**锛氫娇鐢℅it杩涜鐗堟湰鎺у埗锛岄伒寰狦it Flow宸ヤ綔娴?
---

**鏂囨。鐗堟湰鍘嗗彶**锛?
| 鐗堟湰 | 鏃ユ湡 | 浣滆€?| 鍙樻洿璇存槑 |
|-----|------|------|---------|
| v1.0 | 2026-01-15 | AI鍔╂墜 | 鍒濆鐗堟湰锛岃褰曚紒涓氱骇椤圭洰缁撴瀯 |
| v1.1 | 2026-01-18 | AI鍔╂墜 | 鏇存柊Docker閰嶇疆锛屾坊鍔犳暟鎹垵濮嬪寲鑴氭湰璇存槑 |

---

**鏈€鍚庢洿鏂版椂闂?*锛?026-01-18
**涓嬫鏇存柊鏃堕棿**锛氶」鐩粨鏋勫彉鏇存椂
