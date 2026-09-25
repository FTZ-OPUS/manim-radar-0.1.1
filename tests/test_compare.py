# -*- coding: utf-8 -*-
"""0.1.1 feature tests — comparison mode, legend, focus, gap highlight,
overflow chart, camera helpers. No rendering, so they run fast."""

from __future__ import annotations

import math
from types import SimpleNamespace

import numpy as np
import pytest
from manim import Rectangle

from manim_radar import (
    CameraRig,
    OverflowRadarChart,
    RadarChart,
    RadarConfig,
    RadarData,
    RadarReel,
    ease_out_overshoot,
)

AXES = ["A", "B", "C", "D", "E", "F"]
VALUES = [8, 6, 7, 9, 5, 8]


def d(values, name=None, color=None, **kw) -> RadarData:
    return RadarData(axes=AXES, values=values, name=name, color=color, **kw)


# ---------------------------------------------------------------------------
# comparison construction
# ---------------------------------------------------------------------------
def test_compare_chart_builds_and_shares_scale():
    chart = RadarChart(datasets=[d([8, 6, 7, 9, 5, 8], "A"), d([5, 9, 4, 6, 9, 9], "B")])
    assert len(chart._series) == 2
    assert chart.full_scale == 10  # shared scale = max of both snapshots
    assert len(chart._legend_content) >= 1  # legend built


def test_compare_rejects_mixed_axis_layouts():
    with pytest.raises(ValueError):
        RadarChart(datasets=[d([1, 2, 3, 4, 5, 6]), RadarData(axes=["X", "Y", "Z"], values=[1, 2, 3])])


def test_compare_imperative_and_back_to_single():
    chart = RadarChart(axes=AXES, values=VALUES, name="solo")
    chart.compare(d([5, 5, 5, 5, 5, 5], "x"), d([7, 7, 7, 7, 7, 7], "y"))
    assert len(chart._series) == 2 and chart._legend_content is not None
    chart.compare(d([2, 2, 2, 2, 2, 2], "solo again"))
    assert len(chart._series) == 1
    assert chart._legend_content is None
    assert chart._name_text is not None  # nameplate rebuilt


def test_morph_to_list_tweens_every_series_and_stagger():
    chart = RadarChart(datasets=[d(VALUES, "A"), d([1, 2, 3, 4, 5, 6], "B")])
    anim = chart.morph_to([d([2] * 6, "A2"), d([9] * 6, "B2")], stagger=0.2)
    anim.begin()
    for a in (0.2, 0.5, 0.8):
        anim.interpolate_mobject(a)
        # stagger: dataset 1 must lag dataset 0
        assert chart._series[1].values[0] <= chart._series[0].values[0] + 1e-9 or \
            chart._series[0].values[0] >= 2.0 - 1e-9
    anim.interpolate_mobject(1.0)
    anim.finish()
    assert chart._series[0].values == [2.0] * 6
    assert chart._series[1].values == [9.0] * 6
    assert chart.datasets[1].name == "B2"


def test_morph_grows_and_shrinks_the_dataset_count():
    chart = RadarChart(axes=AXES, values=VALUES)
    anim = chart.morph_to([d([1] * 6), d([2] * 6), d([3] * 6)])
    anim.begin()
    anim.interpolate_mobject(0.5)
    assert len(chart._series) == 3
    anim.interpolate_mobject(1.0)
    anim.finish()
    assert len(chart._series) == 3

    anim2 = chart.morph_to(d([4] * 6))
    anim2.begin()
    anim2.interpolate_mobject(1.0)
    anim2.finish()
    assert len(chart._series) == 1
    assert chart.values == [4.0] * 6


def test_single_dataset_morph_still_sets_data_and_colour():
    chart = RadarChart(axes=AXES, values=VALUES)
    target = d([2] * 6, color="#FF0000")
    anim = chart.morph_to(target, transition="smooth")
    anim.begin()
    anim.interpolate_mobject(1.0)
    anim.finish()
    assert chart.data is target
    assert chart.current_color.to_hex().upper().startswith("#FF")


# ---------------------------------------------------------------------------
# focus & number modes
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("mode", ["legend", "all", "first", "focus"])
def test_compare_number_modes(mode):
    chart = RadarChart(
        datasets=[d(VALUES, "A"), d([1] * 6, "B")], compare_numbers=mode
    )
    chart._refresh(chart, 0.0)
    visible = sum(
        1
        for s in chart._series
        if s.numbers is not None
        for t in s.numbers
        for g in t._cache.values()
        if g.get_fill_opacity() > 0.01
    )
    if mode == "all":
        assert visible == 2 * len(VALUES)
    elif mode == "first":
        assert visible == len(VALUES)
    elif mode == "focus":
        assert visible == 0  # nothing focused yet
    else:
        assert visible == 0 and chart._series[0].numbers is None


