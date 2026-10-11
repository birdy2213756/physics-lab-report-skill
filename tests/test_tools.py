"""Observable numerical, confirmation-gate, rendering and packaging checks."""

import copy
import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_prompt import render_prompt
from calculate_oscilloscope import calculate, plot_input
from plot_data import prepare, render


class CalculationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.data = json.loads((ROOT / "examples/oscilloscope/input.json").read_text(encoding="utf-8"))

    def test_reference_results(self) -> None:
        result = calculate(self.data)
        self.assertAlmostEqual(result["tau_approx_s"], 0.760)
        self.assertAlmostEqual(result["capacitance_approx_uF"], 38.0)
        self.assertAlmostEqual(result["capacitance_nominal_deviation_percent"], 19.1489361702)
        self.assertAlmostEqual(result["period_s"], 0.01995)
        self.assertAlmostEqual(result["phase_theory_deg"], 17.3925139401)
        self.assertAlmostEqual(result["phase_dual_trace_deg"], 23.4586466165)
        self.assertAlmostEqual(result["phase_lissajous_deg"], 17.9202131394)
        self.assertAlmostEqual(result["lissajous_relative_difference_percent"], 3.0340593722)

    def test_equivalent_units_and_cursor_direction(self) -> None:
        changed = copy.deepcopy(self.data)
        for rec in changed["quantities"].values():
            if rec["unit"] == "ms":
                rec["value"] /= 1000
                rec["unit"] = "s"
            elif rec["unit"] == "kohm":
                rec["value"] *= 1000
                rec["unit"] = "ohm"
            elif rec["unit"] == "uF":
                rec["value"] /= 1e6
                rec["unit"] = "F"
        changed["quantities"]["rc_cursor_delta"]["value"] *= -1
        changed["quantities"]["phase_cursor_delta"]["value"] *= -1
        actual, expected = calculate(changed), calculate(self.data)
        for key, value in expected.items():
            if isinstance(value, float):
                self.assertAlmostEqual(actual[key], value, places=12)
            else:
                self.assertEqual(actual[key], value)

    def test_two_period_span_is_not_single_period(self) -> None:
        changed = copy.deepcopy(self.data)
        changed["quantities"]["period_count"]["value"] = 1
        result = calculate(changed)
        self.assertAlmostEqual(result["period_s"], 0.03990)
        self.assertAlmostEqual(result["phase_dual_trace_deg"], 11.7293233083)

    def test_rejects_unconfirmed_and_missing_confirmation(self) -> None:
        for field, value in [("confirmed", False), ("confirmed", "true"), ("confirmation_basis", "")]:
            changed = copy.deepcopy(self.data)
            changed[field] = value
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                calculate(changed)

    def test_rejects_ambiguous_units_and_missing_source(self) -> None:
        for field, value in [("unit", "V"), ("unit", "unknown"), ("source", "")]:
            changed = copy.deepcopy(self.data)
            changed["quantities"]["rc_resistance"][field] = value
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                calculate(changed)

    def test_rejects_invalid_domain_and_nonfinite_values(self) -> None:
        cases = [("lissajous_intercept_width", 20), ("period_count", 1.5), ("rc_resistance", 0), ("rc_nominal_capacitance", 0), ("threshold_voltage", 9), ("frequency", float("nan")), ("frequency", True)]
        for name, value in cases:
            changed = copy.deepcopy(self.data)
            changed["quantities"][name]["value"] = value
            with self.subTest(name=name, value=value), self.assertRaises(ValueError):
                calculate(changed)

    def test_cli_does_not_write_when_unconfirmed(self) -> None:
        self.data["confirmed"] = False
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            source = folder / "input.json"
            source.write_text(json.dumps(self.data), encoding="utf-8")
            output = folder / "result.json"
            proc = subprocess.run([sys.executable, str(ROOT / "scripts/calculate_oscilloscope.py"), str(source), "--output", str(output)], capture_output=True)
            self.assertEqual(proc.returncode, 2)
            self.assertFalse(output.exists())

    def test_published_results_are_reproducible(self) -> None:
        expected = json.loads((ROOT / "examples/oscilloscope/result.json").read_text(encoding="utf-8"))
        self.assertEqual(calculate(self.data), expected)
        chart = json.loads((ROOT / "examples/oscilloscope/phase-input.json").read_text(encoding="utf-8"))
        self.assertEqual(plot_input(expected), chart)


