### 运行环境
python>=3.10

### windows 运行
```
<!-- 创建虚拟环境 -->
python -m venv .venv
<!-- 激活虚拟环境 -->
.\.venv\Scripts\activate
<-- 安装依赖 -->
python -m pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
<!-- 运行 -->
python -m app.main
或者
python -m uvicorn app.main:app --host 0.0.0.0 --port 5001

```
### Linux 运行
```
<-- 创建虚拟环境 -->
python -m venv .venv
<-- 激活虚拟环境 -->
source .venv/bin/activate
<-- 安装依赖 -->
python -m pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

python -m uvicorn app.main:app --host 0.0.0.0 --port 5001

```