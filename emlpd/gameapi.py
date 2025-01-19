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

import sys
from math import ceil
from random import choice, randint, random
import struct
from typing import Callable, ClassVar, Dict, Iterable, List, Optional, Tuple, \
                   Union, no_type_check

if sys.version_info >= (3, 13) :
    from warnings import deprecated
else :
    def deprecated(message: str) :
        return lambda o: o

__all__ = ["VER", "VER_STRING", "Slot", "ShootResult", "I18nText",
           "ShootResultAnalyzer", "Game", "GameSave", "Player"]

VER: Union[Tuple[int, int, int], Tuple[int, int, int, str, int]] = \
(0, 4, 3, "a", 1)

VER_STRING: str = \
("{0}.{1}.{2}-{3}{4}" if len(VER) > 4 else "{0}.{1}.{2}").format(*VER)

Slot = Tuple[int, Optional[int]]
ShootResult = Tuple[Optional[Tuple[bool, bool]], Optional[Tuple[bool, bool]],
                    Optional[Tuple[bool, bool]], Optional[Tuple[bool, bool]]]

class I18nText :
    selected_lang: ClassVar[str] = "zh_hans"

    defaulted: str
    translations: Dict[str, str]

    def __init__(self, defaulted: str, **translations) -> None :
        self.defaulted = defaulted
        self.translations = translations

    @property
    def string(self) -> str :
        return self.translations.get(type(self).selected_lang, self.defaulted)

    def __str__(self) -> str :
        return self.string

class ShootResultAnalyzer :
    @staticmethod
    def should_run_turn(result: ShootResult) -> bool :
        return any(x is not None and (x[0] or x[1]) for x in result)

class Player :
    controllable: bool
    hp: int
    slots: List[Slot]
    sending_total: Dict[int, int]
    tools_sending_weight: Dict[int, Union[int, Callable[["Game"], int]]]
    tools_sending_limit_in_game: Dict[int, int]
    tools_sending_limit_in_slot: Dict[int, Union[int, Callable[["Game"], int]]]
    slot_sending_weight: Dict[int, Union[int, Callable[["Game"], int]]]
    stopped_turns: int

    def __init__(
        self, controllable: bool = False, hp: int = 1,
        slots: Union[List[Slot], int] = 0,
        sending_total: Optional[Dict[int, int]] = None,
        tools_sending_weight: Optional[
            Dict[int, Union[int, Callable[["Game"], int]]]
        ] = None, tools_sending_limit_in_game: Optional[Dict[int, int]] = None,
        tools_sending_limit_in_slot: Optional[Dict[
            int, Union[int, Callable[["Game"], int]]
        ]] = None, slot_sending_weight: Optional[Dict[
            int, Union[int, Callable[["Game"], int]]
        ]] = None, stopped_turns: int = 0
    ) -> None :
        """
        :param controllable: 玩家是否用户可控制。
        :param hp: 玩家的生命值。
        :param slots: 槽位或永久空槽位数。
        :param tools_sending_weight: 道具发放相对权重(键为道具ID,值为相对权重值)。
        :param tools_sending_limit_in_game: 一局游戏道具发放的最多次数(键为道具ID,值为最多次数值)。
        :param tools_sending_limit_in_slot: 槽位中道具存在的最大数(键为道具ID,值为最大数值)。
        :param slot_sending_weight: 槽位发放相对权重(键为槽位有效期,值为相对权重值)。
        :param stopped_turns: 玩家接下来不能行动的轮数。
        """

        self.controllable = controllable
        self.hp = hp
        self.slots = \
        [(0, None)] * slots if isinstance(slots, int) else slots[:]
        self.sending_total = \
        {} if sending_total is None else sending_total.copy()
        self.tools_sending_weight = \
        {} if tools_sending_weight is None else tools_sending_weight.copy()
        self.tools_sending_limit_in_game = \
        {} if tools_sending_limit_in_game is None else \
        tools_sending_limit_in_game.copy()
        self.tools_sending_limit_in_slot = \
        {} if tools_sending_limit_in_slot is None else \
        tools_sending_limit_in_slot.copy()
        self.slot_sending_weight = \
        {} if slot_sending_weight is None else slot_sending_weight.copy()
        self.stopped_turns = stopped_turns

    @property
    def alive(self) -> bool :
        return self.hp > 0

    def can_use_tools(self, game: "Game") -> bool :
        for k, v in self.tools_sending_weight.items() :
            if (v if isinstance(v, int) else v(game)) > 0  :
                return True
        return False

    def user_operatable(self, game: "Game") -> bool :
        return self.controllable

    def count_tools(self, toolid: Optional[int]) -> int :
        """
        统计玩家有多少指定的道具或空道具槽位。

        :param toolid: 要统计的道具ID。为None时统计空道具槽位。
        :return: 玩家的指定道具或空槽位的数量。
        """

        res: int = 0
        for slot in self.slots :
            if slot[1] == toolid :
                res += 1
        return res

