"""Build the standalone chat prompt from the rules also read by skill hosts."""

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ("common.md", "prestudy.md", "report.md")
INTRO = """# 大学物理实验报告助手：豆包等聊天工具可复制的完整提示词

你是我的大学物理实验学习与报告助手。请在当前对话中遵循下面的规则。
用户当次明确需求优先；如果需求没有说明，采用这里的默认格式。
我说“预习”时使用课前模式，说“写实验报告”时使用课后模式；概念追问直接解释。
两种模式同时要求时分开输出。模式确实不清楚时只问预习还是课后报告。
请等待我提供实验名称、教材或数据；不要用示例数字填充我的实验。
以下规则可独立使用，不需要读取外部文件，也不预设你有计算或作图工具。

"""


def render_prompt() -> str:
    return INTRO + "\n\n---\n\n".join(
        (ROOT / "references" / name).read_text(encoding="utf-8").strip()
        for name in SOURCES
    ) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    target = ROOT / "prompts" / "doubao.md"
    rendered = render_prompt()
    if args.check:
        if not target.is_file() or target.read_text(encoding="utf-8") != rendered:
            parser.exit(1, "豆包提示词未同步：运行 python scripts/build_prompt.py\n")
        print("豆包提示词与共同规则一致。")
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(rendered, encoding="utf-8")
        print("已生成 prompts/doubao.md")


if __name__ == "__main__":
    main()
