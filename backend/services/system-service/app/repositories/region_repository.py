"""
地区Repository

提供地区数据访问层
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from common.database.models.region import Region


class RegionRepository:
    """地区Repository"""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, region_id: str) -> Optional[Region]:
        """根据ID获取地区"""
        return self.db.query(Region).filter(Region.id == region_id).first()

    def get_by_code(self, code: str) -> Optional[Region]:
        """根据地区编码获取"""
        return self.db.query(Region).filter(Region.code == code).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Region]:
        """获取所有地区"""
        return self.db.query(Region).order_by(Region.sort_order).offset(skip).limit(limit).all()

    def get_by_level(self, level: str, skip: int = 0, limit: int = 100) -> List[Region]:
        """根据地区级别获取地区"""
        return self.db.query(Region).filter(
            Region.level == level,
            Region.status == "active"
        ).order_by(Region.sort_order).offset(skip).limit(limit).all()

    def get_by_parent_id(self, parent_id: Optional[str], skip: int = 0, limit: int = 100) -> List[Region]:
        """根据父级ID获取子地区"""
        if parent_id:
            return self.db.query(Region).filter(
                Region.parent_id == parent_id,
                Region.status == "active"
            ).order_by(Region.sort_order).offset(skip).limit(limit).all()
        else:
            # 获取顶级地区（省级）
            return self.db.query(Region).filter(
                Region.parent_id.is_(None),
                Region.status == "active"
            ).order_by(Region.sort_order).offset(skip).limit(limit).all()

    def get_children(self, region_id: str, skip: int = 0, limit: int = 100) -> List[Region]:
        """获取子地区"""
        return self.get_by_parent_id(region_id, skip=skip, limit=limit)

    def get_all_children(self, region_id: str) -> List[Region]:
        """获取所有子地区（递归）"""
        region = self.get_by_id(region_id)
        if not region:
            return []

        children = []
        self._collect_children(region, children)
        return children

    def _collect_children(self, region: Region, children: List[Region]):
        """递归收集子地区"""
        for child in region.children:
            children.append(child)
            self._collect_children(child, children)

    def get_tree(self, parent_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """获取地区树"""
        regions = self.get_by_parent_id(parent_id)
        tree = []
        for region in regions:
            tree.append({
                "id": region.id,
                "name": region.name,
                "code": region.code,
                "level": region.level,
                "parent_id": region.parent_id,
                "sort_order": region.sort_order,
                "status": region.status,
                "children": self.get_tree(region.id)
            })
        return tree

    def search(self, query_params: Dict[str, Any], skip: int = 0, limit: int = 100) -> tuple:
        """搜索地区"""
        query = self.db.query(Region)

        # 地区名称搜索
        if query_params.get("name"):
            query = query.filter(Region.name.like(f"%{query_params['name']}%"))

        # 地区编码搜索
        if query_params.get("code"):
            query = query.filter(Region.code.like(f"%{query_params['code']}%"))

        # 地区级别过滤
        if query_params.get("level"):
            query = query.filter(Region.level == query_params["level"])

        # 父级ID过滤
        if query_params.get("parent_id"):
            query = query.filter(Region.parent_id == query_params["parent_id"])

        # 状态过滤
        if query_params.get("status"):
            query = query.filter(Region.status == query_params["status"])

        # 统计总数
        total = query.count()

        # 分页
        regions = query.order_by(Region.sort_order).offset(skip).limit(limit).all()

        return regions, total

    def create(self, region: Region) -> Region:
        """创建地区"""
        self.db.add(region)
        self.db.commit()
        self.db.refresh(region)
        return region

    def update(self, region: Region) -> Region:
        """更新地区"""
        self.db.commit()
        self.db.refresh(region)
        return region

    def delete(self, region_id: str) -> bool:
        """删除地区"""
        region = self.get_by_id(region_id)
        if region:
            self.db.delete(region)
            self.db.commit()
            return True
        return False

    def count(self) -> int:
        """统计地区数量"""
        return self.db.query(Region).count()

    def count_by_level(self, level: str) -> int:
        """根据地区级别统计数量"""
        return self.db.query(Region).filter(Region.level == level).count()

    def count_by_parent(self, parent_id: Optional[str]) -> int:
        """根据父级ID统计子地区数量"""
        if parent_id:
            return self.db.query(Region).filter(Region.parent_id == parent_id).count()
        else:
            return self.db.query(Region).filter(Region.parent_id.is_(None)).count()