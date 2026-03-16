# 脚手架生成脚本

## 脚本说明

由于完整的 Python 生成脚本较为复杂，这里提供脚本的核心结构和实现思路。

## 核心功能模块

### 1. 参数解析模块
```python
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='YSS DDD 脚手架生成器')
    parser.add_argument('--project-name', required=True, help='项目名称')
    parser.add_argument('--base-package', required=True, help='基础包名')
    parser.add_argument('--output-dir', default='./output', help='输出目录')
    return parser.parse_args()
```

### 2. 模板渲染模块
```python
def render_template(template_path, variables):
    """渲染模板文件"""
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for key, value in variables.items():
        content = content.replace(f'{{{{{key}}}}}', value)
    
    return content
```

### 3. 文件生成模块
```python
def generate_file(template_path, output_path, variables):
    """生成文件"""
    content = render_template(template_path, variables)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
```

### 4. 项目结构生成模块
```python
def create_project_structure(project_root, base_package):
    """创建项目目录结构"""
    package_path = base_package.replace('.', '/')
    
    modules = [
        f"{project_name}-domain",
        f"{project_name}-application",
        f"{project_name}-infrastructure",
        f"{project_name}-adapter",
        f"{project_name}-bootstrap"
    ]
    
    for module in modules:
        # 创建 src/main/java 目录
        java_path = project_root / module / "src" / "main" / "java" / package_path
        java_path.mkdir(parents=True, exist_ok=True)
        
        # 创建 src/main/resources 目录
        resources_path = project_root / module / "src" / "main" / "resources"
        resources_path.mkdir(parents=True, exist_ok=True)
```

## 使用方法

### 方式1: 手动创建项目（推荐用于学习）

1. 复制模板文件到目标目录
2. 手动替换模板变量
3. 调整包名和类名

### 方式2: 使用 IDE 模板

1. 在 IDE 中创建 File Template
2. 导入模板文件
3. 使用 IDE 的变量替换功能

### 方式3: 完整 Python 脚本

完整的 Python 脚本实现请参考：
- `generate_scaffold.py` (主脚本)
- `template_engine.py` (模板引擎)
- `file_generator.py` (文件生成器)

## 模板变量映射

| 模板变量 | 来源 | 示例 |
|---------|------|------|
| `{{project_name}}` | --project-name | user-service |
| `{{base_package}}` | --base-package | com.yss.datamiddle.user |
| `{{group_id}}` | 从 base_package 提取 | com.yss.datamiddle |
| `{{author}}` | 系统用户名或配置 | YSS Team |
| `{{date}}` | 当前日期 | 2024-01-15 |

## 扩展开发

### 添加新的生成器

```python
class CustomGenerator:
    def __init__(self, config):
        self.config = config
    
    def generate(self):
        # 实现自定义生成逻辑
        pass
```

### 添加新的模板处理器

```python
class TemplateProcessor:
    def process(self, template, context):
        # 实现模板处理逻辑
        return processed_content
```

## 注意事项

1. 确保 Python 版本 >= 3.7
2. 模板文件使用 UTF-8 编码
3. 生成前检查输出目录是否存在
4. 生成后验证文件完整性

## 故障排查

### 问题1: 模板变量未替换
- 检查变量名是否正确
- 确认模板文件格式

### 问题2: 文件生成失败
- 检查输出目录权限
- 确认路径是否正确

### 问题3: 编码问题
- 使用 UTF-8 编码
- 检查系统默认编码
