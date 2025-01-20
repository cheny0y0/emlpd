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

from fractions import Fraction
from random import randint
from typing import Callable, ClassVar, Dict, Iterable, Iterator, List, \
                   Optional, Tuple, Union
from .gameapi import Game, Slot, ShootResult, Player, I18nText

__all__ = ["GENERIC_TOOLS", "GAMEMODE_SET", "gen_tools_from_generic_tools",
           "StageGame", "NormalGame", "NormalPlayer", "Texts"]

GENERIC_TOOLS: Tuple[Tuple[
    Union[str, I18nText], Optional[Union[str, I18nText]]
], ...] = (
    ("良枪(一)", I18nText(
        "保证向自己开枪不会炸膛(无提示)",
        en_en="Promise not to explode when shooting at yourself (no hint)"
    )), # ID0
    ("良枪(二)", I18nText(
        "保证向对方开枪不会炸膛(无提示)",
        en_en="Promise not to explode when shooting at the opposite (no hint)"
    )), # ID1
    ("小刀", I18nText(
        "非常不讲武德的提升1点伤害(无上限)",
        en_en="Increase 1 attack damage very non-woodly (unlimited)"
    )), # ID2
    ("开挂(一)", I18nText(
        "将当前弹夹里的1发子弹退出",
        en_en="Make 1 bullet quit from the current clip"
    )), # ID3
    ("超级小木锤", I18nText(
        "将对方敲晕1轮",
        en_en="Hit the opponent to dazing for 1 turn"
    )), # ID4
    ("道德的崇高赞许", I18nText("回复1点生命值", en_en="Regain 1 HP")), # ID5
    ("透视镜", I18nText(
        "查看当前子弹", en_en="View the outermost bullets"
    )), # ID6
    ("拿来主义", I18nText(
        "拿来1个道具(无提示)", en_en="Fetch 1 tool (no hint)"
    )), # ID7
    ("你的就是我的", I18nText(
        "将对方道具槽位和自己共用(无提示)",
        en_en="Share the opposite's slots with you (no hint)"
    )), # ID8
    ("防弹衣", I18nText(
        "防住对面射来的子弹", en_en="Defend bullets shot from the opposite"
    )), # ID9
    ("反甲", I18nText(
        "可以反弹对面射来的子弹(无提示)",
        en_en="Rebounce bullet shot from the opposite (no hint)"
    )), # ID10 TODO
    ("骰子", I18nText(
        "可以决定命运......", en_en="This can decide your fate..."
    )), # ID11
    ("槽位延期", I18nText(
        "可以让临时槽位延后过期(无提示)",
        en_en="Let temporary slots expire later (no hint)"
    )), # ID12
    ("镜子", I18nText(
        "镜子内外皆为平等", en_en="Equality in the mirror from in to out"
    )), # ID13
    ("接弹套", I18nText(
        "概率接住对面射来的子弹并重新入膛(无提示)",
        en_en="Get a chance catching bullet shot from the opposite and make it"
              " reenter the clip (no hint)"
    )), # ID14
    ("填实", I18nText(
        "随机把空弹变为实弹", en_en="Randomly turn falses into trues"
    )), # ID15
    ("重整弹药", I18nText(
        "给你重新放入弹药的机会",
        en_en="Give you the oppotunity of arranging the bullets"
    )), # ID16
    ("双发射手", I18nText(
        "向对面开枪一次可射出多发子弹",
        en_en="Shoot multiple bullets to the opposite in once"
    )), # ID17
    ("连发射手", I18nText(
        "向对面开枪一次有概率清空弹夹",
        en_en="Get a chance emptying the clip when shooting at the opposite"
    )), # ID18
    ("硬币", I18nText(
        "可以给你道具......", en_en="This can give you tool..."
    )), # ID19
    ("燃烧弹", "让射出的子弹带着火焰"), # ID20 TODO
    ("破枪", I18nText(
        "让对方开枪时必定炸膛(无提示)",
        en_en="Let the opposite's shot definitely exploded (no hint)"
    )), # ID21
    ("取出子弹", I18nText(
        "取出1发由你指定位置的子弹", en_en="Draw out 1 bullet specified by you"
    )), # ID22
    ("空弹", I18nText(
        "放入1发由你指定位置的空弹",
        en_en="Put 1 false into a place specified by you"
    )), # ID23
    ("实弹", I18nText(
        "放入1发由你指定位置的实弹",
        en_en="Put 1 true into a place specified by you"
    )), # ID24
    ("神秘子弹", I18nText(
        "放入1发由你指定位置的未知子弹",
        en_en="Put 1 unknown bullet into a place specified by you"
    )), # ID25
    ("绷带", I18nText(
        "2回合后让负伤数减1",
        en_en="Let hurting point decrease by 1 after 2 rounds"
    )), # ID26
    ("医疗包", I18nText(
        "可以回复生命值,减少负伤数", en_en="Regain HP and reduce hurting point"
    )), # ID27
    ("开挂(二)", I18nText(
        "立即更换一批新的弹夹", en_en="Instantly change a batch of new clips"
    )), # ID28
    ("双枪会给出答案", I18nText(
        "双倍枪筒,双倍快乐", en_en="Doubled clips doubles joy"
    )), # ID29
    ("所有或一无所有", "一夜暴富?一夜归零?"), # ID30 TODO
    ("超级大木锤", I18nText(
        "整回合都是我的了", en_en="The whole round is mine"
    )), # ID31
    ("不死不休", I18nText("打上擂台", en_en="Battle onto the stage")), # ID32
    ("枪筒维修", I18nText(
        "降低开枪的炸膛概率",
        en_en="Reduce the propability of explosion when shooting"
    )), # ID33
    ("空实分离", I18nText(
        "实弹往前,空弹在后", en_en="Trues go ahead, falses be after"
    )), # ID34
    ("弹夹合并", I18nText(
        "一条龙服务(指子弹)", en_en="ALong service (refers to bullets)"
    )), # ID35
    ("能量饮料", I18nText(
        "有力气开枪才不会不由自主地晕",
        en_en="Only shooting with energies doesn't cause to daze beyond your "
              "control"
    )) # ID36
)

