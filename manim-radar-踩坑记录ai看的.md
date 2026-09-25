# manim-radar 使用踩坑记录（给 AI 和人看）

> 环境：Manim **Community (CE) v0.21.0**，Python 3.12，venv 路径 `/Users/fengtianzhu/venvs/manim`。
> 插件：`manim_radar` 0.1.0，可编辑安装自 `/Users/fengtianzhu/Desktop/manim-radar`。
> 这份文件记录一次渲染测试中真实踩到的坑，复制即可避坑。

## 快速验证插件可用

```python
from manim import *
from manim_radar import RadarChart, DeepSpace

AXES = ["Speed", "Power", "Range", "Crit", "Def", "Mana"]

class Demo(Scene):
    def construct(self):
        self.add(DeepSpace())
        chart = RadarChart(axes=AXES, values=[8,5,7,4,6,9],
                           color="#FF6B6B", theme="aurora", style="neo")
        self.play(chart.reveal())
        self.play(chart.morph_to([4,9,5,9,7,6], color="#4ECDC4"))  # 见坑 #1
```

## 坑 #1：`morph_to()` 入参写法

**错误写法（会报 TypeError）：**
```python
chart.morph_to(values=[4,9,5,9,7,6], color="#4ECDC4")
# TypeError: RadarChart.morph_to() missing 1 required positional argument: 'data'
```

**正确写法：** 第一个位置参数直接传数值列表（或 `RadarData` 对象），不要用 `values=`。
```python
chart.morph_to([4,9,5,9,7,6], color="#4ECDC4", name="Mage")
# 或：
from manim_radar import RadarData
chart.morph_to(RadarData(axes=AXES, values=[4,9,5,9,7,6], color="#4ECDC4"))
```

转场特效通过 `transition=` 选：`smooth`（默认）/ `dip` / `shockwave` / `zoom` / `glitch` / `stepped`。

## 坑 #2：在插件源码目录里跑 Python 会循环导入

**症状：** 在 `src/manim_radar/` 目录下执行 `import manim_radar` 或跑脚本，报：
```
AttributeError: partially initialized module 'numpy' has no attribute 'ndarray' (most likely due to a circular import)
```

**根因：** 插件里有个文件叫 `numbers.py`。当 cwd 就在包目录内时，numpy 内部 `import numbers` 会误加载到这个本地文件，而不是 Python 标准库的 `numbers`，于是循环导入。

**解决：** 永远从**普通目录**（项目目录或 `~`）调用 manim / python，不要 `cd` 进 `src/manim_radar/`。
```bash
cd /Users/fengtianzhu/Doubao/chats/<项目目录>
/Users/fengtianzhu/venvs/manim/bin/manim render -qm -r 1920,1080 demo.py Demo
```

## 坑 #3：插件"打包了但没装进环境"

**症状：** 桌面 `manim-radar/dist/` 里有 whl，但 `import manim_radar` 报 `ModuleNotFoundError`。

**解决：** 用可编辑模式安装（不复制第二份代码，改源码即生效，不翻倍占盘）：
```bash
/Users/fengtianzhu/venvs/manim/bin/pip install -e /Users/fengtianzhu/Desktop/manim-radar
```
验证：`/Users/fengtianzhu/venvs/manim/bin/python -c "import manim_radar; print(manim_radar.__file__)"`

## 常用参数速查

- 主题 `theme=`：`midnight / aurora / ember / violet / paper`
- 风格 `style=`：`neo / classic / minimal`
- `numbers=`：`roll / swap / off`
- 其他：`levels=4`、`radius=2.6`、`title=...`、`color=...`
- 批量播放：`RadarReel(chart, [RadarData(...), ...]).play_on(self)`（自动 intro/hold/outro）

---

# 0.1.1 开发中新增的坑（本文件夹副本独有）

## 坑 #4：0.1.1 测试/渲染别动 venv 的可编辑安装

venv 里 `manim_radar` 仍以可编辑模式指向老文件夹 `~/Desktop/manim-radar`（0.1.0）。
0.1.1 文件夹**不要** `pip install -e` 进 venv（除非用户明确要求切换），测试与渲染用
`PYTHONPATH=src` 临时遮蔽即可（PYTHONPATH 先于 site-packages 生效）：

```bash
cd /Users/fengtianzhu/Desktop/manim-radar-0.1.1
PYTHONPATH=src /Users/fengtianzhu/venvs/manim/bin/python -m pytest tests -q
PYTHONPATH=src /Users/fengtianzhu/venvs/manim/bin/manim -ql --media_dir \
  ~/Desktop/manim-radar-0.1.1-scratch/media examples/07_compare.py Compare
```

要正式切换到 0.1.1 时（用户同意后）：
`/Users/fengtianzhu/venvs/manim/bin/pip install -e /Users/fengtianzhu/Desktop/manim-radar-0.1.1`

## 坑 #5：`.animate.scale()` 不能把 `run_time` 塞进 scale()

```python
chart.animate.scale(1.35, about_point=c, run_time=0.8)   # ❌ scale() 不收 run_time，直接 TypeError
builder = chart.animate.scale(1.35, about_point=c)
builder.set_run_time(0.8)                                 # ✅ _AnimationBuilder 有 set_run_time
```

CameraRig 内部统一走 `set_run_time`。

## 坑 #6：Manim 颜色经线性空间往返，hex 会漂移

`RoundedRectangle(stroke_color="#FF0000")` 之后 `get_stroke_color().to_hex()`
返回 `#FF1414`（gamma 往返误差）。测试断言颜色要用通道比较（红分量 > 0.9 等），
不要比对 hex 字符串。

## 坑 #7：越界数值的对齐要跟随尖峰方向

顶点数字若固定左对齐（`aligned_edge=LEFT`），左侧轴的数字会往回压住轴名。
`RollingNumber.render(..., align=)` 支持 `"left"/"right"/"center"`，
图表按 `direction[0]` 自动选（见 `RadarChart._vertex_align`）。

## 坑 #8：Manim 0.21 的 Polygon 必须至少给一个顶点

`Polygon(fill_opacity=0)` 直接构造会在 set_points 时报
`ValueError: not enough values to unpack`。占位多边形要给退化顶点：
`Polygon(ORIGIN, ORIGIN, ORIGIN, ORIGIN)`。