@no_type_check
class Game :
    players: Dict[int, Player]
    turn_orders: List[int]
    tools: Dict[int, Tuple[
        Union[str, I18nText], Optional[Union[str, I18nText]]
    ]]
    slots_sharing: Optional[Tuple[bool, int, List[Slot]]]
    max_bullets: int
    min_bullets: int
    min_true_bullets: int
    min_false_bullets: int
    max_true_bullets: int
    bullets: List[bool]
    rel_turn_lap: int # deprecated
    extra_bullets: Tuple[Optional[List[bool]], Optional[List[bool]],
                         Optional[List[bool]]]
    subgame: Optional["Game"]

    def __init__(
        self, min_bullets: int, max_bullets: int, min_true_bullets: int,
        min_false_bullets: int, max_true_bullets: int, r_hp: int, e_hp: int,
        tools: Dict[int, Tuple[
            Union[str, I18nText], Optional[Union[str, I18nText]]
        ]],
        tools_sending_weight: Dict[int, Union[int, Callable[["Game"], int]]],
        tools_sending_limit_in_game: Dict[int, int],
        tools_sending_limit_in_slot: Dict[int,
                                          Union[int, Callable[["Game"], int]]],
        permanent_slots: int, firsthand: bool,
        slot_sending_weight: Optional[Dict[int, Union[int, Callable[["Game"],
                                                                    int]]]] = \
        None
    ) -> None :
        """
        :param min_bullets: 一回合最少发放的子弹数。
        :param max_bullets: 一回合最多发放的子弹数。
        :param min_true_bullets: 一回合最少发放的实弹数。
        :param min_false_bullets: 一回合最少发放的空弹数。
        :param max_true_bullets: 一回合最多发放的实弹数。
        :param r_hp: 你的生命值。
        :param e_hp: 恶魔的生命值。
        :param tools: 道具(键为道具ID,值为道具名称和描述)。
        :param tools_sending_weight: 道具发放相对权重(键为道具ID,值为相对权重值)。
        :param tools_sending_limit_in_game: 一局游戏道具发放的最多次数(键为道具ID,值为最多次数值)。
        :param tools_sending_limit_in_slot: 槽位中道具存在的最大数(键为道具ID,值为最大数值)。
        :param permanent_slots: 永久槽位数。
        :param firsthand: 指定谁是先手。True为“你”是先手,False为恶魔是先手。
        :param slot_sending_weight: 槽位发放相对权重(键为槽位有效期,值为相对权重值)。
        """

        self.players = {
            0: Player(
                True,
                r_hp,
                permanent_slots,
                None,
                tools_sending_weight,
                tools_sending_limit_in_game,
                tools_sending_limit_in_slot,
                {1: 5, 2: 6, 3: 6, 4: 2, 5: 1} if slot_sending_weight is None \
                else slot_sending_weight
            ),
            1: Player(
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
        }
        self.min_bullets = min_bullets
        self.max_bullets = max_bullets
        self.min_true_bullets = min_true_bullets
        self.min_false_bullets = min_false_bullets
        self.max_true_bullets = max_true_bullets
        self.tools = tools
        self.slots_sharing = None
        self.turn_orders = [0, 1] if firsthand else [1, 0]
        self.rel_turn_lap = 0
        self.extra_bullets = (None, None, None)
        self.subgame = None

    @property
    def r_hp(self) -> int :
        return self.players[0].hp
    @r_hp.setter
    def r_hp(self, value: int) -> None :
        self.players[0].hp = value

    @property
    def e_hp(self) -> int :
        return self.players[1].hp
    @e_hp.setter
    def e_hp(self, value: int) -> None :
        self.players[1].hp = value

    @property
    def r_slots(self) -> List[Slot] :
        return self.players[0].slots
    @r_slots.setter
    def r_slots(self, value: List[Slot]) -> None :
        self.players[0].slots = value

    @property
    def e_slots(self) -> List[Slot] :
        return self.players[1].slots
    @e_slots.setter
    def e_slots(self, value: List[Slot]) -> None :
        self.players[1].slots = value

    @property
    def r_sending_total(self) -> Dict[int, int] :
        return self.players[0].sending_total
    @r_sending_total.setter
    def r_sending_total(self, value: Dict[int, int]) -> None :
        self.players[0].sending_total = value

    @property
    def e_sending_total(self) -> Dict[int, int] :
        return self.players[1].sending_total
    @e_sending_total.setter
    def e_sending_total(self, value: Dict[int, int]) -> None :
        self.players[1].sending_total = value

    @property
    def yourturn(self) -> bool :
        return not self.turn_orders[0]
    @yourturn.setter
    def yourturn(self, value: object) -> None :
        if self.turn_orders[0] :
            if value :
                self.turn_orders.remove(0)
                self.turn_orders.insert(0, 0)
        elif not value :
            self.turn_orders.remove(0)
            self.turn_orders.append(0)

    @property
    @deprecated(
        "将在 0.5.0-a1 移除。请使用 self.players[...].tools_sending_weight。"
    )
    def tools_sending_weight(self) -> Dict[
        int, Union[int, Callable[["Game"], int]]
    ] :
        """
        已弃用,将在 0.5.0-a1 移除。请使用 self.players[...].tools_sending_weight。
        """

        return self.players[self.turn_orders[0]].tools_sending_weight
    @tools_sending_weight.setter
    @deprecated("将在 0.5.0-a1 移除。"
                "请使用 self.players[...].tools_sending_weight = value。")
    def tools_sending_weight(self, value: Dict[
        int, Union[int, Callable[["Game"], int]]
    ]) -> None :
        """
        已弃用,将在 0.5.0-a1 移除。请使用 self.players[...].tools_sending_weight = value。
        """

        self.players[self.turn_orders[0]].tools_sending_weight = value

    @property
    @deprecated("将在 0.5.0-a1 移除。"
                "请使用 self.players[...].tools_sending_limit_in_game。")
    def tools_sending_limit_in_game(self) -> Dict[int, int] :
        """
        已弃用,将在 0.5.0-a1 移除。请使用 self.players[...].tools_sending_limit_in_game。
        """

        return self.players[self.turn_orders[0]].tools_sending_limit_in_game
    @tools_sending_limit_in_game.setter
    @deprecated(
        "将在 0.5.0-a1 移除。"
        "请使用 self.players[...].tools_sending_limit_in_game = value。"
    )
    def tools_sending_limit_in_game(self, value: Dict[int, int]) -> None :
        """
        已弃用,将在 0.5.0-a1 移除。请使用 self.players[...].tools_sending_limit_in_game = value。
        """

        self.players[self.turn_orders[0]].tools_sending_limit_in_game = value

    @property
    @deprecated("将在 0.5.0-a1 移除。"
                "请使用 self.players[...].tools_sending_limit_in_slot。")
    def tools_sending_limit_in_slot(self) -> Dict[
        int, Union[int, Callable[["Game"], int]]
    ] :
        """
        已弃用,将在 0.5.0-a1 移除。请使用 self.players[...].tools_sending_limit_in_slot。
        """

        return self.players[self.turn_orders[0]].tools_sending_limit_in_slot
    @tools_sending_limit_in_slot.setter
    @deprecated(
        "将在 0.5.0-a1 移除。"
        "请使用 self.players[...].tools_sending_limit_in_slot = value。"
    )
    def tools_sending_limit_in_slot(self, value: Dict[
        int, Union[int, Callable[["Game"], int]]
    ]) -> None :
        """
        已弃用,将在 0.5.0-a1 移除。请使用 self.players[...].tools_sending_limit_in_slot = value。
        """

        self.players[self.turn_orders[0]].tools_sending_limit_in_slot = value

    @property
    @deprecated(
        "将在 0.5.0-a1 移除。请使用 self.players[...].slot_sending_weight。"
    )
    def slot_sending_weight(self) -> Dict[
        int, Union[int, Callable[["Game"], int]]
    ] :
        """
        已弃用,将在 0.5.0-a1 移除。请使用 self.players[...].slot_sending_weight。
        """

        return self.players[self.turn_orders[0]].slot_sending_weight
    @slot_sending_weight.setter
    @deprecated("已弃用,将在 0.5.0-a1 移除。"
                "请使用 self.players[...].slot_sending_weight = value。")
    def slot_sending_weight(self, value: Dict[
        int, Union[int, Callable[["Game"], int]]
    ]) -> None :
        """
        已弃用,将在 0.5.0-a1 移除。请使用 self.players[...].slot_sending_weight = value。
        """

        self.players[self.turn_orders[0]].slot_sending_weight = value

    def gen_bullets(self, bullets_id: Optional[int] = None) -> \
        Optional[List[bool]] :
        """
        生成一个新的弹夹。

        :return: 若bullets_id不为None,则为弹夹引用,否则为None。
        """

        if bullets_id is None :
            self.gen_bullets(0)
            if self.extra_bullets[0] is not None :
                self.gen_bullets(1)
            if self.extra_bullets[1] is not None :
                self.gen_bullets(2)
            if self.extra_bullets[2] is not None :
                self.gen_bullets(3)
            return None
        length: int = randint(self.min_bullets, self.max_bullets)
        bullets_ref: List[bool] = []
        if bullets_id == 0 :
            self.bullets = [True] * length
            bullets_ref = self.bullets
        elif bullets_id == 1 :
            self.extra_bullets = ([True] * length, self.extra_bullets[1],
                                  self.extra_bullets[2])
            bullets_ref = self.extra_bullets[0]
        elif bullets_id == 2 :
            self.extra_bullets = (self.extra_bullets[0], [True] * length,
                                  self.extra_bullets[2])
            bullets_ref = self.extra_bullets[1]
        elif bullets_id == 3 :
            self.extra_bullets = (self.extra_bullets[0], self.extra_bullets[1],
                                  [True] * length)
            bullets_ref = self.extra_bullets[2]
        for _ in range(randint(max(self.min_false_bullets,
                                   length-self.max_true_bullets),
                               length-self.min_true_bullets)) :
            while 1 :
                a: int = randint(0, length-1)
                if bullets_ref[a] :
                    bullets_ref[a] = False
                    break
        if bullets_id not in (0, 1, 2, 3) :
            return None
        return bullets_ref

    def has_tools(self, toolid: Optional[int] = None,
                  player: Optional[Player] = None) -> bool :
        """
        指示该游戏是否有任何道具。

        :return: 一个bool值,若有道具则为True。
        """

        if player is None :
            for i in self.players.values() :
                for k, v in i.tools_sending_weight.items() :
                    if (v if isinstance(v, int) else v(self)) > 0 and \
                       (toolid is None or toolid == k) :
                        return True
        else :
            for k, v in player.tools_sending_weight.items() :
                if (v if isinstance(v, int) else v(self)) > 0 and \
                   (toolid is None or toolid == k) :
                    return True
        return False

    def count_tools_of_r(self, toolid: Optional[int]) -> int :
        """
        统计“你”有多少指定的道具或空道具槽位。

        :param toolid: 要统计的道具ID。为None时统计空道具槽位。
        :return: “你”的指定道具或空槽位的数量。
        """

        return self.players[0].count_tools(toolid)

    def count_tools_of_e(self, toolid: Optional[int]) -> int :
        """
        统计恶魔有多少指定的道具或空道具槽位。

        :param toolid: 要统计的道具ID。为None时统计空道具槽位。
        :return: 恶魔的指定道具或空槽位的数量。
        """

        return self.players[1].count_tools(toolid)

    def random_tool_to_player(self, player: Player) -> int :
        """
        基于玩家当前的情况返回一个随机道具。

        :param player: 目标玩家。
        :return: 随机道具的ID。
        """

        randomlist: List[int] = []
        for k, v in player.tools_sending_weight.items() :
            for _ in range(v if isinstance(v, int) else v(self)) :
                randomlist.append(k)
        while 1 :
            randomid: int = choice(randomlist)
            tool_sending_limit_in_slot: int = \
            player.tools_sending_limit_in_slot[randomid] if \
            isinstance(
                player.tools_sending_limit_in_slot[randomid], int
            ) else player.tools_sending_limit_in_slot[randomid](self)
            if (randomid not in player.sending_total or
                player.tools_sending_limit_in_game[randomid] <= 0 or
                player.sending_total[randomid] <
                player.tools_sending_limit_in_game[randomid]) and \
               (tool_sending_limit_in_slot <= 0 or
                player.count_tools(randomid) < tool_sending_limit_in_slot) :
                return randomid
        raise AssertionError

    def random_tool_to_r(self) -> int :
        """
        基于“你”当前的情况返回一个随机道具。

        :return: 随机道具的ID。
        """

        return self.random_tool_to_player(self.players[0])

    def random_tool_to_e(self) -> int :
        """
        基于恶魔当前的情况返回一个随机道具。

        :return: 随机道具的ID。
        """

        return self.random_tool_to_player(self.players[1])

    def send_tools(self, player: Player, max_amount: int = 2) -> int :
        """
        向玩家发放随机道具。

        :param player: 目标玩家。
        :return: 实际发放道具的数量。
        """

        counting_empty_slots_index: List[int] = []
        for slot_id in range(len(player.slots)) :
            if player.slots[slot_id][1] is None :
                counting_empty_slots_index.append(slot_id)
        if counting_empty_slots_index :
            randomtool: int
            if len(counting_empty_slots_index) == 1 :
                if randint(0, 3) :
                    randomtool = self.random_tool_to_player(player)
                    player.sending_total.setdefault(randomtool, 0)
                    player.sending_total[randomtool] += 1
                    player.slots[counting_empty_slots_index[0]] = \
                    (player.slots[counting_empty_slots_index[0]][0],
                     randomtool)
                    return 1
                return 0
            else :
                r: int = min(max_amount-(not randint(0, 4)),
                             len(counting_empty_slots_index))
                for i in range(r) :
                    randomtool = self.random_tool_to_player(player)
                    player.sending_total.setdefault(randomtool, 0)
                    player.sending_total[randomtool] += 1
                    player.slots[counting_empty_slots_index[i]] = \
                    (player.slots[counting_empty_slots_index[i]][0],
                     randomtool)
                return r
        return 0

    def send_tools_to_r(self, max_amount: int = 2) -> int :
        """
        向“你”发放随机道具。

        :return: 实际发放道具的数量。
        """

        return self.send_tools(self.players[0], max_amount)

    def send_tools_to_e(self, max_amount: int = 2) -> int :
        """
        向恶魔发放随机道具。

        :return: 实际发放道具的数量。
        """

        return self.send_tools(self.players[1], max_amount)

    def run_turn(self) -> None :
        """
        运行一轮。
        """

        self.turn_orders.append(self.turn_orders[0])
        del self.turn_orders[0]
        while self.players[self.turn_orders[0]].stopped_turns > 0 :
            self.players[self.turn_orders[0]].stopped_turns -= 1
            self.turn_orders.append(self.turn_orders[0])
            del self.turn_orders[0]

    def shoot(self, to_self: bool, shooter: Optional[bool] = None,
              explosion_probability: Union[float,
                                           Callable[["Game"], float]] = 0.05,
              bullets_id: Optional[int] = None, run_turn: bool = True) -> \
        ShootResult :
        """
        执行开枪操作。

        :param to_self: 是否对着自己开枪。
        :param shooter: 开枪者。True为“你”,False为恶魔,None(未指定)则为当前方。
        :param explosion_probability: 炸膛概率。未指定则为0.05。
        :param bullets_id: 枪筒ID。未指定则为所有枪筒。
        :param run_turn: 是否运行轮。
        :return: 表示子弹类型(实弹或空弹)及是否炸膛。若为None则表示弹夹内无子弹。
        """

        if bullets_id is None :
            SHOOT_RESULT: ShootResult = (
                self.shoot(to_self, shooter, explosion_probability,0,False)[0],
                self.shoot(to_self, shooter, explosion_probability,1,False)[1],
                self.shoot(to_self, shooter, explosion_probability,2,False)[2],
                self.shoot(to_self, shooter, explosion_probability,3,False)[3]
            )
            if run_turn and ShootResultAnalyzer.should_run_turn(SHOOT_RESULT) :
                self.run_turn()
            return SHOOT_RESULT
        if shooter is None :
            shooter = self.yourturn
        bullets_ref: Optional[List[bool]] = self.bullets
        if bullets_id == 1 :
            bullets_ref = self.extra_bullets[0]
        elif bullets_id == 2 :
            bullets_ref = self.extra_bullets[1]
        elif bullets_id == 3 :
            bullets_ref = self.extra_bullets[2]
        if bullets_ref is None or not bullets_ref :
            return (None, None, None, None)
        exploded: bool = random() < (
            explosion_probability if isinstance(explosion_probability, float)
            else explosion_probability(self)
        )
        bullet: bool = bullets_ref.pop(0)
        if run_turn and (exploded or bullet or not to_self) :
            self.run_turn()
        if bullets_id == 1 :
            return (None, (bullet, exploded), None, None)
        if bullets_id == 2 :
            return (None, None, (bullet, exploded), None)
        if bullets_id == 3 :
            return (None, None, None, (bullet, exploded))
        return ((bullet, exploded), None, None, None)

    def shoots(self, to_self: bool, shooter: Optional[bool] = None,
               explosion_probability: Union[float,
                                            Callable[["Game"], float]] = 0.05,
               combo: int = 1, bullets_id: Optional[int] = None,
               run_turn: bool = True) -> List[ShootResult] :
        """
        执行开枪操作。

        :param to_self: 是否对着自己开枪。
        :param shooter: 开枪者。True为“你”,False为恶魔,None(未指定)则为当前方。
        :param explosion_probability: 炸膛概率。未指定则为0.05。
        :param combo: 一次要发出多少子弹。未指定则为1。
        :param bullets_id: 枪筒ID。未指定则为所有枪筒。
        :param run_turn: 是否运行轮。
        :return: 一个列表,每项表示子弹类型(实弹或空弹)及是否炸膛。若为None则表示此时弹夹内无子弹。
        """

        RES: List[ShootResult] = []
        for _ in range(combo) :
            RES.append(self.shoot(to_self, shooter, explosion_probability,
                                  bullets_id, False))
        if run_turn and (any(ShootResultAnalyzer.should_run_turn(x)
                             for x in RES) or not to_self) :
            self.run_turn()
        return RES

    def send_slot(self, player: Player, sent_probability: float = 0.25,
                  sent_weight: Optional[Dict[int, Union[int, Callable[
                      ["Game"], int
                  ]]]] = None) -> Optional[int] :
        """
        向玩家送出一个槽位。

        :param player: 目标玩家。
        :param sent_probability: 送出的概率。
        :param sent_weight: 送出槽位时长权重。键为时长,值为权重值。
        :return: 送出槽位的时长。若未送出则返回None。
        """

        if sent_weight is None :
            return self.send_slot(
                player, sent_probability, player.slot_sending_weight
            )
        if random() >= sent_probability :
            return None
        randomlist: List[int] = []
        for k, v in sent_weight.items() :
            for _ in range(v if isinstance(v, int) else v(self)) :
                randomlist.append(k)
        if not randomlist :
            return None
        duration: int = choice(randomlist)
        self.r_slots.append((duration, None))
        return duration

    def send_r_slot(self, sent_probability: float = 0.25,
                    sent_weight: Optional[Dict[int, Union[int, Callable[
                        ["Game"], int
                    ]]]] = None) -> Optional[int] :
        """
        向“你”送出一个槽位。

        :param sent_probability: 送出的概率。
        :param sent_weight: 送出槽位时长权重。键为时长,值为权重值。
        :return: 送出槽位的时长。若未送出则返回None。
        """

        return self.send_slot(self.players[0], sent_probability, sent_weight)

    def send_e_slot(self, sent_probability: float = 0.25,
                    sent_weight: Optional[Dict[int, Union[int, Callable[
                        ["Game"], int
                    ]]]] = None) -> Optional[int] :
        """
        向恶魔送出一个槽位。

        :param sent_probability: 送出的概率。
        :param sent_weight: 送出槽位时长权重。键为时长,值为权重值。
        :return: 送出槽位的时长。若未送出则返回None。
        """

        return self.send_slot(self.players[1], sent_probability, sent_weight)

    def expire_slots(self, player) -> List[Optional[int]] :
        RES: List[Optional[int]] = []
        slot_index: int = 0
        while slot_index < len(player.slots) :
            if player.slots[slot_index][0] <= 0 :
                slot_index += 1
                continue
            if player.slots[slot_index][0] > 1 :
                player.slots[slot_index] = (player.slots[slot_index][0] - 1,
                                            player.slots[slot_index][1])
                slot_index += 1
                continue
            RES.append(player.slots.pop(slot_index)[1])
        return RES

    def expire_r_slots(self) -> List[Optional[int]] :
        """
        使“你”的临时槽位过期。

        :return: 列表,包含过期的槽位的道具ID。
        """

        return self.expire_slots(self.players[0])

    def expire_e_slots(self) -> List[Optional[int]] :
        """
        使恶魔的临时槽位过期。

        :return: 列表,包含过期的槽位的道具ID。
        """

        return self.expire_slots(self.players[1])

    def copy_bullets_for_new(self) -> int :
        if self.extra_bullets == (None, None, None) :
            self.extra_bullets = (self.bullets[:], None, None)
            return 1
        if self.extra_bullets[0] is not None and self.extra_bullets[1] is None\
           and self.extra_bullets[2] is None :
            self.extra_bullets = (self.extra_bullets[0], self.bullets[:],
                                  self.extra_bullets[0][:])
            return 2
        return 0

    @property
    def debug_message(self) -> Iterable[Tuple[
        Iterable[object], Optional[str], Optional[str]
    ]] :
        return ()

    @property
    def round_start_message(self) -> Iterable[Tuple[
        Iterable[object], Optional[str], Optional[str]
    ]] :
        return ()

def read_256byte_int_from_bytes(src: bytes, digits: Optional[int] = None,
                                signed: bool = False, offset: int = 0) -> int :
    if digits is None :
        digits = src[offset]
        offset += 1
    return int.from_bytes(src[offset:offset+digits], "big", signed=signed)

def int_to_256byte(src: int, digits: Optional[int] = None,
                   signed: bool = False) -> bytes :
    if digits is None :
        res: bytes = \
        src.to_bytes(ceil(src.bit_length()/8.), "big", signed=signed)
        return bytes((len(res),)) + res
    return src.to_bytes(digits, "big", signed=signed)

class GameSave :
    level: int
    exp: int
    coins: int
    success_selfshoot_trues: int
    success_selfshoot_falses: int
    exploded_selfshoot_trues: int
    exploded_selfshoot_falses: int
    success_againstshoot_trues: int
    success_againstshoot_falses: int
    exploded_againstshoot_trues: int
    exploded_againstshoot_falses: int
    damage_caused_to_e: int
    damage_caused_to_r: int
    damage_caught: int
    healed: int
    bullets_caught: int
    play_turns: int
    play_rounds: int
    play_periods: int
    game_runs: int
    active_gametime: float

    def __init__(self, level: int = 0, exp: int = 0, coins: int = 0,
                 success_selfshoot_trues: int = 0,
                 success_selfshoot_falses: int = 0,
                 exploded_selfshoot_trues: int = 0,
                 exploded_selfshoot_falses: int = 0,
                 success_againstshoot_trues: int = 0,
                 success_againstshoot_falses: int = 0,
                 exploded_againstshoot_trues: int = 0,
                 exploded_againstshoot_falses: int = 0,
                 damage_caused_to_e: int = 0, damage_caused_to_r: int = 0,
                 damage_caught: int = 0, healed: int = 0,
                 bullets_caught: int = 0, play_turns: int = 0,
                 play_rounds: int = 0, play_periods: int = 0,
                 game_runs: int = 0, active_gametime: float = 0.) -> None :
        """
        :param level: 等级。
        :param exp: 经验。
        :param coins: 金币数。
        """

        if level < 0 :
            raise ValueError
        self.level = level
        if exp < 0 or exp >= 250 * (level+1) :
            raise ValueError
        self.exp = exp
        if coins < 0 or coins > 65535 :
            raise ValueError
        self.coins = coins
        if success_selfshoot_trues < 0 :
            raise ValueError
        self.success_selfshoot_trues = success_selfshoot_trues
        if success_selfshoot_falses < 0 :
            raise ValueError
        self.success_selfshoot_falses = success_selfshoot_falses
        if exploded_selfshoot_trues < 0 :
            raise ValueError
        self.exploded_selfshoot_trues = exploded_selfshoot_trues
        if exploded_selfshoot_falses < 0 :
            raise ValueError
        self.exploded_selfshoot_falses = exploded_selfshoot_falses
        if success_againstshoot_trues < 0 :
            raise ValueError
        self.success_againstshoot_trues = success_againstshoot_trues
        if success_againstshoot_falses < 0 :
            raise ValueError
        self.success_againstshoot_falses = success_againstshoot_falses
        if exploded_againstshoot_trues < 0 :
            raise ValueError
        self.exploded_againstshoot_trues = exploded_againstshoot_trues
        if exploded_againstshoot_falses < 0 :
            raise ValueError
        self.exploded_againstshoot_falses = exploded_againstshoot_falses
        if damage_caused_to_e < 0 :
            raise ValueError
        self.damage_caused_to_e = damage_caused_to_e
        if damage_caused_to_r < 0 :
            raise ValueError
        self.damage_caused_to_r = damage_caused_to_r
        if damage_caught < 0 :
            raise ValueError
        self.damage_caught = damage_caught
        if healed < 0 :
            raise ValueError
        self.healed = healed
        if bullets_caught < 0 :
            raise ValueError
        self.bullets_caught = bullets_caught
        if play_turns < 0 :
            raise ValueError
        self.play_turns = play_turns
        if play_rounds < 0 :
            raise ValueError
        self.play_rounds = play_rounds
        if play_periods < 0 :
            raise ValueError
        self.play_periods = play_periods
        if game_runs < 0 :
            raise ValueError
        self.game_runs = game_runs
        if active_gametime < 0 :
            raise ValueError
        self.active_gametime = active_gametime

    @classmethod
    def unserialize(cls, src: bytes) :
        """
        从字节源反序列化创建一个GameSave。

        :param src: 字节源。
        :return: 创建的GameSave。
        """

        offset: int = 0
        level: int = read_256byte_int_from_bytes(src, offset=offset)
        exp_digits: int = src[offset] + 1
        offset += src[offset] + 1
        exp: int = read_256byte_int_from_bytes(src, exp_digits, offset=offset)
        offset += exp_digits
        coins: int = read_256byte_int_from_bytes(src, 2, offset=offset)
        offset += 2
        success_selfshoot_trues: int = \
        read_256byte_int_from_bytes(src, offset=offset)
        offset += src[offset] + 1
        success_selfshoot_falses: int = \
        read_256byte_int_from_bytes(src, offset=offset)
        offset += src[offset] + 1
        exploded_selfshoot_trues: int = \
        read_256byte_int_from_bytes(src, offset=offset)
        offset += src[offset] + 1
        exploded_selfshoot_falses: int = \
        read_256byte_int_from_bytes(src, offset=offset)
        offset += src[offset] + 1
        success_againstshoot_trues: int = \
        read_256byte_int_from_bytes(src, offset=offset)
        offset += src[offset] + 1
        success_againstshoot_falses: int = \
        read_256byte_int_from_bytes(src, offset=offset)
        offset += src[offset] + 1
        exploded_againstshoot_trues: int = \
        read_256byte_int_from_bytes(src, offset=offset)
        offset += src[offset] + 1
        exploded_againstshoot_falses: int = \
        read_256byte_int_from_bytes(src, offset=offset)
        offset += src[offset] + 1
        damage_caused_to_e: int = \
        read_256byte_int_from_bytes(src, offset=offset)
        offset += src[offset] + 1
        damage_caused_to_r: int = \
        read_256byte_int_from_bytes(src, offset=offset)
        offset += src[offset] + 1
        damage_caught: int = read_256byte_int_from_bytes(src, offset=offset)
        offset += src[offset] + 1
        healed: int = read_256byte_int_from_bytes(src, offset=offset)
        offset += src[offset] + 1
        bullets_caught: int = read_256byte_int_from_bytes(src, offset=offset)
        offset += src[offset] + 1
        play_turns: int = read_256byte_int_from_bytes(src, offset=offset)
        offset += src[offset] + 1
        play_rounds: int = read_256byte_int_from_bytes(src, offset=offset)
        offset += src[offset] + 1
        play_periods: int = read_256byte_int_from_bytes(src, offset=offset)
        offset += src[offset] + 1
        game_runs: int = read_256byte_int_from_bytes(src, offset=offset)
        offset += src[offset] + 1
        active_gametime: float = struct.unpack(">d", src[offset:offset+8])[0]
        return cls(level, exp, coins, success_selfshoot_trues,
                   success_selfshoot_falses, exploded_selfshoot_trues,
                   exploded_selfshoot_falses, success_againstshoot_trues,
                   success_againstshoot_falses, exploded_againstshoot_trues,
                   exploded_againstshoot_falses, damage_caused_to_e,
                   damage_caused_to_r, damage_caught, healed, bullets_caught,
                   play_turns, play_rounds, play_periods, game_runs,
                   active_gametime)

    def serialize(self) -> bytes :
        """
        序列化并返回字节源。
        """

        eles: List[bytes] = []
        eles.append(int_to_256byte(self.level))
        eles.append(int_to_256byte(self.exp, len(eles[-1])))
        eles.append(int_to_256byte(self.coins, 2))
        eles.append(int_to_256byte(self.success_selfshoot_trues))
        eles.append(int_to_256byte(self.success_selfshoot_falses))
        eles.append(int_to_256byte(self.exploded_selfshoot_trues))
        eles.append(int_to_256byte(self.exploded_selfshoot_falses))
        eles.append(int_to_256byte(self.success_againstshoot_trues))
        eles.append(int_to_256byte(self.success_againstshoot_falses))
        eles.append(int_to_256byte(self.exploded_againstshoot_trues))
        eles.append(int_to_256byte(self.exploded_againstshoot_falses))
        eles.append(int_to_256byte(self.damage_caused_to_e))
        eles.append(int_to_256byte(self.damage_caused_to_r))
        eles.append(int_to_256byte(self.damage_caught))
        eles.append(int_to_256byte(self.healed))
        eles.append(int_to_256byte(self.bullets_caught))
        eles.append(int_to_256byte(self.play_turns))
        eles.append(int_to_256byte(self.play_rounds))
        eles.append(int_to_256byte(self.play_periods))
        eles.append(int_to_256byte(self.game_runs))
        eles.append(struct.pack(">d", self.active_gametime))
        return b"".join(eles)

    def add_exp(self, add: int = 1) -> int :
        if add < 0 :
            raise ValueError
        res: int = 0
        level: int = self.level
        exp: int = self.exp
        exp += add
        while exp >= 250 * (level+1) :
            level += 1
            exp -= 250 * level
            res += 1
        self.level = level
        self.exp = exp
        return res

    def add_coins(self, add: int = 1) -> int :
        coins: int = self.coins + add
        if coins > 65535 :
            coins = 65535
        elif coins < 0 :
            coins = 0
        res: int = coins - self.coins
        self.coins = coins
        return res
