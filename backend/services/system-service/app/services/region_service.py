"""
地区Service

提供地区业务逻辑层
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session

from common.database.models.region import Region
from app.repositories.region_repository import RegionRepository


class RegionService:
    """地区Service"""

    # 地区级别常量
    LEVEL_PROVINCE = "province"  # 省
    LEVEL_CITY = "city"  # 市
    LEVEL_DISTRICT = "district"  # 区
    LEVEL_STREET = "street"  # 街道

    # 状态常量
    STATUS_ACTIVE = "active"
    STATUS_INACTIVE = "inactive"

    def __init__(self, db: Session):
        self.db = db
        self.repository = RegionRepository(db)

    def get_region_by_id(self, region_id: str) -> Optional[Dict[str, Any]]:
        """根据ID获取地区"""
        region = self.repository.get_by_id(region_id)
        if not region:
            return None
        return self._to_dict(region)

    def get_region_by_code(self, code: str) -> Optional[Dict[str, Any]]:
        """根据地区编码获取"""
        region = self.repository.get_by_code(code)
        if not region:
            return None
        return self._to_dict(region)

    def get_all_regions(self, skip: int = 0, limit: int = 100) -> Dict[str, Any]:
        """获取所有地区"""
        regions = self.repository.get_all(skip=skip, limit=limit)
        total = self.repository.count()
        return {
            "items": [self._to_dict(r) for r in regions],
            "total": total
        }

    def get_regions_by_level(self, level: str, skip: int = 0, limit: int = 100) -> Dict[str, Any]:
        """根据地区级别获取地区"""
        regions = self.repository.get_by_level(level, skip=skip, limit=limit)
        total = self.repository.count_by_level(level)
        return {
            "items": [self._to_dict(r) for r in regions],
            "total": total
        }

    def get_regions_by_parent(self, parent_id: Optional[str], skip: int = 0, limit: int = 100) -> Dict[str, Any]:
        """根据父级ID获取子地区"""
        regions = self.repository.get_by_parent_id(parent_id, skip=skip, limit=limit)
        total = self.repository.count_by_parent(parent_id)
        return {
            "items": [self._to_dict(r) for r in regions],
            "total": total
        }

    def get_children(self, region_id: str, skip: int = 0, limit: int = 100) -> Dict[str, Any]:
        """获取子地区"""
        regions = self.repository.get_children(region_id, skip=skip, limit=limit)
        total = self.repository.count_by_parent(region_id)
        return {
            "items": [self._to_dict(r) for r in regions],
            "total": total
        }

    def get_all_children(self, region_id: str) -> List[Dict[str, Any]]:
        """获取所有子地区（递归）"""
        regions = self.repository.get_all_children(region_id)
        return [self._to_dict(r) for r in regions]

    def get_region_tree(self, parent_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """获取地区树"""
        return self.repository.get_tree(parent_id)

    def search_regions(
        self,
        query_params: Dict[str, Any],
        skip: int = 0,
        limit: int = 100
    ) -> Dict[str, Any]:
        """搜索地区"""
        regions, total = self.repository.search(query_params, skip=skip, limit=limit)
        return {
            "items": [self._to_dict(r) for r in regions],
            "total": total
        }

    def create_region(
        self,
        name: str,
        code: str,
        level: str,
        parent_id: Optional[str] = None,
        sort_order: int = 0
    ) -> Dict[str, Any]:
        """创建地区"""
        # 检查地区编码是否已存在
        existing = self.repository.get_by_code(code)
        if existing:
            raise ValueError(f"地区编码 {code} 已存在")

        # 验证父级ID
        if parent_id:
            parent = self.repository.get_by_id(parent_id)
            if not parent:
                raise ValueError(f"父级地区 {parent_id} 不存在")

        # 创建地区
        region = Region(
            name=name,
            code=code,
            level=level,
            parent_id=parent_id,
            sort_order=sort_order,
            status=self.STATUS_ACTIVE
        )

        region = self.repository.create(region)
        return self._to_dict(region)

    def update_region(
        self,
        region_id: str,
        name: Optional[str] = None,
        code: Optional[str] = None,
        level: Optional[str] = None,
        parent_id: Optional[str] = None,
        sort_order: Optional[int] = None,
        status: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """更新地区"""
        region = self.repository.get_by_id(region_id)
        if not region:
            return None

        # 更新字段
        if name is not None:
            region.name = name
        if code is not None:
            region.code = code
        if level is not None:
            region.level = level
        if parent_id is not None:
            region.parent_id = parent_id
        if sort_order is not None:
            region.sort_order = sort_order
        if status is not None:
            region.status = status

        region = self.repository.update(region)
        return self._to_dict(region)

    def delete_region(self, region_id: str) -> bool:
        """删除地区"""
        return self.repository.delete(region_id)

    def get_statistics(self) -> Dict[str, Any]:
        """获取地区统计信息"""
        total = self.repository.count()

        # 按级别统计
        level_stats = {}
        for level in [self.LEVEL_PROVINCE, self.LEVEL_CITY, self.LEVEL_DISTRICT, self.LEVEL_STREET]:
            level_stats[level] = self.repository.count_by_level(level)

        # 按状态统计
        active_count = self.repository.search({"status": self.STATUS_ACTIVE}, skip=0, limit=999999)[1]
        inactive_count = self.repository.search({"status": self.STATUS_INACTIVE}, skip=0, limit=999999)[1]

        # 顶级地区数量
        top_level_count = self.repository.count_by_parent(None)

        return {
            "total": total,
            "by_level": level_stats,
            "by_status": {
                "active": active_count,
                "inactive": inactive_count
            },
            "top_level_count": top_level_count
        }

    def _to_dict(self, region: Region) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": region.id,
            "name": region.name,
            "code": region.code,
            "level": region.level,
            "parent_id": region.parent_id,
            "sort_order": region.sort_order,
            "status": region.status,
            "created_at": region.created_at.isoformat() if region.created_at else None,
            "updated_at": region.updated_at.isoformat() if region.updated_at else None
        }