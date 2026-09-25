# -*- coding: utf-8 -*-
"""07 · Comparison — two datasets on one grid (the 0.1.1 headline feature).

Two inequalities compared on one radar: Hölder vs the AM–GM basic
inequality. Shows the default legend-only look, focus dimming, the four
number modes and the crescent gap highlight.

    manim -qh examples/07_compare.py Compare
"""

from manim import *

from manim_radar import DeepSpace, RadarChart, RadarData, set_scene_background

AXES = ["公理性", "统一性", "推广性", "初等性", "应用广度", "边界情形"]

HÖLDER = dict(
    axes=AXES, name="赫尔德不等式", color="#17B8BA",
    max_value=10,
)
BASIC = dict(
    axes=AXES, name="基本不等式", color="#E868C8",
    max_value=10,
)


class Compare(Scene):
    def construct(self):
        set_scene_background("midnight")

        holder = RadarData(**HÖLDER, values=[8, 9, 10, 4, 9, 7])
        basic = RadarData(**BASIC, values=[10, 6, 5, 10, 7, 9])

        # compare_numbers="legend": names live in the legend, no numbers —
        # the cleanest look (default)
        chart = RadarChart(datasets=[holder, basic], compare_numbers="legend", radius=2.4)
        self.add(DeepSpace().link(chart))
        self.play(chart.reveal())
        self.wait(0.6)

        # 聚焦：高亮赫尔德，压暗基本不等式
        tip = Text("先看赫尔德", font_size=30).to_edge(DOWN)
        self.play(Write(tip))
        chart.focus(0)
        self.wait(1.2)
        chart.unfocus()
        self.play(FadeOut(tip))

        # 一起变形（错峰 stagger 让两组数据波浪推进）
        holder2 = RadarData(**HÖLDER, values=[9, 8, 10, 5, 10, 8])
        basic2 = RadarData(**BASIC, values=[9, 7, 6, 9, 8, 8])
        self.play(chart.morph_to([holder2, basic2], stagger=0.15))
        self.wait(0.5)

        # 差值高亮：月牙差值区着色，各自染上赢家的颜色
        chart.highlight_gap(0, 1, opacity=0.45)
        self.wait(1.4)
        chart.clear_gap()

        # 四种数值模式（都可用，按需切换）
        for mode, label in (
            ("all", "compare_numbers='all'"),
            ("first", "compare_numbers='first'"),
            ("legend", "compare_numbers='legend'"),
            ("focus", "compare_numbers='focus'"),
        ):
            chart.config = chart.config.evolved(compare_numbers=mode)
            if mode == "focus":
                chart.focus(1)
            else:
                chart.unfocus()
            tip = Text(label, font_size=26, color="#8899AA").to_edge(DOWN)
            self.play(Write(tip))
            self.wait(1.0)
            self.play(FadeOut(tip))

        self.play(chart.disappear())