def gen_tools_from_generic_tools(toolids: Iterable[int]) -> \
    Dict[int, Tuple[str, str]] :
    RES: Dict[int, Tuple[str, str]] = {}
    for i in toolids :
        RES[i] = GENERIC_TOOLS[i]
    return RES

class NormalPlayer(Player) :
    hurts: int
    stamina: int
    selfshoot_promises: int
    againstshoot_promises: int
    attack_boost: int
    bulletproof: List[int]
    bullet_catcher_level: int
    multishoot_level: int
    comboshoot_level: int
    cursed_shoot_level: int
    begin_band_level: int
    mid_band_level: int
    breakcare_rounds: int
    breakcare_potential: int

    def __init__(
        self, controllable: bool = False, hp: int = 1,
        slots: Union[List[Slot], int] = 0,
        sending_total: Optional[Dict[int, int]] = None,
        tools_sending_weight: Optional[Dict[
            int, Union[int, Callable[["Game"], int]]
        ]] = None,
        tools_sending_limit_in_game: Optional[Dict[int, int]] = None,
        tools_sending_limit_in_slot: Optional[Dict[
            int, Union[int, Callable[["Game"], int]]
        ]] = None, slot_sending_weight: Optional[Dict[
            int, Union[int, Callable[["Game"], int]]
        ]] = None, stopped_turns: int = 0
    ) -> None :
        super().__init__(
            controllable, hp, slots, sending_total, tools_sending_weight,
            tools_sending_limit_in_game, tools_sending_limit_in_slot,
            slot_sending_weight, stopped_turns
        )
        self.hurts = 0
        self.stamina = 32
        self.selfshoot_promises = 0
        self.againstshoot_promises = 0
        self.attack_boost = 0
        self.bulletproof = []
        self.bullet_catcher_level = 0
        self.multishoot_level = 0
        self.comboshoot_level = 0
        self.cursed_shoot_level = 0
        self.begin_band_level = 0
        self.mid_band_level = 0
        self.breakcare_rounds = 0
        self.breakcare_potential = 0

    def user_operatable(self, game: "Game") -> bool :
        return super().user_operatable(game) and self.breakcare_rounds <= 0

