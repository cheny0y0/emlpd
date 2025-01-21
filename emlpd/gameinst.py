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

    CUR_CLIP: ClassVar[I18nText] = I18nText("当前弹夹:", en_en="Current clip:")
    CUR_EXTRA_CLIPS: ClassVar[I18nText] = \
    I18nText("当前额外弹夹:", en_en="Current extra clips:")
    CUR_DAZE: ClassVar[I18nText] = I18nText(
        "双方晕的轮数: {0} - {1}", en_en="The two's dazing turns: {0} - {1}"
    )
    CUR_STAMINA: ClassVar[I18nText] = \
    I18nText("双方体力: {0} - {1}", en_en="The two's stamina: {0} - {1}")
    PLAYER_0_BULLETPROOF: ClassVar[I18nText] = \
    I18nText("玩家 0 的防弹衣:", en_en="Player 0's 防弹衣:")
    PLAYER_1_BULLETPROOF: ClassVar[I18nText] = \
    I18nText("玩家 1 的防弹衣:", en_en="Player 1's 防弹衣:")
    R_BULLETPROOF: ClassVar[I18nText] = \
    I18nText("你的的防弹衣:", en_en="Your 防弹衣:")
    E_BULLETPROOF: ClassVar[I18nText] = \
    I18nText("恶魔的防弹衣:", en_en="The Evil's 防弹衣:")
    CUR_BULLET_CATCHER: ClassVar[I18nText] = I18nText(
        "双方的叠加接弹套: {0} - {1}",
        en_en="The two's stacked 接弹套: {0} - {1}"
    )
    CUR_REPEATER: ClassVar[I18nText] = I18nText(
        "双方的叠加双发射手: {0} - {1}",
        en_en="The two's stacked 双发射手: {0} - {1}"
    )
    CUR_COMBO_SHOOTER: ClassVar[I18nText] = I18nText(
        "双方的叠加连发射手: {0} - {1}",
        en_en="The two's stacked 连发射手: {0} - {1}"
    )
    CUR_SELFSHOOT_PROMISES: ClassVar[I18nText] = I18nText(
        "双方的叠加良枪(一): {0} - {1}",
        en_en="The two's stacked 良枪(一): {0} - {1}"
    )
    CUR_AGAINSTSHOOT_PROMISES: ClassVar[I18nText] = I18nText(
        "双方的叠加良枪(二): {0} - {1}",
        en_en="The two's stacked 良枪(二): {0} - {1}"
    )
    CUR_CURSED_SHOOT: ClassVar[I18nText] = I18nText(
        "双方的叠加破枪: {0} - {1}", en_en="The two's stacked 破枪: {0} - {1}"
    )
    CUR_BREAKCARE_ROUNDS: ClassVar[I18nText] = I18nText(
        "双方的破防回合数: {0} - {1}",
        en_en="The two's breaking care rounds: {0} - {1}"
    )
    CUR_BREAKCARE_POTENTIAL: ClassVar[I18nText] = I18nText(
        "双方的破防潜能: {0} - {1}",
        en_en="The two's breaking care potential: {0} - {1}"
    )
    CUR_EXPLOSION_EXPON: ClassVar[I18nText] = \
    I18nText("当前炸膛指数: {0}", en_en="Current explosion exponent: {0}")

    @property
    def debug_message(self) -> Iterable[Tuple[
        Iterable[object], Optional[str], Optional[str]
    ]] :
        res: List[Tuple[Iterable[object], Optional[str], Optional[str]]] = \
        [((self.CUR_CLIP, self.bullets), None, None)]
        if self.extra_bullets != (None, None, None) :
            res.append(((self.CUR_EXTRA_CLIPS,self.extra_bullets), None, None))
        r: Player = self.players[0]
        e: Player = self.players[1]
        res.append(((self.CUR_DAZE.format(r.stopped_turns, e.stopped_turns),),
                    None, None))
        if isinstance(r, NormalPlayer) and isinstance(e, NormalPlayer) :
            res.append(((self.CUR_STAMINA.format(r.stamina, e.stamina),), None,
                        None))
            if self.has_tools(9) or r.bulletproof or e.bulletproof :
                if e.controllable :
                    res.append(((self.PLAYER_0_BULLETPROOF, r.bulletproof),
                                None, None))
                    res.append(((self.PLAYER_1_BULLETPROOF, e.bulletproof),
                                None, None))
                else :
                    res.append(((self.R_BULLETPROOF, r.bulletproof),None,None))
                    res.append(((self.E_BULLETPROOF, e.bulletproof),None,None))
            if self.has_tools(14) or r.bullet_catcher_level or \
               e.bullet_catcher_level :
                res.append(((self.CUR_BULLET_CATCHER.format(
                    r.bullet_catcher_level, e.bullet_catcher_level
                ),), None, None))
            if self.has_tools(17) or r.multishoot_level or e.multishoot_level :
                res.append(((self.CUR_REPEATER.format(
                    r.multishoot_level, e.multishoot_level
                ),), None, None))
            if self.has_tools(18) or r.comboshoot_level or e.comboshoot_level :
                res.append(((self.CUR_COMBO_SHOOTER.format(
                    r.comboshoot_level, e.comboshoot_level
                ),), None, None))
            if self.has_tools(0) or r.selfshoot_promises or \
               e.selfshoot_promises :
                res.append(((self.CUR_SELFSHOOT_PROMISES.format(
                    r.selfshoot_promises, e.selfshoot_promises
                ),), None, None))
            if self.has_tools(1) or r.againstshoot_promises or \
               e.againstshoot_promises :
                res.append(((self.CUR_AGAINSTSHOOT_PROMISES.format(
                    r.againstshoot_promises, e.againstshoot_promises
                ),), None, None))
            if self.has_tools(21) or r.cursed_shoot_level or \
               e.cursed_shoot_level :
                res.append(((self.CUR_CURSED_SHOOT.format(
                    r.cursed_shoot_level, e.cursed_shoot_level
                ),), None, None))
            if self.has_tools(9) or self.has_tools(11) or \
               r.breakcare_rounds or e.breakcare_rounds or \
               r.breakcare_potential or e.breakcare_potential :
                res.append(((self.CUR_BREAKCARE_ROUNDS.format(
                    r.breakcare_rounds, e.breakcare_rounds
                ),), None, None))
                res.append(((self.CUR_BREAKCARE_POTENTIAL.format(
                    r.breakcare_potential, e.breakcare_potential
                ),), None, None))
        res.append(((self.CUR_EXPLOSION_EXPON
                     .format(self.explosion_exponent),), None, None))
        return res

    CUR_R_HP: ClassVar[I18nText] = \
    I18nText("当前你的生命值为: {0}", en_en="Your current HP: {0}")
    CUR_R_HURTS: ClassVar[I18nText] = \
    I18nText("当前你的负伤数为: {0}", en_en="Your current hurting point: {0}")
    CUR_E_HP: ClassVar[I18nText] = \
    I18nText("当前恶魔生命值为: {0}", en_en="The Evil's current HP: {0}")
    CUR_E_HURTS: ClassVar[I18nText] = I18nText(
        "当前恶魔负伤数为: {0}", en_en="The Evil's current hurting point: {0}"
    )
    CUR_PLAYER_HP: ClassVar[I18nText] = \
    I18nText("当前玩家 {1} 生命值为: {0}",en_en="Player {1}'s current HP: {0}")
    CUR_PLAYER_HURTS: ClassVar[I18nText] = I18nText(
        "当前玩家 {1} 负伤数为: {0}",
        en_en="Player {1}'s current hurting point: {0}"
    )

    @property
    def round_start_message(self) -> Iterable[Tuple[
        Iterable[object], Optional[str], Optional[str]
    ]] :
        res: List[Tuple[Iterable[object], Optional[str], Optional[str]]] = []
        for i, player in self.players.items() :
            if i == 0 and not self.players[1].controllable :
                res.append(((self.CUR_R_HP.format(player.hp),), None, None))
                if isinstance(player, NormalPlayer) :
                    res.append(((self.CUR_R_HURTS.format(player.hurts),), None,
                                None))
            elif i == 1 and not self.players[1].controllable :
                res.append(((self.CUR_E_HP.format(player.hp),), None, None))
                if isinstance(player, NormalPlayer) :
                    res.append(((self.CUR_E_HURTS.format(player.hurts),), None,
                                None))
            else :
                res.append(((self.CUR_PLAYER_HP.format(player.hp, i),), None,
                            None))
                if isinstance(player, NormalPlayer) :
                    res.append(((self.CUR_PLAYER_HURTS
                                 .format(player.hurts, i),), None, None))
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
    GAME_MODE: ClassVar[I18nText] = I18nText(
        "游戏模式 {0}:", en_en="Game Mode {0}:"
    )
    NO_INTRODUCTION: ClassVar[I18nText] = \
    I18nText("没有介绍", en_en="No introduction")
    INTRODUCTION: ClassVar[I18nText] = I18nText("介绍:", en_en="Introduction:")
    NO_NAME: ClassVar[I18nText] = I18nText("没有名字", en_en="No name")
    CHOOSE_GAME_MODE: ClassVar[I18nText] = I18nText(
        "选择游戏模式请输入对应的编号:",
        en_en="Input the ID for selecting game mode:"
    )
    PLAYER_1_WON_STAGE: ClassVar[I18nText] = I18nText(
        "恭喜玩家 1 赢得了擂台战!",
        en_en="Congratulations to Player 1 for winning the stage battle!"
    )
    PLAYER_0_WON_STAGE: ClassVar[I18nText] = I18nText(
        "恭喜玩家 0 赢得了擂台战!",
        en_en="Congratulations to Player 0 for winning the stage battle!"
    )
    E_WON_STAGE: ClassVar[I18nText] = I18nText(
        "很遗憾,恶魔赢得了擂台战",
        en_en="It's a pity that the Evil won the stage battle"
    )
    R_WON_STAGE: ClassVar[I18nText] = I18nText(
        "恭喜你,你赢得了擂台站!",
        en_en="Congratulations to you for winning the stage battle!"
    )
    PERIOD_COUNT_INFO: ClassVar[I18nText] = I18nText(
        "本周目持续了 {0} 轮,\n{1} 回合",
        en_en="This period kept {0} turn(s),\n{1} round(s)"
    )
    PERIOD_ORDINAL: ClassVar[I18nText] = \
    I18nText("第 {0} 周目", en_en="Period {0}")
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
    R_TEMP_SLOT_SENT: ClassVar[I18nText] = I18nText(
        "你获得1个有效期 {0} 回合的空槽位",
        en_en="You've got 1 empty slot with active time for {0} round(s)"
    )
    E_TEMP_SLOT_SENT: ClassVar[I18nText] = I18nText(
        "恶魔获得1个有效期 {0} 回合的空槽位",
        en_en="The Evil's got 1 empty slot with active time for {0} round(s)"
    )
    PLAYER_TEMP_SLOT_SENT: ClassVar[I18nText] = I18nText(
        "玩家 {1} 获得1个有效期 {0} 回合的空槽位",
        en_en="Player {1}'s got 1 empty slot with active time for {0} round(s)"
    )
    R_PERMASLOT_SENT: ClassVar[I18nText] = I18nText(
        "你获得1个永久空槽位", en_en="You've got 1 empty permanent slot"
    )
    E_PERMASLOT_SENT: ClassVar[I18nText] = I18nText(
        "恶魔获得1个永久空槽位", en_en="The Evil's got 1 empty permanent slot"
    )
    PLAYER_PERMASLOT_SENT: ClassVar[I18nText] = I18nText(
        "玩家 {0} 获得1个永久空槽位",
        en_en="Player {0}'s got 1 empty permanent slot"
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
    PROBLEM_SAVING: ClassVar[I18nText] = \
    I18nText("存档时遇到问题!", en_en="Problem saving!")
    R_DAZING: ClassVar[I18nText] = I18nText(
        "感觉...头晕晕的...要变成{0}了~",
        en_en="Feel...dizzy...turning into {0}~"
    )
    E_DAZING: ClassVar[I18nText] = I18nText(
        "哈哈哈哈,恶魔被敲晕了,还是我的回合!",
        en_en="Hahahaha, the Evil's dazing, still my round!"
    )
    OPPO_DAZING: ClassVar[I18nText] = I18nText(
        "哈哈哈哈,对方被敲晕了,还是我的回合!",
        en_en="Hahahaha, the opposite's dazing, still my round!"
    )
    YOUR_TURN: ClassVar[I18nText] = I18nText(
        "本轮由你操作", en_en="It's time for your operation"
    )
    PLAYER_TURN: ClassVar[I18nText] = I18nText(
        "本轮由玩家 {0} 操作", en_en="It's time for Player {0}'s operation"
    )
    OPER_CHOOSE_1078: ClassVar[I18nText] = I18nText(
        "请选择:1朝对方开枪,0朝自己开枪,7打开道具库,8查看对方道具",
        en_en="Please choose: 1 to shoot at the opposite, 0 to shoot at "
              "yourself, 7 to open tool warehouse, 8 to view the opposite's "
              "tools"
    )
    OPER_CHOOSE_10: ClassVar[I18nText] = I18nText(
        "请选择:1朝对方开枪,0朝自己开枪",
        en_en="Please choose: 1 to shoot at the opposite, 0 to shoot at "
              "yourself"
    )
    TOOL_WAREHOUSE: ClassVar[I18nText] = \
    I18nText("道具库:", en_en="Tool Warehouse:")
    TOOL_NAME_ONE: ClassVar[I18nText] = \
    I18nText("道具 {0}: {1}", en_en="Tool {0}: {1}")
    TOOL_NAME_MORE: ClassVar[I18nText] = \
    I18nText("(*{2}) 道具 {0}: {1}", en_en="(*{2}) Tool {0}: {1}")
    TOOL_NO_DESC: ClassVar[I18nText] = \
    I18nText("此道具无描述", en_en="No description for this tool")
    TOOL_DESC: ClassVar[I18nText] = I18nText("描述:", en_en="Description:")
    SLOT_EXPIRED_AT: ClassVar[I18nText] = \
    I18nText("还有 {0} 回合到期", en_en="Will be expired {0} round(s) later")
    TOOL_WAREHOUSE_EMPTY: ClassVar[I18nText] = I18nText("(空)",en_en="(empty)")
    ENTER_TO_RETURN: ClassVar[I18nText] = \
    I18nText("返回请直接按回车", en_en="Press enter directly to return")
    INPUT_ID_TO_USE: ClassVar[I18nText] = I18nText(
        "使用道具请输入其对应编号:", en_en="Input the tool's ID to use it:"
    )
    R_USES_ID2: ClassVar[I18nText] = I18nText(
        "你使用了小刀,结果会如何呢?真让人期待",
        en_en="You've used 小刀, what will the result be? Let's wait and see"
    )
    R_USES_ID3: ClassVar[Tuple[I18nText, I18nText]] = (I18nText(
        "你排出了一颗空弹", en_en="You've made a false bullet quit"
    ), I18nText("你排出了一颗实弹", en_en="You've made a true bullet quit"))
    R_USES_ID4: ClassVar[I18nText] = I18nText(
        "恭喜你,成功敲晕了对方!",
        en_en="Conguatulations to you for hitting the opposite to dazing!"
    )
    R_USES_ID5: ClassVar[Tuple[I18nText, I18nText]] = (I18nText(
        "因为你的不诚实,你并未回复生命,甚至失去了道德的崇高赞许",
        en_en="Due to your dishonesty, you didn't regain a HP, and even lost "
              "道德的崇高赞许"
    ), I18nText(
        "你使用了道德的崇高赞许,回复了1点生命",
        en_en="You've used 道德的崇高赞许 and regained 1 HP"
    ))
    R_USES_ID6: ClassVar[Tuple[I18nText, I18nText]] = (
        I18nText("当前的子弹为空弹", en_en="The current bullet is false"),
        I18nText("当前的子弹为实弹", en_en="The current bullet is true")
    )
    TOOL_PLUS_1: ClassVar[I18nText] = \
    I18nText("+1 道具 {0}", en_en="+1 Tool {0}")
    R_USES_ID9: ClassVar[I18nText] = \
    I18nText("你穿上了一件防弹衣", en_en="You've put a 防弹衣 on")
    R_USES_ID11: ClassVar[I18nText] = \
    I18nText("你摇出了 {0} 点", en_en="You've rolled out {0} points")
    R_LOST_2_HP: ClassVar[I18nText] = \
    I18nText("你失去了2点生命", en_en="You've lost 2 HP")
    R_LOST_1_HP: ClassVar[I18nText] = \
    I18nText("你失去了1点生命", en_en="You've lost 1 HP")
    R_GOT_1_HP: ClassVar[I18nText] = \
    I18nText("你获得了1点生命", en_en="You've got 1 HP")
    R_ATTACK_BOOSTED_2: ClassVar[I18nText] = I18nText(
        "你的攻击力提高了2点", en_en="Your attack damage has increased by 2"
    )
    OPPO_LOST_1_HP: ClassVar[I18nText] = \
    I18nText("对方失去了1点生命", en_en="The opposite has lost 1 HP")
    E_LOST_1_HP: ClassVar[I18nText] = \
    I18nText("恶魔失去了1点生命", en_en="The Evil has lost 1 HP")
    OPPO_LOST_2_HP: ClassVar[I18nText] = \
    I18nText("对方失去了2点生命", en_en="The opposite has lost 2 HP")
    E_LOST_2_HP: ClassVar[I18nText] = \
    I18nText("恶魔失去了2点生命", en_en="The Evil has lost 2 HP")
    OPPO_CRIT: ClassVar[I18nText] = \
    I18nText("对方受到暴击!!!", en_en="The opposite CRIT!!!")
    OPPO_CUR_HP: ClassVar[I18nText] = \
    I18nText("对方生命值: {0}", en_en="The opposite's HP: {0}")
    E_CRIT: ClassVar[I18nText] = \
    I18nText("恶魔受到暴击!!!", en_en="The Evil CRIT!!!")
    E_CUR_HP: ClassVar[I18nText] = \
    I18nText("恶魔生命值: {0}", en_en="The Evil's HP: {0}")
    R_TURNED_INTO_OPPO: ClassVar[I18nText] = \
    I18nText("你变成了对方的样子", en_en="You've turned into the opposite")
    R_TURNED_INTO_E: ClassVar[I18nText] = \
    I18nText("你变成了恶魔的样子", en_en="You've turned into the Evil")
    OPPO_TURNED_INTO_R: ClassVar[I18nText] = \
    I18nText("对方变成了你的样子", en_en="The opposite has turned into you")
    E_TURNED_INTO_R: ClassVar[I18nText] = \
    I18nText("恶魔变成了你的样子", en_en="The Evil has turned into you")
    CLIP_CHANGED: ClassVar[I18nText] = \
    I18nText("弹夹有变动", en_en="The clip has changed")
    BEFORE_USE_ID16: ClassVar[I18nText] = I18nText(
        "输入0以开始重整弹药,直接按回车以取消。",
        en_en="Input 0 to start arranging bullets or press enter directly to "
              "cancel."
    )
    DURING_USE_ID16: ClassVar[Tuple[I18nText, I18nText]] = \
    (I18nText("空", en_en="F"), I18nText("实", en_en="T"))
    R_USES_ID16: ClassVar[I18nText] = \
    I18nText("你重整了一下弹药", en_en="You've arranged the bullets")
    BEFORE_USE_ID22_1: ClassVar[I18nText] = I18nText(
        "弹夹内只有1发子弹,将其取出会即刻进入下一回合,是否将其取出?(y/[N])",
        en_en="There's only 1 bullet in the clip, drawing it out will make "
              "next round come immediately, proceed? (y/[N])"
    )
    R_USES_ID22: ClassVar[I18nText] = \
    I18nText("你取出了一颗子弹", en_en="You've drawn a bullet out")
    BEFORE_USE_ID22: ClassVar[I18nText] = I18nText(
        "请输入要取出子弹的编号(0~{0},0为当前子弹,输入其它以取消):",
        en_en="Please input the number of the bullet to draw out(0~{0}, 0 "
              "stands for the current bullet, input other content to cancel):"
    )
    BEFORE_USE_ID23: ClassVar[I18nText] = I18nText(
        "请输入要插入空弹的编号(0~{0},0为当前子弹之前,输入其它以取消):",
        en_en="Please input the number of the false bullet to insert(0~{0}, 0 "
              "stands for the place before the cureent bullet, input other "
              "content to cancel):"
    )
    R_USES_ID23: ClassVar[I18nText] = \
    I18nText("你放入了一颗空弹", en_en="You've put a false bullet in")
    BEFORE_USE_ID24: ClassVar[I18nText] = I18nText(
        "请输入要插入实弹的编号(0~{0},0为当前子弹之前,输入其它以取消):",
        en_en="Please input the number of the true bullet to insert(0~{0}, 0 "
              "stands for the place before the cureent bullet, input other "
              "content to cancel):"
    )
    R_USES_ID24: ClassVar[I18nText] = \
    I18nText("你放入了一颗实弹", en_en="You've put a true bullet in")
    BEFORE_USE_ID25: ClassVar[I18nText] = I18nText(
        "请输入要插入神秘子弹的编号(0~{0},0为当前子弹之前,输入其它以取消):",
        en_en="Please input the number of the 神秘子弹 to insert(0~{0}, 0 "
              "stands for the place before the cureent bullet, input other "
              "content to cancel):"
    )
    R_USES_ID25: ClassVar[I18nText] = \
    I18nText("你放入了一颗神秘子弹", en_en="You've put a 神秘子弹 in")
    R_USES_ID26: ClassVar[I18nText] = \
    I18nText("你使用了绷带", en_en="You've used a 绷带")
    R_USES_ID27_5: ClassVar[I18nText] = I18nText(
        "你使用了医疗包,回复了5点生命",
        en_en="You've used 医疗包 and regained 5 HP"
    )
    R_USES_ID27_4: ClassVar[I18nText] = I18nText(
        "你使用了医疗包,回复了4点生命",
        en_en="You've used 医疗包 and regained 4 HP"
    )
    R_USES_ID27_3: ClassVar[I18nText] = I18nText(
        "你使用了医疗包,回复了3点生命",
        en_en="You've used 医疗包 and regained 3 HP"
    )
    R_USES_ID27_2: ClassVar[I18nText] = I18nText(
        "你使用了医疗包,回复了2点生命",
        en_en="You've used 医疗包 and regained 2 HP"
    )
    R_USES_ID27_1: ClassVar[I18nText] = I18nText(
        "你使用了医疗包,回复了1点生命",
        en_en="You've used 医疗包 and regained 1 HP"
    )
    BEFORE_USE_ID32_1: ClassVar[I18nText] = I18nText(
        "你只有1生命值,是否要发起擂台战?(y/[N])",
        en_en="You have only 1 HP, sure to initiate a stage battle?(y/[N])"
    )
    OPPO_INITS_STAGE: ClassVar[I18nText] = I18nText(
        "对方以 {0} 生命值向你发起了擂台战",
        en_en="The opposite has initiated a stage battle using {0} HP with you"
    )
    R_RECEIVES_STAGE_1: ClassVar[I18nText] = I18nText(
        "你以仅有的 1 生命值应战", en_en="You accepted with your only 1 HP"
    )
    OPPO_RECEIVES_STAGE: ClassVar[I18nText] = \
    I18nText("对方以 {0} 生命值应战",en_en="The opposite accepted with {0} HP")
    R_RECEIVES_STAGE: ClassVar[I18nText] = I18nText(
        "请输入你要作为赌注的生命值(1~{0}):",
        en_en="Please input the HP you're going to wager(1~{0}):"
    )
    E_RECEIVES_STAGE: ClassVar[I18nText] = \
    I18nText("恶魔以 {0} 生命值应战", en_en="The Evil accepted with {0} HP")
    BEFORE_USE_ID32: ClassVar[I18nText] = I18nText(
        "请输入你要作为赌注的生命值(1~{0},输入其它以取消):",
        en_en="Please input the HP you're going to wager(1~{0}, input other "
              "content to cancel):"
    )
    R_USES_ID33: ClassVar[I18nText] = \
    I18nText("你维修了一下枪筒", en_en="You've mended the barrel")
    R_USES_ID34: ClassVar[I18nText] = \
    I18nText("弹夹进行了空实分离", en_en="The clip has done 空实分离")
    R_USES_ID35: ClassVar[I18nText] = \
    I18nText("你合并了一下弹夹", en_en="You've merged the clips")
    TOOL_MINUS_1: ClassVar[I18nText] = \
    I18nText("-1 道具 {0}", en_en="-1 Tool {0}")
    NO_SUCH_TOOL: ClassVar[I18nText] = I18nText(
        "道具 {0} 不存在或未拥有",
        en_en="Tool {0} does not exist, or you don't have one"
    )
    OPPO_TOOL_WAREHOUSE: ClassVar[I18nText] = \
    I18nText("对方的道具库:", en_en="The Opposite's Tool Warehouse:")
    E_TOOL_WAREHOUSE: ClassVar[I18nText] = \
    I18nText("恶魔的道具库:", en_en="The Evil's Tool Warehouse:")
    R_EXPLODES: ClassVar[I18nText] = \
    I18nText("哦嘿,子弹居然炸膛了!", en_en="Oh hey, the bullet has exploded!")
    R_TRUE_ON_R: ClassVar[I18nText] = I18nText(
        "感觉像是去奈何桥走了一遭,竟然是个实弹!",
        en_en="Feeling like walking through Naihe Bridge, it was a true bullet!"
    )
    R_CUR_HP: ClassVar[I18nText] = \
    I18nText("你的生命值: {0}", en_en="Your HP: {0}")
    R_FALSE_ON_R: ClassVar[I18nText] = \
    I18nText("啊哈!,是个空弹!", en_en="Aha!, a false bullet!")
    OPPO_CATCHES_BULLET: ClassVar[I18nText] = \
    I18nText("对方接住了一颗子弹", en_en="The opposite caught a bullet")
    E_CATCHES_BULLET: ClassVar[I18nText] = \
    I18nText("恶魔接住了一颗子弹", en_en="The Evil caught a bullet")
    OPPO_BULLETPROOF_DEFENDS: ClassVar[I18nText] = I18nText(
        "对方的防弹衣承受了这次撞击",
        en_en="The opposite's 防弹衣 defended the collision"
    )
    E_BULLETPROOF_DEFENDS: ClassVar[I18nText] = I18nText(
        "恶魔的防弹衣承受了这次撞击",
        en_en="The Evil's 防弹衣 defended the collision"
    )
    OPPO_BULLETPROOF_BREAKS: ClassVar[I18nText] = I18nText(
        "对方的一件防弹衣爆了", en_en="One of the opposite's 防弹衣 was broken"
    )
    E_BULLETPROOF_BREAKS: ClassVar[I18nText] = I18nText(
        "恶魔的一件防弹衣爆了", en_en="One of the Evil's 防弹衣 was broken"
    )
    R_TRUE_ON_E: ClassVar[I18nText] = \
    I18nText("运气非常好,是个实弹!", en_en="Good luck, it was a true bullet!")
    R_FALSE_ON_E: ClassVar[I18nText] = \
    I18nText("很遗憾,是个空弹", en_en="It's a pity that it was a false bullet")
    WRONG_OPER_NUM: ClassVar[I18nText] = I18nText(
        "请确定输入的数字正确", en_en="Please ensure the number is correct"
    )
    E_USES_ID2: ClassVar[I18nText] = I18nText(
        "恶魔使用了小刀,哦吼吼,结果会如何呢?",
        en_en="The Evil has used 小刀, ohoho, what will the result be?"
    )
    E_USES_ID3: ClassVar[Tuple[I18nText, I18nText]] = (I18nText(
        "恶魔排出了一颗空弹", en_en="The Evil has made a false bullet quit"
    ), I18nText("恶魔排出了一颗实弹",
                en_en="The Evil has made a true bullet quit"))
    E_USES_ID4: ClassVar[I18nText] = I18nText(
        "恭喜恶魔,成功把你变成了{0}!",
        en_en="Conguatulations to the Evil for turning you into {0}!"
    )
    E_USES_ID5: ClassVar[Tuple[I18nText, I18nText]] = (I18nText(
        "因为恶魔的不诚实,你并未回复生命,甚至失去了道德的崇高赞许",
        en_en="Due to the Evil's dishonesty, you didn't regain a HP, and even "
              "lost 道德的崇高赞许"
    ), I18nText(
        "恶魔使用了道德的崇高赞许,回复了1点生命",
        en_en="The Evil has used 道德的崇高赞许 and regained 1 HP"
    ))
    E_USES_ID6: ClassVar[I18nText] = I18nText(
        "恶魔查看了枪里的子弹并笑了一下",
        en_en="The Evil has viewed the bullet in the gun and smiled"
    )
    E_USES_ID9: ClassVar[I18nText] = \
    I18nText("恶魔穿上了一件防弹衣", en_en="The Evil has put a 防弹衣 on")
    E_USES_ID11: ClassVar[I18nText] = \
    I18nText("恶魔摇出了 {0} 点", en_en="The Evil has rolled out {0} points")
    E_GOT_1_HP: ClassVar[I18nText] = \
    I18nText("恶魔获得了1点生命", en_en="The Evil has got 1 HP")
    E_ATTACK_BOOSTED_2: ClassVar[I18nText] = I18nText(
        "恶魔的攻击力提高了2点",
        en_en="The Evil's attack damage has increased by 2"
    )
    R_CRIT: ClassVar[I18nText] = \
    I18nText("你受到暴击!!!", en_en="You CRIT!!!")
    E_USES_ID16: ClassVar[I18nText] = \
    I18nText("恶魔重整了一下弹药", en_en="The Evil has arranged the bullets")
    E_USES_ID22: ClassVar[I18nText] = \
    I18nText("恶魔取出了一颗子弹", en_en="The Evil has drawn a bullet out")
    E_USES_ID23: ClassVar[I18nText] = \
    I18nText("恶魔放入了一颗空弹", en_en="The Evil has put a false bullet in")
    E_USES_ID24: ClassVar[I18nText] = \
    I18nText("恶魔放入了一颗实弹", en_en="The Evil has put a true bullet in")
    E_USES_ID25: ClassVar[I18nText] = \
    I18nText("恶魔放入了一颗神秘子弹", en_en="The Evil has put a 神秘子弹 in")
    E_USES_ID26: ClassVar[I18nText] = \
    I18nText("恶魔使用了绷带", en_en="The Evil has used a 绷带")
    E_USES_ID27_5: ClassVar[I18nText] = I18nText(
        "恶魔使用了医疗包,回复了5点生命",
        en_en="The Evil has used 医疗包 and regained 5 HP"
    )
    E_USES_ID27_4: ClassVar[I18nText] = I18nText(
        "恶魔使用了医疗包,回复了4点生命",
        en_en="The Evil has used 医疗包 and regained 4 HP"
    )
    E_USES_ID27_3: ClassVar[I18nText] = I18nText(
        "恶魔使用了医疗包,回复了3点生命",
        en_en="The Evil has used 医疗包 and regained 3 HP"
    )
    E_USES_ID27_2: ClassVar[I18nText] = I18nText(
        "恶魔使用了医疗包,回复了2点生命",
        en_en="The Evil has used 医疗包 and regained 2 HP"
    )
    E_USES_ID27_1: ClassVar[I18nText] = I18nText(
        "恶魔使用了医疗包,回复了1点生命",
        en_en="The Evil has used 医疗包 and regained 1 HP"
    )
    E_INITS_STAGE: ClassVar[I18nText] = I18nText(
        "恶魔以 {0} 生命值向你发起了擂台战",
        en_en="The Evil has initiated a stage battle using {0} HP with you"
    )
    E_USES_ID33: ClassVar[I18nText] = \
    I18nText("恶魔维修了一下枪筒", en_en="The Evil has mended the barrel")
    E_USES_ID34: ClassVar[I18nText] = \
    I18nText("弹夹进行了空实分离", en_en="The clip has done 空实分离")
    E_USES_ID35: ClassVar[I18nText] = \
    I18nText("恶魔合并了一下弹夹", en_en="The Evil has merged the clips")
    E_TO_E: ClassVar[I18nText] = \
    I18nText("恶魔将枪口对准了自己", en_en="The Evil pointed at itself")
    E_EXPLODES: ClassVar[I18nText] = \
    I18nText("啊哦,子弹居然炸膛了!", en_en="Ah oh, the bullet has exploded!")
    R_CATCHES_BULLET: ClassVar[I18nText] = \
    I18nText("你接住了一颗子弹", en_en="You caught a bullet")
    R_BULLETPROOF_DEFENDS: ClassVar[I18nText] = I18nText(
        "你的防弹衣承受了这次撞击", en_en="Your 防弹衣 defended the collision"
    )
    R_BULLETPROOF_BREAKS: ClassVar[I18nText] = \
    I18nText("你的一件防弹衣爆了", en_en="One of your 防弹衣 was broken")
    E_TRUE_ON_R: ClassVar[I18nText] = \
    I18nText("运气非常差,是个实弹!", en_en="Bad luck, it was a true bullet!")
    E_FALSE_ON_R: ClassVar[I18nText] = \
    I18nText("很幸运,是个空弹", en_en="Fortunately, it was a false bullet")
    E_TRUE_ON_E: ClassVar[I18nText] = I18nText(
        "“砰!”一声枪响,它自杀了,你心里暗喜",
        en_en="“Pong!” With the gun sounding, it was on itself, you feel happy"
              " secretly"
    )
    E_FALSE_ON_E: ClassVar[I18nText] = I18nText(
        "“啊哈!,是个空弹!”恶魔嘲讽道",
        en_en="“Aha!, a false bullet!” The Evil snears"
    )
    E_TO_R: ClassVar[I18nText] = \
    I18nText("恶魔朝你开了一枪", en_en="The Evil shot at you")
    PLAYER_0_WON: ClassVar[I18nText] = I18nText(
        "恭喜玩家 0 ,成功把玩家 1 变成了{0}!",
        en_en="Congratulations to Player 0 for turning Player 1 into {0}!"
    )
    PLAYER_1_WON: ClassVar[I18nText] = I18nText(
        "恭喜玩家 1 ,成功把玩家 0 变成了{0}!",
        en_en="Congratulations to Player 1 for turning Player 0 into {0}!"
    )
    END_0_0: ClassVar[I18nText] = \
    I18nText("你们最后同归于尽了", en_en="You finally perished together")
    R_WON: ClassVar[I18nText] = I18nText(
        "恭喜你,成功把恶魔变成了{0}!",
        en_en="Congratulations, you turned the Evil into {0}!"
    )
    R_WON_1: ClassVar[I18nText] = I18nText(
        "恭喜你,成功把恶魔打得体无完肤!",
        en_en="Congratulations, you made the Evil injured all over the body!"
    )
    R_WON_2: ClassVar[I18nText] = I18nText(
        "恭喜你,成功把恶魔化作一团灰烬!",
        en_en="Congratulations, you turned the Evil into ashes!"
    )
    R_WON_3: ClassVar[I18nText] = I18nText(
        "恭喜你,成功让恶魔原地消失!",
        en_en="Congratulations, you made the Evil vanished in-place!"
    )
    E_WON: ClassVar[I18nText] = I18nText(
        "唉....你被恶魔变成了{0}",
        en_en="Sigh.... You're turned into {0} by the Evil"
    )
    END_0_1: ClassVar[I18nText] = I18nText(
        "你让恶魔面目全非,但你也付出了生命的代价",
        en_en="You made the Evil out of all recognition with your life"
    )
    END_0_2: ClassVar[I18nText] = I18nText(
        "恶魔为你化作灰烬,而你成为了{0}",
        en_en="The Evil was turned into ashes by you, who turned into {0}"
    )
    END_0_3: ClassVar[I18nText] = I18nText(
        "你作为{0}看着恶魔消失于世上",
        en_en="You as {0} saw the Evil vanish from the world"
    )
    E_WON_1: ClassVar[I18nText] = I18nText(
        "唉....你被恶魔打得体无完肤",
        en_en="Sigh.... You're injured all over the body by the Evil's hits"
    )
    END_1_0: ClassVar[I18nText] = I18nText(
        "恶魔让你面目全非,但他也付出了生命的代价",
        en_en="The Evil made you out of all recognition with its life"
    )
    END_1_1: ClassVar[I18nText] = I18nText("二人幸终……", en_en="二人幸终...")
    END_1_2: ClassVar[I18nText] = I18nText(
        "恶魔为你化作灰烬,而你也面目狼狈……",
        en_en="The Evil was turned into ashes by you, who is out of all "
              "recognition..."
    )
    END_1_3: ClassVar[I18nText] = I18nText(
        "你用残缺的身躯彻底送走了恶魔",
        en_en="You thoroughly sent the Evil away with your fragmentary body"
    )
    E_WON_2: ClassVar[I18nText] = I18nText(
        "唉....你被恶魔化作一团灰烬",
        en_en="Sigh... You're turned into ashes by the Evil"
    )
    END_2_0: ClassVar[I18nText] = I18nText(
        "你为恶魔化作灰烬,而它成为了{0}",
        en_en="You're turned into ashes by the Evil, who turned into {0}"
    )
    END_2_1: ClassVar[I18nText] = I18nText(
        "你为恶魔化作灰烬,而它也面目狼狈……",
        en_en="You're turned into ashes by the Evil, who is out of all "
              "recognition..."
    )
    END_2_2: ClassVar[I18nText] = \
    I18nText("你们化作了两团灰烬", en_en="You're turned into two ashes")
    END_2_3: ClassVar[I18nText] = I18nText("")
    E_WON_3: ClassVar[I18nText] = I18nText(
        "唉....恶魔让你人间蒸发了", en_en="Sigh... The evil let you vanished"
    )
    END_3_0: ClassVar[I18nText] = I18nText(
        "恶魔作为{0}看着你消失于世上",
        en_en="The Evil as {0} saw you vanish from the world"
    )
    END_3_1: ClassVar[I18nText] = I18nText("")
    END_3_2: ClassVar[I18nText] = I18nText("")
    END_3_3: ClassVar[I18nText] = I18nText(
        "你们俩仿佛从来没存在过一般",
        en_en="It's like you two had never existed"
    )
    GAME_COUNT_INFO: ClassVar[I18nText] = I18nText(
        "本次游戏持续了 {0} 轮,\n{1} 回合,\n{2} 周目",
        en_en="This game kept {0} turn(s),\n{1} round(s),\n{2} period(s)"
    )
