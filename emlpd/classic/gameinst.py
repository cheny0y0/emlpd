# emlpd
# Copyright (C) 2024-2025  REGE
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from typing import ClassVar
from .gameapi import I18nText, Game

__all__ = ["CLASSIC_MODE", "Texts"]

CLASSIC_MODE: Game = Game(
    2,
    8,
    1,
    1,
    7,
    1,
    10,
    {
        2: ("小刀", "非常不讲武德的提升一点伤害（无上限）"),
        3: ("开挂", "将当前弹壳里的一发子弹退出"),
        4: ("超级小木锤", "将对方敲晕一回合"),
        5: ("道德的崇高赞许", "回一滴血"),
        6: ("透视镜", "查看当前子弹")
    },
    {
        2: 1,
        3: 1,
        4: 1,
        5: 1,
        6: 1
    },
    {
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0
    },
    {
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0
    },
    8,
    True
)

class Texts :
    GAME_TITLE: ClassVar[I18nText] = I18nText(
        "恶魔轮盘赌（重构版）",
        en_en="Evil's Mutual Linear Probability Detection"
    )
    PROBLEM_SAVING: ClassVar[I18nText] = \
    I18nText("存档时遇到问题!", en_en="Problem saving!")
    R_CUR_PP: ClassVar[I18nText] = \
    I18nText("当前你的表现分: {0}", en_en="Your current PP: {0}")
    E_CUR_PP: ClassVar[I18nText] = \
    I18nText("当前恶魔表现分: {0}", en_en="The Evil's current PP: {0}")
    GAME_COUNT_INFO: ClassVar[I18nText] = I18nText(
        "本次游戏持续了 {0} 轮,\n{1} 回合",
        en_en="This game kept {0} turn(s),\n{1} round(s)"
    )
    PP: ClassVar[I18nText] = \
    I18nText("表现分: {0} - {1}", en_en="Performance Point: {0} - {1}")
    GAIN_EXP: ClassVar[I18nText] = \
    I18nText("你获得了 {0} 经验", en_en="You've gained {0} EXP")
