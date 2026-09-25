# -*- coding: utf-8 -*-
"""08 · Overflow (越界雷达图) — values that break through the outer ring.

Any value above the full scale escapes as a filled spike: dashed track,
glowing breach where it pierces the ring, and an unclamped read-out riding
the spike. Morphs default to the "burst" transition.

    manim -qh examples/08_overflow.py Overflow
"""

from manim import *

from manim_radar import (
    CameraRig,
    DeepSpace,
    OverflowRadarChart,
    RadarData,
    set_scene_background,
)

AXES = ["速度", "力量", "爆发", "续航", "技巧", "防御"]


class Overflow(Scene):
    def construct(self):
        set_scene_background("midnight")

        # 爆发 14 远远越过 10 的外圈
        chart = OverflowRadarChart(
            axes=AXES,
            values=[8, 6, 14, 9, 5, 8],
            max_value=10,
            name="狂战士",
            color="#F040E0",
        )
        self.add(DeepSpace().link(chart))

        # 入场：数值从中心猛地刺出去，越过目标再回落
        self.play(chart.burst_in())
        self.wait(0.8)

        # 换人：burst 转场（先沉到目标 20%，再一举刺穿外圈）
        berserk2 = RadarData(axes=AXES, values=[7, 9, 17, 6, 8, 5],
                             name="暴走形态", color="#FF7043", max_value=10)
        self.play(chart.morph_to(berserk2))
        self.wait(0.8)

        # 也可以显式选别的转场
        knight = RadarData(axes=AXES, values=[9, 8, 10, 12, 7, 11],
                           name="圣骑士", color="#4DD0E1", max_value=10)
        self.play(chart.morph_to(knight, transition="smooth"))
        self.wait(0.8)

        self.play(chart.disappear())


class OverflowWithCamera(MovingCameraScene):
    """越界 + 真相机：attach_camera 后 burst 会自动向尖峰方向微推镜头。"""

    def construct(self):
        set_scene_background("midnight")

        chart = OverflowRadarChart(
            axes=AXES,
            values=[6, 5, 8, 7, 6, 5],
            max_value=10,
            name="蓄力",
            color="#17B8B7",
        )
        rig = CameraRig(self)          # MovingCameraScene 的真相机
        chart.attach_camera(rig)       # 挂上之后 burst 自动微推
        self.add(DeepSpace().link(chart))

        self.play(chart.reveal())
        self.wait(0.4)

        # 爆发瞬间：镜头自动朝尖峰轻推一下
        burst = RadarData(axes=AXES, values=[7, 6, 16, 8, 7, 6],
                          name="爆发!", color="#FFD166", max_value=10)
        self.play(chart.morph_to(burst, run_time=1.6))
        self.wait(0.6)

        self.play(rig.pull_out())
        self.play(chart.disappear())
