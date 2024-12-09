在 VSCode 中调试 FastAPI 应用是一种高效的方式，能够快速定位问题和测试代码逻辑。以下是设置和调试 FastAPI 的步骤：

---

### 1. **安装必要的扩展和工具**
- **Python扩展**：在 VSCode 的扩展商店中安装官方 Python 插件。
- **Debugger for Python**：默认情况下，Python 插件已经包含调试功能。
- **Uvicorn**：FastAPI 通常使用 Uvicorn 作为 ASGI 服务器运行。
  ```bash
  pip install uvicorn
  ```

---

### 2. **创建 FastAPI 应用**
确保你的项目目录有一个主应用文件，例如 `main.py`：

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
```

---

### 3. **设置启动和调试配置**
#### **添加 `launch.json`**
1. 按 `Ctrl+Shift+P`，输入 `Debug: Open launch.json`，选择 `Python`。
2. 在生成的 `launch.json` 中添加一个配置用于调试：

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: FastAPI",
            "type": "python",
            "request": "launch",
            "program": "uvicorn",
            "args": [
                "main:app",  // 替换为你的应用入口文件:FastAPI实例
                "--host", "127.0.0.1",
                "--port", "8000",
                "--reload"
            ],
            "jinja": true
        }
    ]
}
```

#### **配置说明**：
- `program`: 设置为 `uvicorn`，用于启动 FastAPI。
- `args`: 指定运行的应用路径、主机地址和端口号。
- `--reload`: 开启热加载，方便开发。

---

### 4. **启动调试**
1. 切换到 VSCode 的 **Run and Debug** 面板（左侧调试图标）。
2. 选择 **Python: FastAPI** 配置。
3. 点击 **Start Debugging**（绿色三角按钮）启动调试。

---

### 5. **设置断点**
- 在代码中点击行号左侧添加断点。
- 当触发断点时，调试器会暂停在相应的位置，允许你查看变量、调用堆栈等。

---

### 6. **调试技巧**
- **查看变量**：调试面板中可以实时查看变量的值。
- **使用控制台**：在调试控制台输入 Python 表达式，查看和操作变量。
- **Step In/Out/Over**：使用调试工具栏进行单步调试。
- **日志调试**：可以在代码中加入 `print()` 或 `logging` 查看运行信息。

---

### 7. **其他调试方法**
#### **直接运行 Python 文件**
如果你不想使用 `uvicorn` 命令启动，可以直接运行 Python 文件。例如：
```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
```
然后在 `launch.json` 中直接指定 `program` 为 `main.py`。

---

通过以上步骤，你可以方便地在 VSCode 中调试 FastAPI 应用！