# 可选计算与作图工具

文字技能不依赖Python。只有具备可执行环境、数据已经确认且需要程序验证或作图时才使用这些工具。输入JSON中的`confirmed`与`confirmation_basis`是对实际用户确认的记录，不是让模型自行授权的开关。

## 数字示波器示例复算

Python 3.10+，不需要第三方库。在技能目录运行：

```sh
python scripts/calculate_oscilloscope.py examples/oscilloscope/input.json --output build/result.json --plot-input build/phase-input.json
```

这个计算器只支持示例中的RC阈值法、双踪法及0～90度相位差大小的李萨如法。`input.json`保留原始数值、单位和来源。支持的单位见脚本；遇到其他单位需明确换算，不猜测。它不负责从截图识别数据，也不能证明来源中的用户确认真实存在。

教材若要求用精确指数关系处理任意两个电压点，应另用相应公式；这里依教材阈值法近似取\(\tau=|\Delta t|\)，不能无说明地替换数据处理方法。不得把此脚本用于其他电路或相位分支。

## 通用基础作图

安装`requirements.txt`后运行：

```sh
python scripts/plot_data.py build/phase-input.json --output build/phase-comparison
```

生成PNG、SVG和包含全部原始点、选点及拟合参数的JSON记录。打开图像检查后才宣称图像已核查。

最小输入：

```json
{
  "confirmed": true,
  "confirmation_basis": "用户已确认当前完整数据表",
  "source": "用户实验表格（自行填入实际来源）",
  "title": "Experiment title",
  "xlabel": "x / unit",
  "ylabel": "y / unit",
  "x": [1, 2, 3],
  "y": [2, 4, 6],
  "fit": "none",
  "connect": false
}
```

以上数字仅解释接口，是教学模拟数据，不能用作实测结果。实际使用须换成用户已确认的数据。

- `fit`：`none`或`linear`。直线拟合为普通最小二乘，假定横坐标误差可忽略且纵坐标适合等权处理，不自动给出参数不确定度；不适用时另选方法。
- `connect`：默认`false`。设为`true`时须明确连接测量点有物理意义，横坐标须严格单调；程序不会擅自排序。
- `fit_indices`：仅在线性拟合时可用的零基索引，默认全部点。部分选点需同时提供`selection_confirmed: true`和`selection_reason`，排除点仍显示在图中。
- `xtick_labels`：可选，与点数相同的分类标签；比较不同方法时使用，不用于连续曲线。
- `series_label`：可选，区分实测点、理论值和派生结果。支持中文，但环境需有中文字体，否则可采用明确的英文轴标签并在报告中解释。
- `ylim`：可选的纵轴范围，例如`[0, 30]`。须覆盖全部原始数据点，不通过裁剪坐标隐藏偏离结果。

脚本拒绝未确认数据、无来源、单位标签缺失、非有限数值、无效拟合索引及相同横坐标拟合。复杂拟合、误差棒、权重及非线性模型不由该工具自动推断；根据课程要求另行计算和绘制。
