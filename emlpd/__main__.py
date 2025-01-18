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

from datetime import date
from fractions import Fraction
from math import ceil
from random import choice, randint, random, shuffle
from sys import argv
from time import sleep, time
from typing import Dict, Iterator, List, Optional, TYPE_CHECKING, Tuple

from .gameapi import Game, GameSave, Player, ShootResult, Slot, VER_STRING
from .gameinst import GAMEMODE_SET, NormalGame, NormalPlayer, StageGame

print("""emlpd  Copyright (C) 2024-2025  REGE
This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
This is free software, and you are welcome to redistribute it
under certain conditions; type `show c' for details.""")

gamesave: GameSave = GameSave()
gamemode_i: int = 1

print("恶魔轮盘赌（重构版） v"+VER_STRING)
debug: bool = "debug" in argv[1:]
nightmare: bool = "nightmare" in argv[1:]
skipthread: bool = "skipthread" in argv[1:]
cat_girl: str = chr(
    32848+3365*(-1)**((date.today().month<<5)|date.today().day!=129)
) + chr(29888+6824*(-1)**((date.today().month<<5)|date.today().day!=129)+
        ((date.today().month<<5)|date.today().day==129))

try :
    with open("emlpd.dat", "rb") as gamesave_file :
        gamesave = GameSave.unserialize(gamesave_file.read())
except FileNotFoundError :
    pass
except Exception as err :
    if debug :
        print(repr(err))
    input("读取存档遇到问题。按下回车创建一个新的存档。")

if nightmare :
    print("警告:梦魇模式已激活。恶魔会变得无比强大!!!")
print("“哦!看看,又一个来送死的”")
if not skipthread :
    sleep(2.5)
print("“希望你能让我玩的尽兴”")
if not skipthread :
    sleep(2.5)
print("“现在开始我们的游戏吧”")
if not skipthread :
    sleep(1.5)

print("当前等级:", gamesave.level)
print("当前经验:", gamesave.exp, "/", 250*(gamesave.level+1))
print("当前金币数:", gamesave.coins, "/ 65535")
if not skipthread :
    sleep(2)

print("输入“stat”以查看统计信息。")
for k, v in GAMEMODE_SET.items() :
    if len(v) > 4 :
        print("游戏模式", k, ":", v[3])
        if v[4] is None :
            print("没有介绍")
        else :
            print("介绍:", v[4])
    else :
        print("游戏模式", k)
        print("没有名字")

while 1 :
    gamemode: str = input("选择游戏模式请输入对应的编号:")
    try :
        gamemode_i = int(gamemode)
    except ValueError :
        if gamemode.strip() == "stat" :
            for k, v in gamesave.__dict__.items() :
                print(k, v, sep=": ")
        elif gamemode.strip() == "show w" :
            print("""\
THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY
APPLICABLE LAW.  EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT
HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY
OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO,
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE.  THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM
IS WITH YOU.  SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF
ALL NECESSARY SERVICING, REPAIR OR CORRECTION.""")
        elif gamemode.strip() == "show c" :
            print("""\
  The licenses for most software and other practical works are designed
to take away your freedom to share and change the works.  By contrast,
the GNU General Public License is intended to guarantee your freedom to
share and change all versions of a program--to make sure it remains free
software for all its users.  We, the Free Software Foundation, use the
GNU General Public License for most of our software; it applies also to
any other work released this way by its authors.  You can apply it to
your programs, too.

  When we speak of free software, we are referring to freedom, not
price.  Our General Public Licenses are designed to make sure that you
have the freedom to distribute copies of free software (and charge for
them if you wish), that you receive source code or can get it if you
want it, that you can change the software or use pieces of it in new
free programs, and that you know you can do these things.

  To protect your rights, we need to prevent others from denying you
these rights or asking you to surrender the rights.  Therefore, you have
certain responsibilities if you distribute copies of the software, or if
you modify it: responsibilities to respect the freedom of others.

  For example, if you distribute copies of such a program, whether
gratis or for a fee, you must pass on to the recipients the same
freedoms that you received.  You must make sure that they, too, receive
or can get the source code.  And you must show them these terms so they
know their rights.

  Developers that use the GNU GPL protect your rights with two steps:
(1) assert copyright on the software, and (2) offer you this License
giving you legal permission to copy, distribute and/or modify it.

  For the developers' and authors' protection, the GPL clearly explains
that there is no warranty for this free software.  For both users' and
authors' sake, the GPL requires that modified versions be marked as
changed, so that their problems will not be attributed erroneously to
authors of previous versions.

  Some devices are designed to deny users access to install or run
modified versions of the software inside them, although the manufacturer
can do so.  This is fundamentally incompatible with the aim of
protecting users' freedom to change the software.  The systematic
pattern of such abuse occurs in the area of products for individuals to
use, which is precisely where it is most unacceptable.  Therefore, we
have designed this version of the GPL to prohibit the practice for those
products.  If such problems arise substantially in other domains, we
stand ready to extend this provision to those domains in future versions
of the GPL, as needed to protect the freedom of users.

  Finally, every program is threatened constantly by software patents.
States should not allow patents to restrict development and use of
software on general-purpose computers, but in those that do, we wish to
avoid the special danger that patents applied to a free program could
make it effectively proprietary.  To prevent this, the GPL assures that
patents cannot be used to render the program non-free.""")
    else :
        if gamemode_i in GAMEMODE_SET :
            break

IDENTITIES: Dict[int, Tuple[str, str, int]] = {
    1: ("工人", "加2血/25%免伤/去掉小刀", 0),
    2: ("老兵", "加1攻/回血概率up10%/对面加攻", 0),
    3: ("狙击手", "", 0),
    4: ("圣女", "", 20)
}

chosen_games: Iterator[Game] = iter(GAMEMODE_SET[gamemode_i][0])
base_attack: int = 1

bullets_upgrade: int = 0

true_on_r: bool = False
true_on_e: bool = False

parent_game: Game = next(chosen_games)
sub_game: Optional[Game] = parent_game.subgame
chosen_game: Game = parent_game if sub_game is None else sub_game

round_turn_count: int = 0
period_turn_count: int = 0
total_turn_count: int = 0
period_round_count: int = 0
total_round_count: int = 0
total_period_count: int = 1
player: Player
victim: Player
slotid: int
slot: Slot