class StageGame(Game) :
    tot_hp: int

    def __init__(self, r_hp: int, e_hp: int, firsthand: bool) :
        super().__init__(
            1,
            1,
            0,
            0,
            1,
            r_hp,
            e_hp,
            {},
            {},
            {},
            {},
            0,
            firsthand,
            {}
        )
        self.players[0] = NormalPlayer(
            True,
            r_hp,
            0,
            None,
            {},
            {},
            {},
            {}
        )
        self.players[1] = NormalPlayer(
            False,
            e_hp,
            0,
            None,
            {},
            {},
            {},
            {}
        )
        self.tot_hp = r_hp + e_hp

    def shoot(self, to_self: bool, shooter: Optional[bool] = None,
              explosion_probability: Union[float,
                                           Callable[["Game"], float]] = 0.05,
              bullets_id: Optional[int] = None, run_turn: bool = True) -> \
        ShootResult :
        if bullets_id is not None and bullets_id not in (1, 2, 3) :
            self.bullets.append(not randint(0, 1))
        return super().shoot(
            to_self, shooter, explosion_probability, bullets_id, run_turn
        )

class NormalGame(Game) :
    explosion_exponent: int

    def __init__(
        self, min_bullets: int, max_bullets: int, min_true_bullets: int,
        min_false_bullets: int, max_true_bullets: int, r_hp: int, e_hp: int,
        tools: Dict[int, Tuple[str, Optional[str]]],
        tools_sending_weight: Dict[int, Union[int, Callable[["Game"], int]]],
        tools_sending_limit_in_game: Dict[int, int],
        tools_sending_limit_in_slot: Dict[int,
                                          Union[int, Callable[["Game"], int]]],
        permanent_slots: int, firsthand: bool,
        slot_sending_weight: Optional[Dict[int, Union[int, Callable[["Game"],
                                                                    int]]]] = \
        None
    ) :
        super().__init__(
            min_bullets, max_bullets, min_true_bullets, min_false_bullets,
            max_true_bullets, r_hp, e_hp, tools, tools_sending_weight,
            tools_sending_limit_in_game, tools_sending_limit_in_slot,
            permanent_slots, firsthand, slot_sending_weight
        )
        self.players[0] = NormalPlayer(
            True,
            r_hp,
            permanent_slots,
            None,
            tools_sending_weight,
            tools_sending_limit_in_game,
            tools_sending_limit_in_slot,
            {1: 5, 2: 6, 3: 6, 4: 2, 5: 1} if slot_sending_weight is None \
            else slot_sending_weight
        )
        self.players[1] = NormalPlayer(
            False,
            e_hp,
            permanent_slots,
            None,
            tools_sending_weight,
            tools_sending_limit_in_game,
            tools_sending_limit_in_slot,
            {1: 5, 2: 6, 3: 6, 4: 2, 5: 1} if slot_sending_weight is None \
            else slot_sending_weight
        )
        self.explosion_exponent = 0

    def shoot(self, to_self: bool, shooter: Optional[bool] = None,
              explosion_probability: Union[float, Callable[["Game"], float]] =\
              lambda game: float(
                  (1-Fraction(1023, 1024)**(200+game.explosion_exponent))**2
              ), bullets_id: Optional[int] = None, run_turn: bool = True) -> \
        ShootResult :
        res: ShootResult = super().shoot(
            to_self, shooter, explosion_probability, bullets_id, run_turn
        )
        if bullets_id is not None and res != (None, None, None, None) :
            self.explosion_exponent += 1
        return res

    def shoots(self, to_self: bool, shooter: Optional[bool] = None,
               explosion_probability: Union[float, Callable[["Game"],float]] =\
               lambda game: float(
                   (1-Fraction(1023, 1024)**(200+game.explosion_exponent))**2
               ), combo: int = 1, bullets_id: Optional[int] = None,
               run_turn: bool = True) -> List[ShootResult] :
        return super().shoots(
            to_self, shooter, explosion_probability, combo, bullets_id,run_turn
        )

    @property
    def debug_message(self) -> Iterable[Tuple[
        Iterable[object], Optional[str], Optional[str]
    ]] :
        res: List[Tuple[Iterable[object], Optional[str], Optional[str]]] = \
        [(("当前弹夹:", self.bullets), None, None)]
        if self.extra_bullets != (None, None, None) :
            res.append((("当前额外弹夹:", self.extra_bullets), None, None))
        r: Player = self.players[0]
        e: Player = self.players[1]
        res.append(((
            "双方晕的轮数:", r.stopped_turns, "-", e.stopped_turns
        ), None, None))
        if isinstance(r, NormalPlayer) and isinstance(e, NormalPlayer) :
            res.append((("双方体力:", r.stamina, "-", e.stamina), None, None))
            if self.has_tools(9) or r.bulletproof or e.bulletproof :
                if e.controllable :
                    res.append((("玩家 0 的防弹衣:", r.bulletproof),None,None))
                    res.append((("玩家 1 的防弹衣:", e.bulletproof),None,None))
                else :
                    res.append((("你的防弹衣:", r.bulletproof), None, None))
                    res.append((("恶魔的防弹衣:", e.bulletproof), None, None))
            if self.has_tools(14) or r.bullet_catcher_level or \
               e.bullet_catcher_level :
                res.append((("双方的叠加接弹套:", r.bullet_catcher_level, "-",
                             e.bullet_catcher_level), None, None))
            if self.has_tools(17) or r.multishoot_level or e.multishoot_level :
                res.append((("双方的叠加双发射手:", r.multishoot_level, "-",
                             e.multishoot_level), None, None))
            if self.has_tools(18) or r.comboshoot_level or e.comboshoot_level :
                res.append((("双方的叠加连发射手:", r.comboshoot_level, "-",
                             e.comboshoot_level), None, None))
            if self.has_tools(0) or r.selfshoot_promises or \
               e.selfshoot_promises :
                res.append((("双方的叠加良枪(一):", r.selfshoot_promises, "-",
                             e.selfshoot_promises), None, None))
            if self.has_tools(1) or r.againstshoot_promises or \
               e.againstshoot_promises :
                res.append((("双方的叠加良枪(二):", r.againstshoot_promises,
                             "-", e.againstshoot_promises), None, None))
            if self.has_tools(21) or r.cursed_shoot_level or \
               e.cursed_shoot_level :
                res.append((("双方的叠加破枪:", r.cursed_shoot_level, "-",
                             e.cursed_shoot_level), None, None))
            if self.has_tools(9) or self.has_tools(11) or \
               r.breakcare_rounds or e.breakcare_rounds or \
               r.breakcare_potential or e.breakcare_potential :
                res.append((("双方的破防回合数:", r.breakcare_rounds, "-",
                             e.breakcare_rounds), None, None))
                res.append((("双方的破防潜能:", r.breakcare_potential, "-",
                             e.breakcare_potential), None, None))
        res.append((("当前炸膛指数:", self.explosion_exponent), None, None))
        return res

    @property
    def round_start_message(self) -> Iterable[Tuple[
        Iterable[object], Optional[str], Optional[str]
    ]] :
        res: List[Tuple[Iterable[object], Optional[str], Optional[str]]] = []
        for i, player in self.players.items() :
            if i == 0 and not self.players[1].controllable :
                res.append((("当前你的生命值为:", player.hp), None, None))
                if isinstance(player, NormalPlayer) :
                    res.append((("当前你的负伤数为:", player.hurts),None,None))
            elif i == 1 and not self.players[1].controllable :
                res.append((("当前恶魔生命值为:", player.hp), None, None))
                if isinstance(player, NormalPlayer) :
                    res.append((("当前恶魔负伤数为:", player.hurts),None,None))
            else :
                res.append((("当前玩家", i, "生命值为:", player.hp),None,None))
                if isinstance(player, NormalPlayer) :
                    res.append((("当前玩家", i, "负伤数为:", player.hurts),
                                None, None))
        return res

