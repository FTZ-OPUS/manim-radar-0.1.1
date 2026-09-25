# -*- coding: utf-8 -*-
"""09 · Camera — push-in / pull-out shots wrapped for radar charts.

Part 1 works in a plain ``Scene``: ``chart.push_in()`` scales the chart
about its own centre. Part 2 uses a true camera via ``CameraRig`` in a
``MovingCameraScene`` — the whole frame (starfield included) breathes.

    manim -qh examples/09_camera.py PlainScenePush
    manim -qh examples/09_camera.py TrueCameraPush
"""

from manim import *

from manim_radar import CameraRig, DeepSpace, RadarChart, RadarData, set_scene_background

AXES = ["速度", "力量", "续航", "舒适", "价格", "安全"]
SNAP = RadarData(axes=AXES, values=[8, 6, 7, 9, 5, 8], name="标准型", color="#17B8BA")
SNAP2 = RadarData(axes=AXES, values=[5, 9, 5, 6, 9, 9], name="重装型", color="#E868C8")


class PlainScenePush(Scene):
    """普通 Scene：镜头语言靠缩放图表本体实现。"""

    def construct(self):
        set_scene_background("midnight")
        chart = RadarChart(SNAP, radius=2.4)
        self.add(DeepSpace().link(chart))
        self.play(chart.reveal())

        # 推近（图表放大），顺势变形
        self.play(chart.push_in(factor=1.35, run_time=0.8))
        self.play(chart.morph_to(SNAP2))

        # 拉远还原
        self.play(chart.pull_out(factor=1.35, run_time=0.8))
        self.wait(0.4)
        self.play(chart.disappear())


class TrueCameraPush(MovingCameraScene):
    """MovingCameraScene：真相机推拉，星空背景一起呼吸。"""

    def construct(self):
        set_scene_background("midnight")
        chart = RadarChart(SNAP, title="镜头语言")
        rig = CameraRig(self)
        self.add(DeepSpace().link(chart))
        self.play(chart.reveal())

        self.play(rig.push_in(chart, factor=1.4, run_time=0.9))
        self.play(chart.morph_to(SNAP2))
        self.wait(0.4)

        # 平移到某个顶点特写
        peak = chart._anchor[0].get_center() + UP * 2.2
        self.play(rig.focus_point(peak, factor=1.6, run_time=0.9))
        self.wait(0.4)

        self.play(rig.pull_out(run_time=1.0))
        self.play(chart.disappear())
