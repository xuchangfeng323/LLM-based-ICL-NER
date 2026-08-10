# LLM-based-ICL-NER

基于大语言模型（LLM）+ 上下文学习（In-Context Learning, ICL）的命名实体识别（NER）项目。在 <a href="https://github.com/JHnlp/BioCreative-V-CDR-Corpus">BC5CDR</a> 数据集上，通过 k-shot 示例引导大模型识别摘要和标题中的化学物质（Chemical）和疾病（Disease）实体，并评估精确率、召回率和 F1。
## 项目结构

```
.
├── args/
│   └── config.json              # 运行配置（模型、k-shot、提示词等）
├── data/                        # CDR 数据集（PubTator 格式）
│   ├── CDR_TrainingSet.PubTator.txt
│   ├── CDR_DevelopmentSet.PubTator.txt
│   └── CDR_TestSet.PubTator.txt
├── data_process.py              # 数据解析：构造 k-shot 提示词、加载评估数据
├── get_response.py              # 调用 DeepSeek API 获取模型响应
├── utils.py                     # 配置加载、评估指标（P/R/F1、宏/微平均）
└── eval.py                      # 主评估脚本
```

## 环境准备

```bash
# 安装依赖
pip install openai python-dotenv json-repair

# 配置 API Key：在项目根目录创建 .env 文件
echo 'deepseek_api_key="sk-你的key"' > .env
```

## 配置说明

编辑 `args/config.json`：

| 字段 | 说明 | 示例 |
|---|---|---|
| `model` | 模型供应商标识（用于路由） | `"deepseek"` |
| `model_name` | 实际调用的模型名称 | `"deepseek-v4-flash"` |
| `k` | few-shot 示例数量 | `5` |
| `data_num` | 评估样本数量 | `500` |
| `target_class` | 目标实体类别 | `["Chemical", "Disease"]` |
| `output_dir` | 输出目录 | `"./output"` |
| `data_dir` | 数据目录 | `"./data"` |
| `prompt` | 系统提示词（定义任务与输出格式） | |

## 运行

```bash
python eval.py
```



## 评估指标

指标定义（`utils.py`）：

- **TP**：预测实体与真实实体在 `(文章id, 实体名)` 级别完全匹配（不区分大小写）
- **P** = TP / 预测实体总数
- **R** = TP / 真实实体总数
- **F1** = 2 × P × R / (P + R)
- **微平均（micro）**：所有类别汇总后统一计算 P/R/F1
- **宏平均（macro）**：各类别 P/R/F1 的算术平均

## 数据格式
```bash
        3403780|t|Paracetamol-associated coma, metabolic acidosis, renal and hepatic failure.
		3403780|a|A case of metabolic acidosis, acute renal failure and hepatic failure following paracetamol ingestion is presented. The diagnostic difficulty at presentation is highlighted .....
		3403780	0	11	Paracetamol	Chemical	D000082	
		3403780	23	27	coma	Disease	D003128	
		3403780	29	47	metabolic acidosis	Disease	D000138	
		3403780	39	47	acidosis	Disease	D000138	
		3403780	49	74	renal and hepatic failure	Disease	D058186|D017093	renal failure|hepatic failure
		3403780	86	104	metabolic acidosis	Disease	D000138	
		3403780	96	104	acidosis	Disease	D000138	
		3403780	106	145	acute renal failure and hepatic failure	Disease	D058186|D017114	acute renal failure|acute hepatic failure
		3403780	156	167	paracetamol	Chemical	D000082	
		3403780	CID	D000082	D000138
		3403780	CID	D000082	D017114
		3403780	CID	D000082	D058186
```

## 实验结果
### DeepSeek v4-flash
#### 3-shot
|  | Precision | Recall | F1-Score | Support |
| :--- | :--- | :--- | :--- | :--- |
| Chemical | 0.7727 | 0.6952 | 0.7319 | 5,203 |
| Disease | 0.6668 | 0.7059 | 0.6858 | 4,182 |
| Micro Avg | 0.7212 | 0.6999 | 0.7104 | 9,385 |
| Macro Avg | 0.7198 | 0.7005 | 0.7088 | 9,385 |
