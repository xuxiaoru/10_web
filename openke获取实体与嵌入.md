在 OpenKE 的 PyTorch 版本中，`get_parameters` 方法通常不直接用于提取模型参数。OpenKE 的 PyTorch 版本依赖于 PyTorch 的标准方法（如 `state_dict()`）来访问和管理模型参数。因此，提取嵌入的正确方式是通过 `state_dict()`。

以下是如何提取实体和关系嵌入的示例：

---

### **如何提取模型参数**

#### **方法：使用 `state_dict()`**
在训练或加载模型后，你可以使用 PyTorch 提供的 `state_dict()` 方法来访问模型的所有参数，包括实体和关系的嵌入。

```python
# 提取模型参数
state_dict = transe.state_dict()

# 提取实体和关系嵌入
entity_embeddings = state_dict["ent_embeddings.weight"].cpu().numpy()
relation_embeddings = state_dict["rel_embeddings.weight"].cpu().numpy()
```

---

### **完整示例代码**

以下是使用 OpenKE 的 PyTorch 版本训练 TransE 模型并提取嵌入的完整代码：

```python
from openke.data import TrainDataLoader
from openke.module.model import TransE
from openke.module.loss import MarginLoss
from openke.module.strategy import NegativeSampling
from openke.config import Trainer
import pandas as pd

# 加载数据
train_dataloader = TrainDataLoader(
    in_path="./benchmarks/FB15K/",  # 数据集路径
    nbatches=100,                  # batch 数量
    threads=8,                     # 线程数量
    sampling_mode="normal",        # 负采样模式
    bern_flag=1,                   # 是否使用伯努利采样
    filter_flag=1,                 # 是否过滤无效样本
    neg_ent=25,                    # 每个正例对应负实体样本数
    neg_rel=0                      # 每个正例对应负关系样本数
)

# 定义模型
transe = TransE(
    ent_tot=train_dataloader.get_ent_tot(),  # 实体总数
    rel_tot=train_dataloader.get_rel_tot(),  # 关系总数
    dim=100,                                 # 嵌入维度
    p_norm=1,                                # 范数
    norm_flag=True                           # 是否归一化
)

# 定义损失函数和训练策略
model = NegativeSampling(
    model=transe,
    loss=MarginLoss(margin=5.0),  # margin 值
    batch_size=train_dataloader.get_batch_size()
)

# 训练模型
trainer = Trainer(model=model, data_loader=train_dataloader, train_times=1000, alpha=0.001, use_gpu=True)
trainer.run()

# 保存模型
transe.save_checkpoint("./checkpoint/transe.ckpt")

# 加载模型
transe.load_checkpoint("./checkpoint/transe.ckpt")

# 提取嵌入
state_dict = transe.state_dict()
entity_embeddings = state_dict["ent_embeddings.weight"].cpu().numpy()
relation_embeddings = state_dict["rel_embeddings.weight"].cpu().numpy()

# 加载实体和关系 ID 映射
entity2id = pd.read_csv("./benchmarks/FB15K/entity2id.txt", sep="\t", header=None, names=["entity", "id"])
relation2id = pd.read_csv("./benchmarks/FB15K/relation2id.txt", sep="\t", header=None, names=["relation", "id"])

# 将嵌入保存为 DataFrame
entity_embeddings_df = pd.DataFrame(entity_embeddings)
entity_embeddings_df["entity"] = entity2id["entity"]

relation_embeddings_df = pd.DataFrame(relation_embeddings)
relation_embeddings_df["relation"] = relation2id["relation"]

# 保存为 CSV 文件
entity_embeddings_df.to_csv("./entity_embeddings.csv", index=False)
relation_embeddings_df.to_csv("./relation_embeddings.csv", index=False)

print("实体和关系嵌入已保存为 CSV 文件！")
```

---

### **解释**

1. **提取参数的方式**
   - 使用 `state_dict()` 获取模型的所有参数。
   - 通过键名 `ent_embeddings.weight` 和 `rel_embeddings.weight` 提取实体和关系嵌入。
   - 嵌入通常是 PyTorch 的 `Tensor`，需要用 `.cpu().numpy()` 转换为 NumPy 数组。

2. **映射到实体和关系名称**
   - 加载 `entity2id.txt` 和 `relation2id.txt` 文件，将嵌入与名称对应。
   - 保存为 CSV 文件，方便后续分析。

3. **避免 `get_parameters` 错误**
   - PyTorch 版本的 OpenKE 中不推荐使用 `get_parameters` 方法，建议使用 PyTorch 提供的标准方式如 `state_dict()`。

---

如果还有其他问题，请随时提出！