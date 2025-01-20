第二种方式使用 `asyncio` 的任务控制机制，通过创建 `asyncio.Task` 来运行异步任务，并使用其内置的 `cancel()` 方法实现真正的任务终止。  

以下是完整的示例代码和说明：

---

### 示例代码

```python
from fastapi import FastAPI
import asyncio

app = FastAPI()

# 用于存储任务的全局字典
tasks = {}

# 异步任务函数
async def long_running_task(task_id: str):
    try:
        while True:
            print(f"Task {task_id} is running...")
            await asyncio.sleep(1)  # 模拟异步耗时操作
    except asyncio.CancelledError:
        # 捕获取消异常并执行清理逻辑
        print(f"Task {task_id} has been cancelled.")
        raise

@app.post("/start-task/{task_id}")
def start_task(task_id: str):
    # 检查任务是否已存在
    if task_id in tasks:
        return {"message": f"Task {task_id} is already running."}

    # 创建异步任务并存储
    loop = asyncio.get_event_loop()
    task = loop.create_task(long_running_task(task_id))
    tasks[task_id] = task
    return {"message": f"Task {task_id} started."}

@app.post("/stop-task/{task_id}")
async def stop_task(task_id: str):
    # 查找任务
    task = tasks.get(task_id)
    if task:
        # 取消任务
        task.cancel()
        try:
            await task  # 等待任务完成清理
        except asyncio.CancelledError:
            pass  # 捕获取消异常以防止进一步报错
        del tasks[task_id]  # 从任务列表中移除
        return {"message": f"Task {task_id} has been cancelled."}
    return {"message": f"Task {task_id} not found."}
```

---

### 工作原理

1. **任务启动**
   - 使用 `asyncio.get_event_loop()` 获取事件循环。
   - 调用 `loop.create_task()` 创建任务并异步运行。
   - 将任务存储在全局字典 `tasks` 中，以便后续管理。

2. **任务运行**
   - `long_running_task` 是一个异步函数，每秒输出任务运行状态。
   - 使用 `await asyncio.sleep(1)` 模拟耗时操作，同时让出事件循环以便处理其他请求。

3. **任务终止**
   - 调用 `task.cancel()` 发送取消信号。
   - `long_running_task` 在下一次 `await` 时抛出 `asyncio.CancelledError` 异常。
   - 异常捕获后，执行清理逻辑并终止任务。
   - 删除任务记录。

---

### 关键点解析

1. **`task.cancel()`**  
   这是终止任务的关键，它会向任务抛出 `CancelledError` 异常，任务需要显式捕获该异常并停止运行。

2. **清理逻辑**  
   在 `except asyncio.CancelledError` 块中，可以添加必要的清理代码，例如释放资源或记录日志。

3. **等待任务退出**  
   使用 `await task` 确保任务完全退出，避免资源未释放的问题。

---

### 优势

- **即时性**：相比第一种方法，任务能在最近的 `await` 处迅速响应取消信号。
- **更强控制**：支持任务的强制终止，不依赖标志位。

---

### 注意事项

1. **异步任务中必须有 `await`**  
   如果任务是同步的（如 CPU 密集型操作），需要将其封装为异步任务或使用线程池。
   
2. **异常处理**  
   未捕获 `CancelledError` 异常的任务可能会导致未定义行为，因此建议明确处理。

---

### 示例请求

1. 启动任务：
   ```bash
   curl -X POST http://127.0.0.1:8000/start-task/task1
   ```

2. 停止任务：
   ```bash
   curl -X POST http://127.0.0.1:8000/stop-task/task1
   ```