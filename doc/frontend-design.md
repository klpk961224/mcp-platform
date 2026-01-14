# 企业级AI综合管理平台 - 前端UI/UX设计方案

## 🎨 设计理念

### 美学方向
**风格定位**：现代科技感 + 专业精致

**核心特征**：
- 深色主题，专业稳重
- 玻璃态设计（Glassmorphism）
- 精致的渐变和光效
- 流畅的动画过渡
- 不对称的现代布局

### 色彩系统

**主色调**：
```css
--primary-dark: #0a0e17;      /* 深蓝黑背景 */
--primary-light: #1a1f2e;     /* 次级背景 */
--accent-blue: #00d4ff;       /* 霓虹蓝强调 */
--accent-cyan: #00ff9d;        /* 霓虹青强调 */
--accent-purple: #b388ff;     /* 霓虹紫强调 */
--text-primary: #e2e8f0;      /* 主文本 */
--text-secondary: #94a3b8;    /* 次级文本 */
--border-color: rgba(255, 255, 255, 0.1);  /* 边框色 */
```

**渐变系统**：
```css
--gradient-primary: linear-gradient(135deg, #00d4ff 0%, #00ff9d 100%);
--gradient-dark: linear-gradient(180deg, #0a0e17 0%, #1a1f2e 100%);
--gradient-glass: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
```

### 字体系统

**字体选择**：
- **标题字体**：Orbitron（科技感显示字体）
- **正文字体**：Plus Jakarta Sans（现代几何字体）
- **等宽字体**：JetBrains Mono（代码显示）

**字体大小**：
```css
--font-xs: 0.75rem;      /* 12px */
--font-sm: 0.875rem;     /* 14px */
--font-base: 1rem;       /* 16px */
--font-lg: 1.125rem;     /* 18px */
--font-xl: 1.25rem;      /* 20px */
--font-2xl: 1.5rem;      /* 24px */
--font-3xl: 1.875rem;    /* 30px */
```

---

## 📐 整体布局结构

### 布局框架

```
┌─────────────────────────────────────────────────────────────┐
│  Header（顶部导航）                                            │
├──────────────────┬────────────────────────────────────────────┤
│                  │                                            │
│  Sidebar        │  Main Content Area（主内容区）            │
│  （侧边栏）      │                                            │
│                  │                                            │
│  - 用户信息      │  - 页面标题                                │
│  - 导航菜单      │  - 操作栏                                  │
│  - 快捷操作      │  - 内容卡片                                │
│                  │                                            │
└──────────────────┴────────────────────────────────────────────┘
```

### 设计特点

1. **侧边栏**：
   - 固定宽度：260px
   - 玻璃态效果
   - 微妙的光晕边框
   - 渐变背景

2. **主内容区**：
   - 不对称布局
   - 卡片式设计
   - 流畅的动画过渡
   - 悬停效果

3. **顶部导航**：
   - 简洁的面包屑
   - 搜索栏
   - 用户操作菜单

---

## 🎯 核心页面设计

### 1. 登录页（Login Page）

**设计特点**：
- 全屏渐变背景
- 中心卡片式登录表单
- 动态粒子效果
- 玻璃态卡片

**布局代码**：
```vue
<template>
  <div class="login-container">
    <!-- 背景粒子效果 -->
    <div class="particles"></div>
    
    <!-- 登录卡片 -->
    <div class="login-card">
      <div class="login-header">
        <div class="logo">
          <span class="logo-icon">AI</span>
          <h1 class="logo-text">MCP Platform</h1>
        </div>
        <p class="subtitle">企业级AI综合管理平台</p>
      </div>
      
      <div class="login-form">
        <div class="form-group">
          <label class="form-label">用户名</label>
          <input 
            type="text" 
            class="form-input"
            placeholder="请输入用户名"
          />
        </div>
        
        <div class="form-group">
          <label class="form-label">密码</label>
          <input 
            type="password" 
            class="form-input"
            placeholder="请输入密码"
          />
        </div>
        
        <button class="login-btn">
          <span class="btn-text">登录</span>
          <div class="btn-glow"></div>
        </button>
      </div>
      
      <div class="login-footer">
        <a href="#" class="forgot-link">忘记密码？</a>
      </div>
    </div>
  </div>
</template>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--primary-dark);
  position: relative;
  overflow: hidden;
}

/* 粒子背景 */
.particles {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: 
    radial-gradient(circle at 20% 30%, rgba(0, 212, 255, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 80% 70%, rgba(0, 255, 157, 0.08) 0%, transparent 50%),
    radial-gradient(circle at 40% 80%, rgba(179, 136, 255, 0.1) 0%, transparent 50%);
  animation: pulse 8s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

/* 登录卡片 */
.login-card {
  width: 480px;
  padding: 48px;
  background: var(--gradient-glass);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-color);
  border-radius: 24px;
  box-shadow: 
    0 25px 50px -12px rgba(0, 0, 0, 0.5),
    0 0 0 1px rgba(255, 255, 255, 0.05),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
  animation: cardFloat 6s ease-in-out infinite;
}

@keyframes cardFloat {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

/* Logo */
.login-header {
  text-align: center;
  margin-bottom: 48px;
}

.logo {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  margin-bottom: 16px;
}

.logo-icon {
  width: 56px;
  height: 56px;
  background: var(--gradient-primary);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  font-weight: bold;
  color: var(--primary-dark);
  box-shadow: 0 0 30px rgba(0, 212, 255, 0.4);
}

.logo-text {
  font-family: 'Orbitron', sans-serif;
  font-size: 32px;
  font-weight: 700;
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: 2px;
}

.subtitle {
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: var(--font-sm);
  color: var(--text-secondary);
  margin: 0;
}

/* 表单 */
.login-form {
  margin-bottom: 32px;
}

.form-group {
  margin-bottom: 24px;
}

.form-label {
  display: block;
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: var(--font-sm);
  color: var(--text-secondary);
  margin-bottom: 8px;
  font-weight: 500;
}

.form-input {
  width: 100%;
  padding: 16px 20px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  color: var(--text-primary);
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: var(--font-base);
  transition: all 0.3s ease;
}

.form-input:focus {
  outline: none;
  border-color: var(--accent-blue);
  box-shadow: 0 0 0 4px rgba(0, 212, 255, 0.1);
}

.form-input::placeholder {
  color: var(--text-secondary);
  opacity: 0.6;
}

/* 登录按钮 */
.login-btn {
  width: 100%;
  padding: 16px 32px;
  background: var(--gradient-primary);
  border: none;
  border-radius: 12px;
  color: var(--primary-dark);
  font-family: 'Orbitron', sans-serif;
  font-size: var(--font-lg);
  font-weight: 600;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  margin-top: 8px;
}

.login-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(0, 212, 255, 0.3);
}

.btn-text {
  position: relative;
  z-index: 1;
}

.btn-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  transition: width 0.6s ease, height 0.6s ease;
}

.login-btn:hover .btn-glow {
  width: 300px;
  height: 300px;
}

/* 底部链接 */
.login-footer {
  text-align: center;
}

.forgot-link {
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: var(--font-sm);
  color: var(--accent-blue);
  text-decoration: none;
  transition: color 0.3s ease;
}

.forgot-link:hover {
  color: var(--accent-cyan);
}
</style>

### 5. 待办任务管理页面（Todo Management）

#### 5.1 待办任务列表页

**设计特点**：
- 清晰的任务列表展示
- 优先级标识（高/中/低）
- 截止时间倒计时
- 快速操作按钮
- 筛选和搜索功能

**代码**：
```vue
<template>
  <div class="todo-management">
    <!-- 操作栏 -->
    <div class="action-bar">
      <div class="bar-left">
        <button class="btn-primary">
          <span>+</span>
          <span>新建任务</span>
        </button>
        <button class="btn-secondary">
          <span>📅</span>
          <span>每日计划</span>
        </button>
      </div>
      
      <div class="bar-right">
        <div class="filter-tabs">
          <button class="tab-btn active">全部</button>
          <button class="tab-btn">待办</button>
          <button class="tab-btn">进行中</button>
          <button class="tab-btn">已完成</button>
        </div>
        <div class="search-box">
          <input 
            type="text" 
            class="search-input"
            placeholder="搜索任务..."
          />
          <button class="search-btn">🔍</button>
        </div>
      </div>
    </div>
    
    <!-- 任务列表 -->
    <div class="task-list">
      <div 
        v-for="task in tasks" 
        :key="task.id"
        class="task-card"
        :class="`priority-${task.priority}`"
      >
        <div class="task-header">
          <div class="task-left">
            <input 
              type="checkbox" 
              class="task-checkbox"
              :checked="task.status === 'completed'"
              @change="toggleTaskComplete(task)"
            />
            <div class="task-priority-badge">
              <Icon 
                :icon="getPriorityIcon(task.priority)" 
                :size="16"
                :color="getPriorityColor(task.priority)"
              />
              <span>{{ getPriorityLabel(task.priority) }}</span>
            </div>
          </div>
          <div class="task-right">
            <div class="task-type-badge">
              <Icon 
                :icon="getTaskTypeIcon(task.task_type)" 
                :size="16"
              />
              <span>{{ getTaskTypeLabel(task.task_type) }}</span>
            </div>
            <button class="task-menu">⋮</button>
          </div>
        </div>
        
        <div class="task-body">
          <div class="task-title">{{ task.title }}</div>
          <div class="task-description">{{ task.description }}</div>
          
          <div class="task-meta">
            <div class="task-tags">
              <span 
                v-for="tag in task.tags" 
                :key="tag"
                class="tag"
              >
                {{ tag }}
              </span>
            </div>
            <div class="task-due-date" :class="getDueDateClass(task.due_date)">
              <Icon icon="mdi:calendar-clock" :size="14" />
              <span>{{ formatDate(task.due_date) }}</span>
            </div>
          </div>
        </div>
        
        <div class="task-footer">
          <div class="task-assignee">
            <div class="assignee-avatar">{{ task.user_name[0] }}</div>
          </div>
          <div class="task-actions">
            <button class="action-btn" @click="editTask(task)">
              <Icon icon="mdi:pencil" :size="16" />
            </button>
            <button class="action-btn" @click="deleteTask(task)">
              <Icon icon="mdi:delete" :size="16" />
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
```

#### 5.2 每日计划页

**设计特点**：
- 日历视图展示
- 今日任务统计
- 完成进度条
- 快速添加任务

**代码**：
```vue
<template>
  <div class="daily-plan">
    <!-- 统计卡片 -->
    <div class="stats-row">
      <div class="stat-card">
        <div class="stat-icon">📋</div>
        <div class="stat-content">
          <div class="stat-label">今日任务</div>
          <div class="stat-value">{{ todayTasks }}</div>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">✅</div>
        <div class="stat-content">
          <div class="stat-label">已完成</div>
          <div class="stat-value">{{ completedTasks }}</div>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">📊</div>
        <div class="stat-content">
          <div class="stat-label">完成率</div>
          <div class="stat-value">{{ completionRate }}%</div>
        </div>
        <div class="stat-progress">
          <div 
            class="progress-fill" 
            :style="{ width: completionRate + '%' }"
          ></div>
        </div>
      </div>
    </div>
    
    <!-- 任务列表 -->
    <div class="daily-task-list">
      <div class="list-header">
        <h3 class="list-title">今日任务</h3>
        <button class="add-task-btn">
          <span>+</span>
          <span>添加任务</span>
        </button>
      </div>
      
      <div 
        v-for="task in dailyTasks" 
        :key="task.id"
        class="daily-task-item"
        :class="{ completed: task.completed }"
      >
        <input 
          type="checkbox" 
          class="task-checkbox"
          :checked="task.completed"
          @change="toggleDailyTask(task)"
        />
        <div class="task-info">
          <div class="task-title">{{ task.title }}</div>
          <div class="task-time">{{ task.time }}</div>
        </div>
        <button class="task-delete" @click="deleteDailyTask(task)">
          <Icon icon="mdi:close" :size="16" />
        </button>
      </div>
    </div>
  </div>
