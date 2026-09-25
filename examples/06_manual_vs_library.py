# -*- coding: utf-8 -*-
"""06 · 手写 Manim vs 用 manim-radar —— 同一张雷达图，两种写法。

这个文件里有两套实现：

* ``manual_radar(...)`` + ``ManualRadar`` —— **不用插件**，网格/多边形/标签/数字/
  缓动全自己算，这是手写一张"会变形的雷达图"要付的代价。
* ``LibraryRadar`` —— 用 manim-radar，同样的外观、同样的变形，十几行。
* ``Compare`` —— 把两者的成片并排放在一起（宣传视频用）。

    manim -qh examples/06_manual_vs_library.py ManualRadar     # 手写版
    manim -qh examples/06_manual_vs_library.py LibraryRadar    # 库版
    manim -qh examples/06_manual_vs_library.py Compare         # 并排对比
"""

import math

import numpy as np
from manim import *  # noqa: F401,F403

from manim_radar import RadarChart, set_scene_background

AXES = ["速度", "力量", "续航", "舒适", "价格", "安全"]
START = [8, 6, 7, 9, 5, 8]
TARGET = [5, 9, 5, 6, 9, 9]


# ===========================================================================
# ① 手写版：以下全部要自己写（坐标、网格、多边形、辉光、标签、数字、缓动）
# ===========================================================================
def sign(a):  # noqa: D103 - 下面全部是"手写雷达图"的必要劳动
    return np.array([math.cos(math.radians(a)), math.sin(math.radians(a)), 0.0])


def ease_in_out_cubic(t):  # Manim 没有这个缓动，得自己补
    return 4 * t * t * t if t < 0.5 else 1 - (-2 * t + 2) ** 3 / 2


def manual_radar(values, *, angles=None, radius=2.4, center=(0.0, -0.1),
                 levels=5, scale=10.0, color="#29BDBF",
                 name_size=26, number_size=28, number_gap=0.18):
    """手写雷达图：返回 (整组元素, 每个轴的数值 tracker)。

    每一层都得自己搭：网格环、辐条、填充、辉光、描边、轴名、数字。

    注意：这些 ``always_redraw`` 每帧按**绝对坐标**重算，所以手写版一旦
    ``move_to`` / ``scale`` 就会被覆盖 —— 只能靠传 ``center`` / ``radius``
    在建图时定死位置。
    """
    angles = angles or [90, 30, -30, -90, -150, 150]
    c = np.array([center[0], center[1], 0.0])
    trackers = [ValueTracker(float(v)) for v in values]
    state = {"now": ManimColor(color), "to": ManimColor(color), "t": ValueTracker(0.0)}

    def col():
        return interpolate_color(state["now"], state["to"], state["t"].get_value())

    def pts():
        return [c + sign(angles[i]) * (radius * trackers[i].get_value() / scale)
                for i in range(len(angles))]

    web = VGroup()
    for lvl in range(1, levels + 1):
        ring = [c + sign(a) * (radius * lvl / levels) for a in angles]
        web.add(Polygon(*ring, stroke_color="#8B9BB8",
                        stroke_width=1.6 if lvl == levels else 1.4,
                        stroke_opacity=0.75 if lvl == levels else 0.42))
    for a in angles:
        web.add(Line(c, c + sign(a) * radius, stroke_color="#8B9BB8",
                     stroke_width=1.4, stroke_opacity=0.42))

    fill = always_redraw(lambda: Polygon(*pts(), stroke_width=0,
                                         fill_color=col(), fill_opacity=0.38))
    glow = always_redraw(lambda: Polygon(
        *pts(), fill_opacity=0, stroke_width=18,
        stroke_color=interpolate_color(col(), WHITE, 0.45), stroke_opacity=0.30))
    line = always_redraw(lambda: Polygon(
        *pts(), fill_opacity=0, stroke_width=5,
        stroke_color=interpolate_color(col(), WHITE, 0.55)))

    labels = VGroup()
    numbers = VGroup()
    for i, a in enumerate(angles):
        u = sign(a)
        name = Text(AXES[i], font="PingFang SC", weight=BOLD, font_size=name_size,
                    color=WHITE)
        name.move_to(c + u * (radius * 1.02))
        num = always_redraw(lambda i=i: Text(
            str(int(round(trackers[i].get_value()))), font="Menlo", weight=BOLD,
            font_size=number_size, color=WHITE,
        ).move_to(c + sign(angles[i]) * (radius * 1.02)
                  + RIGHT * (name.width / 2 + number_gap), aligned_edge=LEFT))
        labels.add(name)
        numbers.add(num)

    group = VGroup(web, fill, glow, line, labels, numbers)
    return group, trackers, state