while 1 :
    gametime_time_start: float = time()
    if chosen_game.r_hp <= 0 or chosen_game.e_hp <= 0 :
        if chosen_game is sub_game :
            if isinstance(sub_game, StageGame) :
                if sub_game.players[1].controllable :
                    if not sub_game.players[0].alive :
                        print("恭喜玩家 1 赢得了擂台战!")
                        parent_game.players[1].hp += sub_game.tot_hp
                    elif not sub_game.players[1].alive :
                        print("恭喜玩家 0 赢得了擂台战!")
                        parent_game.players[0].hp += sub_game.tot_hp
                elif not sub_game.players[0].alive :
                    print("很遗憾,恶魔赢得了擂台战")
                    parent_game.e_hp += sub_game.tot_hp
                elif not sub_game.players[1].alive :
                    print("恭喜你,你赢得了擂台战!")
                    parent_game.r_hp += sub_game.tot_hp
            parent_game.subgame = None
            chosen_game = parent_game
        else :
            try :
                if chosen_game.e_hp <= 0 :
                    if nightmare :
                        gamesave.add_exp(ceil(10*(2-chosen_game.e_hp)*\
                                              GAMEMODE_SET[gamemode_i][2]))
                    elif not debug :
                        gamesave.add_exp(10*(2-chosen_game.e_hp))
                    if not debug :
                        gamesave.add_coins()
                parent_game = next(chosen_games)
                sub_game = parent_game.subgame
                chosen_game = parent_game if sub_game is None else sub_game
                try :
                    with open("emlpd.dat", "wb") as gamesave_file :
                        gamesave_file.write(gamesave.serialize())
                except OSError as err :
                    print("存档时遇到问题!", err)
                total_period_count += 1
                gamesave.play_periods += 1
                print("================")
                print("本周目持续了", period_turn_count, "轮,")
                print(period_round_count, "回合,")
                round_turn_count = 0
                period_turn_count = 0
                period_round_count = 0
                base_attack = 1
                print("=== 第", total_period_count, "周目 ===")
            except StopIteration :
                break
    round_turn_count = 0
    period_round_count += 1
    total_round_count += 1
    gamesave.play_rounds += 1
    if chosen_game.slots_sharing is not None :
        if chosen_game.slots_sharing[1] > 0 :
            if TYPE_CHECKING :
                setattr(chosen_game, "slots_sharing", (
                    chosen_game.slots_sharing[0],
                    chosen_game.slots_sharing[1]-1,
                    chosen_game.slots_sharing[2]
                ))
            else :
                chosen_game.slots_sharing = (
                    chosen_game.slots_sharing[0],
                    chosen_game.slots_sharing[1]-1,
                    chosen_game.slots_sharing[2]
                )
        if chosen_game.slots_sharing[1] <= 0 :
            if chosen_game.slots_sharing[0] :
                chosen_game.r_slots = chosen_game.slots_sharing[2]
            else :
                chosen_game.e_slots = chosen_game.slots_sharing[2]
            chosen_game.slots_sharing = None
    for player in chosen_game.players.values() :
        if isinstance(player, NormalPlayer) :
            while player.mid_band_level > 0 and player.hurts > 0 :
                player.hurts -= 1
                player.mid_band_level -= 1
            player.mid_band_level += player.begin_band_level
            player.begin_band_level = 0
            if player.breakcare_rounds > 0 :
                player.breakcare_rounds -= 1
    for i in chosen_game.round_start_message :
        if i[1] is None :
            if i[2] is None :
                print(*i[0])
            else :
                print(*i[0], end=i[2])
        elif i[2] is None :
            print(*i[0], sep=i[1])
        else :
            print(*i[0], sep=i[1], end=i[2])
    sleep(1)
    for i, player in chosen_game.players.items() :
        expired_slots: List[Optional[int]] = chosen_game.expire_slots(player)
        for tool_id in expired_slots :
            if tool_id is not None :
                if i == 0 and not chosen_game.players[1].controllable :
                    print("非常可惜,随着槽位的到期,你的",
                          chosen_game.tools[tool_id][0], "也不翼而飞")
                elif i == 1 and not chosen_game.players[1].controllable :
                    print("非常高兴,随着槽位的到期,恶魔的",
                          chosen_game.tools[tool_id][0], "不翼而飞")
                else :
                    print("随着槽位的到期,玩家", i, "的",
                          chosen_game.tools[tool_id][0], "不翼而飞")
    sleep(1)
    for i, player in chosen_game.players.items() :
        if player.controllable or i != 1 :
            new_slot: Optional[int] = chosen_game.send_slot(player)
            if new_slot is not None :
                if new_slot > 0 :
                    if i == 0 and not chosen_game.players[1].controllable :
                        print("你获得1个有效期", new_slot, "回合的空槽位")
                    else :
                        print("玩家", i, "获得1个有效期", new_slot,
                              "回合的空槽位")
                elif i == 0 and not chosen_game.players[1].controllable :
                    print("你获得1个永久空槽位")
                else :
                    print("玩家", i, "获得1个永久空槽位")
        else :
            new_slot: Optional[int]
            if nightmare :
                filtered: List[int] = []
                for j in filter(lambda key: (
                    player.slot_sending_weight[key] if isinstance(
                        player.slot_sending_weight[key], int
                    ) else player.slot_sending_weight[key](chosen_game)
                ) > 0, player.slot_sending_weight) :
                    filtered.append(j)
                new_slot = chosen_game.send_e_slot(1., {
                    0 if min(filtered) <= 0 else max(filtered): 1
                }) if filtered else None
            else :
                new_slot = chosen_game.send_slot(player)
            if new_slot is not None :
                if new_slot > 0 :
                    print("恶魔获得1个有效期", new_slot, "回合的空槽位")
                else :
                    print("恶魔获得1个永久空槽位")
    any_player_has_tools: bool = False
    for i, player in chosen_game.players.items() :
        if chosen_game.has_tools(player=player) :
            any_player_has_tools = True
            if player.controllable or i != 1 :
                if i == 0 and not chosen_game.players[1].controllable :
                    print("你获得", chosen_game.send_tools(
                        player, GAMEMODE_SET[gamemode_i][1]
                    ), "个道具")
                else :
                    print("玩家", i, "获得", chosen_game.send_tools(
                        player, GAMEMODE_SET[gamemode_i][1]
                    ), "个道具")
            else :
                print("恶魔获得", chosen_game.send_tools(
                    player, GAMEMODE_SET[gamemode_i][1]
                ), "个道具")
    if any_player_has_tools :
        sleep(1)
    chosen_game.gen_bullets()
    print("子弹共有", len(chosen_game.bullets), "发")
    sleep(1)
    print("实弹", chosen_game.bullets.count(True), "发 , 空弹",
          chosen_game.bullets.count(False), "发")
    shoot_result: ShootResult
    shoots_result: List[ShootResult]
    shoot_combo_addition: int
    comboshoot_consume_num: int
    base_shoot: bool
    gamesave.active_gametime += time() - gametime_time_start
    while chosen_game.bullets :
        gametime_time_start = time()
        try :
            with open("emlpd.dat", "wb") as gamesave_file :
                gamesave_file.write(gamesave.serialize())
        except OSError as err :
            print("存档时遇到问题!", err)
        if not (chosen_game.players[0].alive and chosen_game.players[1].alive):
            break
        if chosen_game.players[0].stopped_turns > 0 :
            print("感觉...头晕晕的...要变成{0}了~".format(cat_girl))
        elif chosen_game.players[1].stopped_turns > 0 :
            print("哈哈哈哈,对方被敲晕了,还是我的回合!" if
                  chosen_game.players[1].controllable else
                  "哈哈哈哈,恶魔被敲晕了,还是我的回合!")
        gamesave.active_gametime += time() - gametime_time_start
        if chosen_game.players[chosen_game.turn_orders[0]].controllable :
            if debug :
                for i in chosen_game.debug_message :
                    if i[1] is None :
                        if i[2] is None :
                            print(*i[0])
                        else :
                            print(*i[0], end=i[2])
                    elif i[2] is None :
                        print(*i[0], sep=i[1])
                    else :
                        print(*i[0], sep=i[1], end=i[2])
            operation: int = 2
            if not chosen_game.players[
                chosen_game.turn_orders[0]
            ].user_operatable(chosen_game) :
                operation = randint(0, 1)
            else :
                if sum(x.controllable
                       for x in chosen_game.players.values()) < 2 :
                    print("本轮由你操作")
                else :
                    print("本轮由玩家", chosen_game.turn_orders[0], "操作")
                print(
                    "请选择:1朝对方开枪,0朝自己开枪,7打开道具库,8查看对方道具"\
                    if chosen_game.has_tools() or any(
                        x.count_tools(None) < len(x.slots)
                        for x in chosen_game.players.values()
                    ) else "请选择:1朝对方开枪,0朝自己开枪"
                )
                try :
                    operation = int(input())
                except ValueError :
                    pass
            if operation == 7 and (
                chosen_game.has_tools() or
                chosen_game.count_tools_of_r(None) < len(chosen_game.r_slots)or
                chosen_game.count_tools_of_e(None) < len(chosen_game.e_slots)
            ) :
                player = chosen_game.players[chosen_game.turn_orders[0]]
                victim =chosen_game.players[0+(not chosen_game.turn_orders[0])]
                print("道具库:")
                tools_existence: Dict[int, int] = {}
                permaslots: Dict[int, int] = {}
                for slotid, slot in enumerate(player.slots) :
                    if slot[1] is not None :
                        if slot[0] <= 0 :
                            if slot[1] in permaslots :
                                permaslots[slot[1]] += 1
                            else :
                                permaslots[slot[1]] = 1
                        tools_existence[slot[1]] = slotid
                for k, v in permaslots.items() :
                    if v > 1 :
                        print("(*{0})".format(v), "道具", k, ":",
                              chosen_game.tools[k][0])
                    else :
                        print("道具", k, ":", chosen_game.tools[k][0])
                    if chosen_game.tools[k][1] is None :
                        print("此道具无描述")
                    else :
                        print("描述:", chosen_game.tools[k][1])
                for slot in player.slots :
                    if slot[1] is not None and slot[0] > 0 :
                        print("道具", slot[1], ":",
                              chosen_game.tools[slot[1]][0])
                        if chosen_game.tools[slot[1]][1] is None :
                            print("此道具无描述")
                        else :
                            print("描述:", chosen_game.tools[slot[1]][1])
                        print("还有", slot[0], "回合到期")
                if not tools_existence :
                    print("(空)")
                while tools_existence :
                    print("返回请直接按回车")
                    to_use: Optional[int] = None
                    try:
                        to_use = int(input("使用道具请输入它的对应编号:"))
                    except ValueError:
                        break
                    if to_use in tools_existence :
                        used: bool = True
                        if to_use == 0 :
                            if isinstance(player, NormalPlayer) :
                                player.slots[tools_existence[0]] = \
                                (player.slots[tools_existence[0]][0], None)
                                if player.cursed_shoot_level > 0 :
                                    player.cursed_shoot_level -= 1
                                else :
                                    player.selfshoot_promises += 1
                        elif to_use == 1 :
                            if isinstance(player, NormalPlayer) :
                                player.slots[tools_existence[1]] = \
                                (player.slots[tools_existence[1]][0], None)
                                if player.cursed_shoot_level > 0 :
                                    player.cursed_shoot_level -= 1
                                else :
                                    player.againstshoot_promises += 1
                        elif to_use == 2 :
                            if isinstance(player, NormalPlayer) :
                                player.slots[tools_existence[2]] = \
                                (player.slots[tools_existence[2]][0], None)
                                player.attack_boost += 1
                                print("你使用了小刀,结果会如何呢?真让人期待")
                        elif to_use == 3 :
                            player.slots[tools_existence[3]] = \
                            (player.slots[tools_existence[3]][0], None)
                            print("你排出了一颗实弹" \
                                  if chosen_game.bullets.pop(0) \
                                  else "你排出了一颗空弹")
                        elif to_use == 4 :
                            player.slots[tools_existence[4]] = \
                            (player.slots[tools_existence[4]][0], None)
                            chosen_game.rel_turn_lap += 1
                            victim.stopped_turns += 1
                            print("恭喜你,成功敲晕了对方!")
                        elif to_use == 5 :
                            player.slots[tools_existence[5]] = \
                            (player.slots[tools_existence[5]][0], None)
                            if isinstance(player, NormalPlayer) :
                                if player.hp <= 3 + player.hurts / 4. or \
                                   (random() < 0.5 ** (
                                       player.hp-3-player.hurts/4.
                                   ) and not nightmare) :
                                    player.hp += 1
                                    gamesave.healed += 1
                                    print("你使用了道德的崇高赞许,"
                                          "回复了1点生命")
                                else :
                                    print("因为你的不诚实,你并未回复生命,"
                                          "甚至失去了道德的崇高赞许")
                            else :
                                if player.hp <= 3 or \
                                   (random() < 0.5 ** (player.hp-3) and
                                    not nightmare) :
                                    player.hp += 1
                                    gamesave.healed += 1
                                    print("你使用了道德的崇高赞许,"
                                          "回复了1点生命")
                                else :
                                    print("因为你的不诚实,你并未回复生命,"
                                          "甚至失去了道德的崇高赞许")
                        elif to_use == 6 :
                            player.slots[tools_existence[6]] = \
                            (player.slots[tools_existence[6]][0], None)
                            print("当前的子弹为实弹" if chosen_game.bullets[0]\
                                  else "当前的子弹为空弹")
                            if chosen_game.extra_bullets[0] is not None :
                                if chosen_game.extra_bullets[0] :
                                    print("当前的子弹为实弹" \
                                          if chosen_game.extra_bullets[0][0] \
                                          else "当前的子弹为空弹")
                                if chosen_game.extra_bullets[1] is not None :
                                    if chosen_game.extra_bullets[1] :
                                        print("当前的子弹为实弹" if \
                                              chosen_game.extra_bullets[1][0] \
                                              else "当前的子弹为空弹")
                                    if chosen_game.extra_bullets[2] is not \
                                       None and chosen_game.extra_bullets[2] :
                                        print("当前的子弹为实弹" if \
                                              chosen_game.extra_bullets[2][0] \
                                              else "当前的子弹为空弹")
                        elif to_use == 7 :
                            player.slots[tools_existence[7]] = \
                            (player.slots[tools_existence[7]][0], None)
                            nonlimit_tool_slotids: List[int] = []
                            for slotid, slot in enumerate(victim.slots):
                                if slot[1] is not None :
                                    if victim.tools_sending_limit_in_game[
                                        slot[1]
                                    ] <= 0 :
                                        nonlimit_tool_slotids.append(slotid)
                            bring_tool_id: Optional[int] = None
                            if random() < 1 / (len(nonlimit_tool_slotids)+1) :
                                nonlimit_toolids: List[int] = []
                                for tool_id in chosen_game.tools :
                                    if player.tools_sending_limit_in_game[
                                        tool_id
                                    ] <= 0 :
                                        nonlimit_toolids.append(tool_id)
                                bring_tool_id = choice(nonlimit_toolids)
                            else :
                                taken_slotid: int = \
                                choice(nonlimit_tool_slotids)
                                bring_tool_id = victim.slots[taken_slotid][1]
                                victim.slots[taken_slotid] = \
                                (victim.slots[taken_slotid][0], None)
                            if bring_tool_id is None :
                                assert 0
                            for slotid, slot in enumerate(player.slots):
                                if slot[1] is None :
                                    player.slots[slotid] = \
                                    (player.slots[slotid][0], bring_tool_id)
                                    print("+1 道具", bring_tool_id)
                                    break
                            else :
                                assert 0
                        elif to_use == 8 :
                            if chosen_game.slots_sharing is None :
                                player.slots[tools_existence[8]] = \
                                (player.slots[tools_existence[8]][0], None)
                                new_keep_rounds: int = \
                                choice([1, 1, 1, 2, 2, 2, 2, 2, 3, 3])
                                chosen_game.slots_sharing = \
                                (not 0, new_keep_rounds, player.slots)
                                player.slots = victim.slots
                            elif chosen_game.slots_sharing[0] :
                                player.slots[tools_existence[8]] = \
                                (player.slots[tools_existence[8]][0], None)
                                new_keep_rounds: int
                                if TYPE_CHECKING :
                                    new_keep_rounds = \
                                    getattr(chosen_game, "slots_sharing")[1] +\
                                    choice([1, 1, 1, 2, 2, 2, 2, 2, 3, 3])
                                else :
                                    new_keep_rounds = \
                                    chosen_game.slots_sharing[1] + \
                                    choice([1, 1, 1, 2, 2, 2, 2, 2, 3, 3])
                                chosen_game.slots_sharing = \
                                (not 0, new_keep_rounds, player.slots)
                        elif to_use == 9 :
                            if isinstance(player, NormalPlayer) :
                                player.slots[tools_existence[9]] = \
                                (player.slots[tools_existence[9]][0], None)
                                print("你穿上了一件防弹衣")
                                player.bulletproof.insert(0, 3)
                        elif to_use == 11 :
                            player.slots[tools_existence[11]] = \
                            (player.slots[tools_existence[11]][0], None)
                            dice_sum: int = \
                            randint(1, 6) + randint(1, 6) + randint(1, 6)
                            if debug :
                                print("你摇出了", dice_sum, "点")
                            if dice_sum == 3 :
                                if isinstance(player, NormalPlayer) :
                                    player.breakcare_rounds += 2
                            elif dice_sum == 4 :
                                player.hp -= 2
                                print("你失去了2点生命")
                            elif dice_sum == 5 :
                                for bullet_index \
                                in range(2, len(chosen_game.bullets)) :
                                    chosen_game.bullets[bullet_index] = \
                                    not randint(0, 1)
                            elif dice_sum == 6 :
                                player.hp -= 1
                                print("你失去了1点生命")
                            elif dice_sum == 7 :
                                vanishable_indices: List[int] = []
                                for slotid, slot in enumerate(player.slots) :
                                    if slot[1] is not None :
                                        if player.tools_sending_limit_in_game[
                                            slot[1]
                                        ] <= 0 :
                                            vanishable_indices.append(slotid)
                                if vanishable_indices :
                                    vanish_index: int = \
                                    choice(vanishable_indices)
                                    player.slots[vanish_index] = \
                                    (player.slots[vanish_index][0],None)
                            elif dice_sum == 8 :
                                pass
                            elif dice_sum == 9 :
                                if isinstance(player, NormalPlayer) and \
                                   player.stamina < 32 :
                                    player.stamina += 1
                            elif dice_sum == 10 :
                                player.hp += 1
                                gamesave.healed += 1
                                print("你获得了1点生命")
                            elif dice_sum == 11 :
                                if isinstance(player, NormalPlayer) and \
                                   player.stamina < 32 :
                                    player.stamina += 1
                                    if player.stamina < 32 :
                                        player.stamina += 1
                            elif dice_sum == 12 :
                                if isinstance(player, NormalPlayer) :
                                    player.attack_boost += 2
                                    if randint(0, 1) :
                                        print("你的攻击力提高了2点")
                            elif dice_sum == 13 :
                                victim.hp -= 1
                                print(
                                    "对方失去了1点生命" if victim.controllable
                                    else "恶魔失去了1点生命"
                                )
                            elif dice_sum == 14 :
                                k: int = 2 - (not randint(0, 2))
                                chosen_game.rel_turn_lap += k
                                victim.stopped_turns += k
                            elif dice_sum == 15 :
                                victim.hp -= 2
                                print(
                                    "对方失去了2点生命" if victim.controllable
                                    else "恶魔失去了2点生命"
                                )
                            elif dice_sum == 18 :
                                victim.hp //= 8
                                if victim.controllable :
                                    print("对方受到暴击!!!")
                                    print("对方生命值:", victim.hp)
                                else :
                                    print("恶魔受到暴击!!!")
                                    print("恶魔生命值:", victim.hp)
                                gamesave.add_exp(6)
                        elif to_use == 12 :
                            temporary_slots: List[int] = []
                            for slotid in range(len(player.slots)) :
                                if player.slots[slotid][0] > 0 :
                                    temporary_slots.append(slotid)
                            if temporary_slots :
                                player.slots[tools_existence[12]] = \
                                (player.slots[tools_existence[12]][0],
                                 None)
                                delay_prob: float = len(temporary_slots) ** 0.5
                                for slotid in temporary_slots :
                                    if random() < delay_prob :
                                        player.slots[slotid] = \
                                        (player.slots[slotid][0]+1,
                                         player.slots[slotid][1])
                            else :
                                used = False
                        elif to_use == 13 :
                            player.slots[tools_existence[13]] = \
                            (player.slots[tools_existence[13]][0], None)
                            if randint(0, 1) :
                                print(
                                    "你变成了对方的样子" if victim.controllable
                                    else "你变成了恶魔的样子"
                                )
                                player.hp = victim.hp
                                player.slots.clear()
                                player.slots.extend(victim.slots)
                                player.sending_total.clear()
                                player.sending_total.update(
                                    victim.sending_total.copy()
                                )
                                player.stopped_turns = victim.stopped_turns
                                if isinstance(player, NormalPlayer) and \
                                   isinstance(victim, NormalPlayer) :
                                    player.attack_boost = victim.attack_boost
                                    player.bulletproof.clear()
                                    player.bulletproof.extend(
                                        victim.bulletproof
                                    )
                                    player.bullet_catcher_level = \
                                    victim.bullet_catcher_level
                                    player.selfshoot_promises = \
                                    victim.selfshoot_promises
                                    player.againstshoot_promises = \
                                    victim.againstshoot_promises
                                    player.multishoot_level = \
                                    victim.multishoot_level
                                    player.comboshoot_level = \
                                    victim.comboshoot_level
                                    player.cursed_shoot_level = \
                                    victim.cursed_shoot_level
                                    player.hurts = victim.hurts
                                    player.stamina = victim.stamina
                                    player.begin_band_level = \
                                    victim.begin_band_level
                                    player.mid_band_level = \
                                    victim.mid_band_level
                            else :
                                print(
                                    "对方变成了你的样子" if victim.controllable
                                    else "恶魔变成了你的样子"
                                )
                                victim.hp = player.hp
                                victim.slots.clear()
                                victim.slots.extend(player.slots)
                                victim.sending_total.clear()
                                victim.sending_total.update(
                                    player.sending_total.copy()
                                )
                                victim.stopped_turns = player.stopped_turns
                                if isinstance(player, NormalPlayer) and \
                                   isinstance(victim, NormalPlayer) :
                                    victim.attack_boost = player.attack_boost
                                    victim.bulletproof.clear()
                                    victim.bulletproof.extend(
                                        player.bulletproof
                                    )
                                    victim.bullet_catcher_level = \
                                    player.bullet_catcher_level
                                    victim.selfshoot_promises = \
                                    player.selfshoot_promises
                                    victim.againstshoot_promises = \
                                    player.againstshoot_promises
                                    victim.multishoot_level = \
                                    player.multishoot_level
                                    victim.comboshoot_level = \
                                    player.comboshoot_level
                                    victim.cursed_shoot_level = \
                                    player.cursed_shoot_level
                                    victim.hurts = player.hurts
                                    victim.stamina = player.stamina
                                    victim.begin_band_level = \
                                    player.begin_band_level
                                    victim.mid_band_level = \
                                    player.mid_band_level
                            chosen_game.rel_turn_lap = 0
                        elif to_use == 14 :
                            player.slots[tools_existence[14]] = \
                            (player.slots[tools_existence[14]][0], None)
                            player.bullet_catcher_level += 1
                        elif to_use == 15 :
                            player.slots[tools_existence[15]] = \
                            (player.slots[tools_existence[15]][0], None)
                            fill_probability: float = \
                            1 / len(chosen_game.bullets)
                            original_bullets: List[bool] = \
                            chosen_game.bullets[:]
                            for bullet_index in \
                            range(len(chosen_game.bullets)) :
                                if random() < fill_probability :
                                    chosen_game.bullets[bullet_index] = True
                            if chosen_game.bullets != original_bullets :
                                print("弹夹有变动")
                        elif to_use == 16 :
                            former_bullets: List[bool] = chosen_game.bullets[:]
                            chosen_game.bullets.clear()
                            print("输入0以开始重整弹药,直接按回车以取消。")
                            for i in range(len(former_bullets)) :
                                for bullet_index in range(i) :
                                    print(end=str(bullet_index))
                                    print(
                                        end="实" if \
                                            chosen_game.bullets[bullet_index] \
                                            else "空"
                                    )
                                print(i)
                                insertion: int = -1
                                while not (0 <= insertion <= i) :
                                    try :
                                        insertion = int(input())
                                    except ValueError :
                                        if not chosen_game.bullets :
                                            chosen_game.bullets.extend(
                                                former_bullets
                                            )
                                            used = False
                                            break
                                if not used :
                                    break
                                chosen_game.bullets.insert(
                                    insertion, former_bullets.pop(randint(
                                        0, len(former_bullets)-1
                                    ))
                                )
                            if used :
                                player.slots[tools_existence[16]] = \
                                (player.slots[tools_existence[16]][0], None)
                                for bullet_index in range(len(
                                        chosen_game.bullets
                                )) :
                                    print(end=str(bullet_index))
                                    print(
                                        end="实" if \
                                            chosen_game.bullets[bullet_index] \
                                            else "空"
                                    )
                                print(len(chosen_game.bullets))
                                print("你重整了一下弹药")
                        elif to_use == 17 :
                            if isinstance(player, NormalPlayer) :
                                player.slots[tools_existence[17]] = \
                                (player.slots[tools_existence[17]][0], None)
                                player.multishoot_level += 1
                        elif to_use == 18 :
                            if isinstance(player, NormalPlayer) :
                                player.slots[tools_existence[18]] = \
                                (player.slots[tools_existence[18]][0], None)
                                player.comboshoot_level += 1
                        elif to_use == 19 :
                            op_tools: List[int] = list(filter(
                                lambda x: chosen_game.has_tools(x),
                                (8, 13, 19, 29, 30, 31, 32)
                            ))
                            if op_tools :
                                if randint(0, 1) :
                                    player.slots[tools_existence[19]] = \
                                    (player.slots[tools_existence[19]][0],
                                     choice(op_tools))
                                else :
                                    player.slots[tools_existence[19]] = \
                                    (player.slots[tools_existence[19]][0],None)
                                    player.hp //= 2
                        elif to_use == 21 :
                            if isinstance(victim, NormalPlayer) :
                                player.slots[tools_existence[21]] = \
                                (player.slots[tools_existence[21]][0], None)
                                victim.cursed_shoot_level += 1
                        elif to_use == 22 :
                            if len(chosen_game.bullets) == 1 :
                                if input(
                                    "弹夹内只有1发子弹,将其取出会即刻进入下一"
                                    "回合,是否将其取出?(y/[N])"
                                ).strip().lower() in ("y", "0") :
                                    player.slots[tools_existence[22]] =\
                                    (player.slots[tools_existence[22]][
                                        0
                                    ],24 if chosen_game.bullets.pop(0) else 23)
                                    print("你取出了一颗子弹")
                                    print("+1 道具", player.slots[
                                        tools_existence[22]
                                    ][1])
                                else :
                                    used = False
                            else :
                                try :
                                    bullet_i_to_pick: int = int(input(
                                        "请输入要取出子弹的编号"
                                        "(0~{0},0为当前子弹,输入其它以取消):"
                                        .format(len(chosen_game.bullets)-1)
                                    ))
                                    if 0 <= bullet_i_to_pick < \
                                       len(chosen_game.bullets) :
                                        player.slots[tools_existence[
                                            22
                                        ]] = (player.slots[
                                            tools_existence[22]
                                        ][0], 24 if chosen_game.bullets.pop(
                                            bullet_i_to_pick
                                        ) else 23)
                                        print("你取出了一颗子弹")
                                        print("+1 道具", player.slots[
                                            tools_existence[22]
                                        ][1])
                                    else :
                                        used = False
                                except ValueError :
                                    used = False
                        elif to_use == 23 :
                            try :
                                bullet_i_to_ins: int = \
                                int(input("请输入要插入空弹的编号(0~{0},"
                                          "0为当前子弹之前,输入其它以取消):"
                                          .format(len(chosen_game.bullets))))
                                if 0 <= bullet_i_to_ins <= \
                                    len(chosen_game.bullets) :
                                    player.slots[tools_existence[23]] =\
                                    (player.slots[tools_existence[23]][
                                        0
                                    ], None)
                                    chosen_game.bullets.insert(bullet_i_to_ins,
                                                               False)
                                    print("你放入了一颗空弹")
                                else :
                                    used = False
                            except ValueError :
                                used = False
                        elif to_use == 24 :
                            try :
                                bullet_i_to_ins: int = \
                                int(input("请输入要插入实弹的编号(0~{0},"
                                          "0为当前子弹之前,输入其它以取消):"
                                          .format(len(chosen_game.bullets))))
                                if 0 <= bullet_i_to_ins <= \
                                    len(chosen_game.bullets) :
                                    player.slots[tools_existence[24]] =\
                                    (player.slots[tools_existence[24]][
                                        0
                                    ], None)
                                    chosen_game.bullets.insert(bullet_i_to_ins,
                                                               True)
                                    print("你放入了一颗实弹")
                                else :
                                    used = False
                            except ValueError :
                                used = False
                        elif to_use == 25 :
                            try :
                                bullet_i_to_ins: int = \
                                int(input("请输入要插入神秘子弹的编号(0~{0},"
                                          "0为当前子弹之前,输入其它以取消):"
                                          .format(len(chosen_game.bullets))))
                                if 0 <= bullet_i_to_ins <= \
                                    len(chosen_game.bullets) :
                                    player.slots[tools_existence[25]] =\
                                    (player.slots[tools_existence[25]][
                                        0
                                    ], None)
                                    chosen_game.bullets.insert(
                                        bullet_i_to_ins, not randint(0, 1)
                                    )
                                    if bullet_i_to_ins < \
                                       len(chosen_game.bullets) - 1 :
                                        chosen_game.bullets[
                                            bullet_i_to_ins+1
                                        ] = not randint(0, 1)
                                    print("你放入了一颗神秘子弹")
                                else :
                                    used = False
                            except ValueError :
                                used = False
                        elif to_use == 26 :
                            if isinstance(player, NormalPlayer) :
                                if player.hurts > \
                                   player.begin_band_level + \
                                   player.mid_band_level :
                                    player.slots[tools_existence[26]] = \
                                    (player.slots[tools_existence[26]][0],
                                     None)
                                    player.begin_band_level += 1
                                    print("你使用了绷带")
                                else :
                                    used = False
                        elif to_use == 27 :
                            player.slots[tools_existence[27]] = \
                            (player.slots[tools_existence[27]][0], None)
                            if player.hp < 2 :
                                player.hp += 5
                                gamesave.healed += 5
                                print("你使用了医疗包,回复了5点生命")
                            elif player.hp < 5 :
                                player.hp += 4
                                gamesave.healed += 4
                                print("你使用了医疗包,回复了4点生命")
                            elif player.hp < 9 :
                                player.hp += 3
                                gamesave.healed += 3
                                print("你使用了医疗包,回复了3点生命")
                            elif player.hp < 14 :
                                player.hp += 2
                                gamesave.healed += 2
                                print("你使用了医疗包,回复了2点生命")
                            else :
                                player.hp += 1
                                gamesave.healed += 1
                                print("你使用了医疗包,回复了1点生命")
                            if isinstance(player, NormalPlayer) :
                                if player.hurts < 1 :
                                    player.hp += 2
                                    gamesave.healed += 2
                                elif player.hurts < 4 :
                                    player.hp += 1
                                    gamesave.healed += 1
                                player.hurts = 0
                        elif to_use == 28 :
                            player.slots[tools_existence[28]] = \
                            (player.slots[tools_existence[28]][0], None)
                            while chosen_game.bullets :
                                print("你排出了一颗实弹" \
                                      if chosen_game.bullets.pop(0) \
                                      else "你排出了一颗空弹")
                        elif to_use == 29 :
                            player.slots[tools_existence[29]] = \
                            (player.slots[tools_existence[29]][0], None)
                            chosen_game.copy_bullets_for_new()
                        elif to_use == 30 :
                            player.slots[tools_existence[30]] = \
                            (player.slots[tools_existence[30]][0], None)
                            if randint(0, 1) :
                                for slotid, slot in enumerate(player.slots) :
                                    player.slots[slotid] = (slot[0], None)
                                for slotid, slot in enumerate(victim.slots) :
                                    victim.slots[slotid] = (slot[0], None)
                                if isinstance(player, NormalPlayer) :
                                    player.attack_boost = 0
                                    player.bulletproof.clear()
                                if isinstance(victim, NormalPlayer) :
                                    victim.attack_boost = 0
                                    victim.bulletproof.clear()
                            else :
                                pass
                        elif to_use == 31 :
                            player.slots[tools_existence[31]] = \
                            (player.slots[tools_existence[31]][0], None)
                            chosen_game.rel_turn_lap += \
                            len(chosen_game.bullets)
                            victim.stopped_turns += len(chosen_game.bullets)
                            print("恭喜你,成功敲晕了对方!")
                        elif to_use == 32 :
                            if player.hp == 1 :
                                if "y" == input(
                                    "你只有1生命值,是否要发起擂台战?(y/[N])"
                                ).strip().lower() :
                                    player.slots[tools_existence[32]] = \
                                    (player.slots[tools_existence[32]][0],
                                     None)
                                    evil_hp: int = randint(1, victim.hp)
                                    print("恶魔以", evil_hp, "生命值应战")
                                    player.hp -= 1
                                    victim.hp -= evil_hp
                                    parent_game.subgame = StageGame(
                                        1, evil_hp, True
                                    )
                                    sub_game = parent_game.subgame
                                    chosen_game = \
                                    parent_game if sub_game is None \
                                    else sub_game
                                    if isinstance(sub_game, StageGame) :
                                        sub_game.gen_bullets()
                                else :
                                    used = False
                            else :
                                try :
                                    your_hp: int = \
                                    int(input("请输入你要作为赌注的生命值"
                                              "(1~{0},输入其它以取消):"
                                              .format(player.hp)))
                                    if 0 < your_hp <= player.hp :
                                        player.slots[tools_existence[32]] = \
                                        (player.slots[tools_existence[32]][0],
                                         None)
                                        evil_hp: int = \
                                        randint(1, victim.hp)
                                        print("恶魔以", evil_hp, "生命值应战")
                                        player.hp -= your_hp
                                        victim.hp -= evil_hp
                                        parent_game.subgame = StageGame(
                                            your_hp, evil_hp, True
                                        )
                                        sub_game = parent_game.subgame
                                        chosen_game = \
                                        parent_game if sub_game is None \
                                        else sub_game
                                        if isinstance(sub_game, StageGame) :
                                            sub_game.gen_bullets()
                                    else :
                                        used = False
                                except ValueError :
                                    used = False
                        elif to_use == 33 :
                            if isinstance(chosen_game, NormalGame) and \
                               chosen_game.explosion_exponent > 0 :
                                player.slots[tools_existence[33]] = \
                                (player.slots[tools_existence[33]][0],
                                 None)
                                chosen_game.explosion_exponent = int(
                                    Fraction(2, 3)*\
                                    chosen_game.explosion_exponent
                                )
                                print("你维修了一下枪筒")
                            else :
                                used = False
                        elif to_use == 34 :
                            player.slots[tools_existence[34]] = \
                            (player.slots[tools_existence[34]][0], None)
                            false_count: int = 0
                            while False in chosen_game.bullets :
                                false_count += 1
                                chosen_game.bullets.remove(False)
                            for _ in range(false_count) :
                                chosen_game.bullets.append(False)
                            for i in chosen_game.extra_bullets :
                                if i is not None :
                                    false_count = 0
                                    while False in i :
                                        false_count += 1
                                        i.remove(False)
                                    for _ in range(false_count) :
                                        i.append(False)
                            print("弹夹进行了空实分离")
                        elif to_use == 35 :
                            if any(chosen_game.extra_bullets) :
                                player.slots[tools_existence[35]] = \
                                (player.slots[tools_existence[35]][0], None)
                                for i in chosen_game.extra_bullets :
                                    if i :
                                        chosen_game.bullets.extend(i)
                                        i.clear()
                                print("你合并了一下弹夹")
                            else :
                                used = False
                        if used :
                            print("-1 道具", to_use)
                        if not chosen_game.bullets :
                            break
                        tools_existence.clear()
                        permaslots.clear()
                        for slotid, slot in enumerate(player.slots) :
                            if slot[1] is not None :
                                if slot[0] <= 0 :
                                    if slot[1] in permaslots :
                                        permaslots[slot[1]] += 1
                                    else :
                                        permaslots[slot[1]] = 1
                                tools_existence[slot[1]] = slotid
                    else :
                        print("道具", to_use, "不存在或未拥有")
            elif operation == 8  and (
                chosen_game.has_tools() or
                chosen_game.count_tools_of_r(None) < len(chosen_game.r_slots)or
                chosen_game.count_tools_of_e(None) < len(chosen_game.e_slots)
            ) :
                player =chosen_game.players[0+(not chosen_game.turn_orders[0])]
                print("对方的道具库:" if player.controllable
                      else "恶魔的道具库:")
                permaslots: Dict[int, int] = {}
                e_has_tool: bool = False
                for slot in player.slots :
                    if slot[1] is not None and slot[0] <= 0 :
                        e_has_tool = True
                        if slot[1] in permaslots :
                            permaslots[slot[1]] += 1
                        else :
                            permaslots[slot[1]] = 1
                for k, v in permaslots.items() :
                    if v > 1 :
                        print("(*{0})".format(v), "道具", k, ":",
                              chosen_game.tools[k][0])
                    else :
                        print("道具", k, ":", chosen_game.tools[k][0])
                    if chosen_game.tools[k][1] is None :
                        print("此道具无描述")
                    else :
                        print("描述:", chosen_game.tools[k][1])
                for slot in player.slots :
                    if slot[1] is not None and slot[0] > 0 :
                        e_has_tool = True
                        print("道具", slot[1], ":",
                              chosen_game.tools[slot[1]][0])
                        if chosen_game.tools[slot[1]][1] is None :
                            print("此道具无描述")
                        else :
                            print("描述:", chosen_game.tools[slot[1]][1])
                        print("还有", slot[0], "回合到期")
                if not e_has_tool :
                    print("(空)")
            elif operation == 1 :
                player = chosen_game.players[chosen_game.turn_orders[0]]
                victim =chosen_game.players[0+(not chosen_game.turn_orders[0])]
                round_turn_count += 1
                period_turn_count += 1
                total_turn_count += 1
                gamesave.play_turns += 1
                if isinstance(player, NormalPlayer) and player.stamina > 0 :
                    player.stamina -= 1
                true_on_r = False
                true_on_e = False
                shoot_combo_addition = 0
                if isinstance(player, NormalPlayer) :
                    comboshoot_consume_num = 0
                    while shoot_combo_addition < len(chosen_game.bullets) :
                        comboshoot_consume_num += 1
                        if random() >= 0.5 ** player.comboshoot_level :
                            shoot_combo_addition += 1
                        else :
                            break
                    if shoot_combo_addition == len(chosen_game.bullets) :
                        chosen_game.rel_turn_lap += 1
                        victim.stopped_turns += 1
                    player.comboshoot_level -= comboshoot_consume_num
                    if player.comboshoot_level < 0 :
                        player.comboshoot_level = 0
                    if player.cursed_shoot_level > 0 :
                        shoots_result = chosen_game.shoots(
                            False, True, 1.,
                            shoot_combo_addition+player.multishoot_level+1 \
                            if shoot_combo_addition+player.multishoot_level<\
                               len(chosen_game.bullets) \
                            else len(chosen_game.bullets)
                        )
                        player.cursed_shoot_level -= 1
                    elif player.againstshoot_promises > 0 :
                        shoots_result = chosen_game.shoots(
                            False, True, 0.,
                            shoot_combo_addition+player.multishoot_level+1 \
                            if shoot_combo_addition+player.multishoot_level<\
                               len(chosen_game.bullets) \
                            else len(chosen_game.bullets)
                        )
                        player.againstshoot_promises -= 1
                    else :
                        shoots_result = chosen_game.shoots(
                            False, True,
                            combo=(
                                shoot_combo_addition+player.multishoot_level+1
                                if shoot_combo_addition+player.multishoot_level<
                                   len(chosen_game.bullets)
                                else len(chosen_game.bullets)
                            )
                        )
                else :
                    shoots_result = chosen_game.shoots(False, True)
                base_shoot = True
                for shoot_result in shoots_result :
                    if shoot_result[0] is not None :
                        if base_shoot :
                            base_shoot = False
                        elif shoot_combo_addition :
                            shoot_combo_addition -= 1
                        elif isinstance(player, NormalPlayer) :
                            player.multishoot_level -= 1
                    for bullets_i in shoot_result :
                        if bullets_i is not None :
                            if nightmare :
                                if bullets_i[0] or not randint(0, 3) :
                                    gamesave.add_exp(ceil(
                                        GAMEMODE_SET[gamemode_i][2]
                                    ))
                            elif not debug :
                                if bullets_i[0] or not randint(0, 3) :
                                    gamesave.add_exp()
                            if bullets_i[1] :
                                print("哦嘿,子弹居然炸膛了!")
                                if bullets_i[0] :
                                    gamesave.exploded_againstshoot_trues += 1
                                    if nightmare :
                                        gamesave.add_exp(ceil((
                                            base_attack+player.attack_boost if
                                            isinstance(player, NormalPlayer)
                                            else base_attack
                                        )*GAMEMODE_SET[gamemode_i][2]/2))
                                    elif not debug :
                                        gamesave.add_exp((
                                            base_attack+player.attack_boost if
                                            isinstance(player, NormalPlayer)
                                            else base_attack
                                        )//2)
                                    true_on_r = True
                                    print("感觉像是去奈何桥走了一遭,"
                                          "竟然是个实弹!")
                                    for _ in range(
                                        base_attack+player.attack_boost \
                                        if isinstance(player, NormalPlayer) \
                                        else base_attack
                                    ):
                                        if isinstance(player, NormalPlayer) \
                                           and random() < player.hurts / 8. :
                                            player.hp -= 2
                                            gamesave.damage_caused_to_r += 2
                                            gamesave.damage_caught += 2
                                        else :
                                            player.hp -= 1
                                            gamesave.damage_caused_to_r += 1
                                            gamesave.damage_caught += 1
                                    print("你的生命值:", player.hp)
                                    if isinstance(player, NormalPlayer) and \
                                       random() >= player.hurts / 8. :
                                        player.hurts += 1
                                        assert 0 <= player.hurts < 9
                                else :
                                    gamesave.exploded_againstshoot_falses += 1
                                    print("啊哈!,是个空弹!")
                            else :
                                if bullets_i[0] :
                                    gamesave.success_againstshoot_trues += 1
                                else :
                                    gamesave.success_againstshoot_falses += 1
                                if isinstance(victim, NormalPlayer) and \
                                   victim.bullet_catcher_level :
                                    if bullets_i[0] :
                                        if random() < (
                                            1-0.8**victim.bullet_catcher_level
                                        ) / (1+player.attack_boost if
                                             isinstance(player, NormalPlayer)
                                             else 1) :
                                            victim.bullet_catcher_level = 0
                                            chosen_game.bullets.append(True)
                                            if victim.stamina > 0 :
                                                victim.stamina -= 1
                                            print("对方接住了一颗子弹"
                                                  if victim.controllable
                                                  else "恶魔接住了一颗子弹")
                                            continue
                                    else :
                                        if random() < 0.8 / (
                                            1+player.attack_boost if
                                            isinstance(player, NormalPlayer)
                                            else 1
                                        ):
                                            victim.bullet_catcher_level -= 1
                                            chosen_game.bullets.append(False)
                                            if victim.stamina > 0 :
                                                victim.stamina -= 1
                                            print("对方接住了一颗子弹"
                                                  if victim.controllable
                                                  else "恶魔接住了一颗子弹")
                                            continue
                                if isinstance(victim, NormalPlayer) and \
                                   victim.bulletproof :
                                    victim.bulletproof[0] -= randint(1, ceil(
                                        (player.attack_boost+1)**0.5
                                    )) if isinstance(player, NormalPlayer) \
                                    else 1
                                    print("对方的防弹衣承受了这次撞击"
                                          if victim.controllable
                                          else "恶魔的防弹衣承受了这次撞击")
                                    if victim.bulletproof[0] <= 0 :
                                        if random() >= \
                                           2 ** (victim.bulletproof[0]-1) :
                                            del victim.bulletproof[0]
                                            victim.breakcare_potential += 1
                                            if not victim.bulletproof :
                                                for _ in range(
                                                    victim.breakcare_potential
                                                ) :
                                                    if random() < 0.15 :
                                                        victim.\
                                                        breakcare_rounds += 1
                                                victim.breakcare_potential = 0
                                            print("对方的一件防弹衣爆了"
                                                  if victim.controllable
                                                  else "恶魔的一件防弹衣爆了")
                                elif bullets_i[0] :
                                    if nightmare :
                                        gamesave.add_exp(ceil((
                                            base_attack+player.attack_boost if
                                            isinstance(player, NormalPlayer)
                                            else base_attack
                                        )/2))
                                    elif not debug :
                                        gamesave.add_exp((
                                            base_attack+player.attack_boost if
                                            isinstance(player, NormalPlayer)
                                            else base_attack
                                        )//2)
                                    true_on_e = True
                                    print("运气非常好,是个实弹!")
                                    for _ in range(
                                        base_attack+player.attack_boost
                                        if isinstance(player, NormalPlayer)
                                        else base_attack
                                    ):
                                        if isinstance(victim, NormalPlayer) \
                                           and random() < victim.hurts / 8. :
                                            victim.hp -= 2
                                            gamesave.damage_caused_to_e += 2
                                        else :
                                            victim.hp -= 1
                                            gamesave.damage_caused_to_e += 1
                                    print("对方生命值:" if victim.controllable
                                          else "恶魔生命值:", victim.hp)
                                    if isinstance(victim, NormalPlayer) and \
                                       random() >= victim.hurts / 8. :
                                        victim.hurts += 1
                                        assert 0 <= victim.hurts < 9
                                else :
                                    print("很遗憾,是个空弹")
                if isinstance(player, NormalPlayer) and not true_on_r and \
                   player.stamina < 32 and random() < 1. / (player.hurts+1) :
                    player.stamina += 1
                if isinstance(victim, NormalPlayer) and not true_on_e and \
                   victim.stamina < 32 and random() < 1. / (victim.hurts+1) :
                    victim.stamina += 1
                if isinstance(player, NormalPlayer) and player.stamina < 8 and\
                   random() < 1 - (player.stamina/8.) :
                    chosen_game.rel_turn_lap -= 1
                    player.stopped_turns += 1
                if isinstance(victim, NormalPlayer) and victim.stamina < 8 and\
                   random() < 1 - (victim.stamina/8.) :
                    chosen_game.rel_turn_lap += 1
                    victim.stopped_turns += 1
                if isinstance(player, NormalPlayer) :
                    player.attack_boost = 0
            elif operation == 0 :
                player = chosen_game.players[chosen_game.turn_orders[0]]
                victim =chosen_game.players[0+(not chosen_game.turn_orders[0])]
                round_turn_count += 1
                period_turn_count += 1
                total_turn_count += 1
                gamesave.play_turns += 1
                true_on_r = False
                true_on_e = False
                if isinstance(player, NormalPlayer) and player.stamina > 0 :
                    player.stamina -= 1
                if isinstance(player, NormalPlayer) and \
                   player.cursed_shoot_level > 0 :
                    shoot_result = chosen_game.shoot(True, True, 1.)
                    player.cursed_shoot_level -= 1
                elif isinstance(player, NormalPlayer) and \
                     player.selfshoot_promises :
                    shoot_result = chosen_game.shoot(True, True, 0.)
                    player.selfshoot_promises -= 1
                else :
                    shoot_result = chosen_game.shoot(True, True)
                for bullets_i in shoot_result :
                    if bullets_i is not None :
                        if bullets_i[1] :
                            if bullets_i[0] :
                                gamesave.exploded_selfshoot_trues += 1
                            else :
                                gamesave.exploded_selfshoot_falses += 1
                            print("哦嘿,子弹居然炸膛了!")
                            if isinstance(victim, NormalPlayer) and \
                               victim.bullet_catcher_level :
                                if bullets_i[0] :
                                    if random() < (
                                        1-0.8**victim.bullet_catcher_level
                                    ) / (1+player.attack_boost if
                                         isinstance(player, NormalPlayer) else
                                         1):
                                        victim.bullet_catcher_level = 0
                                        chosen_game.bullets.append(True)
                                        if victim.stamina > 0 :
                                            victim.stamina -= 1
                                        print("对方接住了一颗子弹"
                                              if victim.controllable
                                              else "恶魔接住了一颗子弹")
                                        continue
                                else :
                                    if random() < 0.8 / (
                                        1+player.attack_boost if
                                        isinstance(player, NormalPlayer) else 1
                                    ) :
                                        victim.bullet_catcher_level -= 1
                                        chosen_game.bullets.append(False)
                                        if victim.stamina > 0 :
                                            victim.stamina -= 1
                                        print("对方接住了一颗子弹"
                                              if victim.controllable
                                              else "恶魔接住了一颗子弹")
                                        continue
                            if isinstance(victim, NormalPlayer) and \
                               victim.bulletproof :
                                victim.bulletproof[0] -= randint(1, ceil(
                                    (player.attack_boost+1)**0.5
                                )) if isinstance(player, NormalPlayer) else 1
                                print("对方的防弹衣承受了这次撞击"
                                      if victim.controllable
                                      else "恶魔的防弹衣承受了这次撞击")
                                if victim.bulletproof[0] <= 0 :
                                    if random() >= \
                                       2 ** (victim.bulletproof[0]-1) :
                                        del victim.bulletproof[0]
                                        victim.breakcare_potential += 1
                                        if not victim.bulletproof :
                                            for _ in \
                                            range(victim.breakcare_potential) :
                                                if random() < 0.15 :
                                                    victim.breakcare_rounds +=1
                                            victim.breakcare_potential = 0
                                        print("对方的一件防弹衣爆了"
                                              if victim.controllable
                                              else "恶魔的一件防弹衣爆了")
                            elif bullets_i[0] :
                                true_on_e = True
                                print("运气非常好,是个实弹!")
                                for _ in range(
                                    base_attack+player.attack_boost if
                                    isinstance(player, NormalPlayer) else
                                    base_attack
                                ) :
                                    if isinstance(victim, NormalPlayer) and \
                                       random() < victim.hurts / 8. :
                                        victim.hp -= 2
                                        gamesave.damage_caused_to_e += 2
                                    else :
                                        victim.hp -= 1
                                        gamesave.damage_caused_to_e += 1
                                print("对方生命值:" if victim.controllable
                                      else "恶魔生命值:", victim.hp)
                                if isinstance(victim, NormalPlayer) and \
                                   random() >= victim.hurts / 8. :
                                    victim.hurts += 1
                                    assert 0 <= victim.hurts < 9
                            else :
                                print("很遗憾,是个空弹")
                        else :
                            if bullets_i[0] :
                                gamesave.success_selfshoot_trues += 1
                                true_on_r = True
                                print("感觉像是去奈何桥走了一遭,竟然是个实弹!")
                                for _ in range(
                                    base_attack+player.attack_boost if
                                    isinstance(player, NormalPlayer) else
                                    base_attack
                                ) :
                                    if isinstance(player, NormalPlayer) and \
                                       random() < player.hurts / 8. :
                                        player.hp -= 2
                                        gamesave.damage_caused_to_r += 2
                                        gamesave.damage_caught += 2
                                    else :
                                        player.hp -= 1
                                        gamesave.damage_caused_to_r += 1
                                        gamesave.damage_caught += 1
                                print("你的生命值:", player.hp)
                                if isinstance(player, NormalPlayer) and \
                                   random() >= player.hurts / 8. :
                                    player.hurts += 1
                                    assert 0 <= player.hurts < 9
                            else :
                                gamesave.success_selfshoot_falses += 1
                                print("啊哈!,是个空弹!")
                if isinstance(player, NormalPlayer) and not true_on_r and \
                   player.stamina < 32 and random() < 1. / (player.hurts+1) :
                    player.stamina += 1
                if isinstance(victim, NormalPlayer) and not true_on_e and \
                   victim.stamina < 32 and random() < 1. / (victim.hurts+1) :
                    victim.stamina += 1
                if isinstance(player, NormalPlayer) and player.stamina < 8 and\
                   random() < 1 - (player.stamina/8.) :
                    chosen_game.rel_turn_lap -= 1
                    player.stopped_turns += 1
                if isinstance(victim, NormalPlayer) and victim.stamina < 8 and\
                   random() < 1 - (victim.stamina/8.) :
                    chosen_game.rel_turn_lap += 1
                    victim.stopped_turns += 1
                if isinstance(player, NormalPlayer) :
                    player.attack_boost = 0
            else :
                print("请确定输入的数字正确")
        else :
            player = chosen_game.players[chosen_game.turn_orders[0]]
            victim = chosen_game.players[0+(not chosen_game.turn_orders[0])]
            gametime_time_start = time()
            if not chosen_game.bullets :
                break
            for slotid, slot in enumerate(player.slots) :
                will_use: bool
                if isinstance(player, NormalPlayer) and \
                   player.breakcare_rounds > 0 or not chosen_game.bullets :
                    break
                if slot[1] == 0 :
                    will_use = nightmare or not randint(0, 3)
                    if isinstance(player, NormalPlayer) and will_use :
                        player.slots[slotid] = (slot[0], None)
                        if player.cursed_shoot_level > 0 :
                            player.cursed_shoot_level -= 1
                        else :
                            player.selfshoot_promises += 1
                elif slot[1] == 1 :
                    will_use = nightmare or not randint(0, 3)
                    if isinstance(player, NormalPlayer) and will_use :
                        player.slots[slotid] = (slot[0], None)
                        if player.cursed_shoot_level > 0 :
                            player.cursed_shoot_level -= 1
                        else :
                            player.againstshoot_promises += 1
                elif slot[1] == 3 :
                    will_use = \
                    True if nightmare and chosen_game.bullets[0] and \
                            chosen_game.bullets.count(True) == 1 else \
                    not randint(0, 1)
                    if will_use :
                        player.slots[slotid] = (slot[0], None)
                        print("恶魔排出了一颗实弹" \
                              if chosen_game.bullets.pop(0) \
                              else "恶魔排出了一颗空弹")
                        if not chosen_game.bullets :
                            break
                elif slot[1] == 2 :
                    will_use = chosen_game.bullets[0] if nightmare else \
                                     not randint(0, 1)
                    if isinstance(player, NormalPlayer) and will_use :
                        player.slots[slotid] = (slot[0], None)
                        player.attack_boost += 1
                        print("恶魔使用了小刀,哦吼吼,结果会如何呢?")
                elif slot[1] == 4 :
                    will_use = nightmare or not randint(0, 1)
                    if will_use :
                        player.slots[slotid] = (slot[0], None)
                        chosen_game.rel_turn_lap -= 1
                        victim.stopped_turns += 1
                        print("恭喜恶魔,成功把你变成了{0}!".format(cat_girl))
                elif slot[1] == 5 :
                    will_use = nightmare or not randint(0, 1)
                    if will_use :
                        player.slots[slotid] = (slot[0], None)
                        if isinstance(player, NormalPlayer) :
                            if nightmare or player.hp <= 3 + player.hurts / 4.\
                               or random() < \
                                  0.5 ** (player.hp-3-player.hurts/4.) :
                                player.hp += 1
                                print("恶魔使用了道德的崇高赞许,回复了1点生命")
                            else :
                                print("因为恶魔的不诚实,恶魔并未回复生命,"
                                      "甚至失去了道德的崇高赞许")
                        else :
                            if nightmare or player.hp <= 3 or \
                               random() < 0.5 ** (player.hp-3) :
                                player.hp += 1
                                print("恶魔使用了道德的崇高赞许,回复了1点生命")
                            else :
                                print("因为恶魔的不诚实,恶魔并未回复生命,"
                                      "甚至失去了道德的崇高赞许")
                elif slot[1] == 6 :
                    will_use = nightmare or not randint(0, 1)
                    if will_use :
                        player.slots[slotid] = (slot[0], None)
                        print("恶魔查看了枪里的子弹并笑了一下")
                elif slot[1] == 7 :
                    will_use = not randint(0, 3)
                    if will_use :
                        player.slots[slotid] = (slot[0], None)
                        nonlimit_tool_slotids: List[int] = []
                        for slotid, slot in enumerate(victim.slots) :
                            if slot[1] is not None :
                                if victim.tools_sending_limit_in_game[slot[1]]\
                                   <= 0 :
                                    nonlimit_tool_slotids.append(slotid)
                        bring_tool_id: Optional[int] = None
                        if random() < 1 / (len(nonlimit_tool_slotids)+1) :
                            nonlimit_toolids: List[int] = []
                            for tool_id in chosen_game.tools :
                                if player.tools_sending_limit_in_game[tool_id]\
                                   <= 0 :
                                    nonlimit_toolids.append(tool_id)
                            bring_tool_id = choice(nonlimit_toolids)
                        else :
                            taken_slotid: int = choice(nonlimit_tool_slotids)
                            bring_tool_id = victim.slots[taken_slotid][1]
                            victim.slots[taken_slotid] = \
                            (victim.slots[taken_slotid][0], None)
                        if bring_tool_id is None :
                            assert 0
                        for slotid, slot in enumerate(player.slots) :
                            if slot[1] is None :
                                player.slots[slotid] = \
                                (player.slots[slotid][0], bring_tool_id)
                                break
                        else :
                            assert False
                elif slot[1] == 8 :
                    will_use = not randint(0, 7)
                    if will_use :
                        if chosen_game.slots_sharing is None :
                            player.slots[slotid] = (slot[0], None)
                            new_keep_rounds: int = \
                            choice([1, 1, 1, 2, 2, 2, 2, 2, 3, 3])
                            chosen_game.slots_sharing = \
                            (not 1, new_keep_rounds, player.slots)
                            player.slots = victim.slots
                        elif not chosen_game.slots_sharing[0] :
                            player.slots[slotid] = (slot[0], None)
                            new_keep_rounds: int
                            if TYPE_CHECKING :
                                new_keep_rounds = \
                                getattr(chosen_game, "slots_sharing")[1] + \
                                choice([1, 1, 1, 2, 2, 2, 2, 2, 3, 3])
                            else :
                                new_keep_rounds = \
                                chosen_game.slots_sharing[1] + \
                                choice([1, 1, 1, 2, 2, 2, 2, 2, 3, 3])
                            chosen_game.slots_sharing = \
                            (not 1, new_keep_rounds, player.slots)
                elif isinstance(player, NormalPlayer) and slot[1] == 9 :
                    will_use = nightmare or not randint(0, 1)
                    if will_use :
                        player.slots[slotid] = (slot[0], None)
                        print("恶魔穿上了一件防弹衣")
                        player.bulletproof.insert(0, 3)
                elif slot[1] == 11 :
                    will_use = nightmare or not randint(0, 5)
                    if will_use :
                        player.slots[slotid] = (slot[0], None)
                        dice_sum: int = \
                        randint(1, 6) + randint(1, 6) + randint(1, 6)
                        if debug :
                            print("恶魔摇出了", dice_sum, "点")
                        if dice_sum == 3 :
                            if isinstance(player, NormalPlayer) :
                                player.breakcare_rounds += 2
                        elif dice_sum == 4 :
                            player.hp -= 2
                            print("恶魔失去了2点生命")
                            if player.hp <= 0 :
                                break
                        elif dice_sum == 5 :
                            for bullet_index \
                            in range(2, len(chosen_game.bullets)) :
                                chosen_game.bullets[bullet_index] = \
                                not randint(0, 1)
                        elif dice_sum == 6 :
                            player.hp -= 1
                            print("恶魔失去了1点生命")
                            if player.hp <= 0 :
                                break
                        elif dice_sum == 7 :
                            vanishable_indices: List[int] = []
                            for slotid,slot in enumerate(player.slots) :
                                if slot[1] is not None :
                                    if player.tools_sending_limit_in_game[
                                        slot[1]
                                    ] <= 0 :
                                        vanishable_indices.append(slotid)
                            if vanishable_indices :
                                vanish_index: int = choice(vanishable_indices)
                                player.slots[vanish_index] = \
                                (player.slots[vanish_index][0], None)
                        elif dice_sum == 8 :
                            pass
                        elif dice_sum == 9 :
                            if isinstance(player, NormalPlayer) and \
                               player.stamina < 32 :
                                player.stamina += 1
                        elif dice_sum == 10 :
                            player.hp += 1
                            print("恶魔获得了1点生命")
                        elif dice_sum == 11 :
                            if isinstance(player, NormalPlayer) and \
                               player.stamina < 32 :
                                player.stamina += 1
                                if player.stamina < 32 :
                                    player.stamina += 1
                        elif dice_sum == 12 :
                            if isinstance(player, NormalPlayer) :
                                player.attack_boost += 2
                                if randint(0, 1) :
                                    print("恶魔的攻击力提高了2点")
                        elif dice_sum == 13 :
                            victim.hp -= 1
                            print("你失去了1点生命")
                            if victim.hp <= 0 :
                                break
                        elif dice_sum == 14 :
                            k: int = 2 - (not randint(0, 2))
                            chosen_game.rel_turn_lap -= k
                            victim.stopped_turns += k
                        elif dice_sum == 15 :
                            victim.hp -= 2
                            print("你失去了2点生命")
                            if victim.hp <= 0 :
                                break
                        elif dice_sum == 18 :
                            victim.hp //= 8
                            print("你受到暴击!!!")
                            print("你的生命值:", victim.hp)
                elif slot[1] == 12 :
                    will_use = not randint(0, 1)
                    if will_use :
                        temporary_slots: List[int] = []
                        for slotid in range(len(player.slots)) :
                            if player.slots[slotid][0] > 0 :
                                temporary_slots.append(slotid)
                        if temporary_slots :
                            player.slots[slotid] = (slot[0], None)
                            delay_prob: float = len(temporary_slots) ** 0.5
                            for slotid in temporary_slots :
                                if random() < delay_prob :
                                    player.slots[slotid] = \
                                    (player.slots[slotid][0]+1,
                                     player.slots[slotid][1])
                elif slot[1] == 13 :
                    will_use = not randint(0, 7) and \
                               abs(victim.hp-player.hp) > 1
                    if will_use :
                        player.slots[slotid] = (slot[0], None)
                        if randint(0, 1) :
                            print("恶魔变成了你的样子")
                            player.hp = victim.hp
                            player.slots.clear()
                            player.slots.extend(victim.slots)
                            player.sending_total.clear()
                            player.sending_total.update(
                                victim.sending_total.copy()
                            )
                            player.stopped_turns = victim.stopped_turns
                            if isinstance(player, NormalPlayer) and \
                               isinstance(victim, NormalPlayer) :
                                player.attack_boost = victim.attack_boost
                                player.bulletproof.clear()
                                player.bulletproof.extend(victim.bulletproof)
                                player.bullet_catcher_level = \
                                victim.bullet_catcher_level
                                player.selfshoot_promises = \
                                victim.selfshoot_promises
                                player.againstshoot_promises = \
                                victim.againstshoot_promises
                                player.multishoot_level = \
                                victim.multishoot_level
                                player.comboshoot_level = \
                                victim.comboshoot_level
                                player.cursed_shoot_level = \
                                victim.cursed_shoot_level
                                player.hurts = victim.hurts
                                player.stamina = victim.stamina
                                player.begin_band_level = \
                                victim.begin_band_level
                                player.mid_band_level = victim.mid_band_level
                        else :
                            print("你变成了恶魔的样子")
                            victim.hp = player.hp
                            victim.slots.clear()
                            victim.slots.extend(player.slots)
                            victim.sending_total.clear()
                            victim.sending_total.update(
                                player.sending_total.copy()
                            )
                            victim.stopped_turns = player.stopped_turns
                            if isinstance(player, NormalPlayer) and \
                               isinstance(victim, NormalPlayer) :
                                victim.attack_boost = player.attack_boost
                                victim.bulletproof.clear()
                                victim.bulletproof.extend(player.bulletproof)
                                victim.bullet_catcher_level = \
                                player.bullet_catcher_level
                                victim.selfshoot_promises = \
                                player.selfshoot_promises
                                victim.againstshoot_promises = \
                                player.againstshoot_promises
                                victim.multishoot_level = \
                                player.multishoot_level
                                victim.comboshoot_level = \
                                player.comboshoot_level
                                victim.cursed_shoot_level = \
                                player.cursed_shoot_level
                                victim.hurts = player.hurts
                                victim.stamina = player.stamina
                                victim.begin_band_level = \
                                player.begin_band_level
                                victim.mid_band_level = player.mid_band_level
                        chosen_game.rel_turn_lap = 0
                elif slot[1] == 14 :
                    will_use = not randint(0, 2)
                    if isinstance(player, NormalPlayer) and will_use :
                        player.slots[slotid] = (slot[0], None)
                        player.bullet_catcher_level += 1
                elif slot[1] == 15 :
                    will_use = not randint(0, 3)
                    if will_use :
                        player.slots[slotid] = (slot[0], None)
                        fill_probability: float = 1 / len(chosen_game.bullets)
                        original_bullets: List[bool] = chosen_game.bullets[:]
                        for bullet_index in range(len(chosen_game.bullets)) :
                            if random() < fill_probability :
                                chosen_game.bullets[bullet_index] = True
                        if chosen_game.bullets != original_bullets :
                            print("弹夹有变动")
                elif slot[1] == 16 :
                    will_use = not randint(0, 3)
                    if will_use :
                        player.slots[slotid] = (slot[0], None)
                        shuffle(chosen_game.bullets)
                        print("恶魔重整了一下弹药")
                elif slot[1] == 17 :
                    if isinstance(player, NormalPlayer) :
                        will_use = all(chosen_game.bullets[
                            :player.multishoot_level+2
                        ]) if nightmare else not randint(0, 3)
                        if will_use :
                            player.slots[slotid] = (slot[0], None)
                            player.multishoot_level += 1
                elif slot[1] == 18 :
                    will_use = not randint(0, 3)
                    if isinstance(player, NormalPlayer) and will_use :
                        player.slots[slotid] = (slot[0], None)
                        player.comboshoot_level += 1
                elif slot[1] == 19 :
                    will_use = not randint(0, 9)
                    if will_use :
                        op_tools: List[int] = list(filter(
                            lambda x: chosen_game.has_tools(x),
                            (8, 13, 19, 29, 30, 31, 32)
                        ))
                        if op_tools :
                            if randint(0, 1) :
                                player.slots[slotid] = \
                                (slot[0], choice(op_tools))
                            else :
                                player.slots[slotid] = (slot[0], None)
                                player.hp //= 2
                elif slot[1] == 21 :
                    will_use = nightmare or not randint(0, 2)
                    if isinstance(player, NormalPlayer) and will_use :
                        player.slots[slotid] = (slot[0], None)
                        player.cursed_shoot_level += 1
                elif slot[1] == 22 :
                    will_use = not randint(0, 2)
                    if will_use :
                        player.slots[slotid] = (
                            slot[0], 24 if chosen_game.bullets.pop(randint(
                                0, len(chosen_game.bullets)-1
                            )) else 23
                        )
                        print("恶魔取出了一颗子弹")
                elif slot[1] == 23 :
                    will_use = not randint(0, 2)
                    if will_use :
                        player.slots[slotid] = (slot[0], None)
                        chosen_game.bullets.insert(randint(0, len(
                            chosen_game.bullets
                        )), False)
                        print("恶魔放入了一颗空弹")
                elif slot[1] == 24 :
                    will_use = not randint(0, 2)
                    if will_use :
                        player.slots[slotid] = (slot[0], None)
                        chosen_game.bullets.insert(randint(0, len(
                            chosen_game.bullets
                        )), True)
                        print("恶魔放入了一颗实弹")
                elif slot[1] == 25 :
                    will_use = not randint(0, 2)
                    if will_use :
                        player.slots[slotid] = (slot[0], None)
                        bullet_i_to_ins: int = randint(0, len(
                            chosen_game.bullets
                        ))
                        chosen_game.bullets.insert(bullet_i_to_ins, True)
                        if bullet_i_to_ins < len(chosen_game.bullets) - 1 :
                            chosen_game.bullets[bullet_i_to_ins+1] = \
                            not randint(0, 1)
                        print("恶魔放入了一颗神秘子弹")
                elif slot[1] == 26 :
                    if isinstance(player, NormalPlayer) :
                        will_use = player.hurts > player.begin_band_level + \
                                                  player.mid_band_level and \
                                   not randint(0, 1)
                        if will_use :
                            player.slots[slotid] = (slot[0], None)
                            player.begin_band_level += 1
                            print("恶魔使用了绷带")
                elif slot[1] == 27 :
                    will_use = not randint(0, 4)
                    if will_use :
                        player.slots[slotid] = (slot[0], None)
                        if player.hp < 2 :
                            player.hp += 5
                            print("恶魔使用了医疗包,回复了5点生命")
                        elif player.hp < 5 :
                            player.hp += 4
                            print("恶魔使用了医疗包,回复了4点生命")
                        elif player.hp < 9 :
                            player.hp += 3
                            print("恶魔使用了医疗包,回复了3点生命")
                        elif player.hp < 14 :
                            player.hp += 2
                            print("恶魔使用了医疗包,回复了2点生命")
                        else :
                            player.hp += 1
                            print("恶魔使用了医疗包,回复了1点生命")
                        if isinstance(player, NormalPlayer) :
                            if player.hurts < 1 :
                                player.hp += 2
                            elif player.hurts < 4 :
                                player.hp += 1
                            player.hurts = 0
                elif slot[1] == 28 :
                    will_use = not (not chosen_game.bullets.count(True) >> 1
                                    if nightmare else randint(0, 5))
                    if will_use :
                        player.slots[slotid] = (slot[0], None)
                        while chosen_game.bullets :
                            print("恶魔排出了一颗实弹" \
                                  if chosen_game.bullets.pop(0) \
                                  else "恶魔排出了一颗空弹")
                elif slot[1] == 29 :
                    will_use = not randint(0, 7)
                    if will_use :
                        player.slots[slotid] = (slot[0], None)
                        chosen_game.copy_bullets_for_new()
                elif slot[1] == 31 :
                    will_use = nightmare or not randint(0, 5)
                    if will_use :
                        player.slots[slotid] = (slot[0], None)
                        chosen_game.rel_turn_lap -= len(chosen_game.bullets)
                        victim.stopped_turns += len(chosen_game.bullets)
                        print("恭喜恶魔,成功把你变成了{0}!".format(cat_girl))
                elif slot[1] == 32 :
                    will_use = not randint(0, 9)
                    if will_use :
                        evil_hp: int = randint(1, player.hp)
                        print("恶魔以", evil_hp, "生命值向你发起了擂台战")
                        if victim.controllable :
                            if victim.hp == 1 :
                                print("你以仅有的 1 生命值应战")
                                victim.hp -= 1
                                player.hp -= evil_hp
                                parent_game.subgame = StageGame(
                                    1, evil_hp, False
                                )
                                sub_game = parent_game.subgame
                                chosen_game = \
                                parent_game if sub_game is None else sub_game
                                if isinstance(sub_game, StageGame) :
                                    sub_game.gen_bullets()
                            else :
                                while True :
                                    try :
                                        your_hp: int = int(input(
                                            "请输入你要作为赌注的生命值"
                                            "(1~{0}):".format(victim.hp)
                                        ))
                                        if 0 < your_hp <= victim.hp :
                                            victim.hp -= your_hp
                                            player.hp -= evil_hp
                                            parent_game.subgame = StageGame(
                                                your_hp, evil_hp, False
                                            )
                                            sub_game = parent_game.subgame
                                            chosen_game = \
                                            parent_game if sub_game is None \
                                            else sub_game
                                            if isinstance(sub_game, StageGame):
                                                sub_game.gen_bullets()
                                            break
                                    except ValueError :
                                        pass
                        else :
                            your_hp = randint(1, victim.hp)
                            print("你以", your_hp, "生命值应战")
                            victim.hp -= your_hp
                            player.hp -= evil_hp
                            parent_game.subgame = StageGame(
                                your_hp, evil_hp, False
                            )
                            sub_game = parent_game.subgame
                            chosen_game = \
                            parent_game if sub_game is None else sub_game
                            if isinstance(sub_game, StageGame) :
                                sub_game.gen_bullets()
                        break
                elif slot[1] == 33 :
                    will_use = nightmare or not randint(0, 4)
                    if will_use and isinstance(chosen_game, NormalGame) and \
                       chosen_game.explosion_exponent > 0 :
                        player.slots[slotid] = (slot[0], None)
                        chosen_game.explosion_exponent = int(
                            Fraction(2, 3)*chosen_game.explosion_exponent
                        )
                        print("恶魔维修了一下枪筒")
                elif slot[1] == 34 :
                    will_use = nightmare or not randint(0, 4)
                    if will_use :
                        player.slots[slotid] = (slot[0], None)
                        false_count: int = 0
                        while False in chosen_game.bullets :
                            false_count += 1
                            chosen_game.bullets.remove(False)
                        for _ in range(false_count) :
                            chosen_game.bullets.append(False)
                        for i in chosen_game.extra_bullets :
                            if i is not None :
                                false_count = 0
                                while False in i :
                                    false_count += 1
                                    i.remove(False)
                                for _ in range(false_count) :
                                    i.append(False)
                        print("弹夹进行了空实分离")
                elif slot[1] == 35 :
                    will_use = \
                    any(chosen_game.extra_bullets) and not randint(0, 4)
                    if will_use :
                        player.slots[slotid] = (slot[0], None)
                        for i in chosen_game.extra_bullets :
                            if i :
                                chosen_game.bullets.extend(i)
                                i.clear()
                        print("恶魔合并了一下弹夹")
            if not chosen_game.bullets :
                break
            round_turn_count += 1
            period_turn_count += 1
            total_turn_count += 1
            gamesave.play_turns += 1
            true_on_r = False
            true_on_e = False
            if isinstance(player, NormalPlayer) and player.stamina > 0 :
                player.stamina -= 1
            is_to_self: bool = (
                ((not player.cursed_shoot_level) != chosen_game.bullets[0]) if
                nightmare and player.breakcare_rounds <= 0 else
                not randint(0, 1)
            ) if isinstance(player, NormalPlayer) else not (
                chosen_game.bullets[0] if nightmare else randint(0, 1)
            )
            if is_to_self :
                if isinstance(player, NormalPlayer) and \
                   player.cursed_shoot_level > 0 :
                    shoot_result = chosen_game.shoot(True, False, 1.)
                    player.cursed_shoot_level -= 1
                elif isinstance(player, NormalPlayer) and \
                     player.selfshoot_promises > 0 :
                    shoot_result = chosen_game.shoot(True, False, 0.)
                    player.selfshoot_promises -= 1
                else :
                    shoot_result = chosen_game.shoot(True, False)
                print("恶魔将枪口对准了自己")
                for bullets_i in shoot_result :
                    if bullets_i is not None :
                        if bullets_i[1] :
                            print("啊哦,子弹居然炸膛了!")
                            if isinstance(victim, NormalPlayer) and \
                               victim.bullet_catcher_level :
                                if bullets_i[0] :
                                    if random() < (
                                        1-0.8**victim.bullet_catcher_level
                                    ) / (1+player.attack_boost if
                                         isinstance(player, NormalPlayer) else
                                         1):
                                        gamesave.bullets_caught += 1
                                        victim.bullet_catcher_level = 0
                                        chosen_game.bullets.append(True)
                                        if victim.stamina > 0 :
                                            victim.stamina -= 1
                                        print("你接住了一颗子弹")
                                        continue
                                else :
                                    if random() < 0.8 / (
                                        1+player.attack_boost if
                                        isinstance(player, NormalPlayer) else 1
                                    ) :
                                        gamesave.bullets_caught += 1
                                        victim.bullet_catcher_level -= 1
                                        chosen_game.bullets.append(False)
                                        if victim.stamina > 0 :
                                            victim.stamina -= 1
                                        print("你接住了一颗子弹")
                                        continue
                            if isinstance(victim, NormalPlayer) and \
                               victim.bulletproof :
                                victim.bulletproof[0] -= \
                                randint(1, ceil((player.attack_boost+1)**0.5))\
                                if isinstance(player, NormalPlayer) else 1
                                print("你的防弹衣承受了这次撞击")
                                if victim.bulletproof[0] <= 0 :
                                    if random() >= \
                                       2 ** (victim.bulletproof[0]-1) :
                                        del victim.bulletproof[0]
                                        victim.breakcare_potential += 1
                                        if not victim.bulletproof :
                                            for _ in \
                                            range(victim.breakcare_potential) :
                                                if random() < 0.15 :
                                                    victim.breakcare_rounds +=1
                                            victim.breakcare_potential = 0
                                        print("你的一件防弹衣爆了")
                            elif bullets_i[0] :
                                true_on_r = True
                                print("运气非常差,是个实弹!")
                                for _ in range(
                                    base_attack+player.attack_boost if
                                    isinstance(player, NormalPlayer) else
                                    base_attack
                                ) :
                                    if isinstance(victim, NormalPlayer) and \
                                       random() < victim.hurts / 8. :
                                        victim.hp -= 2
                                        gamesave.damage_caught += 2
                                    else :
                                        victim.hp -= 1
                                        gamesave.damage_caught += 1
                                print("你的生命值:", victim.hp)
                                if isinstance(victim, NormalPlayer) and \
                                   random() >= victim.hurts / 8. :
                                    victim.hurts += 1
                                    assert 0 <= victim.hurts < 9
                            else :
                                print("很幸运,是个空弹")
                        else :
                            if bullets_i[0] :
                                true_on_e = True
                                print("“砰!”一声枪响,它自杀了,你心里暗喜")
                                for _ in range(
                                    base_attack+player.attack_boost if
                                    isinstance(player, NormalPlayer) else
                                    base_attack
                                ) :
                                    player.hp -= \
                                    2 if isinstance(player, NormalPlayer) and \
                                         random() < player.hurts / 8. else 1
                                print("恶魔生命值:", player.hp)
                                if isinstance(player, NormalPlayer) and \
                                   random() >= player.hurts / 8. :
                                    player.hurts += 1
                                    assert 0 <= player.hurts < 9
                            else :
                                print("“啊哈!,是个空弹!”恶魔嘲讽道")
            else :
                shoot_combo_addition = 0
                if isinstance(player, NormalPlayer) :
                    comboshoot_consume_num = 0
                    while shoot_combo_addition < len(chosen_game.bullets) :
                        comboshoot_consume_num += 1
                        if random() >= 0.5 ** player.comboshoot_level :
                            shoot_combo_addition += 1
                        else :
                            break
                    if shoot_combo_addition == len(chosen_game.bullets) :
                        chosen_game.rel_turn_lap -= 1
                        victim.stopped_turns += 1
                    player.comboshoot_level -= comboshoot_consume_num
                    if player.comboshoot_level < 0 :
                        player.comboshoot_level = 0
                    if player.cursed_shoot_level > 0 :
                        shoots_result = chosen_game.shoots(
                            False, False, 1.,
                            shoot_combo_addition+player.multishoot_level+1 \
                            if shoot_combo_addition+player.multishoot_level<\
                               len(chosen_game.bullets) \
                            else len(chosen_game.bullets)
                        )
                        player.cursed_shoot_level -= 1
                    elif player.againstshoot_promises > 0 or nightmare :
                        shoots_result = chosen_game.shoots(
                            False, False, 0.,
                            1 if isinstance(chosen_game, StageGame) else (
                                shoot_combo_addition+player.multishoot_level+1
                                if shoot_combo_addition+player.multishoot_level<
                                   len(chosen_game.bullets)
                                else len(chosen_game.bullets)
                            )
                        )
                        if player.againstshoot_promises :
                            player.againstshoot_promises -= 1
                    else :
                        shoots_result = chosen_game.shoots(
                            False, False,
                            combo=1 if isinstance(chosen_game, StageGame) else (
                                shoot_combo_addition+player.multishoot_level+1
                                if shoot_combo_addition+player.multishoot_level<
                                   len(chosen_game.bullets)
                                else len(chosen_game.bullets)
                            )
                        )
                else :
                    shoots_result = chosen_game.shoots(False, False)
                base_shoot = True
                print("恶魔朝你开了一枪")
                for shoot_result in shoots_result :
                    if shoot_result[0] is not None :
                        if base_shoot :
                            base_shoot = False
                        elif shoot_combo_addition :
                            shoot_combo_addition -= 1
                        elif isinstance(player, NormalPlayer) :
                            player.multishoot_level -= 1
                    for bullets_i in shoot_result :
                        if bullets_i is not None :
                            if bullets_i[1] :
                                print("啊哦,子弹居然炸膛了!")
                                if bullets_i[0] :
                                    true_on_e = True
                                    print("“砰!”一声枪响,它自杀了,你心里暗喜")
                                    for _ in range(
                                        base_attack+player.attack_boost if
                                        isinstance(player, NormalPlayer) else
                                        base_attack
                                    ):
                                        player.hp -= \
                                        2 if isinstance(player, NormalPlayer) \
                                             and random() < player.hurts / 8. \
                                        else 1
                                    print("恶魔生命值:", player.hp)
                                    if isinstance(player, NormalPlayer) and \
                                       random() >= player.hurts / 8. :
                                        player.hurts += 1
                                        assert 0 <= player.hurts < 9
                                else :
                                    print("“啊哈!,是个空弹!”恶魔嘲讽道")
                            else :
                                if isinstance(victim, NormalPlayer) and \
                                   victim.bullet_catcher_level :
                                    if bullets_i[0] :
                                        if random() < (
                                            1-0.8**victim.bullet_catcher_level
                                        ) / (1+player.attack_boost if
                                             isinstance(player, NormalPlayer)
                                             else 1) :
                                            gamesave.bullets_caught += 1
                                            victim.bullet_catcher_level = 0
                                            chosen_game.bullets.append(True)
                                            if victim.stamina > 0 :
                                                victim.stamina -= 1
                                            print("你接住了一颗子弹")
                                            continue
                                    else :
                                        if random() < 0.8 / (
                                            1+player.attack_boost if
                                            isinstance(player, NormalPlayer)
                                            else 1
                                        ):
                                            gamesave.bullets_caught += 1
                                            victim.bullet_catcher_level -= 1
                                            chosen_game.bullets.append(False)
                                            if victim.stamina > 0 :
                                                victim.stamina -= 1
                                            print("你接住了一颗子弹")
                                            continue
                                if isinstance(victim, NormalPlayer) and \
                                   victim.bulletproof :
                                    victim.bulletproof[0] -= randint(1, ceil(
                                        (player.attack_boost+1)**0.5
                                    ))if isinstance(player, NormalPlayer)else 1
                                    print("你的防弹衣承受了这次撞击")
                                    if victim.bulletproof[0] <= 0 :
                                        if random() >= \
                                           2 ** (victim.bulletproof[0]-1) :
                                            del victim.bulletproof[0]
                                            victim.breakcare_potential += 1
                                            if not victim.bulletproof :
                                                for _ in \
                                                range(victim.breakcare_potential) :
                                                    if random() < 0.15 :
                                                        victim.breakcare_rounds += 1
                                                victim.breakcare_potential = 0
                                            print("你的一件防弹衣爆了")
                                elif bullets_i[0] :
                                    true_on_r = True
                                    print("运气非常差,是个实弹!")
                                    for _ in range(
                                        base_attack+player.attack_boost if
                                        isinstance(player, NormalPlayer) else
                                        base_attack
                                    ):
                                        if isinstance(victim, NormalPlayer) \
                                           and random() < victim.hurts / 8. :
                                            victim.hp -= 2
                                            gamesave.damage_caught += 2
                                        else :
                                            victim.hp -= 1
                                            gamesave.damage_caught += 1
                                    print("你的生命值:", victim.hp)
                                    if isinstance(victim, NormalPlayer) and \
                                       random() >= victim.hurts / 8. :
                                        victim.hurts += 1
                                        assert 0 <= victim.hurts < 9
                                else :
                                    print("很幸运,是个空弹")
            if isinstance(victim, NormalPlayer) and not true_on_r and \
               victim.stamina < 32 and random() < 1. / (victim.hurts+1) :
                victim.stamina += 1
            if isinstance(player, NormalPlayer) and not true_on_e and \
               player.stamina < 32 and random() < 1. / (player.hurts+1) :
                player.stamina += 1
            if isinstance(victim, NormalPlayer) and victim.stamina < 8 and \
               random() < 1 - (victim.stamina/8.) :
                chosen_game.rel_turn_lap -= 1
                victim.stopped_turns += 1
            if isinstance(player, NormalPlayer) and player.stamina < 8 and \
               random() < 1 - (player.stamina/8.) :
                chosen_game.rel_turn_lap += 1
                player.stopped_turns += 1
            if isinstance(player, NormalPlayer) :
                player.attack_boost = 0
            gamesave.active_gametime += time() - gametime_time_start
        if not debug :
            gamesave.add_exp()

if chosen_game.players[1].controllable :
    if chosen_game.players[0].alive :
        print("恭喜玩家 0 ,成功把玩家 1 变成了{0}!".format(cat_girl))
    elif chosen_game.players[1].alive :
        print("恭喜玩家 1 ,成功把玩家 0 变成了{0}!".format(cat_girl))
    else :
        print("你们最后同归于尽了")
elif chosen_game.r_hp > 0 :
    if chosen_game.e_hp == 0 :
        print("恭喜你,成功把恶魔变成了{0}!".format(cat_girl))
    elif chosen_game.e_hp == -1 :
        print("恭喜你,成功把恶魔打得体无完肤!")
    elif chosen_game.e_hp == -2 :
        print("恭喜你,成功把恶魔化作一团灰烬!")
    else :
        print("恭喜你,成功让恶魔原地消失!")
elif chosen_game.r_hp == 0 :
    if chosen_game.e_hp > 0 :
        print("唉....你被恶魔变成了{0}".format(cat_girl))
    elif chosen_game.e_hp == 0 :
        print("你们最后同归于尽了")
        gamesave.add_exp(25)
        gamesave.add_coins()
    elif chosen_game.e_hp == -1 :
        print("你让恶魔面目全非,但你也付出了生命的代价")
        gamesave.add_exp(80)
        gamesave.add_coins(3)
    elif chosen_game.e_hp == -2 :
        print("恶魔为你化作灰烬,而你成为了{0}".format(cat_girl))
        gamesave.add_exp(400)
        gamesave.add_coins(10)
    else :
        print("你作为{0}看着恶魔消失于世上".format(cat_girl))
        gamesave.add_exp(1500)
        gamesave.add_coins(32)
elif chosen_game.r_hp == -1 :
    if chosen_game.e_hp > 0 :
        print("唉....你被恶魔打得体无完肤")
    elif chosen_game.e_hp == 0 :
        print("恶魔让你面目全非,但他也付出了生命的代价")
        gamesave.add_exp(80)
        gamesave.add_coins(3)
    elif chosen_game.e_hp == -1 :
        print("二人幸终……")
        gamesave.add_exp(400)
        gamesave.add_coins(10)
    elif chosen_game.e_hp == -2 :
        print("恶魔为你化作灰烬,而你也面目狼狈……")
        gamesave.add_exp(1500)
        gamesave.add_coins(32)
    else :
        print("你用残缺的身躯彻底送走了恶魔")
        gamesave.add_exp(4800)
        gamesave.add_coins(100)
elif chosen_game.r_hp == -2 :
    if chosen_game.e_hp > 0 :
        print("唉....你被恶魔化作一团灰烬")
    elif chosen_game.e_hp == 0 :
        print("你为恶魔化作灰烬,而它成为了{0}".format(cat_girl))
        gamesave.add_exp(400)
        gamesave.add_coins(10)
    elif chosen_game.e_hp == -1 :
        print("你为恶魔化作灰烬,而它也面目狼狈……")
        gamesave.add_exp(1500)
        gamesave.add_coins(32)
    elif chosen_game.e_hp == -2 :
        print("你们化作了两团灰烬")
        gamesave.add_exp(4800)
        gamesave.add_coins(100)
    else:
        print("")
        gamesave.add_exp(16000)
        gamesave.add_coins(320)
else :
    if chosen_game.e_hp > 0 :
        print("唉....恶魔让你人间蒸发了")
    elif chosen_game.e_hp == 0 :
        print("恶魔作为{0}看着你消失于世上".format(cat_girl))
        gamesave.add_exp(1500)
        gamesave.add_coins(32)
    elif chosen_game.e_hp == -1 :
        print()
        gamesave.add_exp(4800)
        gamesave.add_coins(100)
    elif chosen_game.e_hp == -2 :
        print()
        gamesave.add_exp(16000)
        gamesave.add_coins(320)
    else :
        print("你们俩仿佛从来没存在过一般")
        gamesave.add_exp(54000)
        gamesave.add_coins(1000)

gamesave.play_periods += 1
gamesave.game_runs += 1
print("================================")
print("本次游戏持续了", total_turn_count, "轮,")
print(total_round_count, "回合,")
print(total_period_count, "周目")

try :
    with open("emlpd.dat", "wb") as gamesave_file :
        gamesave_file.write(gamesave.serialize())
except OSError as err :
    print("存档时遇到问题!", err)
