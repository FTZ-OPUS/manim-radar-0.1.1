# -*- coding: utf-8 -*-
"""继业者战争 · 八维战力越界雷达图鉴

12 位继业者，每人一张越界雷达图（8 维度，超 10 即刺出外圈）。
雷达图居左（约占全屏 7/12，无扫光），人物画像居右（大幅竖卡），
卡下配两行古风诗；burst 变形 + 白闪 + 自动镜头微推。

    manim -qh diadochi_radar.py DiadochiShowcase
"""

import math
from pathlib import Path

import numpy as np
from manim import *

from manim_radar import (
    CameraRig,
    DeepSpace,
    OverflowRadarChart,
    RadarConfig,
    RadarData,
    set_scene_background,
)

# ----------------------------------------------------------------------------
# 数据
# ----------------------------------------------------------------------------
AXES = ["统帅", "政治", "野心", "背刺", "骑兵", "气运", "善终", "王业"]
ASSET_DIR = Path(__file__).resolve().parent / "assets" / "portraits"

# (名字, 档案文件名, 一句话人设, 主色, 八维分, 古风诗两行)
PEOPLE = [
    ("安提帕特", "安提帕特", "老狐狸摄政 · 帝国现实的看守人", "#8F86E8",
     [7, 10, 6, 8, 5, 9, 12, 7],
     "白发执舵定风波\n坐看群雄逐鹿忙"),
    ("佩亚迪卡斯", "佩亚迪卡斯", "亚历山大的印玺 · 帝国首任摄政", "#4FC3F7",
     [8, 7, 12, 8, 7, 4, 2, 4],
     "王印在手令群雄\n未渡尼罗葬鳄口"),
    ("克拉特鲁斯", "克拉特鲁斯", "全军最爱的人物 · 第一个倒下的巨人", "#E8944A",
     [10, 5, 7, 3, 10, 3, 2, 2],
     "万军齐呼万岁时\n先折军中最高枝"),
    ("库娜涅", "库娜涅", "上战场的公主 · 阵斩敌国女王", "#E868C8",
     [8, 7, 9, 4, 7, 3, 2, 6],
     "红妆不守深宫月\n阵前亲斩敌酋头"),
    ("欧律狄刻", "欧律狄刻", "十九岁的王后 · 马其顿首位临朝女性", "#F0ABFC",
     [6, 9, 12, 7, 6, 2, 1, 3],
     "十九垂帘执王印\n红颜一恸殒王秋"),
    ("奥林匹亚斯", "奥林匹亚斯", "驯蛇的王母 · 亚历山大背后的雷霆", "#BA68C8",
     [6, 8, 14, 13, 4, 3, 1, 8],
     "豢蛇巫女育天骄\n一怒王冠化火烧"),
    ("欧迈尼斯", "欧迈尼斯", "文书出身的名将 · 一生未尝一败", "#4DD0E1",
     [11, 6, 6, 2, 8, 2, 2, 1],
     "一管文书点万军\n至死不曾输一阵"),
    ("安提柯", "安提柯", "独眼之王 · 塞琉古一生最强的对手", "#F040E0",
     [11, 9, 15, 8, 11, 6, 4, 11],
     "独目犹吞天下志\n八旬一掷帝国梦"),
    ("卡山德", "卡山德", "弑灭王脉 · 亚历山大全家的终结者", "#FF6B6B",
     [6, 9, 11, 14, 5, 6, 7, 5],
     "斩尽王脉起新城\n青史骂名亦称雄"),
    ("托勒密", "托勒密", "盗走亚历山大遗体 · 活到最后的人", "#FFD166",
     [7, 10, 8, 6, 6, 13, 14, 10],
     "盗得帝骸镇海疆\n群雄血尽我登基"),
    ("科西马科斯", "科西马科斯", "色雷斯之主 · 七十八岁战死沙场", "#40C878",
     [8, 7, 11, 9, 8, 8, 3, 6],
     "古稀披甲冲敌阵\n马革裹尸气未降"),
    ("塞琉古", "塞琉古", "继业者中的六边形战士 · 唯独没得善终", "#17B8BA",
     [13, 13, 15, 12, 14, 13, 3, 15],
     "五百战象开万里\n功成断刃夜未央"),
    ("皮洛士", "皮洛士png", "汉尼拔口中的第二 · 每场胜利都是灾难", "#A8C840",
     [12, 5, 13, 6, 10, 5, 3, 6],
     "百战功高皆险胜\n一片飞瓦坠将星"),
    ("阿尔特弥西亚二世", "阿尔特弥西亚二世", "为夫筑起世界奇观 · 海陆双绝的女王", "#80DEEA",
     [9, 8, 7, 4, 3, 9, 10, 11],
     "楼船千帆征罗德\n一冢凌云冠古今"),
    ("阿尔西诺伊二世", "阿尔西诺伊二世", "嫁与兄弟的女神 · 死后被供奉三百年", "#FFB74D",
     [5, 14, 11, 13, 5, 12, 9, 13],
     "兄妹同辇承大统\n身后成神三百年"),
]