class ManualRadar(Scene):
    """手写版：入场 → 先沉后滚的变形 → 出场。"""

    def construct(self):
        group, tr, state = manual_radar(START)
        self.play(FadeIn(group), run_time=0.8)
        self.wait(0.3)

        state["now"], state["to"] = ManimColor("#29BDBF"), ManimColor("#E8944A")
        dip = [max(2.0, v - 1.0) for v in TARGET]
        self.play(state["t"].animate.set_value(1.0),
                  *[tr[i].animate.set_value(dip[i]) for i in range(6)],
                  run_time=0.25)
        self.play(*[tr[i].animate.set_value(TARGET[i]) for i in range(6)],
                  run_time=1.05, rate_func=ease_in_out_cubic)
        self.wait(0.5)
        self.play(FadeOut(group), run_time=0.8)


# ===========================================================================
# ② 库版：同样的外观、同样的变形 —— 这就是全部代码
# ===========================================================================
class LibraryRadar(Scene):
    def construct(self):
        set_scene_background("midnight")
        chart = RadarChart(axes=AXES, values=START, style="classic")
        self.play(chart.reveal(run_time=0.8))
        self.wait(0.3)
        self.play(chart.morph_to(TARGET, color="#E8944A"), run_time=1.3)
        self.wait(0.5)
        self.play(chart.disappear(run_time=0.8))


# ===========================================================================
# ③ 并排对比（宣传视频用）
# ===========================================================================
class Compare(Scene):
    def construct(self):
        set_scene_background("midnight")

        # 左：手写（只能靠 center/radius 在建图时定位置）
        manual, tr, state = manual_radar(START, radius=2.1, center=(-3.7, -0.1))
        # 右：库版（就是个普通 mobject，位置随便摆）
        chart = RadarChart(axes=AXES, values=START, style="classic", radius=2.1,
                           position=(0.0, 0.0))
        chart.move_to(RIGHT * 3.7 + DOWN * 0.1)

        cap_l = Text("手写 Manim · 70 行", font="PingFang SC", weight=BOLD,
                     font_size=30, color="#FF6B6B")
        cap_r = Text("manim-radar · 9 行", font="PingFang SC", weight=BOLD,
                     font_size=30, color="#4DD0E1")
        cap_l.move_to(LEFT * 3.7 + DOWN * 3.3)
        cap_r.move_to(RIGHT * 3.7 + DOWN * 3.3)

        self.play(FadeIn(manual), chart.reveal(run_time=0.8), run_time=0.8)
        self.play(Write(cap_l), Write(cap_r), run_time=0.5)
        self.wait(0.4)

        # 两边同时变形：左边手动推 tracker，右边一句 morph_to
        state["now"], state["to"] = ManimColor("#29BDBF"), ManimColor("#E8944A")
        dip = [max(2.0, v - 1.0) for v in TARGET]
        self.play(state["t"].animate.set_value(1.0),
                  *[tr[i].animate.set_value(dip[i]) for i in range(6)],
                  chart.morph_to(TARGET, color="#E8944A"),
                  run_time=0.25)
        self.play(*[tr[i].animate.set_value(TARGET[i]) for i in range(6)],
                  run_time=1.05, rate_func=ease_in_out_cubic)
        self.wait(1.2)
