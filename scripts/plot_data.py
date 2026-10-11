"""Plot confirmed points, with optional connection or ordinary linear fit."""

import argparse
import json
import math
from pathlib import Path
from statistics import mean


def prepare(data: dict) -> dict:
    if data.get("confirmed") is not True:
        raise ValueError("数据未确认，不能生成实验图")
    for key in ("confirmation_basis", "source", "title", "xlabel", "ylabel"):
        if not isinstance(data.get(key), str) or not data[key].strip():
            raise ValueError(f"缺少 {key}")
    x, y = data.get("x"), data.get("y")
    if not isinstance(x, list) or not isinstance(y, list) or len(x) != len(y) or not x:
        raise ValueError("x和y须为长度相同的非空列表")
    if any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) for v in x + y):
        raise ValueError("数据点必须是有限数值")
    fit = data.get("fit", "none")
    if fit not in ("none", "linear"):
        raise ValueError("仅支持none或linear；其他模型须按实际实验另行实现")
    connect = data.get("connect", False)
    if not isinstance(connect, bool):
        raise ValueError("connect须为布尔值")
    if connect and not (all(b > a for a, b in zip(x, x[1:])) or all(b < a for a, b in zip(x, x[1:]))):
        raise ValueError("连接点时x须严格单调；不会擅自排序或合并数据")
    ticks = data.get("xtick_labels")
    if ticks is not None and (not isinstance(ticks, list) or len(ticks) != len(x) or not all(isinstance(t, str) for t in ticks)):
        raise ValueError("xtick_labels须与点数一致")
    indices = data.get("fit_indices", list(range(len(x))))
    ylim = data.get("ylim")
    if ylim is not None:
        if not isinstance(ylim, list) or len(ylim) != 2 or any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) for v in ylim) or ylim[0] >= ylim[1]:
            raise ValueError("ylim须为递增的两个有限数值")
        if min(y) < ylim[0] or max(y) > ylim[1]:
            raise ValueError("ylim不能裁掉原始数据点")
    if not isinstance(indices, list) or not indices or any(type(i) is not int or i < 0 or i >= len(x) for i in indices) or len(set(indices)) != len(indices):
        raise ValueError("拟合索引须为不重复且有效的整数")
    if fit == "none" and "fit_indices" in data:
        raise ValueError("没有拟合时不要设置fit_indices")
    excluded = [i for i in range(len(x)) if i not in indices] if fit == "linear" else []
    if excluded and (data.get("selection_confirmed") is not True or not isinstance(data.get("selection_reason"), str) or not data["selection_reason"].strip()):
        raise ValueError("部分选点须有原因且经用户明确确认")
    result = {"source": data["source"], "confirmation_basis": data["confirmation_basis"], "x": x[:], "y": y[:], "fit": fit, "connect": connect, "fit_indices": indices if fit == "linear" else [], "excluded_indices": excluded}
    if ylim is not None:
        result["ylim"] = ylim[:]
    if fit == "linear":
        if len(indices) < 2:
            raise ValueError("拟合至少需要两个点")
        xs, ys = [x[i] for i in indices], [y[i] for i in indices]
        mx, my = mean(xs), mean(ys)
        sxx = sum((v - mx) ** 2 for v in xs)
        if sxx == 0:
            raise ValueError("横坐标完全相同，无法拟合斜率")
        slope = sum((a - mx) * (b - my) for a, b in zip(xs, ys)) / sxx
        intercept = my - slope * mx
        residuals = [b - (slope * a + intercept) for a, b in zip(xs, ys)]
        if not all(math.isfinite(v) for v in [slope, intercept] + residuals):
            raise ValueError("拟合数值溢出，请核对单位和量级")
        result.update(slope=slope, intercept=intercept, residuals=residuals)
        if excluded:
            result["selection_reason"] = data["selection_reason"]
    return result


def render(data: dict, output: Path) -> dict:
    result = prepare(data)  # Validate before writing any output.
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import font_manager

    installed = {f.name for f in font_manager.fontManager.ttflist}
    for font in ("Microsoft YaHei", "SimHei", "Noto Sans CJK SC", "WenQuanYi Micro Hei"):
        if font in installed:
            plt.rcParams["font.sans-serif"] = [font, "DejaVu Sans"]
            break
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["svg.fonttype"] = "none"
    fig, ax = plt.subplots(figsize=(7.6, 4.8), layout="constrained")
    try:
        x, y = result["x"], result["y"]
        ax.scatter(x, y, color="#205a91", label=data.get("series_label", "Confirmed data"), zorder=3)
        if result["connect"]:
            ax.plot(x, y, color="#205a91", alpha=0.6, label="Point connection")
        if result["fit"] == "linear":
            used = result["fit_indices"]
            ends = [min(x[i] for i in used), max(x[i] for i in used)]
            ax.plot(ends, [result["slope"] * v + result["intercept"] for v in ends], color="#b45324", label="Linear fit")
            excluded = result["excluded_indices"]
            if excluded:
                ax.scatter([x[i] for i in excluded], [y[i] for i in excluded], facecolors="none", edgecolors="#b45324", s=100, label="Excluded from fit", zorder=4)
        if data.get("xtick_labels") is not None:
            ax.set_xticks(x, data["xtick_labels"])
        ax.set(title=data["title"], xlabel=data["xlabel"], ylabel=data["ylabel"])
        if data.get("ylim") is not None:
            ax.set_ylim(data["ylim"])
        ax.grid(alpha=0.2)
        ax.legend()
        output.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output.with_suffix(".png"), dpi=180)
        fig.savefig(output.with_suffix(".svg"))
        result.update(title=data["title"], xlabel=data["xlabel"], ylabel=data["ylabel"])
        output.with_suffix(".json").write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    finally:
        plt.close(fig)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path, required=True, help="Output stem; creates .png, .svg, .json")
    args = parser.parse_args()
    try:
        render(json.loads(args.input.read_text(encoding="utf-8-sig")), args.output)
    except (ValueError, KeyError, TypeError, OSError, ImportError) as exc:
        parser.exit(2, f"无法作图：{exc}\n")
    print("已生成图像和作图记录；请打开图像核对标签、数据点与拟合。")


if __name__ == "__main__":
    main()
