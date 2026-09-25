# -*- coding: utf-8 -*-
"""10 · Showcase — the 0.1.1 promo reel: two overflow + multi-dataset radar
charts, a glitch/shockwave switch between them, and full camera language.

Everything on screen is the library doing the work: comparison legend,
focus dimming, crescent gap highlight, burst morphs with breach glows,
unclamped spike read-outs, camera push/focus/pull and the auto micro-push
that rides every burst.

    manim -qh examples/10_showcase.py Showcase
"""

import math

import numpy as np
from manim import *

from manim_radar import (
    CameraRig,
    DeepSpace,
    OverflowRadarChart,
    RadarData,
    Shockwave,
    set_scene_background,
)

TEAL, PINK = "#17B8BA", "#E868C8"
GOLD, EMBER = "#FFD166", "#FF7043"

AXES_MATH = ["公理性", "统一性", "推广性", "初等性", "应用广度", "边界情形"]
AXES_GAME = ["爆发", "速度", "技巧", "防御", "续航", "力量"]


def spike_tip(chart, axis: int, value: float) -> np.ndarray:
    """World position where ``value`` lands on ``axis`` (for camera moves)."""
    a = chart._anchor[0].get_center()
    u = chart._anchor[1].get_center() - a
    unit = float(np.linalg.norm(u)) or 1.0
    un = u / unit
    vn = np.array([-u[1], u[0], 0.0]) / unit
    ang = math.radians(chart._angles[axis])
    direction = np.cos(ang) * un + np.sin(ang) * vn
    R = chart.config.radius * unit
    return a + direction * R * (value / chart.full_scale)


class Showcase(MovingCameraScene):
    def construct(self):
        set_scene_background("midnight")
        rig = CameraRig(self)

        # ============ 序幕：标题卡 ============
        brand = Text("manim-radar", font_size=76, weight="BOLD")
        brand.set_color_by_gradient(TEAL, PINK)
        tag = Text("越界 · 对比 · 镜头语言", font_size=30, color="#8899AA")
        tag.next_to(brand, DOWN, buff=0.35)
        space = DeepSpace()
        self.add(space)
        self.play(FadeIn(brand, shift=UP * 0.3), FadeIn(tag, shift=UP * 0.2), run_time=0.9)
        self.play(rig.frame.animate.scale(0.96), run_time=1.4)
        self.play(FadeOut(brand), FadeOut(tag), run_time=0.5)

        # ============ 第一幕：多组越界雷达（对比） ============
        holder = RadarData(axes=AXES_MATH, values=[8, 9, 15, 4, 9, 7],
                           name="赫尔德不等式", color=TEAL, max_value=10)
        basic = RadarData(axes=AXES_MATH, values=[10, 6, 5, 12, 7, 9],
                          name="基本不等式", color=PINK, max_value=10)
        chart1 = OverflowRadarChart(datasets=[holder, basic], position=(0.0, 0.30))
        space.link(chart1)                                 # 星云颜色跟随图表主色

        self.play(chart1.burst_in(run_time=1.2))           # 双双刺出外圈
        self.wait(0.7)

        chart1.focus(0)                                    # 聚焦赫尔德
        self.wait(0.9)
        chart1.unfocus()
        chart1.highlight_gap(0, 1, opacity=0.5)            # 月牙差值染色
        self.wait(1.1)
        chart1.clear_gap()

        holder2 = RadarData(axes=AXES_MATH, values=[9, 8, 17, 5, 10, 8],
                            name="赫尔德 · 推广形态", color=TEAL, max_value=10)
        basic2 = RadarData(axes=AXES_MATH, values=[9, 7, 6, 13, 8, 8],
                           name="基本 · 强化形态", color=PINK, max_value=10)
        # burst 大转场：先沉再刺穿，镜头自动朝尖峰微推
        self.play(chart1.morph_to([holder2, basic2], stagger=0.15, run_time=1.6))
        self.wait(0.5)

        # ============ 切换：推近尖峰 → 白闪 + 冲击波 → 故障闪入第二张 ============
        self.play(rig.focus_point(spike_tip(chart1, 2, 17), factor=1.45, run_time=0.8))
        flash = Rectangle(width=config.frame_width * 2.4, height=config.frame_height * 2.4,
                          fill_color=WHITE, fill_opacity=0, stroke_width=0)
        self.add(flash)
        self.play(flash.animate.set_opacity(0.45), run_time=0.12)
        self.play(
            chart1.disappear(run_time=0.5),
            Shockwave(center=chart1._anchor[0].get_center(), color=TEAL, radius_end=8.0),
            flash.animate.set_opacity(0.0), run_time=0.55,
        )
        self.remove(flash, chart1)

        gold = RadarData(axes=AXES_GAME, values=[8, 9, 7, 6, 8, 12],
                         name="烈焰", color=GOLD, max_value=10)
        ember = RadarData(axes=AXES_GAME, values=[9, 12, 8, 7, 6, 8],
                          name="疾风", color=EMBER, max_value=10)
        chart2 = OverflowRadarChart(datasets=[gold, ember], compare_numbers="all")
        space.link(chart2)
        self.play(chart2.glitch_in(run_time=0.8))          # 故障闪入，直接带尖峰
        self.play(rig.pull_out(run_time=0.7))              # 相机回到全景
        self.wait(0.4)

        # ============ 第二幕：另一组多组越界（顶点彩色数值模式） ============
        self.play(rig.push_in(chart2, factor=1.08, run_time=0.7))
        chart2.focus(1)                                    # 聚焦疾风
        self.wait(0.8)
        chart2.unfocus()
        self.wait(0.3)

        # ============ 终章：双 20 刺穿双倍圈，镜头跟随 ============
        gold_f = RadarData(axes=AXES_GAME, values=[20, 9, 8, 7, 10, 9],
                           name="烈焰 · 觉醒", color=GOLD, max_value=10)
        ember_f = RadarData(axes=AXES_GAME, values=[10, 13, 9, 8, 7, 17],
                            name="疾风 · 极限", color=EMBER, max_value=10)
        self.play(
            chart2.morph_to([gold_f, ember_f], stagger=0.15, run_time=1.8),
            rig.focus_point(spike_tip(chart2, 0, 20), factor=1.4, run_time=1.8),
        )
        self.play(Shockwave(center=chart2._anchor[0].get_center(), color=GOLD,
                            radius_end=9.0, run_time=0.6))
        self.wait(0.6)

        # ============ 落版 ============
        self.play(rig.pull_out(run_time=1.0))
        self.play(chart2.disappear(run_time=0.7))
        self.remove(chart2)

        brand2 = Text("manim-radar 0.1.1", font_size=60, weight="BOLD")
        brand2.set_color_by_gradient(TEAL, PINK)
        pip = Text("pip install manim_radar", font="Menlo", font_size=28, color="#EAF2FF")
        gh = Text("github.com/FTZ-OPUS/manim-radar", font_size=22, color="#8899AA")
        card = VGroup(brand2, pip, gh).arrange(DOWN, buff=0.32)
        self.play(FadeIn(card, shift=UP * 0.3), run_time=0.8)
        self.wait(1.6)
        self.play(FadeOut(card), run_time=0.6)
