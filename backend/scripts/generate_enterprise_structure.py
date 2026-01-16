# -*- coding: utf-8 -*-
"""
Enterprise Project Structure Generator

Description:
1. Create enterprise-level directory structure for all services
2. Auto-generate base files
3. Create necessary configuration files

Usage:
    python scripts/generate_enterprise_structure.py
"""

import os
import sys
from pathlib import Path

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

# Project root directory
PROJECT_ROOT = Path("D:/WorkSpace/mcp-platform")
BACKEND_ROOT = PROJECT_ROOT / "backend"
SERVICES_ROOT = BACKEND_ROOT / "services"

# Service list
SERVICES = [
    {
        "name": "auth-service",
        "port": 8001,
        "description": "Authentication Service",
        "models": ["user", "token"],
        "schemas": ["auth"],
        "apis": ["auth"],
    },
    {
        "name": "user-service",
        "port": 8002,
        "description": "User Service",
        "models": ["user", "department", "tenant"],
        "schemas": ["user", "department", "tenant"],
        "apis": ["users", "departments", "tenants"],
    },
    {
        "name": "permission-service",
        "port": 8003,
        "description": "Permission Service",
        "models": ["role", "permission", "menu"],
        "schemas": ["role", "permission", "menu"],
        "apis": ["roles", "permissions", "menus"],
    },
    {
        "name": "system-service",
        "port": 8004,
        "description": "System Service",
        "models": ["mcp_tool", "datasource", "dict"],
        "schemas": ["mcp_tool", "datasource", "dict"],
        "apis": ["mcp_tools", "datasources", "dicts"],
    },
    {
        "name": "support-service",
        "port": 8005,
        "description": "Support Service",
        "models": ["log", "notification", "todo"],
        "schemas": ["log", "notification", "todo"],
        "apis": ["logs", "notifications", "todos"],
    },
    {
        "name": "business-service",
        "port": 8006,
        "description": "Business Service",
        "models": ["workflow", "workflow_template", "workflow_task"],
        "schemas": ["workflow", "workflow_template", "workflow_task"],
        "apis": ["workflows", "workflow_templates", "workflow_tasks"],
    },
]


def create_directory_structure():
    """Create enterprise-level directory structure"""
    print("Starting to create enterprise project structure...")
    
    for service in SERVICES:
        service_path = SERVICES_ROOT / service["name"]
        print(f"\nCreating service: {service['name']}")
        
        # Create directories
        directories = [
            service_path / "app" / "models",
            service_path / "app" / "services",
            service_path / "app" / "repositories",
            service_path / "tests" / "unit",
            service_path / "tests" / "integration",
            service_path / "alembic" / "versions",
            service_path / "scripts",
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"  ✓ Created directory: {directory.relative_to(BACKEND_ROOT)}")
        
        # Create __init__.py files
        init_files = [
            service_path / "app" / "models" / "__init__.py",
            service_path / "app" / "services" / "__init__.py",
            service_path / "app" / "repositories" / "__init__.py",
            service_path / "tests" / "__init__.py",
            service_path / "tests" / "unit" / "__init__.py",
            service_path / "tests" / "integration" / "__init__.py",
        ]
        
        for init_file in init_files:
            init_file.touch(exist_ok=True)
            print(f"  ✓ Created file: {init_file.relative_to(BACKEND_ROOT)}")
        
        # Create model files
        for model_name in service["models"]:
            model_file = service_path / "app" / "models" / f"{model_name}.py"
            model_file.touch(exist_ok=True)
            print(f"  ✓ Created model file: {model_file.relative_to(BACKEND_ROOT)}")
        
        # Create service files
        for model_name in service["models"]:
            service_file = service_path / "app" / "services" / f"{model_name}_service.py"
            service_file.touch(exist_ok=True)
            print(f"  ✓ Created service file: {service_file.relative_to(BACKEND_ROOT)}")
        
        # Create repository files
        for model_name in service["models"]:
            repo_file = service_path / "app" / "repositories" / f"{model_name}_repository.py"
            repo_file.touch(exist_ok=True)
            print(f"  ✓ Created repository file: {repo_file.relative_to(BACKEND_ROOT)}")
        
        # Create Alembic files
        alembic_file = service_path / "alembic" / "env.py"
        alembic_file.touch(exist_ok=True)
        print(f"  ✓ Created Alembic config: {alembic_file.relative_to(BACKEND_ROOT)}")
        
        script_file = service_path / "alembic" / "script.py.mako"
        script_file.touch(exist_ok=True)
        print(f"  ✓ Created Alembic template: {script_file.relative_to(BACKEND_ROOT)}")
        
        # Create configuration files
        env_prod_file = service_path / ".env.production"
        env_prod_file.touch(exist_ok=True)
        print(f"  ✓ Created production config: {env_prod_file.relative_to(BACKEND_ROOT)}")
        
        # Create Docker files
        docker_compose_file = service_path / "docker-compose.yml"
        docker_compose_file.touch(exist_ok=True)
        print(f"  ✓ Created Docker compose: {docker_compose_file.relative_to(BACKEND_ROOT)}")
        
        # Create README
        readme_file = service_path / "README.md"
        readme_file.touch(exist_ok=True)
        print(f"  ✓ Created README: {readme_file.relative_to(BACKEND_ROOT)}")
    
    print("\n✅ Enterprise project structure created successfully!")
    print(f"\nCreated {len(SERVICES)} services, each service contains:")
    print("  - models/ (SQLAlchemy models)")
    print("  - services/ (Business logic layer)")
    print("  - repositories/ (Data access layer)")
    print("  - tests/ (Test directory)")
    print("  - alembic/ (Database migration)")
    print("  - scripts/ (Script tools)")
    print("  - .env.production (Production config)")
    print("  - docker-compose.yml (Docker compose)")
    print("  - README.md (Service documentation)")


if __name__ == "__main__":
    create_directory_structure()