# 特殊人物：换更大的转场 + 更久的停留；塞琉古额外开强调描边 + 镜头拉伸
SPECIAL = {
    "安提柯": dict(transition="zoom", hold=1.8),
    "奥林匹亚斯": dict(transition="zoom", hold=1.7),
    "塞琉古": dict(transition="zoom", hold=1.6, rim=True, camera=True),
    "阿尔西诺伊二世": dict(transition="zoom", hold=1.9),
}

# 其余人物轮换库内转场，避免每次同一效果
TRANS_CYCLE = {
    "克拉特鲁斯": "burst",
    "库娜涅": "shockwave",
    "欧律狄刻": "burst",
    "欧迈尼斯": "dip",
    "卡山德": "glitch",
    "佩亚迪卡斯": "burst",
    "阿尔特弥西亚二世": "shockwave",
    "托勒密": "burst",
    "科西马科斯": "shockwave",
    "皮洛士": "burst",
}

GOLD = "#FFD166"
POEM_C = "#F0E6C8"
SUB_C = "#D8A48F"
CHART_POS = (-3.25, 0.05, 0.0)     # 图在左
PIC_POS = (4.60, 1.06, 0.0)        # 人在右：底边 -1.60 不动，向上顶到近框顶
PIC_H = 5.32                       # 3.72(顶) - (-1.60)(底)
PIC_W = 3.35                       # 宽度随比例适当放缩
TAG_POS = DOWN * 3.55


def cropped_path(file: str) -> str:
    """返回随案例一起分发的预处理人物竖图。"""
    return str(ASSET_DIR / f"{file}.png")

def portrait(file: str):
    """人物画像（裁窄竖卡）+ 金框。"""
    img = ImageMobject(cropped_path(file))
    img.height = PIC_H
    frame = RoundedRectangle(
        corner_radius=0.12, width=img.width + 0.16, height=PIC_H + 0.16,
        stroke_color=GOLD, stroke_width=3.0, stroke_opacity=0.95,
    ).move_to(img.get_center())
    return Group(img, frame)


def poem(text: str, font: str):
    """卡下两行古风诗（与人名同款字体加粗）。"""
    lines = [
        Text(t, font=font, font_size=26, color=POEM_C, weight="BOLD")
        for t in text.split("\n")
    ]
    grp = VGroup(*lines).arrange(DOWN, buff=0.22)
    grp.move_to([PIC_POS[0], -2.38, 0.0])
    return grp


def spike_tip(chart, axis: int, value: float) -> np.ndarray:
    """尖峰落点的世界坐标（相机 focus 用）。"""
    a = chart._anchor[0].get_center()
    u = chart._anchor[1].get_center() - a
    unit = float(np.linalg.norm(u)) or 1.0
    un = u / unit
    vn = np.array([-u[1], u[0], 0.0]) / unit
    ang = math.radians(chart._angles[axis])
    direction = np.cos(ang) * un + np.sin(ang) * vn
    R = chart.config.radius * unit
    return a + direction * R * (value / chart.full_scale)