normal_mode: NormalGame = NormalGame(
    2,
    8,
    1,
    1,
    8,
    1,
    10,
    gen_tools_from_generic_tools(filter((lambda x: x!=10), range(36))),
    {
        0: 8,
        1: 4,
        2: 16,
        3: 16,
        4: 16,
        5: 42,
        6: 16,
        7: 8,
        8: 2,
        9: 4,
        11: 4,
        12: 16,
        13: 1,
        14: 16,
        15: 8,
        16: 10,
        17: 12,
        18: 12,
        19: 1,
        21: 6,
        22: 6,
        23: 4,
        24: 2,
        25: 3,
        26: 42,
        27: 4,
        28: 4,
        29: 1,
        30: 1,
        31: 1,
        32: 1,
        33: 2,
        34: 3,
        35: lambda game: (0 if game.extra_bullets == (None, None, None) else (
            4 if game.extra_bullets.count(None) else 8
        ))
    },
    {
        0: 0,
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0,
        8: 10,
        9: 0,
        11: 0,
        12: 0,
        13: 1,
        14: 0,
        15: 0,
        16: 0,
        17: 0,
        18: 0,
        19: 2,
        20: 0,
        21: 0,
        22: 0,
        23: 0,
        24: 0,
        25: 0,
        26: 0,
        27: 0,
        28: 0,
        29: 1,
        30: 8,
        31: 32,
        32: 5,
        33: 0,
        34: 0,
        35: 0
    },
    {
        0: 0,
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 3,
        8: 3,
        9: 0,
        11: 0,
        12: 0,
        13: 1,
        14: 0,
        15: 0,
        16: 0,
        17: 0,
        18: 0,
        19: 2,
        20: 0,
        21: 0,
        22: 0,
        23: 0,
        24: 0,
        25: 0,
        26: 0,
        27: 0,
        28: 0,
        29: 0,
        30: 4,
        31: 16,
        32: 3,
        33: 3,
        34: 0,
        35: 0
    },
    8,
    True
)

