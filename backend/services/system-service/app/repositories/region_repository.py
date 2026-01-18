"""
鍦板尯Repository

鎻愪緵鍦板尯鏁版嵁璁块棶灞?"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from common.database.models.region import Region


class RegionRepository:
    """鍦板尯Repository"""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, region_id: str) -> Optional[Region]:
        """鏍规嵁ID鑾峰彇鍦板尯"""
        return self.db.query(Region).filter(Region.id == region_id).first()

    def get_by_code(self, code: str) -> Optional[Region]:
        """鏍规嵁鍦板尯缂栫爜鑾峰彇"""
        return self.db.query(Region).filter(Region.code == code).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Region]:
        """鑾峰彇鎵€鏈夊湴鍖?""
        return self.db.query(Region).order_by(Region.sort_order).offset(skip).limit(limit).all()

    def get_by_level(self, level: str, skip: int = 0, limit: int = 100) -> List[Region]:
        """鏍规嵁鍦板尯绾у埆鑾峰彇鍦板尯"""
        return self.db.query(Region).filter(
            Region.level == level,
            Region.status == "active"
        ).order_by(Region.sort_order).offset(skip).limit(limit).all()

    def get_by_parent_id(self, parent_id: Optional[str], skip: int = 0, limit: int = 100) -> List[Region]:
        """鏍规嵁鐖剁骇ID鑾峰彇瀛愬湴鍖?""
        if parent_id:
            return self.db.query(Region).filter(
                Region.parent_id == parent_id,
                Region.status == "active"
            ).order_by(Region.sort_order).offset(skip).limit(limit).all()
        else:
            # 鑾峰彇椤剁骇鍦板尯锛堢渷绾э級
            return self.db.query(Region).filter(
                Region.parent_id.is_(None),
                Region.status == "active"
            ).order_by(Region.sort_order).offset(skip).limit(limit).all()

    def get_children(self, region_id: str, skip: int = 0, limit: int = 100) -> List[Region]:
        """鑾峰彇瀛愬湴鍖?""
        return self.get_by_parent_id(region_id, skip=skip, limit=limit)

    def get_all_children(self, region_id: str) -> List[Region]:
        """鑾峰彇鎵€鏈夊瓙鍦板尯锛堥€掑綊锛?""
        region = self.get_by_id(region_id)
        if not region:
            return []

        children = []
        self._collect_children(region, children)
        return children

    def _collect_children(self, region: Region, children: List[Region]):
        """閫掑綊鏀堕泦瀛愬湴鍖?""
        for child in region.children:
            children.append(child)
            self._collect_children(child, children)

    def get_tree(self, parent_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """鑾峰彇鍦板尯鏍?""
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
        """鎼滅储鍦板尯"""
        query = self.db.query(Region)

        # 鍦板尯鍚嶇О鎼滅储
        if query_params.get("name"):
            query = query.filter(Region.name.like(f"%{query_params['name']}%"))

        # 鍦板尯缂栫爜鎼滅储
        if query_params.get("code"):
            query = query.filter(Region.code.like(f"%{query_params['code']}%"))

        # 鍦板尯绾у埆杩囨护
        if query_params.get("level"):
            query = query.filter(Region.level == query_params["level"])

        # 鐖剁骇ID杩囨护
        if query_params.get("parent_id"):
            query = query.filter(Region.parent_id == query_params["parent_id"])

        # 鐘舵€佽繃婊?        if query_params.get("status"):
            query = query.filter(Region.status == query_params["status"])

        # 缁熻鎬绘暟
        total = query.count()

        # 鍒嗛〉
        regions = query.order_by(Region.sort_order).offset(skip).limit(limit).all()

        return regions, total

    def create(self, region: Region) -> Region:
        """鍒涘缓鍦板尯"""
        self.db.add(region)
        self.db.commit()
        self.db.refresh(region)
        return region

    def update(self, region: Region) -> Region:
        """鏇存柊鍦板尯"""
        self.db.commit()
        self.db.refresh(region)
        return region

    def delete(self, region_id: str) -> bool:
        """鍒犻櫎鍦板尯"""
        region = self.get_by_id(region_id)
        if region:
            self.db.delete(region)
            self.db.commit()
            return True
        return False

    def count(self) -> int:
        """缁熻鍦板尯鏁伴噺"""
        return self.db.query(Region).count()

    def count_by_level(self, level: str) -> int:
        """鏍规嵁鍦板尯绾у埆缁熻鏁伴噺"""
        return self.db.query(Region).filter(Region.level == level).count()

    def count_by_parent(self, parent_id: Optional[str]) -> int:
        """鏍规嵁鐖剁骇ID缁熻瀛愬湴鍖烘暟閲?""
        if parent_id:
            return self.db.query(Region).filter(Region.parent_id == parent_id).count()
        else:
            return self.db.query(Region).filter(Region.parent_id.is_(None)).count()
