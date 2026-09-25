# manim-radar

**给 [Manim](https://www.manim.community/) 用的雷达图（蛛网图）动画库 —— 建一张图、一句话变形到另一张、或者一句话播完整条序列。**

[![PyPI](https://img.shields.io/pypi/v/manim-radar?color=17b8ba)](https://pypi.org/project/manim-radar/)
[![Python](https://img.shields.io/pypi/pyversions/manim-radar)](https://pypi.org/project/manim-radar/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![CI](https://github.com/FTZ-OPUS/manim-radar/actions/workflows/ci.yml/badge.svg)](https://github.com/FTZ-OPUS/manim-radar/actions/workflows/ci.yml)

![manim-radar 0.1.1 showcase](https://raw.githubusercontent.com/FTZ-OPUS/manim-radar-0.1.1/main/docs/showcase-0.1.1.gif)

```python
from manim import *
from manim_radar import RadarChart, DeepSpace, set_scene_background

AXES = ["速度", "力量", "续航", "舒适", "价格", "安全"]

class Demo(Scene):
    def construct(self):
        set_scene_background("midnight")
        chart = RadarChart(axes=AXES, values=[8, 6, 7, 9, 5, 8], title="六维雷达图")

        self.add(DeepSpace().link(chart))              # 可选：星空背景
        self.play(chart.reveal())                      # 从中心生长入场
        self.play(chart.morph_to([5, 9, 5, 6, 9, 9],   # 一句命令 = 一次变形
                                 color="#FFB74D"))
        self.play(chart.disappear())
```

```bash
manim -qh demo.py Demo          # 1080p60
```

---

## 安装

```bash
pip install manim_radar
```

需要 Python ≥ 3.9、`manim >= 0.18`、`numpy`（pip 会自动装）。

## 特性

| | |
|---|---|
| **一句话变形** | `chart.morph_to(...)` 同时补间：数值、满量程、颜色、强调描边、透明度 |
| **七种转场预设** | `smooth`、`dip`、`shockwave`、`zoom`、`glitch`、`stepped`、`burst`（0.1.1 新增），且每个参数都可细调 |
| **多组同图对比** | `datasets=[dA, dB]`：多张数据多边形共享一张网格，一起变形、一起播放（0.1.1 新增） |
| **越界雷达图** | `OverflowRadarChart`：数值超过满量程直接刺出外圈，虚线轨道 + 破口辉光 + 真实值大数字（0.1.1 新增） |
| **镜头语言** | `chart.push_in() / pull_out()`，或 `CameraRig` 真相机推拉平移（0.1.1 新增） |
| **一句话播序列** | `RadarReel(chart, snapshots).play_on(self)` 自动串起整条序列，含黑场间隔 |
| **3 种风格 × 5 套主题** | `neo`（辉光/彩虹描边/扫光）、`classic`（1.0 的简洁版）、`minimal`（浅色报告用） |
| **滚轮数字** | 数字连续滚动而不是硬跳，超出满量程自动显示 `10+` |
| **标准 Manim 元素** | 图表就是 `VGroup`：`shift` / `move_to` / `scale` / `rotate` / `FadeIn` / `FadeOut` 都正常 |
| **深空背景** | `DeepSpace` 提供中心辉光、四角暗角、星云团与漂移星点，颜色跟随图表呼吸 |
| **两代版本内置** | `RadarV1Scene` / `RadarV2Scene` 用本库重建 1.0 与 2.0 两条成片序列 |
| **跨平台字体** | 自动挑选系统里可用的中文字体/等宽字体，macOS / Linux / Windows 都能跑 |

## 演示动图

下面每张 GIF 都是用对应的示例场景直接渲出来的（`manim -ql` + `ffmpeg`），原图都在 [`docs/`](docs/) 里。

| | |
|---|---|
| ![0.1.1 新功能展示](https://raw.githubusercontent.com/FTZ-OPUS/manim-radar-0.1.1/main/docs/showcase-0.1.1.gif) | **0.1.1 新功能展示** —— 多组数据对比、越界尖峰和镜头推进。`examples/10_showcase.py` |
| ![quickstart](https://raw.githubusercontent.com/FTZ-OPUS/manim-radar-0.1.1/main/docs/quickstart.gif) | **快速上手** —— 建图 → 入场 → 变形 → 出场，一共十行。`examples/01_quickstart.py` |
| ![transitions](https://raw.githubusercontent.com/FTZ-OPUS/manim-radar-0.1.1/main/docs/demo.gif) | **转场一览** —— smooth / shockwave / zoom / glitch / rim。`examples/02_morph_gallery.py` |
| ![reel](https://raw.githubusercontent.com/FTZ-OPUS/manim-radar-0.1.1/main/docs/reel.gif) | **一句话播序列** —— 含黑场间隔的整条成片。`examples/03_reel.py` |
| ![styles](https://raw.githubusercontent.com/FTZ-OPUS/manim-radar-0.1.1/main/docs/styles.gif) | **3 种风格 × 5 套主题** —— 从 `neo` 辉光到浅色 `paper` 报告风。`examples/04_styles_themes.py` |
| ![classic vs neo](https://raw.githubusercontent.com/FTZ-OPUS/manim-radar-0.1.1/main/docs/classic-vs-neo.gif) | **两代对比** —— 同一组数据，classic(1.0) vs neo(2.0) 并排。`examples/05_two_styles.py` |

## 0.1.1 新功能

### 多组同图对比

0.1.0 的一张图只能挂一组数据；0.1.1 起可以画"赫尔德 vs 基本不等式"这种同图对比：

```python
holder = RadarData(axes=AXES, values=[8, 9, 10, 4, 9, 7], name="赫尔德不等式",
                   color="#17B8BA", max_value=10)
basic  = RadarData(axes=AXES, values=[10, 6, 5, 10, 7, 9], name="基本不等式",
                   color="#E868C8", max_value=10)

chart = RadarChart(datasets=[holder, basic], radius=2.4)
self.play(chart.reveal())

# 一起变形（stagger 让各组错峰推进，有波浪感）
self.play(chart.morph_to([holder_next, basic_next], stagger=0.15))

chart.focus(0)          # 高亮第 1 组、压暗其余（chart.unfocus() 还原）
chart.highlight_gap(0, 1)   # 差值高亮：月牙差值区着色，各瓣染上赢家的颜色
chart.clear_gap()
```

* 对比模式自动带**图例**（色块 + 名字胶囊，放不下自动换行）。
* 轴上数值有四种模式，用 `compare_numbers=` 切换：
  * `"legend"`（默认）—— 只显示图例，画面最干净；
  * `"all"` —— 每组数据在自己顶点旁显示各自颜色的小号数值；
  * `"first"` —— 数值只跟第一组；
  * `"focus"` —— 跟随 `chart.focus(i)`，显示聚焦组的数值。
* 满量程取各组快照的最大值，所有组在同一把尺子上读数。
* `RadarReel` 也支持对比快照——每一步传一组 `RadarData` 列表即可：

```python
RadarReel(chart, [
    [holder_a, basic_a],
    [holder_b, basic_b],
], hold=0.8, backdrop=True).play_on(self)
```

### 越界雷达图 OverflowRadarChart

数值超过满量程时不再是"10+"截断，而是直接**刺出外圈**：

```python
from manim_radar import OverflowRadarChart

chart = OverflowRadarChart(axes=AXES, values=[8, 6, 14, 9, 5, 8],
                           max_value=10, name="狂战士", color="#F040E0")
self.play(chart.burst_in())                     # 入场：从中心猛地刺出去
self.play(chart.morph_to([7, 9, 17, 6, 8, 5]))  # 默认 burst 转场
```

* 越界轴自动画**虚线轨道**延长轴线，尖峰保持多边形填充；
* 外圈被刺穿处有**破口辉光**（橙色呼吸光斑）；
* 越界数值显示**真实值**（14、17……），字号放大、骑在尖峰上；
* `transition="burst"`：数值先沉到目标的 20%，再一举刺穿、过冲回落；
* 普通图表也能用 burst：`chart.morph_to(data, transition="burst")`；
* **多组对比同样越界**：`OverflowRadarChart(datasets=[dA, dB], max_value=10)`
  —— 每组数据各自拥有尖峰、虚线轨道、破口辉光和真实值读数（见
  `examples/10_showcase.py` 宣传案例）。

### 镜头语言

```python
# 普通 Scene：缩放图表本体
self.play(chart.push_in(factor=1.35, run_time=0.8))   # 推近
self.play(chart.pull_out(factor=1.35, run_time=0.8))  # 拉远

# MovingCameraScene：真相机，星空背景一起呼吸
from manim_radar import CameraRig

class MyScene(MovingCameraScene):
    def construct(self):
        rig = CameraRig(self)
        self.play(rig.push_in(chart, factor=1.4))
        self.play(rig.focus_point(peak_vertex, factor=1.6))
        self.play(rig.pull_out())               # 回到原始取景
        chart.attach_camera(rig)                # 之后 burst 变形自动微推镜头
```

配套示例：`examples/07_compare.py`、`examples/08_overflow.py`、`examples/09_camera.py`。

## 三个核心对象

```python
from manim_radar import RadarChart, RadarData, RadarReel
```

**`RadarData`** —— 一份数据快照：轴名 + 每轴数值。

```python
RadarData(
    axes=["A", "B", "C", "D", "E", "F"],
    values=[8, 6, 7, 9, 5, 8],
    name="A 型",            # 可选：名字牌（每次变形都会做淡入淡出）
    color="#17B8BA",        # 可选：主色（不填则按主题调色板轮换）
    max_value=10,           # 可选：满量程；超出部分显示为 "10+"
    emphasis="rim",         # "zoom" | "gap" | "rim"，供 RadarReel 使用
    hold=0.6,               # 本快照停留秒数（RadarReel）
    transition="glitch",    # 单独指定该快照的转场
)
```

**`RadarChart`** —— 图表本体。

```python
chart = RadarChart(data_or_axes=..., style="neo", theme="midnight", radius=3.2)

chart.set_values([1, 2, 3, 4, 5, 6])   # 直接改（无动画）
chart.set_main_color("#E868C8")
chart.set_rim(1.0)                     # 橙蓝强调描边
chart.set_radius(2.4)
chart.attach_backdrop(self)            # 等价于 DeepSpace().link(chart)

self.play(chart.reveal())              # 入场
self.play(chart.morph_to(other))       # 主角：一次变形
self.play(chart.glitch_in())           # 故障闪入
self.play(chart.disappear())           # 出场
```

**`RadarReel`** —— 一行播完整条序列。

```python
RadarReel(
    chart,
    snapshots=[d1, d2, d3, d4],   # list[RadarData]
    hold=0.6,                     # 每个快照默认停留
    transition="shockwave",       # 默认转场
    backdrop=True,                # 星空背景（自动跟随主色）
    gap_hold=1.5,                 # 某快照标 emphasis="gap" 时的黑场时长
).play_on(self)
```

## 转场一览

| `transition=` | 效果 |
|---|---|
| `None`（默认） | 数值先沉到目标下方，再滚动上涨（`neo` 招牌动作） |
| `"smooth"` | 直接平滑补间，不沉 |
| `"shockwave"` | 先沉 + 一圈扩散冲击波，把形变盖住 |
| `"zoom"` | 冲击波 + 缩放压暗再回弹（大转场） |
| `"glitch"` | RGB 分离 + 闪烁，边抖边变形 |
| `"stepped"` | 数值按整数跳（`classic` 的手感） |
| `"burst"` | 沉到目标 20% 再一举刺穿、过冲回落（越界雷达图招牌，0.1.1 新增） |

```python
self.play(chart.morph_to(target, transition="zoom", run_time=1.6))
```

## 风格与主题

```python
chart = RadarChart(data, style="neo",              theme="midnight")
RadarChart(data, style="classic")                  # 1.0 的观感
RadarChart(data, style="minimal", theme="paper")   # 浅色底
```

* **风格**改结构：`neo` / `classic` / `minimal`（见 `STYLES`）。
* **主题**改颜色：`midnight` / `aurora` / `ember` / `violet` / `paper`。

两者都是 dataclass，可以基于预设改任意一项：

```python
from manim_radar import RadarChart, RadarConfig, RadarTheme

cfg = RadarConfig(radius=2.4, levels=4, numbers="swap", sweep=False, rainbow_edges=False)
theme = RadarTheme(name="mine", grid="#8899AA", axis_colors=("#5EEAD4", "#F0ABFC") * 3)
chart = RadarChart(data, config=cfg, theme=theme)
```

`RadarConfig` 有约 60 个带注释的字段：几何、网格、多边形分层、字体字号、装饰、
转场时长、标题/名字牌位置……`RadarTheme` 管理所有颜色（网格、逐轴配色、调色板、
描边、星点强调色等）。

## 放进更大的场景里用

```python
chart = RadarChart(AXES_DATA, radius=2.2)
chart.move_to(LEFT * 3.4)
self.play(chart.reveal())
self.play(chart.morph_to(next_data), Write(my_formula))
```

图表是普通 `VGroup`，几何每帧在自身坐标系里重算，所以随便移动/缩放都不会画崩。

## 背景

```python
from manim_radar import DeepSpace, set_scene_background

set_scene_background("midnight")           # 设置画布底色
backdrop = DeepSpace(theme="midnight", star_count=80, nebula_count=8)
backdrop.link(chart)                       # 星云/光晕跟随图表主色
self.add(backdrop)
```

## 两代版本内置

```bash
manim -qh examples/legacy_v1.py RadarV1Scene   # 1.0：冷灰网格、亮白描边、跳变数字
manim -qh examples/legacy_v2.py RadarV2Scene   # 2.0：辉光、彩虹描边、冲击波
```

两条序列播放的都是内置的 23 段示例数据（`manim_radar.legacy.REPLICA_TIMELINE`）。

## 命令行

```bash
manim-radar --version
manim-radar themes                  # 列出主题
manim-radar styles                  # 列出风格
manim-radar template my_chart.py    # 生成起始场景
manim-radar demo --render           # 渲染内置演示
```

## 渲染

```bash
manim -ql scene.py MyScene      # 480p15 快速预览
manim -qh scene.py MyScene      # 1080p60 正式
```

## 发布（PyPI）

标准 PEP 621 项目，构建后端为 **hatchling**：

```bash
python -m build            # -> dist/manim_radar-<版本>-py3-none-any.whl + .tar.gz
twine check dist/*
twine upload dist/*        # 或者用仓库里的 Release 工作流（PyPI Trusted Publishing）
```

本包注册为 Manim 插件（`manim.plugins` 入口），装完后 `manim plugins` 里能看到它。

## 许可

MIT，见 [LICENSE](LICENSE)。

---

同作者的另一件作品：[`manim-handdraw`](https://github.com/FTZ-OPUS/manim-handdraw)
（把线稿变成逐笔手绘动画）。
