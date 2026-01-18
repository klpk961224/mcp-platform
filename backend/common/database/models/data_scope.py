"""
鏁版嵁鑼冨洿鏉冮檺妯″瀷

鍔熻兘璇存槑锛?1. 鏁版嵁鑼冨洿绫诲瀷瀹氫箟
2. 鏁版嵁鑼冨洿鏉冮檺閰嶇疆
3. 鐢ㄦ埛鏁版嵁鑼冨洿鏉冮檺鍏宠仈

浣跨敤绀轰緥锛?    from common.database.models.data_scope import DataScope, UserDataScope
    
    # 鍒涘缓鏁版嵁鑼冨洿
    data_scope = DataScope(
        name="鏈儴闂ㄦ暟鎹?,
        code="department",
        description="鍙兘鏌ョ湅鏈儴闂ㄧ殑鏁版嵁"
    )
"""

from sqlalchemy import Column, String, Text, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from ..base import BaseModel, TimestampMixin


class DataScope(BaseModel, TimestampMixin):
    """
    鏁版嵁鑼冨洿绫诲瀷琛?
    鍔熻兘锛?    - 瀹氫箟鏁版嵁鑼冨洿绫诲瀷锛堝叏閮ㄣ€佹湰閮ㄩ棬銆佹湰閮ㄩ棬鍙婁互涓嬨€佷粎鏈汉绛夛級
    - 閰嶇疆鏁版嵁鑼冨洿鐨勬弿杩板拰璇存槑

    灞炴€ц鏄庯細
    - id: 鏁版嵁鑼冨洿ID锛堜富閿級
    - name: 鏁版嵁鑼冨洿鍚嶇О
    - code: 鏁版嵁鑼冨洿缂栫爜锛坅ll/department/department_and_below/self锛?    - description: 鎻忚堪
    - level: 鏉冮檺绾у埆锛堟暟瀛楄秺澶ф潈闄愯秺楂橈級
    - created_at: 鍒涘缓鏃堕棿
    - updated_at: 鏇存柊鏃堕棿
    """

    __tablename__ = "data_scopes"

    # 鍩烘湰淇℃伅
    name = Column(String(100), nullable=False, comment="鏁版嵁鑼冨洿鍚嶇О")
    code = Column(String(50), nullable=False, unique=True, comment="鏁版嵁鑼冨洿缂栫爜")
    description = Column(Text, nullable=True, comment="鎻忚堪")

    # 鏉冮檺绾у埆
    level = Column(Integer, nullable=False, default=0, comment="鏉冮檺绾у埆")

    def __repr__(self):
        return f"<DataScope(id={self.id}, name={self.name}, code={self.code})>"

    def to_dict(self):
        """杞崲涓哄瓧鍏?""
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "description": self.description,
            "level": self.level,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class UserDataScope(BaseModel, TimestampMixin):
    """
    鐢ㄦ埛鏁版嵁鑼冨洿鏉冮檺琛?
    鍔熻兘锛?    - 瀹氫箟鐢ㄦ埛鐨勬暟鎹寖鍥存潈闄?    - 鏀寔鎸夋ā鍧楅厤缃笉鍚岀殑鏁版嵁鑼冨洿

    灞炴€ц鏄庯細
    - id: 鐢ㄦ埛鏁版嵁鑼冨洿ID锛堜富閿級
    - user_id: 鐢ㄦ埛ID
    - module: 妯″潡锛坲ser/department/tenant绛夛級
    - data_scope_id: 鏁版嵁鑼冨洿ID
    - created_at: 鍒涘缓鏃堕棿
    - updated_at: 鏇存柊鏃堕棿
    """

    __tablename__ = "user_data_scopes"

    # 鍩烘湰淇℃伅
    user_id = Column(String(50), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, comment="鐢ㄦ埛ID")
    module = Column(String(50), nullable=False, comment="妯″潡")
    data_scope_id = Column(String(50), ForeignKey("data_scopes.id", ondelete="CASCADE"), nullable=False, comment="鏁版嵁鑼冨洿ID")

    # 鍏崇郴
    user = relationship("User", backref="data_scopes")
    data_scope = relationship("DataScope", backref="user_data_scopes")

    def __repr__(self):
        return f"<UserDataScope(id={self.id}, user_id={self.user_id}, module={self.module}, data_scope_id={self.data_scope_id})>"

    def to_dict(self):
        """杞崲涓哄瓧鍏?""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "module": self.module,
            "data_scope_id": self.data_scope_id,
            "data_scope_name": self.data_scope.name if self.data_scope else None,
            "data_scope_code": self.data_scope.code if self.data_scope else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