class PlotTests(unittest.TestCase):
    def setUp(self) -> None:
        # Deliberately synthetic points for mathematical tests, not measured data.
        self.data = {"confirmed": True, "confirmation_basis": "Confirmed synthetic test fixture", "source": "Synthetic mathematical test", "title": "Synthetic linear test", "xlabel": "Time / s", "ylabel": "Distance / m", "x": [0, 1, 2, 3], "y": [1, 3, 5, 7], "fit": "linear"}

    def test_known_linear_relation(self) -> None:
        result = prepare(self.data)
        self.assertEqual(result["slope"], 2)
        self.assertEqual(result["intercept"], 1)
        self.assertEqual(result["residuals"], [0, 0, 0, 0])
        self.assertEqual(result["fit_indices"], [0, 1, 2, 3])

    def test_selection_requires_confirmation_and_preserves_all_points(self) -> None:
        self.data.update(y=[1, 3, 5, 100], fit_indices=[0, 1, 2])
        with self.assertRaises(ValueError):
            prepare(self.data)
        self.data.update(selection_confirmed=True, selection_reason="Synthetic selection test")
        result = prepare(self.data)
        self.assertEqual(result["slope"], 2)
        self.assertEqual(result["y"], [1, 3, 5, 100])
        self.assertEqual(result["excluded_indices"], [3])

    def test_invalid_inputs(self) -> None:
        for update in [{"confirmed": False}, {"x": [1, 1, 1, 1]}, {"y": [1, 2]}, {"y": [1, 2, 3, math.inf]}, {"fit_indices": [0, 0]}, {"fit_indices": [0, 8]}, {"fit_indices": [True, 1]}, {"fit": "quadratic"}, {"xlabel": ""}, {"connect": "yes"}, {"x": [0, 2, 1, 3], "connect": True}, {"ylim": [4, 5]}, {"ylim": [0, math.inf]}]:
            with self.subTest(update=update), self.assertRaises(ValueError):
                prepare({**self.data, **update})

    def test_rendered_labels_points_and_image(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            stem = Path(tmp) / "chart"
            result = render(self.data, stem)
            self.assertEqual(result["x"], self.data["x"])
            self.assertEqual(result["y"], self.data["y"])
            self.assertEqual(json.loads(stem.with_suffix(".json").read_text(encoding="utf-8")), result)
            svg = ET.parse(stem.with_suffix(".svg"))
            text = " ".join(svg.getroot().itertext())
            for label in [self.data["title"], self.data["xlabel"], self.data["ylabel"], "Linear fit"]:
                self.assertIn(label, text)
            from PIL import Image, ImageStat
            with Image.open(stem.with_suffix(".png")) as img:
                self.assertGreater(img.width, 1000)
                self.assertGreater(min(ImageStat.Stat(img.convert("RGB")).stddev), 10)

    def test_no_files_created_before_confirmation(self) -> None:
        self.data["confirmed"] = False
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "new-folder/chart"
            with self.assertRaises(ValueError):
                render(self.data, output)
            self.assertFalse(output.parent.exists())

    def test_published_plot_matches_computed_points(self) -> None:
        folder = ROOT / "examples/oscilloscope"
        chart = json.loads((folder / "phase-input.json").read_text(encoding="utf-8"))
        manifest = json.loads((folder / "phase-comparison.json").read_text(encoding="utf-8"))
        for key, value in prepare(chart).items():
            self.assertEqual(manifest[key], value)


class PackagingTests(unittest.TestCase):
    def test_standalone_prompt_matches_rule_sources(self) -> None:
        self.assertEqual((ROOT / "prompts/doubao.md").read_text(encoding="utf-8"), render_prompt())

    def test_local_markdown_links_resolve(self) -> None:
        import re
        for file in ROOT.rglob("*.md"):
            for target in re.findall(r"\]\(([^\s)]+)\)", file.read_text(encoding="utf-8")):
                if "://" in target or target.startswith("#"):
                    continue
                with self.subTest(file=file.relative_to(ROOT), target=target):
                    self.assertTrue((file.parent / target.split("#")[0]).exists())


if __name__ == "__main__":
    unittest.main()
