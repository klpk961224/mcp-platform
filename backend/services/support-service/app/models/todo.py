# -*- coding: utf-8 -*-
"""
寰呭姙浠诲姟妯″瀷

鍔熻兘璇存槑锛?1. 涓汉寰呭姙浠诲姟绠＄悊
2. 姣忔棩璁″垝绠＄悊
3. 浠诲姟鎻愰啋

浣跨敤绀轰緥锛?    from app.models.todo import TodoTask, DailyPlan
    
    # 创建寰呭姙浠诲姟
    todo = TodoTask(
        title="瀹屾垚椤圭洰鏂囨。",
        description="缂栧啓椤圭洰璁捐鏂囨。",
        priority="high"
    )
"""

from common.database.models.todo import TodoTask, DailyPlan

# 閲嶆柊瀵煎嚭妯″瀷锛屾柟渚夸娇鐢?__all__ = ['TodoTask', 'DailyPlan']
