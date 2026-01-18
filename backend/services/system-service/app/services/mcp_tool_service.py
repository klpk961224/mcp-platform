# -*- coding: utf-8 -*-
"""
MCP宸ュ叿鏈嶅姟

鍔熻兘璇存槑锛?1. MCP宸ュ叿绠＄悊
2. MCP宸ュ叿璋冪敤
3. MCP宸ュ叿鐩戞帶

浣跨敤绀轰緥锛?    from app.services.mcp_tool_service import MCPToolService
    
    tool_service = MCPToolService(db)
    tool = tool_service.create_tool(name="鏁版嵁鍒嗘瀽", code="data_analysis")
"""

from sqlalchemy.orm import Session
from loguru import logger
from typing import Optional, Dict, Any, List
import httpx
from datetime import datetime

from common.database.models.system import MCPTool
from app.repositories.mcp_tool_repository import MCPToolRepository


class MCPToolService:
    """
    MCP宸ュ叿鏈嶅姟
    
    鍔熻兘锛?    - MCP宸ュ叿绠＄悊
    - MCP宸ュ叿璋冪敤
    - MCP宸ュ叿鐩戞帶
    
    浣跨敤鏂规硶锛?        tool_service = MCPToolService(db)
        tool = tool_service.create_tool(name="鏁版嵁鍒嗘瀽", code="data_analysis")
    """
    
    def __init__(self, db: Session):
        """
        鍒濆鍖朚CP宸ュ叿鏈嶅姟
        
        Args:
            db: 鏁版嵁搴撲細璇?        """
        self.db = db
        self.tool_repo = MCPToolRepository(db)
    
    def create_tool(self, tool_data: Dict[str, Any]) -> MCPTool:
        """
        鍒涘缓MCP宸ュ叿
        
        Args:
            tool_data: 宸ュ叿鏁版嵁
        
        Returns:
            MCPTool: 鍒涘缓鐨勫伐鍏峰璞?        
        Raises:
            ValueError: 宸ュ叿缂栫爜宸插瓨鍦?        """
        logger.info(f"鍒涘缓MCP宸ュ叿: name={tool_data.get('name')}, code={tool_data.get('code')}")
        
        # 妫€鏌ュ伐鍏风紪鐮佹槸鍚﹀凡瀛樺湪
        if self.tool_repo.exists_by_code(tool_data.get("code")):
            raise ValueError("宸ュ叿缂栫爜宸插瓨鍦?)
        
        # 鍒涘缓宸ュ叿
        tool = MCPTool(**tool_data)
        return self.tool_repo.create(tool)
    
    def get_tool(self, tool_id: str) -> Optional[MCPTool]:
        """
        鑾峰彇宸ュ叿
        
        Args:
            tool_id: 宸ュ叿ID
        
        Returns:
            Optional[MCPTool]: 宸ュ叿瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.tool_repo.get_by_id(tool_id)
    
    def get_tool_by_code(self, code: str) -> Optional[MCPTool]:
        """
        鏍规嵁缂栫爜鑾峰彇宸ュ叿
        
        Args:
            code: 宸ュ叿缂栫爜
        
        Returns:
            Optional[MCPTool]: 宸ュ叿瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        return self.tool_repo.get_by_code(code)
    
    def update_tool(self, tool_id: str, tool_data: Dict[str, Any]) -> Optional[MCPTool]:
        """
        鏇存柊宸ュ叿
        
        Args:
            tool_id: 宸ュ叿ID
            tool_data: 宸ュ叿鏁版嵁
        
        Returns:
            Optional[MCPTool]: 鏇存柊鍚庣殑宸ュ叿瀵硅薄锛屼笉瀛樺湪杩斿洖None
        """
        logger.info(f"鏇存柊MCP宸ュ叿: tool_id={tool_id}")
        
        tool = self.tool_repo.get_by_id(tool_id)
        if not tool:
            return None
        
        # 鏇存柊宸ュ叿
        for key, value in tool_data.items():
            if hasattr(tool, key):
                setattr(tool, key, value)
        
        return self.tool_repo.update(tool)
    
    def delete_tool(self, tool_id: str) -> bool:
        """
        鍒犻櫎宸ュ叿
        
        Args:
            tool_id: 宸ュ叿ID
        
        Returns:
            bool: 鍒犻櫎鏄惁鎴愬姛
        """
        logger.info(f"鍒犻櫎MCP宸ュ叿: tool_id={tool_id}")
        return self.tool_repo.delete(tool_id)
    
    def list_tools(self, tenant_id: Optional[str] = None, keyword: Optional[str] = None,
                   status: Optional[str] = None, is_public: Optional[bool] = None,
                   page: int = 1, page_size: int = 10) -> List[MCPTool]:
        """
        鑾峰彇宸ュ叿鍒楄〃
        
        Args:
            tenant_id: 绉熸埛ID锛堝彲閫夛級
            keyword: 鎼滅储鍏抽敭璇嶏紙鍙€夛級
            status: 鐘舵€侊紙鍙€夛級
            is_public: 鏄惁鍏紑锛堝彲閫夛級
            page: 椤电爜
            page_size: 姣忛〉鏁伴噺
        
        Returns:
            List[MCPTool]: 宸ュ叿鍒楄〃
        """
        if keyword:
            return self.tool_repo.search(keyword, tenant_id, page, page_size)
        elif tenant_id:
            return self.tool_repo.get_available_tools(tenant_id, page, page_size)
        else:
            return self.tool_repo.get_all(page, page_size)
    
    async def execute_tool(self, tool_id: str, params: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """
        鎵цMCP宸ュ叿
        
        Args:
            tool_id: 宸ュ叿ID
            params: 鍙傛暟
            user_id: 鐢ㄦ埛ID
        
        Returns:
            Dict[str, Any]: 鎵ц缁撴灉
        
        Raises:
            ValueError: 宸ュ叿涓嶅瓨鍦ㄦ垨涓嶅彲鐢?            ValueError: 鍙傛暟楠岃瘉澶辫触
        """
        logger.info(f"鎵цMCP宸ュ叿: tool_id={tool_id}, user_id={user_id}")
        
        # 鑾峰彇宸ュ叿
        tool = self.tool_repo.get_by_id(tool_id)
        if not tool:
            raise ValueError("宸ュ叿涓嶅瓨鍦?)
        
        if not tool.is_available():
            raise ValueError("宸ュ叿涓嶅彲鐢?)
        
        # 鎵ц宸ュ叿
        result = await self._execute_http_request(tool, params)
        
        # 鏇存柊缁熻淇℃伅
        tool.increment_call_count(success=True)
        self.tool_repo.update(tool)
        
        return result
    
    async def _execute_http_request(self, tool: MCPTool, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        鎵цHTTP璇锋眰
        
        Args:
            tool: 宸ュ叿瀵硅薄
            params: 鍙傛暟
        
        Returns:
            Dict[str, Any]: 鎵ц缁撴灉
        """
        timeout = tool.api_timeout
        
        async with httpx.AsyncClient(timeout=timeout) as client:
            try:
                if tool.api_method.upper() == "GET":
                    response = await client.get(tool.api_endpoint, params=params)
                elif tool.api_method.upper() == "POST":
                    response = await client.post(tool.api_endpoint, json=params)
                elif tool.api_method.upper() == "PUT":
                    response = await client.put(tool.api_endpoint, json=params)
                elif tool.api_method.upper() == "DELETE":
                    response = await client.delete(tool.api_endpoint, json=params)
                else:
                    raise ValueError(f"涓嶆敮鎸佺殑HTTP鏂规硶: {tool.api_method}")
                
                response.raise_for_status()
                return response.json()
                
            except httpx.HTTPError as e:
                logger.error(f"HTTP璇锋眰澶辫触: {e}")
                raise ValueError(f"HTTP璇锋眰澶辫触: {str(e)}")
    
    def get_tool_statistics(self, tool_id: str) -> Dict[str, Any]:
        """
        鑾峰彇宸ュ叿缁熻淇℃伅
        
        Args:
            tool_id: 宸ュ叿ID
        
        Returns:
            Dict[str, Any]: 缁熻淇℃伅
        """
        tool = self.tool_repo.get_by_id(tool_id)
        if not tool:
            return {}
        
        return {
            "tool_id": tool.id,
            "name": tool.name,
            "call_count": tool.call_count,
            "success_count": tool.success_count,
            "fail_count": tool.fail_count,
            "success_rate": tool.get_success_rate(),
            "last_called_at": tool.last_called_at.isoformat() if tool.last_called_at else None,
        }
    
    def count_tools(self, tenant_id: Optional[str] = None) -> int:
        """
        缁熻宸ュ叿鏁伴噺
        
        Args:
            tenant_id: 绉熸埛ID锛堝彲閫夛級
        
        Returns:
            int: 宸ュ叿鏁伴噺
        """
        if tenant_id:
            return self.tool_repo.count_by_tenant(tenant_id)
        else:
            return self.tool_repo.count_all()
