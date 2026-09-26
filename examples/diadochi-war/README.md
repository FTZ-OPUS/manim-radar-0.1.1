# 继业者战争：manim-radar 0.1.1 应用案例

这个案例使用 `manim-radar` 0.1.1 制作一段继业者人物战力雷达图动画。场景展示 15 位人物的八维评分，包含越界数值、多色图表、镜头强调，以及 `burst`、`shockwave`、`zoom`、`dip`、`glitch` 等转场。

## 文件

- `diadochi_radar.py`：Manim 动画源码。
- `assets/portraits/`：源码使用的人物竖图素材。
- 成片： [下载 1080p60 MP4](./DiadochiShowcase.mp4)。

## 运行

需要 Python 3.10 或更新版本、Manim Community 以及 `manim-radar` 0.1.1。安装依赖后，在本目录运行：

```bash
pip install manim manim-radar==0.1.1
manim -qh diadochi_radar.py DiadochiShowcase
```

源码与素材目录相对定位，不依赖作者电脑上的绝对路径。运行后，Manim 会在 `media/` 下生成渲染文件。

## 说明

人物评分、文案、转场与布局都在 `diadochi_radar.py` 中，适合作为多数据绘图、越界雷达图、镜头控制和转场效果的组合示例。
