# 大学物理实验报告 Skill

**课前写预习，课后先核对数据，再写报告。** 适合需要手写大学物理实验报告的同学，提供技能安装和完整提示词两种入口。

本项目提供可安装的 AI 技能和可复制的中文提示词，不需要项目自己的模型 API Key。输入自己的教材和实验数据，不会拿示例数据替你完成实验。

## 先选使用方式

| 你的AI工具 | 怎么开始 | 是否需要复制提示词 |
|---|---|---|
| 支持安装外部技能，例如Codex、Claude Code | 按下方说明安装完整技能目录，确认能调用后提供任务和资料 | 安装并调用成功后不需要 |
| 没有外部技能安装入口，例如豆包普通聊天界面 | 把完整提示词发送到新对话，再提供任务和资料 | 需要；同一对话通常只发一次，新对话重新发送 |
| 豆包界面有外部技能导入入口 | 可尝试按当前界面导入完整技能包，检查是否出现在技能列表并能调用 | 成功调用后不需要；未成功时使用完整提示词 |

选择方式取决于当前界面的能力，不只取决于电脑或手机。**把GitHub链接发到聊天里，不等于安装成功。** 本项目尚未实测豆包的外部技能导入，不能承诺仅凭仓库链接自动安装。

Codex和Claude Code安装见[下方安装说明](#codex-与-claude-code-安装)；无安装入口的用户见[完整提示词用法](#没有技能安装入口复制完整提示词使用)。

## 教材下载

技能包已附《大学物理实验》（第三版），没有教材的同学可以直接下载，并结合自己的课程要求使用。

- [下载教材 PDF](https://github.com/birdy2213756/physics-lab-report-skill/releases/download/v1.1.0/university-physics-lab-3rd-edition.pdf)
- [下载含教材的完整技能包](https://github.com/birdy2213756/physics-lab-report-skill/releases/download/v1.1.0/physics-lab-report-skill-v1.1.0.zip)
- [仓库中的教材文件](textbooks/university-physics-lab-3rd-edition.pdf)
- [教材信息与授权说明](textbooks/README.md)

PDF为354页扫描版，约92.8 MB。Codex、Claude Code安装完整仓库后，可读取技能目录下的教材；豆包用户先下载，再按账户支持的附件方式提供相关页面。复制提示词不会自动把教材传入豆包，附件过大时可仅提供当前实验的页面。

已核对的定位：2.10波尔共振在PDF第119—125页，2.16数字示波器及其应用Ⅱ在PDF第182—186页。详细读取规则见[教材使用说明](references/textbook.md)。教材规定的标称参数不能当作个人实测数据。

教材由维护者确认具有公开分发授权后加入；教材不适用项目代码的MIT许可证，具体范围见授权说明。

## 没有技能安装入口：复制完整提示词使用

“完整提示词”是给AI的一整套报告规则，包含预习格式、课后格式、数据确认、计算及作图要求。这种方式把规则交给当前对话，不是在电脑或手机里安装软件。

1. 打开 [完整提示词](prompts/doubao.md)，复制文件的全部正文，在豆包或其他聊天工具的新对话中粘贴并发送。GitHub 的 Raw 按钮可查看纯文本；复制文字内容，不是只复制页面链接。
2. 接着发“预习＋实验名称”，附教材内容；或发“写实验报告＋实验名称”，附教材要求与实验记录。使用当前环境支持的附件方式，也可以直接输入文字。
3. 写课后报告时，先核对 AI 列出的全部原始数据。明确回复确认范围，例如“表中全部数据确认，39.90 ms是两个周期”。
4. 核对报告结果与原始记录；补充资料后继续同一对话。

示例请求：

> 预习波尔共振实验。按下面的教材写原理概述和3个预习问题。

> 写数字示波器及其应用Ⅱ的实验报告。前面是教材，后面是实验记录。先完整列出原始数据让我核对。

> 这次老师要求写实验原理，请加在实验目的之前。

同一对话通常只需发送一次完整提示词，新开对话时重新发送。已经成功安装并调用技能的用户无需重复粘贴。两种方式都需要提供自己的实验数据；复制提示词不会自动传入教材附件，也不预设账户具有计算或作图工具。工具不足时提供可复算步骤、作图表和手绘指导，并标明尚未程序复核或生成验证图像。

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

已进行[独立Codex回答测试](docs/behavior-validation.md)，覆盖预习、数据确认、修改、单位冲突、可选原理及工具限制等8个场景，修正了教材反复读取、小结篇幅和FFT漏项问题。Claude Code与豆包尚未实测；本技能通过可复用规则约束输出，不涉及模型权重训练，也不承诺每次回答无误。

欢迎提交真实问题、规则改进或去除个人信息的复现案例。新增实验案例需说明数据来源、确认状态、公式条件和验证方法，不能上传未经授权的教材全文或个人实验资料。

项目自编代码、规则与文档采用MIT，见[LICENSE](LICENSE)；内附教材的版权与使用范围见[教材授权说明](textbooks/README.md)。
