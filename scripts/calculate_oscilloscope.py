"""Reproduce the confirmed oscilloscope text example; not a general solver."""

import argparse
import json
import math
from pathlib import Path

UNITS = {
    "resistance": {"ohm": 1.0, "kohm": 1e3},
    "capacitance": {"F": 1.0, "uF": 1e-6, "nF": 1e-9},
    "time": {"s": 1.0, "ms": 1e-3},
    "voltage": {"V": 1.0, "mV": 1e-3},
    "frequency": {"Hz": 1.0, "kHz": 1e3},
    "count": {"cycles": 1.0},
}


def quantity(data: dict, name: str, dimension: str) -> float:
    record = data["quantities"][name]
    raw = record["value"]
    if isinstance(raw, bool) or not isinstance(raw, (int, float)) or not math.isfinite(raw):
        raise ValueError(f"{name}: 数值必须有限且不是布尔值")
    unit = record["unit"]
    if unit not in UNITS[dimension]:
        raise ValueError(f"{name}: 不支持或量纲错误的单位 {unit!r}")
    if not isinstance(record.get("source"), str) or not record["source"].strip():
        raise ValueError(f"{name}: 缺少来源")
    return raw * UNITS[dimension][unit]


def calculate(data: dict) -> dict:
    if data.get("confirmed") is not True:
        raise ValueError("原始数据未确认：先展示核对表，等待用户明确确认")
    if not isinstance(data.get("confirmation_basis"), str) or not data["confirmation_basis"].strip():
        raise ValueError("缺少明确确认依据，不能自行把 confirmed 改为 true")
    rc_r = quantity(data, "rc_resistance", "resistance")
    nominal_c = quantity(data, "rc_nominal_capacitance", "capacitance")
    initial_u = quantity(data, "initial_voltage", "voltage")
    final_u = quantity(data, "threshold_voltage", "voltage")
    rc_dt = quantity(data, "rc_cursor_delta", "time")
    r = quantity(data, "phase_resistance", "resistance")
    c = quantity(data, "phase_capacitance", "capacitance")
    f = quantity(data, "frequency", "frequency")
    delay = quantity(data, "phase_cursor_delta", "time")
    span = quantity(data, "period_cursor_span", "time")
    cycles = quantity(data, "period_count", "count")
    a = quantity(data, "lissajous_full_width", "voltage")
    b = quantity(data, "lissajous_intercept_width", "voltage")
    if min(rc_r, nominal_c, initial_u, r, c, f, span, a) <= 0:
        raise ValueError("电阻、电容、初始电压、频率、周期跨度和全宽须大于零")
    if not 0 < final_u < initial_u or rc_dt == 0:
        raise ValueError("RC放电须满足 0 < U < E 且时间间隔非零")
    if cycles < 1 or not cycles.is_integer():
        raise ValueError("跨越周期数必须为已确认的正整数")
    if not 0 <= b <= a:
        raise ValueError("李萨如截距宽度须在0与全宽之间；检查量的定义与单位")
    tau = abs(rc_dt)
    period = span / cycles
    phi0 = math.degrees(math.atan(2 * math.pi * f * r * c))
    phi1 = abs(delay) / period * 360
    if phi1 >= 90:
        raise ValueError("本示例仅支持已确认的0～90度相位差大小，不能自行选择分支")
    phi2 = math.degrees(math.asin(b / a))
    measured_c = tau / rc_r
    return {
        "verification": "executed_python_from_confirmed_text",
        "source_limit": "原始截图未重新核验；计算仅对应已确认的文字数据",
        "tau_approx_s": tau,
        "capacitance_approx_uF": measured_c * 1e6,
        "capacitance_nominal_deviation_percent": abs(measured_c - nominal_c) / nominal_c * 100,
        "threshold_ratio": final_u / initial_u,
        "threshold_ratio_target": math.exp(-1),
        "period_s": period,
        "phase_theory_deg": phi0,
        "phase_dual_trace_deg": phi1,
        "phase_lissajous_deg": phi2,
        "dual_trace_relative_difference_percent": abs(phi1 - phi0) / phi0 * 100,
        "lissajous_relative_difference_percent": abs(phi2 - phi0) / phi0 * 100,
        "phase_sign": "只比较相位差大小，资料不足以判定超前或滞后",
        "approximation": "依教材阈值法将接近E/e的读数对应间隔近似取为时间常数",
    }


def plot_input(result: dict) -> dict:
    return {
        "confirmed": True,
        "confirmation_basis": "源数据已明确确认且calculate_oscilloscope.py成功复算",
        "source": result["source_limit"] + "；本图为派生结果比较，非示波器实测波形",
        "title": "Phase comparison (derived values)",
        "xlabel": "Method",
        "ylabel": "Phase difference / deg",
        "x": [1, 2, 3],
        "y": [result["phase_theory_deg"], result["phase_dual_trace_deg"], result["phase_lissajous_deg"]],
        "xtick_labels": ["Circuit theory", "Dual trace", "Lissajous"],
        "series_label": "Derived from confirmed text",
        "ylim": [0, 30],
        "fit": "none",
        "connect": False,
    }


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--plot-input", type=Path)
    args = parser.parse_args()
    try:
        result = calculate(json.loads(args.input.read_text(encoding="utf-8-sig")))
    except (ValueError, KeyError, TypeError, OSError) as exc:
        parser.exit(2, f"无法计算：{exc}\n")
    if args.output:
        write_json(args.output, result)
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
    if args.plot_input:
        write_json(args.plot_input, plot_input(result))


if __name__ == "__main__":
    main()