</template>
```

### 6. 工作流管理页面（Workflow Management）

#### 6.1 工作流列表页

**设计特点**：
- 卡片式布局
- 工作流类型标识
- 状态标签
- 快捷操作按钮

**代码**：
```vue
<template>
  <div class="workflow-list">
    <!-- 操作栏 -->
    <div class="action-bar">
      <div class="bar-left">
        <button class="btn-primary">
          <span>+</span>
          <span>新建工作流</span>
        </button>
        <button class="btn-secondary">
          <span>📋</span>
          <span>从模板创建</span>
        </button>
      </div>
      
      <div class="bar-right">
        <div class="filter-tabs">
          <button class="tab-btn active">全部</button>
          <button class="tab-btn">人事审批</button>
          <button class="tab-btn">权限审批</button>
          <button class="tab-btn">财务审批</button>
          <button class="tab-btn">IT审批</button>
        </div>
        <div class="search-box">
          <input 
            type="text" 
            class="search-input"
            placeholder="搜索工作流..."
          />
          <button class="search-btn">🔍</button>
        </div>
      </div>
    </div>
    
    <!-- 工作流卡片列表 -->
    <div class="workflow-grid">
      <div 
        v-for="workflow in workflows" 
        :key="workflow.id"
        class="workflow-card"
      >
        <div class="card-header">
          <div class="workflow-type-badge">
            <Icon 
              :icon="getWorkflowTypeIcon(workflow.workflow_type)" 
              :size="20"
            />
            <span>{{ getWorkflowTypeLabel(workflow.workflow_type) }}</span>
          </div>
          <div class="workflow-status" :class="workflow.status">
            {{ getWorkflowStatusLabel(workflow.status) }}
          </div>
        </div>
        
        <div class="card-body">
          <h3 class="workflow-name">{{ workflow.name }}</h3>
          <p class="workflow-description">{{ workflow.description }}</p>
          
          <div class="workflow-meta">
            <div class="meta-item">
              <Icon icon="mdi:code-tags" :size="14" />
              <span>{{ workflow.code }}</span>
            </div>
            <div class="meta-item">
              <Icon icon="mdi:update" :size="14" />
              <span>{{ workflow.version }}</span>
            </div>
            <div class="meta-item">
              <Icon icon="mdi:account" :size="14" />
              <span>{{ workflow.created_by }}</span>
            </div>
          </div>
        </div>
        
        <div class="card-footer">
          <div class="workflow-stats">
            <div class="stat-item">
              <span class="stat-label">运行中</span>
              <span class="stat-value">{{ workflow.running_count }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">已完成</span>
              <span class="stat-value">{{ workflow.completed_count }}</span>
            </div>
          </div>
          
          <div class="workflow-actions">
            <button class="action-btn" @click="viewWorkflow(workflow)">
              <Icon icon="mdi:eye" :size="16" />
              <span>查看</span>
            </button>
            <button class="action-btn" @click="editWorkflow(workflow)">
              <Icon icon="mdi:pencil" :size="16" />
              <span>编辑</span>
            </button>
            <button class="action-btn" @click="copyWorkflow(workflow)">
              <Icon icon="mdi:content-copy" :size="16" />
              <span>复制</span>
            </button>
            <button class="action-btn" @click="deleteWorkflow(workflow)">
              <Icon icon="mdi:delete" :size="16" />
              <span>删除</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
```

#### 6.2 工作流设计器页

**设计特点**：
- 拖拽式节点编辑
- 流程图展示
- 节点配置面板
- 连接线配置

**代码**：
```vue
<template>
  <div class="workflow-designer">
    <!-- 工具栏 -->
    <div class="toolbar">
      <div class="toolbar-left">
        <button class="btn-primary" @click="saveWorkflow">
          <Icon icon="mdi:content-save" :size="16" />
          <span>保存</span>
        </button>
        <button class="btn-secondary" @click="publishWorkflow">
          <Icon icon="mdi:rocket-launch" :size="16" />
          <span>发布</span>
        </button>
      </div>
      
      <div class="toolbar-right">
        <button class="btn-secondary" @click="previewWorkflow">
          <Icon icon="mdi:play" :size="16" />
          <span>预览</span>
        </button>
        <button class="btn-secondary" @click="undo">
          <Icon icon="mdi:undo" :size="16" />
          <span>撤销</span>
        </button>
        <button class="btn-secondary" @click="redo">
          <Icon icon="mdi:redo" :size="16" />
          <span>重做</span>
        </button>
      </div>
    </div>
    
    <!-- 主内容区 -->
    <div class="designer-content">
      <!-- 节点工具栏 -->
      <div class="node-palette">
        <h4 class="palette-title">节点类型</h4>
        <div class="palette-items">
          <div 
            v-for="nodeType in nodeTypes" 
            :key="nodeType.type"
            class="palette-item"
            draggable="true"
            @dragstart="onNodeDragStart(nodeType)"
          >
            <Icon :icon="nodeType.icon" :size="24" />
            <span>{{ nodeType.label }}</span>
          </div>
        </div>
      </div>
      
      <!-- 流程图画布 -->
      <div class="canvas-container">
        <div class="canvas-toolbar">
          <button class="zoom-btn" @click="zoomIn">
            <Icon icon="mdi:magnify-plus" :size="16" />
          </button>
          <button class="zoom-btn" @click="zoomOut">
            <Icon icon="mdi:magnify-minus" :size="16" />
          </button>
          <button class="zoom-btn" @click="zoomFit">
            <Icon icon="mdi:fit-to-screen" :size="16" />
          </button>
        </div>
        
        <div 
          class="workflow-canvas"
          @drop="onNodeDrop"
          @dragover.prevent
        >
          <div 
            v-for="node in workflowNodes" 
            :key="node.id"
            class="workflow-node"
            :class="`node-${node.type} ${node.status}`"
            :style="{ left: node.x + 'px', top: node.y + 'px' }"
            @click="selectNode(node)"
            @mousedown="startNodeDrag(node, $event)"
          >
            <div class="node-icon">
              <Icon 
                :icon="getNodeTypeIcon(node.type)" 
                :size="24"
                :color="getNodeStatusColor(node.status)"
              />
            </div>
            <div class="node-label">{{ node.name }}</div>
            
            <!-- 当前节点高亮效果 -->
            <div v-if="node.status === 'in_progress'" class="node-highlight">
              <div class="pulse-ring"></div>
            </div>
          </div>
          
          <!-- 连接线 -->
          <svg class="edges">
            <line 
              v-for="edge in workflowEdges" 
              :key="edge.id"
              :x1="edge.from.x" 
              :y1="edge.from.y"
              :x2="edge.to.x" 
              :y2="edge.to.y"
              :stroke="getEdgeColor(edge.status)"
              stroke-width="2"
            />
          </svg>
        </div>
      </div>
      
      <!-- 属性面板 -->
      <div class="properties-panel">
        <h4 class="panel-title">节点属性</h4>
        
        <div v-if="selectedNode" class="node-properties">
          <div class="property-group">
            <label class="property-label">节点名称</label>
            <input 
              type="text" 
              class="property-input"
              v-model="selectedNode.name"
            />
          </div>
          
          <div class="property-group">
            <label class="property-label">节点类型</label>
            <div class="property-value">{{ getNodeTypeLabel(selectedNode.type) }}</div>
          </div>
          
          <div v-if="selectedNode.type === 'approval'" class="property-group">
            <label class="property-label">审批人</label>
            <select class="property-input" v-model="selectedNode.config.assignee">
              <option value="dept_leader">部门领导</option>
              <option value="role">角色</option>
              <option value="user">指定用户</option>
            </select>
          </div>
          
          <div v-if="selectedNode.type === 'approval'" class="property-group">
            <label class="property-label">审批方式</label>
            <select class="property-input" v-model="selectedNode.config.approval_type">
              <option value="single">单人审批</option>
              <option value="all">会签（全部同意）</option>
              <option value="any">或签（任一同意）</option>
            </select>
          </div>
          
          <div class="property-actions">
            <button class="btn-primary" @click="saveNodeProperties">
              <Icon icon="mdi:content-save" :size="16" />
              <span>保存</span>
            </button>
            <button class="btn-danger" @click="deleteNode">
              <Icon icon="mdi:delete" :size="16" />
              <span>删除</span>
            </button>
          </div>
        </div>
        
        <div v-else class="no-selection">
          <Icon icon="mdi:cursor-default-click" :size="48" />
          <p>请选择一个节点查看属性</p>
        </div>
      </div>
    </div>
  </div>
</template>
```

#### 6.3 工作流实例详情页

**设计特点**：
- 流程图高亮展示
- 节点进度条
- 审批记录
- 表单数据展示

**代码**：
```vue
<template>
  <div class="workflow-instance-detail">
    <!-- 流程进度 -->
    <div class="progress-section">
      <h3 class="section-title">流程进度</h3>
      <div class="workflow-diagram">
        <div 
          v-for="node in instanceNodes" 
          :key="node.id"
          class="diagram-node"
          :class="`node-${node.status}`"
          @click="viewNodeDetail(node)"
        >
          <div class="node-icon">
            <Icon 
              :icon="getNodeTypeIcon(node.type)" 
              :size="24"
              :color="getNodeStatusColor(node.status)"
            />
          </div>
          <div class="node-label">{{ node.name }}</div>
          <div class="node-status">
            <Icon 
              :icon="getNodeStatusIcon(node.status)" 
              :size="16"
              :color="getNodeStatusColor(node.status)"
            />
          </div>
          
          <!-- 当前节点高亮效果 -->
          <div v-if="node.status === 'in_progress'" class="node-highlight">
            <div class="pulse-ring"></div>
          </div>
        </div>
        
        <!-- 进度条 -->
        <div class="progress-bar">
          <div class="progress-label">流程进度</div>
          <div class="progress-track">
            <div 
              class="progress-fill" 
              :style="{ width: progressPercentage + '%' }"
            ></div>
          </div>
          <div class="progress-text">{{ progressPercentage }}% ({{ completedNodes }}/{{ totalNodes }} 节点完成)</div>
        </div>
      </div>
    </div>
    
    <!-- 基本信息 -->
    <div class="info-section">
      <h3 class="section-title">基本信息</h3>
      <div class="info-grid">
        <div class="info-item">
          <span class="info-label">实例编号</span>
          <span class="info-value">{{ instance.instance_no }}</span>
        </div>
        <div class="info-item">
          <span class="info-label">工作流名称</span>
          <span class="info-value">{{ instance.workflow_name }}</span>
        </div>
        <div class="info-item">
          <span class="info-label">申请人</span>
          <span class="info-value">{{ instance.created_by }}</span>
        </div>
        <div class="info-item">
          <span class="info-label">申请时间</span>
          <span class="info-value">{{ instance.started_at }}</span>
        </div>
        <div class="info-item">
          <span class="info-label">当前状态</span>
          <span class="info-value status-badge" :class="instance.status">
            {{ getInstanceStatusLabel(instance.status) }}
          </span>
        </div>
        <div class="info-item">
          <span class="info-label">当前节点</span>
          <span class="info-value">{{ instance.current_node_name }}</span>
        </div>
      </div>
    </div>
    
    <!-- 表单数据 -->
    <div class="form-section">
      <h3 class="section-title">表单数据</h3>
      <div class="form-data">
        <div 
          v-for="(value, key) in formData" 
          :key="key"
          class="form-field"
        >
          <span class="field-label">{{ key }}</span>
          <span class="field-value">{{ value }}</span>
        </div>
      </div>
    </div>
    
    <!-- 审批记录 -->
    <div class="approval-history">
      <h3 class="section-title">审批记录</h3>
      <div 
        v-for="record in approvalRecords" 
        :key="record.id"
        class="approval-record"
      >
        <div class="record-header">
          <div class="record-title">
            <Icon icon="mdi:account-check" :size="16" />
            <span>{{ record.node_name }}</span>
          </div>
          <div class="record-status" :class="record.status">
            {{ getApprovalStatusLabel(record.status) }}
          </div>
        </div>
        
        <div class="record-info">
          <span class="record-approver">审批人：{{ record.approver }}</span>
          <span class="record-time">时间：{{ record.completed_at }}</span>
        </div>
        
        <div v-if="record.comment" class="record-comment">
          <span class="comment-label">审批意见：</span>
          <span class="comment-text">{{ record.comment }}</span>
        </div>
        
        <div v-if="record.status === 'pending'" class="record-actions">
          <button class="btn-success" @click="approve(record)">
            <Icon icon="mdi:check" :size="16" />
            <span>同意</span>
          </button>
          <button class="btn-danger" @click="reject(record)">
            <Icon icon="mdi:close" :size="16" />
            <span>驳回</span>
          </button>
          <button class="btn-secondary" @click="transfer(record)">
            <Icon icon="mdi:arrow-right" :size="16" />
            <span>转交</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
```

#### 6.4 待办审批任务列表页

**设计特点**：
- 任务卡片展示
- 优先级标识
- 快速处理按钮
- 任务详情查看

**代码**：
```vue
<template>
  <div class="approval-tasks">
    <!-- 操作栏 -->
    <div class="action-bar">
      <div class="bar-left">
        <h3 class="page-title">我的待办</h3>
      </div>
      
      <div class="bar-right">
        <button class="btn-primary" @click="viewAllTasks">
          <span>查看全部</span>
        </button>
      </div>
    </div>
    
    <!-- 任务列表 -->
    <div class="task-list">
      <div 
        v-for="task in pendingTasks" 
        :key="task.id"
        class="task-card"
      >
        <div class="task-header">
          <div class="task-type-badge">
            <Icon 
              :icon="getWorkflowTypeIcon(task.workflow_type)" 
              :size="16"
            />
            <span>{{ task.workflow_name }}</span>
          </div>
          <div class="task-priority" :class="task.priority">
            {{ getPriorityLabel(task.priority) }}
          </div>
        </div>
        
        <div class="task-body">
          <div class="task-title">{{ task.task_name }}</div>
          <div class="task-description">{{ task.description }}</div>
          
          <div class="task-meta">
            <div class="meta-item">
              <Icon icon="mdi:account" :size="14" />
              <span>发起人：{{ task.initiator }}</span>
            </div>
            <div class="meta-item">
              <Icon icon="mdi:clock" :size="14" />
              <span>创建时间：{{ task.created_at }}</span>
            </div>
          </div>
        </div>
        
        <div class="task-footer">
          <div class="task-actions">
            <button class="btn-success" @click="approveTask(task)">
              <Icon icon="mdi:check" :size="16" />
              <span>同意</span>
            </button>
            <button class="btn-danger" @click="rejectTask(task)">
              <Icon icon="mdi:close" :size="16" />
              <span>驳回</span>
            </button>
            <button class="btn-secondary" @click="viewDetail(task)">
              <Icon icon="mdi:eye" :size="16" />
              <span>详情</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
```

```

---

### 2. 主布局（Main Layout）

**设计特点**：
- 固定侧边栏 + 可滚动主内容区
- 玻璃态效果
- 微妙的动画过渡
- 响应式设计

**布局代码**：
```vue
<template>
  <div class="main-layout">
    <!-- 侧边栏 -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <div class="sidebar-logo">
          <span class="logo-icon">AI</span>
          <span class="logo-text">MCP</span>
        </div>
      </div>
      
      <nav class="sidebar-nav">
        <div class="nav-section">
          <div class="nav-title">系统管理</div>
          <a href="#" class="nav-item active">
            <span class="nav-icon">📊</span>
            <span class="nav-text">仪表盘</span>
          </a>
          <a href="#" class="nav-item">
            <span class="nav-icon">👥</span>
            <span class="nav-text">用户管理</span>
          </a>
          <a href="#" class="nav-item">
            <span class="nav-icon">🏢</span>
            <span class="nav-text">部门管理</span>
          </a>
          <a href="#" class="nav-item">
            <span class="nav-icon">🔒</span>
            <span class="nav-text">权限管理</span>
          </a>
        </div>
        
        <div class="nav-section">
          <div class="nav-title">MCP工具</div>
          <a href="#" class="nav-item">
            <span class="nav-icon">🔧</span>
            <span class="nav-text">工具管理</span>
          </a>
          <a href="#" class="nav-item">
            <span class="nav-icon">💾</span>
            <span class="nav-text">数据源管理</span>
          </a>
        </div>
        
        <div class="nav-section">
          <div class="nav-title">支撑服务</div>
          <a href="#" class="nav-item">
            <span class="nav-icon">📝</span>
            <span class="nav-text">日志审计</span>
          </a>
          <a href="#" class="nav-item">
            <span class="nav-icon">🔔</span>
            <span class="nav-text">通知中心</span>
          </a>
        </div>
      </nav>
      
      <div class="sidebar-footer">
        <div class="user-info">
          <div class="user-avatar">A</div>
          <div class="user-details">
            <div class="user-name">Admin User</div>
            <div class="user-role">超级管理员</div>
          </div>
        </div>
        <button class="logout-btn">
          <span>退出登录</span>
        </button>
      </div>
    </aside>
    
    <!-- 主内容区 -->
    <main class="main-content">
      <!-- 顶部导航 -->
      <header class="top-header">
        <div class="header-left">
          <h1 class="page-title">仪表盘</h1>
          <div class="breadcrumb">
            <span>首页</span>
            <span class="separator">/</span>
            <span>仪表盘</span>
          </div>
        </div>
        
        <div class="header-right">
          <div class="search-box">
            <input 
              type="text" 
              class="search-input"
              placeholder="搜索..."
            />
            <button class="search-btn">🔍</button>
          </div>
          
          <div class="header-actions">
            <button class="action-btn notification">
              🔔
              <span class="badge">3</span>
            </button>
            <button class="action-btn settings">⚙️</button>
          </div>
        </div>
      </header>
      
      <!-- 页面内容 -->
      <div class="content-area">
        <slot></slot>
      </div>
    </main>
  </div>
</template>

<style scoped>
.main-layout {
  display: flex;
  min-height: 100vh;
  background: var(--primary-dark);
}

/* 侧边栏 */
.sidebar {
  width: 260px;
  background: var(--gradient-dark);
  border-right: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  position: relative;
}

.sidebar::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 1px;
  height: 100%;
  background: var(--gradient-primary);
  opacity: 0.3;
}

.sidebar-header {
  padding: 24px;
  border-bottom: 1px solid var(--border-color);
}

.sidebar-logo {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  width: 40px;
  height: 40px;
  background: var(--gradient-primary);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: bold;
  color: var(--primary-dark);
  box-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
}

.logo-text {
  font-family: 'Orbitron', sans-serif;
  font-size: 24px;
  font-weight: 700;
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* 导航 */
.sidebar-nav {
  flex: 1;
  padding: 24px 0;
  overflow-y: auto;
}

.nav-section {
  margin-bottom: 32px;
}

.nav-title {
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: var(--font-xs);
  font-weight: 600;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 1px;
  padding: 0 24px;
  margin-bottom: 12px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 24px;
  color: var(--text-secondary);
  text-decoration: none;
  transition: all 0.3s ease;
  position: relative;
  margin: 4px 0;
  border-radius: 8px;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.05);
  color: var(--text-primary);
}

.nav-item.active {
  background: var(--gradient-primary);
  color: var(--primary-dark);
}

.nav-item.active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 3px;
  background: var(--primary-dark);
  border-radius: 0 2px 2px 0;
}

.nav-icon {
  font-size: 20px;
  width: 24px;
  text-align: center;
}

.nav-text {
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: var(--font-base);
  font-weight: 500;
}

/* 侧边栏底部 */
.sidebar-footer {
  padding: 24px;
  border-top: 1px solid var(--border-color);
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.user-avatar {
  width: 40px;
  height: 40px;
  background: var(--gradient-primary);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Orbitron', sans-serif;
  font-weight: bold;
  color: var(--primary-dark);
  box-shadow: 0 0 15px rgba(0, 212, 255, 0.3);
}

.user-details {
  flex: 1;
}

.user-name {
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: var(--font-base);
  font-weight: 600;
  color: var(--text-primary);
}

.user-role {
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: var(--font-sm);
  color: var(--text-secondary);
}

.logout-btn {
  width: 100%;
  padding: 12px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  color: var(--text-secondary);
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: var(--font-sm);
  cursor: pointer;
  transition: all 0.3s ease;
}

.logout-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: var(--text-primary);
}

/* 主内容区 */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: var(--primary-dark);
}

/* 顶部导航 */
.top-header {
  padding: 24px 32px;
  background: var(--gradient-dark);
  border-bottom: 1px solid var(--border-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  align-items: baseline;
  gap: 16px;
}

.page-title {
  font-family: 'Orbitron', sans-serif;
  font-size: var(--font-2xl);
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
}

.breadcrumb {
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: var(--font-sm);
  color: var(--text-secondary);
}

.separator {
  color: var(--text-secondary);
  opacity: 0.5;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.search-box {
  position: relative;
  display: flex;
  align-items: center;
}

.search-input {
  width: 240px;
  padding: 12px 48px 12px 20px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  color: var(--text-primary);
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: var(--font-sm);
  transition: all 0.3s ease;
}

.search-input:focus {
  outline: none;
  border-color: var(--accent-blue);
  width: 280px;
}

.search-input::placeholder {
  color: var(--text-secondary);
  opacity: 0.6;
}

.search-btn {
  position: absolute;
  right: 12px;
  background: none;
  border: none;
  font-size: 16px;
  cursor: pointer;
  color: var(--text-secondary);
  transition: color 0.3s ease;
}

.search-btn:hover {
  color: var(--accent-blue);
}

.header-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  font-size: 18px;
  cursor: pointer;
  position: relative;
  transition: all 0.3s ease;
}

.action-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: var(--accent-blue);
}

.badge {
  position: absolute;
  top: -4px;
  right: -4px;
  width: 16px;
  height: 16px;
  background: var(--accent-cyan);
  border-radius: 50%;
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 10px;
  font-weight: bold;
  color: var(--primary-dark);
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 内容区 */
.content-area {
  flex: 1;
  padding: 32px;
  overflow-y: auto;
}
</style>
```

---

### 3. 仪表盘页面（Dashboard）

**设计特点**：
- 卡片式布局
- 数据可视化
- 渐变背景
- 悬停效果

**代码**：
```vue
<template>
  <div class="dashboard">
    <!-- 统计卡片 -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon">👥</div>
        <div class="stat-content">
          <div class="stat-label">用户总数</div>
          <div class="stat-value">1,234</div>
          <div class="stat-change positive">+12.5%</div>
        </div>
        <div class="stat-gradient"></div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">🔧</div>
        <div class="stat-content">
          <div class="stat-label">MCP工具</div>
          <div class="stat-value">56</div>
          <div class="stat-change positive">+8.3%</div>
        </div>
        <div class="stat-gradient"></div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">🔒</div>
        <div class="stat-content">
          <div class="stat-label">角色权限</div>
          <div class="stat-value">23</div>
          <div class="stat-change neutral">0%</div>
        </div>
        <div class="stat-gradient"></div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">📊</div>
        <div class="stat-content">
          <div class="stat-label">今日访问</div>
          <div class="stat-value">8,902</div>
          <div class="stat-change positive">+32.1%</div>
        </div>
        <div class="stat-gradient"></div>
      </div>
    </div>
    
    <!-- 图表区域 -->
    <div class="charts-section">
      <div class="chart-card">
        <div class="chart-header">
          <h3 class="chart-title">用户增长趋势</h3>
          <div class="chart-actions">
            <button class="chart-btn active">7天</button>
            <button class="chart-btn">30天</button>
            <button class="chart-btn">90天</button>
          </div>
        </div>
        <div class="chart-body">
          <!-- 图表占位 -->
          <div class="chart-placeholder">
            <div class="chart-line"></div>
            <div class="chart-line"></div>
            <div class="chart-line"></div>
            <div class="chart-line"></div>
            <div class="chart-line"></div>
          </div>
        </div>
      </div>
      
      <div class="chart-card">
        <div class="chart-header">
          <h3 class="chart-title">工具使用排行</h3>
        </div>
        <div class="chart-body">
          <div class="rank-list">
            <div class="rank-item">
              <div class="rank-number">1</div>
              <div class="rank-info">
                <div class="rank-name">数据查询工具</div>
                <div class="rank-bar">
                  <div class="rank-progress" style="width: 85%"></div>
                </div>
              </div>
              <div class="rank-value">2,341</div>
            </div>
            
            <div class="rank-item">
              <div class="rank-number">2</div>
              <div class="rank-info">
                <div class="rank-name">AI对话工具</div>
                <div class="rank-bar">
                  <div class="rank-progress" style="width: 72%"></div>
                </div>
              </div>
              <div class="rank-value">1,892</div>
            </div>
            
            <div class="rank-item">
              <div class="rank-number">3</div>
              <div class="rank-info">
                <div class="rank-name">文件处理工具</div>
                <div class="rank-bar">
                  <div class="rank-progress" style="width: 58%"></div>
                </div>
              </div>
              <div class="rank-value">1,456</div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 看板管理 -->
    <div class="kanban-section">
      <div class="kanban-header">
        <h3 class="kanban-title">任务看板</h3>
        <button class="add-task-btn">
          <span>+</span>
          <span>新建任务</span>
        </button>
      </div>
      
      <div class="kanban-board">
        <!-- 待办列 -->
        <div class="kanban-column">
          <div class="column-header">
            <div class="column-title">
              <span class="column-icon">📋</span>
              <span>待办</span>
            </div>
            <span class="task-count">4</span>
          </div>
          
          <div class="column-tasks">
            <div class="task-card" draggable="true">
              <div class="task-header">
                <span class="task-priority high">高优先级</span>
                <button class="task-menu">⋮</button>
              </div>
              <div class="task-title">优化MCP工具性能</div>
              <div class="task-description">提升工具响应速度，优化数据库查询</div>
              <div class="task-meta">
                <div class="task-tags">
                  <span class="tag">性能优化</span>
                  <span class="tag">后端</span>
                </div>
                <div class="task-deadline">
                  <span>📅</span>
                  <span>2026-01-20</span>
                </div>
              </div>
              <div class="task-footer">
                <div class="task-assignees">
                  <div class="assignee-avatar">张</div>
                  <div class="assignee-avatar">李</div>
                </div>
                <div class="task-comments">💬 3</div>
              </div>
            </div>
            
            <div class="task-card" draggable="true">
              <div class="task-header">
                <span class="task-priority medium">中优先级</span>
                <button class="task-menu">⋮</button>
              </div>
              <div class="task-title">新增用户权限管理功能</div>
              <div class="task-description">实现细粒度的权限控制</div>
              <div class="task-meta">
                <div class="task-tags">
                  <span class="tag">功能开发</span>
                  <span class="tag">权限</span>
                </div>
                <div class="task-deadline">
                  <span>📅</span>
                  <span>2026-01-25</span>
                </div>
              </div>
              <div class="task-footer">
                <div class="task-assignees">
                  <div class="assignee-avatar">王</div>
                </div>
                <div class="task-comments">💬 1</div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 进行中列 -->
        <div class="kanban-column">
          <div class="column-header">
            <div class="column-title">
              <span class="column-icon">🔄</span>
              <span>进行中</span>
            </div>
            <span class="task-count">3</span>
          </div>
          
          <div class="column-tasks">
            <div class="task-card" draggable="true">
              <div class="task-header">
                <span class="task-priority high">高优先级</span>
                <button class="task-menu">⋮</button>
              </div>
              <div class="task-title">前端界面UI/UX设计</div>
              <div class="task-description">设计现代化的深色主题界面</div>
              <div class="task-meta">
                <div class="task-tags">
                  <span class="tag">UI设计</span>
                  <span class="tag">前端</span>
                </div>
                <div class="task-deadline">
                  <span>📅</span>
                  <span>2026-01-15</span>
                </div>
              </div>
              <div class="task-footer">
                <div class="task-assignees">
                  <div class="assignee-avatar">刘</div>
                  <div class="assignee-avatar">陈</div>
                </div>
                <div class="task-comments">💬 8</div>
              </div>
            </div>
            
            <div class="task-card" draggable="true">
              <div class="task-header">
                <span class="task-priority medium">中优先级</span>
                <button class="task-menu">⋮</button>
              </div>
              <div class="task-title">数据库表结构优化</div>
              <div class="task-description">优化索引，提升查询效率</div>
              <div class="task-meta">
                <div class="task-tags">
                  <span class="tag">数据库</span>
                  <span class="tag">优化</span>
                </div>
                <div class="task-deadline">
                  <span>📅</span>
                  <span>2026-01-18</span>
                </div>
              </div>
              <div class="task-footer">
                <div class="task-assignees">
                  <div class="assignee-avatar">周</div>
                </div>
                <div class="task-comments">💬 2</div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 已完成列 -->
        <div class="kanban-column">
          <div class="column-header">
            <div class="column-title">
              <span class="column-icon">✅</span>
              <span>已完成</span>
            </div>
            <span class="task-count">2</span>
          </div>
          
          <div class="column-tasks">
            <div class="task-card completed" draggable="true">
              <div class="task-header">
                <span class="task-priority low">低优先级</span>
                <button class="task-menu">⋮</button>
              </div>
              <div class="task-title">系统文档编写</div>
              <div class="task-description">完成所有技术文档的编写</div>
              <div class="task-meta">
                <div class="task-tags">
                  <span class="tag">文档</span>
                </div>
                <div class="task-deadline">
                  <span>📅</span>
                  <span>2026-01-10</span>
                </div>
              </div>
              <div class="task-footer">
                <div class="task-assignees">
                  <div class="assignee-avatar">吴</div>
                </div>
                <div class="task-comments">💬 5</div>
              </div>
            </div>
            
            <div class="task-card completed" draggable="true">
              <div class="task-header">
                <span class="task-priority low">低优先级</span>
                <button class="task-menu">⋮</button>
              </div>
              <div class="task-title">Git仓库初始化</div>
              <div class="task-description">配置Git并推送到GitHub</div>
              <div class="task-meta">
                <div class="task-tags">
                  <span class="tag">Git</span>
                  <span class="tag">部署</span>
                </div>
                <div class="task-deadline">
                  <span>📅</span>
                  <span>2026-01-12</span>
                </div>
              </div>
              <div class="task-footer">
                <div class="task-assignees">
                  <div class="assignee-avatar">郑</div>
                </div>
                <div class="task-comments">💬 0</div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 已归档列 -->
        <div class="kanban-column">
          <div class="column-header">
            <div class="column-title">
              <span class="column-icon">📦</span>
              <span>已归档</span>
            </div>
            <span class="task-count">1</span>
          </div>
          
          <div class="column-tasks">
            <div class="task-card archived" draggable="true">
              <div class="task-header">
                <span class="task-priority low">低优先级</span>
                <button class="task-menu">⋮</button>
              </div>
              <div class="task-title">旧版本API重构</div>
              <div class="task-description">重构旧版API接口，提升性能</div>
              <div class="task-meta">
                <div class="task-tags">
                  <span class="tag">重构</span>
                  <span class="tag">API</span>
                </div>
                <div class="task-deadline">
                  <span>📅</span>
                  <span>2026-01-05</span>
                </div>
              </div>
              <div class="task-footer">
                <div class="task-assignees">
                  <div class="assignee-avatar">冯</div>
                </div>
                <div class="task-comments">💬 12</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 最近活动 -->
    <div class="activity-section">
      <div class="activity-card">
        <div class="activity-header">
          <h3 class="activity-title">最近活动</h3>
          <a href="#" class="view-all">查看全部</a>
        </div>
        <div class="activity-list">
          <div class="activity-item">
            <div class="activity-icon success">✓</div>
            <div class="activity-content">
              <div class="activity-text">用户张三创建了新工具</div>
              <div class="activity-time">2分钟前</div>
            </div>
          </div>
          
          <div class="activity-item">
            <div class="activity-icon warning">⚠</div>
            <div class="activity-content">
              <div class="activity-text">系统检测到异常登录</div>
              <div class="activity-time">15分钟前</div>
            </div>
          </div>
          
          <div class="activity-item">
            <div class="activity-icon info">ℹ</div>
            <div class="activity-content">
              <div class="activity-text">数据源配置已更新</div>
              <div class="activity-time">1小时前</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard {
  animation: fadeIn 0.6s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* 统计卡片网格 */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.stat-card {
  position: relative;
  padding: 24px;
  background: var(--gradient-glass);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  display: flex;
  align-items: center;
  gap: 16px;
  overflow: hidden;
  transition: all 0.3s ease;
  cursor: pointer;
}

.stat-card:hover {
  transform: translateY(-4px);
  border-color: var(--accent-blue);
  box-shadow: 0 10px 30px rgba(0, 212, 255, 0.2);
}

.stat-icon {
  width: 56px;
  height: 56px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  position: relative;
  z-index: 1;
}

.stat-content {
  flex: 1;
  position: relative;
  z-index: 1;
}

.stat-label {
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: var(--font-sm);
  color: var(--text-secondary);
  margin-bottom: 4px;
}

.stat-value {
  font-family: 'Orbitron', sans-serif;
  font-size: var(--font-2xl);
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.stat-change {
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: var(--font-sm);
  font-weight: 500;
}

.stat-change.positive {
  color: var(--accent-cyan);
}

.stat-change.neutral {
  color: var(--text-secondary);
}

.stat-gradient {
  position: absolute;
  top: -50%;
  right: -50%;
  width: 200%;
  height: 200%;
  background: var(--gradient-primary);
  opacity: 0.05;
  border-radius: 50%;
  filter: blur(40px);
  transition: all 0.6s ease;
}

.stat-card:hover .stat-gradient {
  opacity: 0.1;
  transform: scale(1.2);
}

/* 图表区域 */
.charts-section {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 24px;
  margin-bottom: 32px;
}

.chart-card {
  background: var(--gradient-glass);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  padding: 24px;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.chart-title {
  font-family: 'Orbitron', sans-serif;
  font-size: var(--font-lg);
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.chart-actions {
  display: flex;
  gap: 8px;
}

.chart-btn {
  padding: 8px 16px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--border-color);
  border-radius: 6px;
  color: var(--text-secondary);
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: var(--font-sm);
  cursor: pointer;
  transition: all 0.3s ease;
}

.chart-btn:hover,
.chart-btn.active {
  background: var(--gradient-primary);
  color: var(--primary-dark);
  border-color: transparent;
}

.chart-body {
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chart-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 8px;
}

.chart-line {
  height: 4px;
  background: var(--gradient-primary);
  border-radius: 2px;
  animation: growWidth 2s ease forwards;
  opacity: 0.6;
}

@keyframes growWidth {
  from { width: 0; }
  to { width: 100%; }
}

/* 排行列表 */
.rank-list {
  width: 100%;
}

.rank-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 0;
  border-bottom: 1px solid var(--border-color);
}

.rank-item:last-child {
  border-bottom: none;
}

.rank-number {
  width: 32px;
  height: 32px;
  background: var(--gradient-primary);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Orbitron', sans-serif;
  font-weight: bold;
  color: var(--primary-dark);
  font-size: var(--font-sm);
}

.rank-info {
  flex: 1;
}

.rank-name {
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: var(--font-base);
  color: var(--text-primary);
  margin-bottom: 8px;
}

.rank-bar {
  height: 4px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 2px;
  overflow: hidden;
}

.rank-progress {
  height: 100%;
  background: var(--gradient-primary);
  border-radius: 2px;
  transition: width 1s ease;
}

.rank-value {
  font-family: 'Orbitron', sans-serif;
  font-size: var(--font-lg);
  font-weight: 600;
  color: var(--text-primary);
}

/* 活动区域 */
.activity-section {
  margin-bottom: 32px;
}

.activity-card {
  background: var(--gradient-glass);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  padding: 24px;
}

.activity-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.activity-title {
  font-family: 'Orbitron', sans-serif;
  font-size: var(--font-lg);
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.view-all {
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: var(--font-sm);
  color: var(--accent-blue);
  text-decoration: none;
  transition: color 0.3s ease;
}

.view-all:hover {
  color: var(--accent-cyan);
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.activity-item {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding: 16px;
  background: rgba(255, 255, 255, 0.02);
  border-radius: 12px;
  transition: all 0.3s ease;
}

.activity-item:hover {
  background: rgba(255, 255, 255, 0.05);
}

.activity-icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  flex-shrink: 0;
}

.activity-icon.success {
  background: rgba(0, 255, 157, 0.2);
  color: var(--accent-cyan);
}

.activity-icon.warning {
  background: rgba(255, 193, 7, 0.2);
  color: var(--accent-purple);
}

.activity-icon.info {
  background: rgba(0, 212, 255, 0.2);
  color: var(--accent-blue);
}

.activity-content {
  flex: 1;
}

.activity-text {
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: var(--font-base);
  color: var(--text-primary);
  margin-bottom: 4px;
}

.activity-time {
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: var(--font-sm);
  color: var(--text-secondary);
}

/* 看板样式 */
.kanban-section {
  margin-bottom: 32px;
}

.kanban-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.kanban-title {
  font-family: 'Orbitron', sans-serif;
  font-size: var(--font-lg);
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.add-task-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: var(--gradient-primary);
  border: none;
  border-radius: 8px;
  color: var(--primary-dark);
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: var(--font-base);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.add-task-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 212, 255, 0.3);
}

.kanban-board {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
  overflow-x: auto;
  padding-bottom: 16px;
}

.kanban-column {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  padding: 20px;
  min-width: 300px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.column-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--border-color);
}

.column-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: var(--font-base);
  font-weight: 600;
  color: var(--text-primary);
}

.column-icon {
  font-size: 20px;
}

.task-count {
  padding: 4px 12px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  font-family: 'Orbitron', sans-serif;
  font-size: var(--font-sm);
  font-weight: 600;
  color: var(--text-secondary);
}

.column-tasks {
  display: flex;
  flex-direction: column;
  gap: 12px;
  min-height: 200px;
}

.task-card {
  background: var(--gradient-glass);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 16px;
  cursor: grab;
  transition: all 0.3s ease;
  position: relative;
}

.task-card:hover {
  transform: translateY(-2px);
  border-color: var(--accent-blue);
  box-shadow: 0 8px 24px rgba(0, 212, 255, 0.15);
}

.task-card:active {
  cursor: grabbing;
}

.task-card.dragging {
  opacity: 0.5;
  transform: scale(0.95);
}

.task-card.completed {
  opacity: 0.7;
}

.task-card.archived {
  opacity: 0.5;
}

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.task-priority {
  padding: 4px 12px;
  border-radius: 4px;
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: var(--font-xs);
  font-weight: 600;
  text-transform: uppercase;
}

.task-priority.high {
  background: rgba(255, 59, 48, 0.2);
  border: 1px solid rgba(255, 59, 48, 0.3);
  color: #ff8e8e;
}

.task-priority.medium {
  background: rgba(255, 193, 7, 0.2);
  border: 1px solid rgba(255, 193, 7, 0.3);
  color: #ffd93d;
}

.task-priority.low {
  background: rgba(0, 255, 157, 0.2);
  border: 1px solid rgba(0, 255, 157, 0.3);
  color: var(--accent-cyan);
}

.task-menu {
  background: none;
  border: none;
  color: var(--text-secondary);
  font-size: 20px;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.task-menu:hover {
  background: rgba(255, 255, 255, 0.1);
  color: var(--text-primary);
}

.task-title {
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: var(--font-base);
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 8px;
  line-height: 1.4;
}

.task-description {
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: var(--font-sm);
  color: var(--text-secondary);
  margin-bottom: 12px;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.task-meta {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 12px;
}

.task-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.tag {
  padding: 2px 8px;
  background: rgba(0, 212, 255, 0.1);
  border: 1px solid rgba(0, 212, 255, 0.2);
  border-radius: 4px;
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: var(--font-xs);
  color: var(--accent-blue);
}

.task-deadline {
  display: flex;
  align-items: center;
  gap: 6px;
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: var(--font-sm);
  color: var(--text-secondary);
}

.task-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 12px;
  border-top: 1px solid var(--border-color);
}

.task-assignees {
  display: flex;
  gap: -8px;
}

.assignee-avatar {
  width: 28px;
  height: 28px;
  background: var(--gradient-primary);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: var(--font-xs);
  font-weight: 600;
  color: var(--primary-dark);
  border: 2px solid var(--primary-dark);
  margin-left: -8px;
}

.assignee-avatar:first-child {
  margin-left: 0;
}

.task-comments {
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: var(--font-sm);
  color: var(--text-secondary);
}

/* 拖拽占位符样式 */
.kanban-column.drag-over {
  background: rgba(0, 212, 255, 0.05);
  border-color: var(--accent-blue);
}

.task-card.drag-over {
  border-color: var(--accent-cyan);
  box-shadow: 0 0 0 2px var(--accent-cyan);
}

/* 响应式 */
@media (max-width: 1200px) {
  .charts-section {
    grid-template-columns: 1fr;
  }
  
  .kanban-board {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .header-right {
    display: none;
  }
  
  .kanban-board {
    grid-template-columns: 1fr;
  }
  
  .kanban-column {
    min-width: 100%;
  }
}
</style>
```

---

### 4. 用户管理页面（User Management）

**设计特点**：
- 表格样式优化
- 操作按钮组
- 批量操作栏
- 搜索和筛选

**代码**：
```vue
<template>
  <div class="user-management">
    <!-- 操作栏 -->
    <div class="action-bar">
      <div class="bar-left">
        <button class="btn-primary">
          <span>+</span>
          <span>新增用户</span>
        </button>
        <button class="btn-secondary">
          <span>📥</span>
          <span>批量导入</span>
        </button>
      </div>
      
      <div class="bar-right">
        <div class="search-box">
          <input 
            type="text" 
            class="search-input"
            placeholder="搜索用户..."
          />
          <button class="search-btn">🔍</button>
        </div>
        <button class="filter-btn">🔽</button>
      </div>
    </div>
    
    <!-- 用户表格 -->
    <div class="table-container">
      <table class="user-table">
        <thead>
          <tr>
            <th class="checkbox-col">
              <input type="checkbox" class="checkbox" />
            </th>
            <th>用户名</th>
            <th>邮箱</th>
            <th>部门</th>
            <th>角色</th>
            <th>状态</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td class="checkbox-col">
              <input type="checkbox" class="checkbox" />
            </td>
            <td>
              <div class="user-cell">
                <div class="user-avatar">{{ user.name.charAt(0) }}</div>
                <div class="user-info">
                  <div class="user-name">{{ user.name }}</div>
                  <div class="user-id">{{ user.id }}</div>
                </div>
              </div>
            </td>
            <td>{{ user.email }}</td>
            <td>{{ user.department }}</td>
            <td>
              <span class="role-tag">{{ user.role }}</span>
            </td>
            <td>
              <span class="status-badge" :class="user.status">
                {{ user.status === 'active' ? '启用' : '禁用' }}
              </span>
            </td>
            <td>
              <div class="action-buttons">
                <button class="action-btn" title="编辑">✏️</button>
                <button class="action-btn" title="重置密码">🔑</button>
                <button class="action-btn" title="删除">🗑️</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
      
      <!-- 分页 -->
      <div class="pagination">
        <button class="page-btn" :disabled="currentPage === 1">←</button>
        <button 
          v-for="page in pages" 
          :key="page"
          class="page-btn"
          :class="{ active: page === currentPage }"
        >
          {{ page }}
        </button>
        <button class="page-btn" :disabled="currentPage === pages">→</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.user-management {
  animation: fadeIn 0.6s ease;
}

/* 操作栏 */
.action-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding: 20px;
  background: var(--gradient-glass);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-color);
  border-radius: 12px;
}

.bar-left {
  display: flex;
  gap: 12px;
}

.btn-primary,
.btn-secondary {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: var(--font-base);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary {
  background: var(--gradient-primary);
  color: var(--primary-dark);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 212, 255, 0.3);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--border-color);
  color: var(--text-primary);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.1);
}

.bar-right {
  display: flex;
  gap: 12px;
  align-items: center;
}

.search-box {
  position: relative;
  display: flex;
  align-items: center;
}

.search-input {
  width: 240px;
  padding: 12px 48px 12px 20px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  color: var(--text-primary);
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: var(--font-sm);
  transition: all 0.3s ease;
}

.search-input:focus {
  outline: none;
  border-color: var(--accent-blue);
  width: 280px;
}

.search-btn {
  position: absolute;
  right: 12px;
  background: none;
  border: none;
  font-size: 16px;
  cursor: pointer;
  color: var(--text-secondary);
}

.filter-btn {
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  font-size: 18px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.filter-btn:hover {
  border-color: var(--accent-blue);
}

/* 表格容器 */
.table-container {
  background: var(--gradient-glass);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  overflow: hidden;
}

.user-table {
  width: 100%;
  border-collapse: collapse;
}

.user-table thead {
  background: rgba(255, 255, 255, 0.02);
}

.user-table th {
  padding: 16px;
  text-align: left;
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: var(--font-sm);
  font-weight: 600;
  color: var(--text-secondary);
  border-bottom: 1px solid var(--border-color);
}

.user-table th.checkbox-col {
  width: 48px;
  text-align: center;
}

.user-table td {
  padding: 16px;
  border-bottom: 1px solid var(--border-color);
  color: var(--text-primary);
  font-family: 'Plus Jakarta Sans', sans-font-family: 'Plus Jakarta Sans', sans-serif);
  font-size: var(--font-base);
}

.user-table tbody tr:hover {
  background: rgba(255, 255, 255, 0.02);
}

.checkbox {
  width: 18px;
  height: 18px;
  border: 2px solid var(--border-color);
  border-radius: 4px;
  background: transparent;
  cursor: pointer;
  appearance: none;
  transition: all 0.3s ease;
}

.checkbox:checked {
  background: var(--gradient-primary);
  border-color: transparent;
}

/* 用户单元格 */
.user-cell {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-avatar {
  width: 40px;
  height: 40px;
  background: var(--gradient-primary);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Orbitron', sans-serif;
  font-weight: bold;
  color: var(--primary-dark);
  font-size: var(--font-base);
}

.user-info {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: var(--font-base);
  font-weight: 600;
  color: var(--text-primary);
}

.user-id {
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: var(--font-sm);
  color: var(--text-secondary);
}

/* 角色标签 */
.role-tag {
  padding: 4px 12px;
  background: rgba(0, 212, 255, 0.1);
  border: 1px solid rgba(0, 212, 255, 0.2);
  border-radius: 4px;
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: var(--font-sm);
  color: var(--accent-blue);
}

/* 状态徽章 */
.status-badge {
  padding: 4px 12px;
  border-radius: 4px;
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: var(--font-sm);
  font-weight: 500;
}

.status-badge.active {
  background: rgba(0, 255, 157, 0.1);
  border: 1px solid rgba(0, 255, 157, 0.2);
  color: var(--accent-cyan);
}

.status-badge.inactive {
  background: rgba(255, 59, 48, 0.1);
  border: 1px solid rgba(255, 59, 48, 0.2);
  color: #ff8e8e;
}

/* 操作按钮 */
.action-buttons {
  display: flex;
  gap: 4px;
}

.action-btn {
  width: 32px;
  height: 32px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--border-color);
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: var(--accent-blue);
}

/* 分页 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  padding: 20px;
  border-top: 1px solid var(--border-color);
}

.page-btn {
  width: 36px;
  height: 36px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  color: var(--text-primary);
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: var(--font-base);
  cursor: pointer;
  transition: all 0.3s ease;
}

.page-btn:hover:not(:disabled) {
  background: var(--gradient-primary);
  color: var(--primary-dark);
  border-color: transparent;
}

.page-btn.active {
  background: var(--gradient-primary);
  color: var(--primary-dark);
  border-color: transparent;
}

.page-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}
</style>
```

---

## 🎨 全局样式（Global Styles）

```css
/* 全局样式 */
:root {
  /* 主色调 */
  --primary-dark: #0a0e17;
  --primary-light: #1a1f2e;
  --accent-blue: #00d4ff;
  --accent-cyan: #00ff9d;
  --accent-purple: #b388ff;
  
  /* 文本颜色 */
  --text-primary: #e2e8f0;
  --text-secondary: #94a3b8;
  --text-muted: #64748b;
  
  /* 边框颜色 */
  --border-color: rgba(255, 255, 255, 0.1);
  --border-light: rgba(255, 255, 255, 0.05);
  
  /* 渐变 */
  --gradient-primary: linear-gradient(135deg, #00d4ff 0%, #00ff9d 100%);
  --gradient-dark: linear-gradient(180deg, #0a0e17 0%, #1a1f2e 100%);
  --gradient-glass: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
  
  /* 阴影 */
  --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.3);
  --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.4);
  --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.5);
  --shadow-xl: 0 16px 64px rgba(0, 0, 0, 0.6);
  
  /* 字体 */
  --font-xs: 0.75rem;
  --font-sm: 0.875rem;
  --font-base: 1rem;
  --font-lg: 1.125rem;
  --font-xl: 1.25rem;
  --font-2xl: 1.5rem;
  --font-3xl: 1.875rem;
  
  /* 动画 */
  --transition-fast: 0.2s ease;
  --transition-base: 0.3s ease;
  --transition-slow: 0.5s ease;
}

/* 全局样式 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Plus Jakarta Sans', sans-serif;
  background: var(--primary-dark);
  color: var(--text-primary);
  line-height: 1.6;
}

/* 滚动条 */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: var(--primary-dark);
}

::-webkit-scrollbar-thumb {
  background: var(--border-color);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: var(--accent-blue);
}

/* 选择文本 */
::selection {
  background: var(--accent-blue);
  color: var(--primary-dark);
}

/* 字体导入 */
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
```

---

## 🎯 设计总结

### 核心特点

1. **独特的字体选择**：
   - 标题：Orbitron（科技感显示字体）
   - 正文：Plus Jakarta Sans（现代几何字体）
   - 避免了常见的Inter、Arial等通用字体

2. **专业的配色方案**：
   - 深蓝黑色背景，专业稳重
   - 霓虹蓝/青色/紫色强调色，科技感强
   - 避免了常见的紫色渐变

3. **精致的视觉效果**：
   - 玻璃态效果（Glassmorphism）
   - 微妙的渐变背景
   - 精致的阴影和光晕
   - 流畅的动画过渡

4. **现代的布局设计**：
   - 不对称布局
   - 卡片式设计
   - 悬停效果
   - 响应式设计

### 技术实现

- ✅ Vue 3 + TypeScript
- ✅ CSS变量系统
- ✅ 动画效果
- ✅ 响应式设计
- ✅ 生产级代码质量

这个设计方案既专业又现代，避免了通用的AI美学，创造了一个独特的企业级AI管理平台界面。