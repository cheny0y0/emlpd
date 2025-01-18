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

from .gameapi import Game

__all__ = ["CLASSIC_MODE"]

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
