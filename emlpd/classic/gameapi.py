from random import choice, randint
from typing import Callable, Dict, List, Optional, Tuple, Union

from ..gameapi import VER, VER_STRING, GameSave

__all__ = ["VER", "VER_STRING", "Game", "GameSave"]

class Game :
    tools: Dict[int, Tuple[str, str]]
    tools_sending_weight: Dict[int, Union[int, Callable[["Game"], int]]]
    tools_sending_limit_in_game: Dict[int, int]
    tools_sending_limit_in_hand: Dict[int, Union[int, Callable[["Game"], int]]]
    r_hp: int
    e_hp: int
    r_tools: List[int]
    e_tools: List[int]
    max_tools_storing: int
    r_sending_total: Dict[int, int]
    e_sending_total: Dict[int, int]
    max_bullets: int
    min_bullets: int
    min_true_bullets: int
    min_false_bullets: int
    max_true_bullets: int
    bullets: List[bool]
    yourturn: bool
    rel_turn_lap: int

    def __init__(
        self, min_bullets: int, max_bullets: int, min_true_bullets: int,
        min_false_bullets: int, max_true_bullets: int, r_hp: int, e_hp: int,
        tools: Dict[int, Tuple[str, str]],
        tools_sending_weight: Dict[int, Union[int, Callable[["Game"], int]]],
        tools_sending_limit_in_game: Dict[int, int],
        tools_sending_limit_in_hand: Dict[int,
                                          Union[int, Callable[["Game"], int]]],
        max_tools_storing: int = 8, firsthand: bool = True
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
        :param tools_sending_limit_in_hand: 道具库中道具存在的最大数(键为道具ID,值为最大数值)。
        :param max_tools_storing: 最大道具数。
        :param firsthand: 指定谁是先手。True为“你”是先手,False为恶魔是先手。
        """

        self.min_bullets = min_bullets
        self.max_bullets = max_bullets
        self.min_true_bullets = min_true_bullets
        self.min_false_bullets = min_false_bullets
        self.max_true_bullets = max_true_bullets
        self.r_hp = r_hp
        self.e_hp = e_hp
        self.tools = tools
        self.tools_sending_weight = tools_sending_weight
        self.tools_sending_limit_in_game = tools_sending_limit_in_game
        self.tools_sending_limit_in_hand = tools_sending_limit_in_hand
        self.r_tools = []
        self.e_tools = []
        self.max_tools_storing = max_tools_storing
        self.r_sending_total = {}
        self.e_sending_total = {}
        self.yourturn = firsthand
        self.rel_turn_lap = 0

    def gen_bullets(self) -> None :
        """
        生成一个新的弹夹。
        """

        length: int = randint(self.min_bullets, self.max_bullets)
        self.bullets = [True] * length
        for _ in range(randint(max(self.min_false_bullets,
                                   length-self.max_true_bullets),
                               length-self.min_true_bullets)) :
            while 1 :
                a: int = randint(0, length-1)
                if self.bullets[a] :
                    self.bullets[a] = False
                    break

    def random_tool_to_r(self) -> int :
        """
        基于“你”当前的情况返回一个随机道具。

        :return: 随机道具的ID。
        """

        randomlist: List[int] = []
        for k, v in self.tools_sending_weight.items() :
            for _ in range(v if isinstance(v, int) else v(self)) :
                randomlist.append(k)
        while 1 :
            randomid: int = choice(randomlist)
            tool_sending_limit_in_hand: int = \
            self.tools_sending_limit_in_hand[randomid] \
            if isinstance(self.tools_sending_limit_in_hand[randomid], int) \
            else self.tools_sending_limit_in_hand[randomid](self)
            if (randomid not in self.r_sending_total or \
                self.tools_sending_limit_in_game[randomid] <= 0 or \
                self.r_sending_total[randomid] < \
                self.tools_sending_limit_in_game[randomid]) and \
               (tool_sending_limit_in_hand <= 0 or \
                self.r_tools.count(randomid) < tool_sending_limit_in_hand) :
                return randomid
        raise AssertionError

    def random_tool_to_e(self) -> int :
        """
        基于恶魔当前的情况返回一个随机道具。

        :return: 随机道具的ID。
        """

        randomlist: List[int] = []
        for k, v in self.tools_sending_weight.items() :
            for _ in range(v if isinstance(v, int) else v(self)) :
                randomlist.append(k)
        while 1 :
            randomid: int = choice(randomlist)
            tool_sending_limit_in_hand: int = \
            self.tools_sending_limit_in_hand[randomid] \
            if isinstance(self.tools_sending_limit_in_hand[randomid], int) \
            else self.tools_sending_limit_in_hand[randomid](self)
            if (randomid not in self.e_sending_total or \
                self.tools_sending_limit_in_game[randomid] <= 0 or \
                self.e_sending_total[randomid] < \
                self.tools_sending_limit_in_game[randomid]) and \
               (tool_sending_limit_in_hand <= 0 or \
                self.e_tools.count(randomid) < tool_sending_limit_in_hand) :
                return randomid
        raise AssertionError

    def send_tools_to_r(self, max_amount: int = 2) -> int :
        """
        向“你”发放随机道具。

        :return: 实际发放道具的数量。
        """

        max_amount = min(max_amount, self.max_tools_storing-len(self.r_tools))
        for _ in range(max_amount) :
            randomtool = self.random_tool_to_r()
            self.r_sending_total.setdefault(randomtool, 0)
            self.r_sending_total[randomtool] += 1
            self.r_tools.append(randomtool)
        return max_amount

    def send_tools_to_e(self, max_amount: int = 2) -> int :
        """
        向恶魔发放随机道具。

        :return: 实际发放道具的数量。
        """

        max_amount = min(max_amount, self.max_tools_storing-len(self.e_tools))
        for _ in range(max_amount) :
            randomtool = self.random_tool_to_e()
            self.e_sending_total.setdefault(randomtool, 0)
            self.e_sending_total[randomtool] += 1
            self.e_tools.append(randomtool)
        return max_amount

    def shoot(self, to_self: bool,
              shooter: Optional[bool] = None) -> Optional[bool] :
        """
        执行开枪操作。

        :param to_self: 是否对着自己开枪。
        :param shooter: 开枪者。True为“你”,False为恶魔,None(未指定)则为当前方。
        :return: 表示子弹类型(实弹或空弹)。若为None则表示弹夹内无子弹。
        """

        if shooter is None :
            shooter = self.yourturn
        if not self.bullets :
            return None
        bullet: bool = self.bullets.pop(0)
        if bullet or not to_self :
            if self.rel_turn_lap > 0 :
                self.rel_turn_lap -= 1
            elif self.rel_turn_lap < 0 :
                self.rel_turn_lap += 1
            else :
                self.yourturn = not self.yourturn
        return bullet