infinite_mode: NormalGame = NormalGame(
    2,
    8,
    1,
    1,
    8,
    2,
    18446744073709551615,
    gen_tools_from_generic_tools(
        filter((lambda x: x not in (10, 11, 13, 32)), range(36))
    ),
    {
        0: 8,
        1: 4,
        2: 16,
        3: 16,
        4: 16,
        5: 42,
        6: 16,
        7: 8,
        8: 2,
        9: 4,
        12: 16,
        14: 16,
        15: 8,
        16: 10,
        17: 12,
        18: 12,
        19: 1,
        21: 6,
        22: 6,
        23: 4,
        24: 2,
        25: 3,
        26: 42,
        27: 4,
        28: 4,
        29: 1,
        30: 1,
        31: 2,
        33: 2,
        34: 3,
        35: lambda game: (0 if game.extra_bullets == (None, None, None) else (
            4 if game.extra_bullets.count(None) else 8
        ))
    },
    {
        0: 0,
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0,
        8: 10,
        9: 0,
        12: 0,
        14: 0,
        15: 0,
        16: 0,
        17: 0,
        18: 0,
        19: 4,
        20: 0,
        21: 0,
        22: 0,
        23: 0,
        24: 0,
        25: 0,
        26: 0,
        27: 0,
        28: 0,
        29: 1,
        30: 8,
        31: 32,
        33: 0,
        34: 0,
        35: 0
    },
    {
        0: 0,
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 3,
        8: 3,
        9: 0,
        12: 0,
        14: 0,
        15: 0,
        16: 0,
        17: 0,
        18: 0,
        19: 2,
        20: 0,
        21: 0,
        22: 0,
        23: 0,
        24: 0,
        25: 0,
        26: 0,
        27: 0,
        28: 0,
        29: 0,
        30: 4,
        31: 16,
        33: 3,
        34: 0,
        35: 0
    },
    9,
    True
)

xiaodao_party: NormalGame = NormalGame(
    2,
    8,
    1,
    1,
    2,
    1,
    10,
    gen_tools_from_generic_tools((2, 3)),
    {
        2: 4,
        3: 1
    },
    {
        2: 0,
        3: 0
    },
    {
        2: 0,
        3: 10
    },
    100,
    True,
    {}
)

dice_kingdom: NormalGame = NormalGame(
    2,
    8,
    1,
    1,
    8,
    50,
    randint(50, 90),
    gen_tools_from_generic_tools((11,)),
    {
        11: 1
    },
    {
        11: 0
    },
    {
        11: 0
    },
    100,
    True,
    {}
)