def test_compare_numbers_validation():
    with pytest.raises(ValueError):
        RadarChart(axes=AXES, values=VALUES, compare_numbers="banana")


def test_focus_dims_the_other_dataset():
    chart = RadarChart(datasets=[d(VALUES), d([1] * 6)])
    chart.focus(1)
    assert chart._series[1].opacity_target == 1.0
    assert chart._series[0].opacity_target == chart.config.focus_dim
    chart._refresh(chart, 0.2)  # a few frames of easing
    chart._refresh(chart, 0.2)
    assert chart._series[1].opacity > chart._series[0].opacity
    chart.unfocus()
    assert all(s.opacity_target == 1.0 for s in chart._series)


def test_focus_mode_numbers_follow_focus():
    chart = RadarChart(
        datasets=[d(VALUES), d([1] * 6)], compare_numbers="focus"
    )
    chart.focus(1)
    chart._refresh(chart, 0.0)
    visible = [
        g
        for s in chart._series
        if s.numbers is not None
        for t in s.numbers
        for g in t._cache.values()
        if g.get_fill_opacity() > 0.01
    ]
    assert len(visible) == len(VALUES)


# ---------------------------------------------------------------------------
# gap highlight
# ---------------------------------------------------------------------------
def test_highlight_gap_builds_lobes_and_clears():
    chart = RadarChart(datasets=[d(VALUES), d([1] * 6)])
    chart.highlight_gap(0, 1)
    assert chart.gap_group is not None
    assert len(chart.gap_group) == 2 * chart.axis_count
    assert any(p.get_fill_opacity() > 0 for p in chart.gap_group)
    chart.clear_gap()
    chart._refresh(chart, 0.0)
    assert all(p.get_fill_opacity() == 0 for p in chart.gap_group)


def test_highlight_gap_needs_two_datasets():
    chart = RadarChart(axes=AXES, values=VALUES)
    with pytest.raises(ValueError):
        chart.highlight_gap()


def test_highlight_gap_side_filter():
    chart = RadarChart(datasets=[d(VALUES), d([1] * 6)])
    chart.highlight_gap(0, 1, side="a")
    # dataset 0 wins everywhere here, so side="a" keeps every lobe visible
    assert any(p.get_fill_opacity() > 0 for p in chart.gap_group)
    chart.highlight_gap(0, 1, side="b")
    chart._refresh(chart, 0.0)
    assert all(p.get_fill_opacity() == 0 for p in chart.gap_group)


# ---------------------------------------------------------------------------
# overflow chart
# ---------------------------------------------------------------------------
def test_overflow_chart_builds_with_tracks():
    chart = OverflowRadarChart(axes=AXES, values=[8, 6, 14, 9, 5, 8], max_value=10)
    assert chart.config.overflow is True
    chart._refresh(chart, 0.0)
    s0 = chart._series[0]
    # axis 2 overflows: its track shows dashes and a breach glow exists
    assert s0.dash_pool[2] is not None
    assert any(line.get_stroke_opacity() > 0 for line in s0.dash_pool[2])
    assert s0.breach[2] is not None
    assert s0.breach[2][0].get_fill_opacity() > 0
    # the quiet axes show nothing special
    assert s0.dash_pool == [] or s0.dash_pool[0] is None
    assert s0.breach == [] or s0.breach[0] is None


def test_overflow_every_dataset_gets_spikes_tracks_and_breaches():
    chart = OverflowRadarChart(
        datasets=[
            RadarData(axes=AXES, values=[12, 6, 7, 9, 5, 8], max_value=10, color="#17B8BA"),
            RadarData(axes=AXES, values=[8, 6, 7, 9, 13, 8], max_value=10, color="#E868C8"),
        ],
    )
    assert len(chart._series) == 2
    chart._refresh(chart, 0.0)
    sA, sB = chart._series
    # dataset 0 spikes on axis 0, dataset 1 on axis 4 — each with its own fx
    assert any(line.get_stroke_opacity() > 0 for line in sA.dash_pool[0])
    assert any(line.get_stroke_opacity() > 0 for line in sB.dash_pool[4])
    assert sA.breach[0][2].get_fill_opacity() > 0
    assert sB.breach[4][2].get_fill_opacity() > 0
    assert sB.breach[0] is None  # dataset 1 does not overflow axis 0
    # two unclamped read-outs, one per dataset
    big_a = chart._ensure_overflow_number(0, 0)
    big_b = chart._ensure_overflow_number(1, 4)
    assert big_a.label_for(12) == "12" and big_b.label_for(13) == "13"
    assert big_a is not big_b


def test_overflow_numbers_are_unclamped():
    chart = OverflowRadarChart(axes=AXES, values=[8, 6, 14, 9, 5, 8], max_value=10)
    num = chart._ensure_overflow_number(0, 2)
    assert num.label_for(14) == "14"
    assert num.label_for(17) == "17"


