# 大学物理实验报告 Skill

**课前写预习，课后先核对数据，再写报告。** 适合需要手写大学物理实验报告的同学，支持 Codex、Claude Code 和豆包。

本项目提供可安装的 AI 技能和可复制的中文提示词，不需要项目自己的模型 API Key。输入自己的教材和实验数据，不会拿示例数据替你完成实验。

## 豆包：复制就能开始

1. 打开 [豆包完整提示词](prompts/doubao.md)，复制正文到一个新对话。GitHub 的 Raw 按钮可查看纯文本。
2. 发“预习＋实验名称”，附教材内容；或发“写实验报告＋实验名称”，附教材要求与实验记录。使用当前环境支持的附件方式，也可以直接输入文字。
3. 写课后报告时，先核对 AI 列出的全部原始数据。明确回复确认范围，例如“表中全部数据确认，39.90 ms是两个周期”。
4. 核对报告结果与原始记录；补充资料后继续同一对话。

示例请求：

> 预习波尔共振实验。按下面的教材写原理概述和3个预习问题。

> 写数字示波器及其应用Ⅱ的实验报告。前面是教材，后面是实验记录。先完整列出原始数据让我核对。

> 这次老师要求写实验原理，请加在实验目的之前。

豆包版不预设账户有程序执行工具。不能执行计算或作图时，会给可复算步骤、作图表和手绘指导，并标明验证状态。

## 默认格式

| 阶段 | 输出 |
|---|---|
| 课前预习 | 300～500字原理概述＋3个问题，默认不附答案 |
| 课后报告 | 实验目的 → 实验仪器与实验方法 → 实验内容及数据处理 → 小结 → 实验思考题 |
| 课后实验原理 | 默认省略；用户明确要求或课程要求包含时，放在实验目的前 |
| 小结 | 约600字，分实验结论、误差分析、改进建议 |

所有来源的数据都先核对。已经明确确认的数据不重复问；更改数据后重新确认并更新相关结果。缺少资料时完成有依据的部分，标出待补，不编造数据、题目、观察结果或仪器精度。

数据处理优先遵循教材；未规定时，AI评估是否需要统计、不确定度和误差传递，并说明依据。有执行工具时运行计算与作图，输出实验图及手绘说明。

## Codex 与 Claude Code 安装

整个仓库就是一个技能目录，必须保留 `SKILL.md`、`references/` 和其他配套文件，不能只复制入口文件。

### Codex

在 Windows PowerShell 中安装到个人技能目录：

```powershell
New-Item -ItemType Directory -Force -Path "$HOME/.agents/skills" | Out-Null
git clone https://github.com/birdy2213756/physics-lab-report-skill.git "$HOME/.agents/skills/physics-lab-report-skill"
```

macOS/Linux：

```sh
mkdir -p ~/.agents/skills
git clone https://github.com/birdy2213756/physics-lab-report-skill.git ~/.agents/skills/physics-lab-report-skill
```

在新对话输入 `$physics-lab-report-skill` 并给出任务。未出现时重启或重新打开对话。也可放在项目的 `.agents/skills/physics-lab-report-skill/` 下；本地安装不会自动同步到云端，应将项目技能一起提交到云端使用的仓库。

目录与调用方式依据 [OpenAI 官方技能文档](https://learn.chatgpt.com/docs/build-skills)。旧版工具的安装位置可能不同，请按其支持的技能目录放置完整文件夹。

### Claude Code

Windows PowerShell：

```powershell
New-Item -ItemType Directory -Force -Path "$HOME/.claude/skills" | Out-Null
git clone https://github.com/birdy2213756/physics-lab-report-skill.git "$HOME/.claude/skills/physics-lab-report-skill"
```

macOS/Linux：

```sh
mkdir -p ~/.claude/skills
git clone https://github.com/birdy2213756/physics-lab-report-skill.git ~/.claude/skills/physics-lab-report-skill
```

输入 `/physics-lab-report-skill`，附教材和任务。项目安装可放在 `.claude/skills/physics-lab-report-skill/` 下。个人本地安装不会自动用于云端会话，云端需使用已提交的项目技能。

目录与调用方式依据 [Claude Code 官方技能文档](https://code.claude.com/docs/en/skills)。

已有同名目录时不要覆盖；确认目录来源后，在原仓库运行 `git pull --ff-only` 更新。

## 看看示例

- [波尔共振：课前预习](examples/bohl-prestudy.md)
- [数字示波器：原始数据核对记录](examples/oscilloscope/data.md)
- [数字示波器：课后报告](examples/oscilloscope/report.md)

数字示波器示例采用历史对话中已明确确认的文字数据，**没有重新核验原始截图**。部分资料缺失被保留为待补。图像仅比较派生结果，不是实测波形。

## 可选计算与作图

使用技能或豆包提示词无需安装Python。复现示例和运行绘图工具时使用 Python 3.10+：

```sh
python -m pip install -r requirements.txt
python scripts/calculate_oscilloscope.py examples/oscilloscope/input.json --output build/result.json --plot-input build/phase-input.json
python scripts/plot_data.py build/phase-input.json --output build/phase-comparison
```

详细参数见 [作图工具说明](references/tools.md)。数值脚本只适用于该示例；其他实验仍需选择相应公式。绘图工具支持散点、连接点及普通线性拟合，不自动判断复杂模型。

## 验证与贡献

```sh
python scripts/build_prompt.py --check
python -m unittest discover -s tests -v
```

修改规则后运行 `python scripts/build_prompt.py`，重新生成豆包提示词。同一套共同规则和两种模式规则会完整组合到提示词中。

当前验收范围及待实测内容见 [验证记录](docs/validation.md)。脚本测试不代表AI一定遵循每条规则，也不代表三平台已经端到端实测。

欢迎提交真实问题、规则改进或去除个人信息的复现案例。新增实验案例需说明数据来源、确认状态、公式条件和验证方法，不能上传未经授权的教材全文或个人实验资料。

MIT，见 [LICENSE](LICENSE)。