class DiadochiShowcase(MovingCameraScene):
    def construct(self):
        set_scene_background("midnight")
        rig = CameraRig(self)
        space = DeepSpace(theme="midnight")
        self.add(space)

        # ============ 序章 ============
        brand = Text("继业者战争", font_size=68, weight="BOLD")
        brand.set_color_by_gradient(GOLD, "#FF7043")
        sub1 = Text("亚历山大殁 · 帝国裂为猎场", font_size=28, color=SUB_C)
        sub2 = Text("八维战力 · 越界雷达", font_size=22, color="#8899AA")
        card = VGroup(brand, sub1, sub2).arrange(DOWN, buff=0.32)
        self.play(FadeIn(card, shift=UP * 0.3), run_time=0.9)
        self.wait(1.1)
        self.play(FadeOut(card), run_time=0.5)

        # ============ 图表（左）与画像（右） ============
        first = PEOPLE[0]
        chart = OverflowRadarChart(
            axes=AXES,
            values=first[4],
            name=first[0],
            color=first[3],
            config=RadarConfig(colored_axis_names=False, sweep=False,
                              inner_tint=False, fill_opacity=0.62),  # 无扫光，填充加深
            radius=2.35,                      # 网格直径 ≈ 全屏 7/12
            position=CHART_POS,
        )
        space.link(chart)
        chart.attach_camera(rig)              # burst 变形自动向尖峰微推

        tag = Text(first[2], font_size=27, color=GOLD).move_to(TAG_POS)
        pic = portrait(first[1]).move_to(PIC_POS)
        poem_card = poem(first[5], chart._font_name)

        self.play(FadeIn(pic, shift=RIGHT * 0.4), FadeIn(poem_card, shift=UP * 0.2),
                  run_time=0.5)
        self.play(chart.burst_in(run_time=1.3))
        self.play(Write(tag), run_time=0.5)
        self.wait(1.4)

        # ============ 12 人巡回（转场轮换：burst / 冲击波 / zoom / dip / glitch）============
        for name, file, tagline, color, values, verse in PEOPLE[1:]:
            data = RadarData(axes=AXES, values=values, name=name,
                             color=color, max_value=10,
                             rim=SPECIAL.get(name, {}).get("rim", False))
            trans = SPECIAL.get(name, {}).get(
                "transition", TRANS_CYCLE.get(name, "burst"))
            hold = SPECIAL.get(name, {}).get("hold", 1.5)
            new_pic = portrait(file).move_to(PIC_POS)
            new_poem = poem(verse, chart._font_name)
            new_tag = Text(tagline, font_size=27, color=GOLD).move_to(TAG_POS)

            # 大变形（自带冲击波）→ 画像横移换人 → 换人设
            self.play(
                chart.morph_to(data, transition=trans, run_time=1.5),
                FadeOut(pic, shift=LEFT * 0.5),
                FadeIn(new_pic, shift=RIGHT * 0.5),
                FadeOut(poem_card, shift=DOWN * 0.25),
                FadeIn(new_poem, shift=UP * 0.25),
                FadeOut(tag, shift=UP * 0.25),
                run_time=1.5,
            )
            self.play(FadeIn(new_tag, shift=UP * 0.25), run_time=0.35)
            pic, poem_card, tag = new_pic, new_poem, new_tag

            if SPECIAL.get(name, {}).get("camera"):
                # 塞琉古专属：推近野心 15 的尖峰看数值有多高，再拉远看七刺全景
                self.play(rig.focus_point(spike_tip(chart, 2, 15),
                                          factor=1.3, run_time=0.8))
                self.wait(0.3)
                self.play(rig.pull_out(run_time=0.9))
            self.wait(hold)

        # ============ 终章 ============
        self.play(
            FadeOut(pic), FadeOut(poem_card), FadeOut(tag),
            chart.disappear(run_time=0.7),
            run_time=0.8,
        )
        self.remove(chart)

        end1 = Text("帝国裂成五份 · 赌桌再未收场", font_size=34, weight="BOLD")
        end1.set_color_by_gradient(GOLD, "#FF7043")
        end2 = Text("made with manim-radar 0.1.1", font_size=20,
                    color="#8899AA", font="Menlo")
        ending = VGroup(end1, end2).arrange(DOWN, buff=0.4)
        self.play(FadeIn(ending, shift=UP * 0.3), run_time=0.8)
        self.wait(1.6)
        self.play(FadeOut(ending), run_time=0.6)