def test_overflow_burst_morph_overshoots():
    chart = OverflowRadarChart(axes=AXES, values=[8, 6, 14, 9, 5, 8], max_value=10)
    anim = chart.morph_to([7, 9, 17, 6, 8, 5])
    assert anim.burst is True
    anim.begin()
    peak = None
    for a in np.linspace(0.0, 1.0, 60):
        anim.interpolate_mobject(float(a))
        v = chart._series[0].values[2]
        peak = v if peak is None else max(peak, v)
    anim.finish()
    assert chart._series[0].values == [7.0, 9.0, 17.0, 6.0, 8.0, 5.0]
    assert peak > 17.0 + 0.5  # stabbed past the target before settling


def test_burst_in_restores_values():
    chart = OverflowRadarChart(axes=AXES, values=[8, 6, 14, 9, 5, 8], max_value=10)
    anim = chart.burst_in(run_time=1.0)
    anim.begin()
    anim.interpolate_mobject(0.5)
    anim.interpolate_mobject(1.0)
    anim.finish()
    assert chart._series[0].values == [8.0, 6.0, 14.0, 9.0, 5.0, 8.0]


def test_plain_chart_can_also_burst():
    chart = RadarChart(axes=AXES, values=VALUES)
    anim = chart.morph_to(d([9] * 6), transition="burst")
    assert anim.burst is True
    anim.begin()
    anim.interpolate_mobject(1.0)
    anim.finish()
    assert chart.values == [9.0] * 6


# ---------------------------------------------------------------------------
# camera helpers
# ---------------------------------------------------------------------------
def test_camera_rig_needs_a_moving_camera_scene():
    with pytest.raises(TypeError):
        CameraRig(SimpleNamespace(camera=None))


def test_camera_rig_animations():
    frame = Rectangle(width=14.2, height=8.0)
    rig = CameraRig(SimpleNamespace(camera=SimpleNamespace(frame=frame)))
    anim = rig.push_in(target=np.zeros(3), factor=1.4)
    assert anim is not None
    back = rig.pull_out()
    assert back is not None
    micro = rig.micro_push([1.0, 0.0, 0.0])
    assert micro is not None
    point = rig.focus_point([1.0, 2.0, 0.0])
    assert point is not None


def test_chart_push_in_returns_animation_builder():
    chart = RadarChart(axes=AXES, values=VALUES)
    assert chart.push_in(factor=1.3) is not None
    assert chart.pull_out(factor=1.3) is not None
    chart.attach_camera(None)
    assert chart._rig is None


# ---------------------------------------------------------------------------
# reel with comparison snapshots
# ---------------------------------------------------------------------------
def test_reel_accepts_comparison_snapshots():
    chart = RadarChart(datasets=[d(VALUES, "A"), d([1] * 6, "B")])
    reel = RadarReel(
        chart,
        [[d([5] * 6, "A"), d([9] * 6, "B")], [d([7] * 6, "A"), d([2] * 6, "B")]],
        hold=0.4,
    )
    assert len(reel.steps) == 2
    # position-based colours: dataset 0 keeps its colour across steps
    assert reel.steps[0][0].color == reel.steps[1][0].color
    assert reel.steps[0][1].color == reel.steps[1][1].color
    assert reel.steps[0][0].color != reel.steps[0][1].color
    assert " vs " in reel.summary()
    assert reel.total_time > 0


def test_reel_single_snapshots_keep_legacy_colour_cycling():
    chart = RadarChart(axes=AXES, values=VALUES)
    snapshots = [d([i + 1] * 6, name=f"n{i}") for i in range(4)]
    reel = RadarReel(chart, snapshots, hold=0.5)
    assert all(dd.color for dd in reel.datasets)
    assert len({dd.color for dd in reel.datasets}) == 4


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def test_ease_out_overshoot_peak_matches_fraction():
    for f in (0.08, 0.16, 0.25):
        peak = max(ease_out_overshoot(t / 400.0, f) for t in range(401))
        assert peak == pytest.approx(1.0 + f, rel=0.02)


def test_legend_chips_follow_dataset_colours():
    from manim import ManimColor

    chart = RadarChart(
        datasets=[d(VALUES, "红方", color="#FF0000"), d([1] * 6, "蓝方", color="#0000FF")]
    )
    chips = chart._legend_content._chips
    assert len(chips) == 2
    # Manim round-trips colours through linear space, so compare channels
    red = ManimColor(chips[0][0].get_stroke_color())
    blue = ManimColor(chips[1][0].get_stroke_color())
    assert red[0] > 0.9 and red[1] < 0.25  # red-dominant
    assert blue[2] > 0.9 and blue[0] < 0.25  # blue-dominant
