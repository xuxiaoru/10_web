在调试 FastAPI 时，可以使用 Python 的 `requests` 库发送 HTTP 请求，以模拟客户端的行为。以下是具体操作步骤：

---

### **1. 安装 requests 库**
如果尚未安装 `requests`，运行以下命令：

```bash
pip install requests
```

---

### **2. 编写测试脚本**
创建一个单独的 Python 文件，例如 `test_request.py`，用于发送请求。

#### 示例代码：

```python
import requests

# 发送 GET 请求
response = requests.get("http://127.0.0.1:8000/")
print("GET Response:", response.json())

# 发送带参数的 GET 请求
response = requests.get("http://127.0.0.1:8000/items/42", params={"q": "example"})
print("GET with params Response:", response.json())

# 发送 POST 请求
data = {"name": "item_name", "value": 123}
response = requests.post("http://127.0.0.1:8000/create", json=data)
print("POST Response:", response.json())
```

---

### **3. 启动 FastAPI 应用**
1. 确保 FastAPI 应用正在运行，例如通过 `uvicorn main:app --reload` 启动。
2. 调试模式下通过 VSCode 的调试工具启动你的应用。

---

### **4. 执行测试脚本**
1. 在终端运行 `test_request.py`：
   ```bash
   python test_request.py
   ```
2. 脚本会发送请求到 FastAPI 服务，并打印返回结果。

---

### **5. 配合调试器查看断点**
- 确保你的 FastAPI 应用代码中已设置断点（点击行号左侧设置红点）。
- 当 `requests` 发送的请求触发断点时，调试器会暂停在对应代码行。
- 你可以在调试界面查看变量、调用堆栈等信息。

---

### **6. 示例 FastAPI 应用**
确保 FastAPI 的路由匹配上你的测试脚本中的请求：

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.post("/create")
def create_item(item: BaseModel):
    return {"item_name": item.name, "value": item.value}
```

---

### **7. 测试效果**
运行 `test_request.py` 后：
- **在终端**：会看到 `requests` 的输出，如：
  ```
  GET Response: {'Hello': 'World'}
  GET with params Response: {'item_id': 42, 'q': 'example'}
  POST Response: {'item_name': 'item_name', 'value': 123}
  ```
- **在调试器**：当请求命中断点时，调试器会暂停在代码相应位置，方便你查看和调试。

---

通过 `requests` 发送请求，结合调试器查看 FastAPI 的行为，可以有效调试和测试你的应用。