class InfiniteMode2 :
    period_count: int
    last_game: Optional[NormalGame]

    def __init__(self, period_count: int = 0) -> None :
        self.period_count = period_count
        self.last_game = None

    def __iter__(self) -> Iterator[Game] :
        return self

    def __next__(self) -> Game :
        lg: Optional[NormalGame] = self.last_game
        if lg is not None and not lg.players[0].alive :
            raise StopIteration
        r_slots: Optional[List[Slot]] = None if lg is None else (
            lg.r_slots if lg.slots_sharing is None or \
                          not lg.slots_sharing[0] else lg.slots_sharing[2]
        )
        r: Optional[Player] = None if lg is None else lg.players[0]
        explosion_exponent: Optional[int] = \
        None if lg is None else lg.explosion_exponent
        self.last_game = NormalGame(
            2,
            8,
            1,
            1,
            8,
            2,
            10+self.period_count,
            normal_mode.tools.copy(),
            {
                0: 8,
                1: 4,
                2: 16,
                3: 16,
                4: 16,
                5: 42,
                6: 16,
                7: 8,
                8: 2,
                9: 4,
                11: 4,
                12: 16,
                13: 1,
                14: 16,
                15: 8,
                16: 10,
                17: 12,
                18: 12,
                19: 1,
                21: 6,
                22: 6,
                23: 4,
                24: 2,
                25: 3,
                26: 42,
                27: 4,
                28: 4,
                29: 1,
                30: 1,
                31: 3,
                32: 1,
                33: 2,
                34: 3,
                35: lambda game: (
                    0 if game.extra_bullets == (None, None, None) else (
                        4 if game.extra_bullets.count(None) else 8
                    )
                )
            },
            {
                0: 0,
                1: 0,
                2: 0,
                3: 0,
                4: 0,
                5: 0,
                6: 0,
                7: 0,
                8: 10,
                9: 0,
                11: 0,
                12: 0,
                13: 1,
                14: 0,
                15: 0,
                16: 0,
                17: 0,
                18: 0,
                19: 4,
                20: 0,
                21: 0,
                22: 0,
                23: 0,
                24: 0,
                25: 0,
                26: 0,
                27: 0,
                28: 0,
                29: 1,
                30: 8,
                31: 32,
                32: 5,
                33: 0,
                34: 0,
                35: 0
            },
            {
                0: 0,
                1: 0,
                2: 0,
                3: 0,
                4: 0,
                5: 0,
                6: 0,
                7: 3,
                8: 3,
                9: 0,
                11: 0,
                12: 0,
                13: 1,
                14: 0,
                15: 0,
                16: 0,
                17: 0,
                18: 0,
                19: 2,
                20: 0,
                21: 0,
                22: 0,
                23: 0,
                24: 0,
                25: 0,
                26: 0,
                27: 0,
                28: 0,
                29: 0,
                30: 4,
                31: 16,
                32: 3,
                33: 3,
                34: 0,
                35: 0
            },
            9,
            True
        )
        if r is not None :
            r.stamina = 32 - (32-r.stamina) // 2
            self.last_game.players[0] = r
        if r_slots is not None :
            self.last_game.r_slots = r_slots
        if explosion_exponent is not None :
            self.last_game.explosion_exponent = explosion_exponent
        self.period_count += 1
        return self.last_game

combo_party: NormalGame = NormalGame(
    4,
    20,
    2,
    1,
    18,
    40,
    200,
    gen_tools_from_generic_tools((
        0, 1, 2, 9, 15, 17, 18, 21, 27, 28, 29, 34, 35
    )),
    {
        0: 2,
        1: 1,
        2: 6,
        9: 3,
        15: 8,
        17: 24,
        18: 20,
        21: 4,
        27: 3,
        28: 5,
        29: 1,
        34: 5,
        35: lambda game: (0 if game.extra_bullets == (None, None, None) else (
            4 if game.extra_bullets.count(None) else 8
        ))
    },
    {
        0: 0,
        1: 0,
        2: 0,
        9: 0,
        15: 0,
        17: 0,
        18: 0,
        21: 0,
        27: 0,
        28: 0,
        29: 1,
        34: 0,
        35: 0
    },
    {
        0: 0,
        1: 0,
        2: 0,
        9: 0,
        15: 0,
        17: 0,
        18: 0,
        21: 0,
        27: 0,
        28: 0,
        29: 1,
        34: 0,
        35: 0
    },
    12,
    True
)

exploded_test: NormalGame = NormalGame(
    2,
    8,
    1,
    1,
    8,
    10,
    50,
    gen_tools_from_generic_tools((5, 9, 21)),
    {
        5: 1,
        9: 16,
        21: 2
    },
    {
        5: 0,
        9: 0,
        21: 0
    },
    {
        5: 1,
        9: 0,
        21: 2
    },
    6,
    False
)

onlybyhand: NormalGame = NormalGame(
    2,
    8,
    1,
    1,
    8,
    18,
    50,
    {},
    {},
    {},
    {},
    0,
    not randint(0, 1),
    {}
)

GAMEMODE_SET: Dict[int, Union[
    Tuple[Iterable[Game], int, float],
    Tuple[Iterable[Game], int, float, str, Optional[str]]
]] = {
    1: ((normal_mode,), 2, 2.5, "普通模式", "新手入门首选"),
    2: ((infinite_mode,), 2, 2.5, "无限模式(一)", "陪你到天荒地老"),
    3: ((xiaodao_party,), 3, 3., "小刀狂欢", "哪发是实弹?"),
    4: ((dice_kingdom,), 4, 2.25, "骰子王国", "最考验运气的一集"),
    5: (InfiniteMode2(), 2, 2.5, "无限模式(二)",
        "霓为衣兮风为马,云之君兮纷纷而来下"),
    6: ((combo_party,), 3, 2.5, "连射派对", "火力全开"),
    7: ((exploded_test,), 2, 1.75, "炸膛测试", "枪在哪边好使?"),
    8: ((onlybyhand,), 1, 2.5, "赤手空“枪”", "没有道具了")
}

class Texts :
    GAME_TITLE: ClassVar[I18nText] = I18nText(
        "恶魔轮盘赌（重构版）",
        en_en="Evil's Mutual Linear Probability Detection"
    )
    GAME_MODE: ClassVar[I18nText] = I18nText("游戏模式", en_en="Game Mode")
    NO_INTRODUCTION: ClassVar[I18nText] = \
    I18nText("没有介绍", en_en="No introduction")
    INTRODUCTION: ClassVar[I18nText] = I18nText("介绍:", en_en="Introduction:")
    NO_NAME: ClassVar[I18nText] = I18nText("没有名字", en_en="No name")
    CHOOSE_GAME_MODE: ClassVar[I18nText] = I18nText(
        "选择游戏模式请输入对应的编号:",
        en_en="Input the ID for selecting game mode:"
    )
    R_SLOT_EXPIRED: ClassVar[I18nText] = I18nText(
        "非常可惜,随着槽位的到期,你的 {0} 也不翼而飞",
        en_en="It's a pity that your {0} went AWOL with the slot expired"
    )
    E_SLOT_EXPIRED: ClassVar[I18nText] = I18nText(
        "非常高兴,随着槽位的到期,恶魔的 {0} 不翼而飞",
        en_en="It's a delight that the Evil's {0} went AWOL with the slot "
              "expired"
    )
    PLAYER_SLOT_EXPIRED: ClassVar[I18nText] = I18nText(
        "随着槽位的到期,玩家 {1} 的 {0} 不翼而飞",
        en_en="Player {1}'s {0} went AWOL with the slot expired"
    )
    R_TOOL_SENT: ClassVar[I18nText] = I18nText(
        "你获得 {0} 个道具", en_en="You've got {0} tool(s)"
    )
    E_TOOL_SENT: ClassVar[I18nText] = I18nText(
        "恶魔获得 {0} 个道具", en_en="The Evil's got {0} tool(s)"
    )
    PLAYER_TOOL_SENT: ClassVar[I18nText] = I18nText(
        "玩家 {1} 获得 {0} 个道具", en_en="Player {1}'s got {0} tool(s)"
    )
    BULLET_TOTAL: ClassVar[I18nText] = I18nText(
        "子弹共有 {0} 发", en_en="Bullet total {0}"
    )
    TRUES_FALSES_COUNT: ClassVar[I18nText] = I18nText(
        "实弹 {0} 发 , 空弹 {1} 发", en_en="{0} true(s), {1} false(s)"
    )
    PROBLEM_SAVING: ClassVar[I18nText] = I18nText(
        "存档时遇到问题!", en_en="Problem saving!"
    )
