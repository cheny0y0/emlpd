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

from .gameapi import Game, GameSave, I18nText, Player, ShootResult, Slot, \
                     VER_STRING
from .gameinst import GAMEMODE_SET, NormalGame, NormalPlayer, StageGame, Texts

print("""emlpd  Copyright (C) 2024-2025  REGE
This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
This is free software, and you are welcome to redistribute it
under certain conditions; type `show c' for details.""")

gamesave: GameSave = GameSave()
gamemode_i: int = 1
gamesave_filename: str = "emlpd.dat"

for i in argv[1:] :
    if i.startswith("lang=") :
        I18nText.selected_lang = i[5:]
    elif i.startswith("save=") :
        gamesave_filename = i[5:]
print(Texts.GAME_TITLE, "v"+VER_STRING)
debug: bool = "debug" in argv[1:]
nightmare: bool = "nightmare" in argv[1:]
skipthread: bool = "skipthread" in argv[1:]
cat_girl: I18nText = I18nText(chr(
    32848+3365*(-1)**((date.today().month<<5)|date.today().day!=129)
) + chr(29888+6824*(-1)**((date.today().month<<5)|date.today().day!=129)+
        ((date.today().month<<5)|date.today().day==129)), en_en="Cat Girl")

try :
    with open(gamesave_filename, "rb") as gamesave_file :
        gamesave = GameSave.unserialize(gamesave_file.read())
except FileNotFoundError :
    pass
except Exception as err :
    if debug :
        print(repr(err))
    input(I18nText(
        "读取存档遇到问题。按下回车创建一个新的存档。",
        en_en="Problem reading game save. Press enter to create a new save."
    ))

if nightmare :
    print(I18nText(
        "警告:梦魇模式已激活。恶魔会变得无比强大!!!",
        en_en="WARNING: NIGHTMARE MODE ACTIVATED. THE EVIL WILL BE "
              "EXTRAORDINARILY STRONG!!!"
    ))
print(I18nText(
    "“哦!看看,又一个来送死的”",
    en_en="“Oh! Look, someone looking for death again”"
))
if not skipthread :
    sleep(2.5)
print(I18nText(
    "“希望你能让我玩的尽兴”", en_en="“Hope you'll be played joyfully by me”"
))
if not skipthread :
    sleep(2.5)
print(I18nText("“现在开始我们的游戏吧”", en_en="“Let's now start our game”"))
if not skipthread :
    sleep(1.5)

print(I18nText("当前等级:", en_en="Current LVL:"), gamesave.level)
print(I18nText("当前经验:", en_en="Current EXP:"), gamesave.exp, "/",
      250*(gamesave.level+1))
print(I18nText("当前金币数:", en_en="Current gold coin count:"),
      gamesave.coins, "/ 65535")
if not skipthread :
    sleep(2)

print(I18nText("输入“stat”以查看统计信息。", en_en="Input “stat” for stats."))
for k, v in GAMEMODE_SET.items() :
    if len(v) > 4 :
        print(Texts.GAME_MODE.format(k), v[3])
        if v[4] is None :
            print(Texts.NO_INTRODUCTION)
        else :
            print(Texts.INTRODUCTION, v[4])
    else :
        print(Texts.GAME_MODE, k)
        print(Texts.NO_NAME)

while 1 :
    gamemode: str = input(Texts.CHOOSE_GAME_MODE)
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
    if not (chosen_game.players[0].alive and chosen_game.players[1].alive) :
        if chosen_game is sub_game :
            if isinstance(sub_game, StageGame) :
                if sub_game.players[1].controllable :
                    if not sub_game.players[0].alive :
                        print(Texts.PLAYER_1_WON_STAGE)
                        parent_game.players[1].hp += sub_game.tot_hp
                    elif not sub_game.players[1].alive :
                        print(Texts.PLAYER_0_WON_STAGE)
                        parent_game.players[0].hp += sub_game.tot_hp
                elif not sub_game.players[0].alive :
                    print(Texts.E_WON_STAGE)
                    parent_game.players[1].hp += sub_game.tot_hp
                elif not sub_game.players[1].alive :
                    print(Texts.R_WON_STAGE)
                    parent_game.players[0].hp += sub_game.tot_hp
            parent_game.subgame = None
            chosen_game = parent_game
        else :
            try :
                if not chosen_game.players[1].alive :
                    if nightmare and not chosen_game.players[1].controllable :
                        gamesave.add_exp(max(ceil(10*(
                            2-chosen_game.players[1].hp
                        )*GAMEMODE_SET[gamemode_i][2]), 0))
                    elif not debug :
                        gamesave.add_exp(max(10*(
                            2-chosen_game.players[1].hp
                        ), 0))
                    if not debug :
                        gamesave.add_coins()
                parent_game = next(chosen_games)
                sub_game = parent_game.subgame
                chosen_game = parent_game if sub_game is None else sub_game
                try :
                    with open(gamesave_filename, "wb") as gamesave_file :
                        gamesave_file.write(gamesave.serialize())
                except OSError as err :
                    print(Texts.PROBLEM_SAVING, err)
                total_period_count += 1
                gamesave.play_periods += 1
                print("================")
                print(Texts.PERIOD_COUNT_INFO.format(
                    period_turn_count, period_round_count
                ))
                round_turn_count = 0
                period_turn_count = 0
                period_round_count = 0
                base_attack = 1
                print("===", Texts.PERIOD_ORDINAL.format(total_period_count),
                      "===")
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
                    print(Texts.R_SLOT_EXPIRED.format(
                        chosen_game.tools[tool_id][0]
                    ))
                elif i == 1 and not chosen_game.players[1].controllable :
                    print(Texts.E_SLOT_EXPIRED.format(
                        chosen_game.tools[tool_id][0]
                    ))
                else :
                    print(Texts.R_SLOT_EXPIRED.format(
                        chosen_game.tools[tool_id][0], i
                    ))
    sleep(1)
    for i, player in chosen_game.players.items() :
        if player.controllable or i != 1 :
            new_slot: Optional[int] = chosen_game.send_slot(player)
            if new_slot is not None :
                if new_slot > 0 :
                    if i == 0 and not chosen_game.players[1].controllable :
                        print(Texts.R_TEMP_SLOT_SENT.format(new_slot))
                    else :
                        print(Texts.PLAYER_TEMP_SLOT_SENT.format(new_slot, i))
                elif i == 0 and not chosen_game.players[1].controllable :
                    print(Texts.R_PERMASLOT_SENT)
                else :
                    print(Texts.PLAYER_PERMASLOT_SENT.format(i))
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
                    print(Texts.E_TEMP_SLOT_SENT.format(new_slot))
                else :
                    print(Texts.E_PERMASLOT_SENT)
    any_player_has_tools: bool = False
    for i, player in chosen_game.players.items() :
        if chosen_game.has_tools(player=player) :
            any_player_has_tools = True
            if player.controllable or i != 1 :
                if i == 0 and not chosen_game.players[1].controllable :
                    print(Texts.R_TOOL_SENT.format(chosen_game.send_tools(
                        player, GAMEMODE_SET[gamemode_i][1]
                    )))
                else :
                    print(Texts.PLAYER_TOOL_SENT.format(chosen_game.send_tools(
                        player, GAMEMODE_SET[gamemode_i][1]
                    ), i))
            else :
                print(Texts.E_TOOL_SENT.format(chosen_game.send_tools(
                    player, GAMEMODE_SET[gamemode_i][1]
                )))
    if any_player_has_tools :
        sleep(1)
    chosen_game.gen_bullets()
    print(Texts.BULLET_TOTAL.format(len(chosen_game.bullets)))
    sleep(1)
    print(Texts.TRUES_FALSES_COUNT.format(
        chosen_game.bullets.count(True), chosen_game.bullets.count(False)
    ))
    shoot_result: ShootResult
    shoots_result: List[ShootResult]
    shoot_combo_addition: int
    comboshoot_consume_num: int
    base_shoot: bool
    gamesave.active_gametime += time() - gametime_time_start
    while chosen_game.bullets :
        gametime_time_start = time()
        try :
            with open(gamesave_filename, "wb") as gamesave_file :
                gamesave_file.write(gamesave.serialize())
        except OSError as err :
            print(Texts.PROBLEM_SAVING, err)
        if not (chosen_game.players[0].alive and chosen_game.players[1].alive):
            break
        if chosen_game.players[0].stopped_turns > 0 :
            print(Texts.R_DAZING.format(cat_girl))
        elif chosen_game.players[1].stopped_turns > 0 :
            print(Texts.OPPO_DAZING if chosen_game.players[1].controllable else
                  Texts.E_DAZING)
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
                    print(Texts.YOUR_TURN)
                else :
                    print(Texts.PLAYER_TURN.format(chosen_game.turn_orders[0]))
                print(
                    Texts.OPER_CHOOSE_1078 if chosen_game.has_tools() or any(
                        x.count_tools(None) < len(x.slots)
                        for x in chosen_game.players.values()
                    ) else Texts.OPER_CHOOSE_10
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
                print(Texts.TOOL_WAREHOUSE)
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
                        print(Texts.TOOL_NAME_MORE.format(
                            k, chosen_game.tools[k][0], v
                        ))
                    else :
                        print(Texts.TOOL_NAME_ONE.format(
                            k, chosen_game.tools[k][0]
                        ))
                    if chosen_game.tools[k][1] is None :
                        print(Texts.TOOL_NO_DESC)
                    else :
                        print(Texts.TOOL_DESC, chosen_game.tools[k][1])
                for slot in player.slots :
                    if slot[1] is not None and slot[0] > 0 :
                        print(Texts.TOOL_NAME_ONE.format(
                            slot[1], chosen_game.tools[slot[1]][0]
                        ))
                        if chosen_game.tools[slot[1]][1] is None :
                            print(Texts.TOOL_NO_DESC)
                        else :
                            print(Texts.TOOL_DESC,
                                  chosen_game.tools[slot[1]][1])
                        print(Texts.SLOT_EXPIRED_AT.format(slot[0]))
                if not tools_existence :
                    print(Texts.TOOL_WAREHOUSE_EMPTY)
                while tools_existence :
                    print(Texts.ENTER_TO_RETURN)
                    to_use: Optional[int] = None
                    try:
                        to_use = int(input(Texts.INPUT_ID_TO_USE))
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
                                print(Texts.R_USES_ID2)
                        elif to_use == 3 :
                            player.slots[tools_existence[3]] = \
                            (player.slots[tools_existence[3]][0], None)
                            print(Texts.R_USES_ID3[chosen_game.bullets.pop(0)])
                        elif to_use == 4 :
                            player.slots[tools_existence[4]] = \
                            (player.slots[tools_existence[4]][0], None)
                            chosen_game.rel_turn_lap += 1
                            victim.stopped_turns += 1
                            print(Texts.R_USES_ID4)
                        elif to_use == 5 :
                            player.slots[tools_existence[5]] = \
                            (player.slots[tools_existence[5]][0], None)
                            heal_succeeded: bool = \
                            player.hp <= 3 + player.hurts / 4. or \
                            (random() < 0.5 ** (player.hp-3-player.hurts/4.)
                             and not nightmare) \
                            if isinstance(player, NormalPlayer) else \
                            player.hp <= 3 or \
                            (random() < 0.5 ** (player.hp-3) and not nightmare)
                            if heal_succeeded :
                                player.hp += 1
                                gamesave.healed += 1
                            print(Texts.R_USES_ID5[heal_succeeded])
                        elif to_use == 6 :
                            player.slots[tools_existence[6]] = \
                            (player.slots[tools_existence[6]][0], None)
                            print(Texts.R_USES_ID6[chosen_game.bullets[0]])
                            if chosen_game.extra_bullets[0] is not None :
                                if chosen_game.extra_bullets[0] :
                                    print(Texts.R_USES_ID6[
                                        chosen_game.extra_bullets[0][0]
                                    ])
                                if chosen_game.extra_bullets[1] is not None :
                                    if chosen_game.extra_bullets[1] :
                                        print(Texts.R_USES_ID6[
                                            chosen_game.extra_bullets[1][0]
                                        ])
                                    if chosen_game.extra_bullets[2] is not \
                                       None and chosen_game.extra_bullets[2] :
                                        print(Texts.R_USES_ID6[
                                            chosen_game.extra_bullets[2][0]
                                        ])
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
                                    print(Texts.TOOL_PLUS_1.format(
                                        bring_tool_id
                                    ))
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
                                print(Texts.R_USES_ID9)
                                player.bulletproof.insert(0, 3)
                        elif to_use == 11 :
                            player.slots[tools_existence[11]] = \
                            (player.slots[tools_existence[11]][0], None)
                            dice_sum: int = \
                            randint(1, 6) + randint(1, 6) + randint(1, 6)
                            if debug :
                                print(Texts.R_USES_ID11.format(dice_sum))
                            if dice_sum == 3 :
                                if isinstance(player, NormalPlayer) :
                                    player.breakcare_rounds += 2
                            elif dice_sum == 4 :
                                player.hp -= 2
                                print(Texts.R_LOST_2_HP)
                            elif dice_sum == 5 :
                                for bullet_index \
                                in range(2, len(chosen_game.bullets)) :
                                    chosen_game.bullets[bullet_index] = \
                                    not randint(0, 1)
                            elif dice_sum == 6 :
                                player.hp -= 1
                                print(Texts.R_LOST_1_HP)
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
                                print(Texts.R_GOT_1_HP)
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
                                        print(Texts.R_ATTACK_BOOSTED_2)
                            elif dice_sum == 13 :
                                victim.hp -= 1
                                print(
                                    Texts.OPPO_LOST_1_HP if victim.controllable
                                    else Texts.E_LOST_1_HP
                                )
                            elif dice_sum == 14 :
                                k: int = 2 - (not randint(0, 2))
                                chosen_game.rel_turn_lap += k
                                victim.stopped_turns += k
                            elif dice_sum == 15 :
                                victim.hp -= 2
                                print(
                                    Texts.OPPO_LOST_2_HP if victim.controllable
                                    else Texts.E_LOST_2_HP
                                )
                            elif dice_sum == 18 :
                                victim.hp //= 8
                                if victim.controllable :
                                    print(Texts.OPPO_CRIT)
                                    print(Texts.OPPO_CUR_HP.format(victim.hp))
                                else :
                                    print(Texts.E_CRIT)
                                    print(Texts.E_CUR_HP.format(victim.hp))
                                gamesave.add_exp(6)
                        elif to_use == 12 :
                            temporary_slots: List[int] = []
                            for slotid in range(len(player.slots)) :
                                if player.slots[slotid][0] > 0 :
                                    temporary_slots.append(slotid)
                            if temporary_slots :
                                player.slots[tools_existence[12]] = \
                                (player.slots[tools_existence[12]][0], None)
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
                                print(Texts.R_TURNED_INTO_OPPO
                                      if victim.controllable
                                      else Texts.R_TURNED_INTO_E)
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
                                print(Texts.OPPO_TURNED_INTO_R
                                      if victim.controllable
                                      else Texts.E_TURNED_INTO_R)
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
                                print(Texts.CLIP_CHANGED)
                        elif to_use == 16 :
                            former_bullets: List[bool] = chosen_game.bullets[:]
                            chosen_game.bullets.clear()
                            print(Texts.BEFORE_USE_ID16)
                            for i in range(len(former_bullets)) :
                                for bullet_index in range(i) :
                                    print(end=str(bullet_index))
                                    print(end=Texts.DURING_USE_ID16[
                                        chosen_game.bullets[bullet_index]
                                    ].string)
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
                                    print(end=Texts.DURING_USE_ID16[
                                        chosen_game.bullets[bullet_index]
                                    ].string)
                                print(len(chosen_game.bullets))
                                print(Texts.R_USES_ID16)
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
                                    Texts.BEFORE_USE_ID22_1
                                ).strip().lower() in ("y", "0") :
                                    player.slots[tools_existence[22]] = \
                                    (player.slots[tools_existence[22]][0],
                                     24 if chosen_game.bullets.pop(0) else 23)
                                    print(Texts.R_USES_ID22)
                                    print(Texts.TOOL_PLUS_1.format(
                                        player.slots[tools_existence[22]][1]
                                    ))
                                else :
                                    used = False
                            else :
                                try :
                                    bullet_i_to_pick: int = int(input(
                                        Texts.BEFORE_USE_ID22.format(
                                            len(chosen_game.bullets)-1
                                        )
                                    ))
                                    if 0 <= bullet_i_to_pick < \
                                       len(chosen_game.bullets) :
                                        player.slots[tools_existence[22]] = \
                                        (player.slots[tools_existence[22]][0],
                                         24 if chosen_game.bullets.pop(
                                            bullet_i_to_pick
                                        ) else 23)
                                        print(Texts.R_USES_ID22)
                                        print(Texts.TOOL_PLUS_1.format(
                                            player.slots[
                                                tools_existence[22]
                                            ][1]
                                        ))
                                    else :
                                        used = False
                                except ValueError :
                                    used = False
                        elif to_use == 23 :
                            try :
                                bullet_i_to_ins: int = int(input(
                                    Texts.BEFORE_USE_ID23.format(len(
                                        chosen_game.bullets
                                    ))
                                ))
                                if 0 <= bullet_i_to_ins <= \
                                   len(chosen_game.bullets) :
                                    player.slots[tools_existence[23]] = \
                                    (player.slots[tools_existence[23]][0],None)
                                    chosen_game.bullets.insert(bullet_i_to_ins,
                                                               False)
                                    print(Texts.R_USES_ID23)
                                else :
                                    used = False
                            except ValueError :
                                used = False
                        elif to_use == 24 :
                            try :
                                bullet_i_to_ins: int = int(input(
                                    Texts.BEFORE_USE_ID24.format(len(
                                        chosen_game.bullets
                                    ))
                                ))
                                if 0 <= bullet_i_to_ins <= \
                                   len(chosen_game.bullets) :
                                    player.slots[tools_existence[24]] = \
                                    (player.slots[tools_existence[24]][0],None)
                                    chosen_game.bullets.insert(bullet_i_to_ins,
                                                               True)
                                    print(Texts.R_USES_ID24)
                                else :
                                    used = False
                            except ValueError :
                                used = False
                        elif to_use == 25 :
                            try :
                                bullet_i_to_ins: int = int(input(
                                    Texts.BEFORE_USE_ID25.format(len(
                                        chosen_game.bullets
                                    ))
                                ))
                                if 0 <= bullet_i_to_ins <= \
                                   len(chosen_game.bullets) :
                                    player.slots[tools_existence[25]] = \
                                    (player.slots[tools_existence[25]][0],None)
                                    chosen_game.bullets.insert(
                                        bullet_i_to_ins, not randint(0, 1)
                                    )
                                    if bullet_i_to_ins < \
                                       len(chosen_game.bullets) - 1 :
                                        chosen_game.bullets[
                                            bullet_i_to_ins+1
                                        ] = not randint(0, 1)
                                    print(Texts.R_USES_ID25)
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
                                    (player.slots[tools_existence[26]][0],None)
                                    player.begin_band_level += 1
                                    print(Texts.R_USES_ID26)
                                else :
                                    used = False
                        elif to_use == 27 :
                            player.slots[tools_existence[27]] = \
                            (player.slots[tools_existence[27]][0], None)
                            if player.hp < 2 :
                                player.hp += 5
                                gamesave.healed += 5
                                print(Texts.R_USES_ID27_5)
                            elif player.hp < 5 :
                                player.hp += 4
                                gamesave.healed += 4
                                print(Texts.R_USES_ID27_4)
                            elif player.hp < 9 :
                                player.hp += 3
                                gamesave.healed += 3
                                print(Texts.R_USES_ID27_3)
                            elif player.hp < 14 :
                                player.hp += 2
                                gamesave.healed += 2
                                print(Texts.R_USES_ID27_2)
                            else :
                                player.hp += 1
                                gamesave.healed += 1
                                print(Texts.R_USES_ID27_1)
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
                                print(Texts.R_USES_ID3[
                                    chosen_game.bullets.pop(0)
                                ])
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
                            print(Texts.R_USES_ID4)
                        elif to_use == 32 :
                            if player.hp == 1 :
                                if "y" == input(
                                    Texts.BEFORE_USE_ID32_1
                                ).strip().lower() :
                                    player.slots[tools_existence[32]] = \
                                    (player.slots[tools_existence[32]][0],None)
                                    if victim.controllable :
                                        print(Texts.OPPO_INITS_STAGE.string
                                              .format(1))
                                        if victim.hp == 1 :
                                            print(Texts.R_RECEIVES_STAGE_1)
                                            print(Texts.OPPO_RECEIVES_STAGE
                                                  .format(1))
                                            player.hp -= 1
                                            victim.hp -= 1
                                            parent_game.subgame = StageGame(
                                                1, 1, True
                                            )
                                            sub_game = parent_game.subgame
                                            chosen_game = \
                                            parent_game if sub_game is None \
                                            else sub_game
                                            player = chosen_game.players[0]
                                            victim = chosen_game.players[1]
                                            if isinstance(sub_game, StageGame) :
                                                sub_game.gen_bullets()
                                        else :
                                            while True :
                                                try :
                                                    evil_hp: int = int(input(
                                                        Texts.R_RECEIVES_STAGE
                                                        .format(victim.hp)
                                                    ))
                                                    if 0 < evil_hp <= \
                                                       victim.hp :
                                                        print(
                                                            Texts.
                                                            OPPO_RECEIVES_STAGE
                                                            .format(evil_hp)
                                                        )
                                                        player.hp -= 1
                                                        victim.hp -= evil_hp
                                                        parent_game.subgame = \
                                                        StageGame(
                                                            1, evil_hp, True
                                                        )
                                                        sub_game = \
                                                        parent_game.subgame
                                                        chosen_game = \
                                                        parent_game \
                                                        if sub_game is None \
                                                        else sub_game
                                                        player = \
                                                        chosen_game.players[0]
                                                        victim = \
                                                        chosen_game.players[1]
                                                        if isinstance(
                                                            sub_game, StageGame
                                                        ) :
                                                            sub_game\
                                                            .gen_bullets()
                                                        break
                                                except ValueError :
                                                    pass
                                    else :
                                        evil_hp: int = randint(1, victim.hp)
                                        print(Texts.E_RECEIVES_STAGE.string
                                              .format(evil_hp))
                                        player.hp -= 1
                                        victim.hp -= evil_hp
                                        parent_game.subgame = StageGame(
                                            1, evil_hp, True
                                        )
                                        sub_game = parent_game.subgame
                                        chosen_game = \
                                        parent_game if sub_game is None \
                                        else sub_game
                                        player = chosen_game.players[0]
                                        victim = chosen_game.players[1]
                                        if isinstance(sub_game, StageGame) :
                                            sub_game.gen_bullets()
                                else :
                                    used = False
                            else :
                                try :
                                    your_hp: int = int(input(
                                        Texts.BEFORE_USE_ID32.format(player.hp)
                                    ))
                                    if 0 < your_hp <= player.hp :
                                        player.slots[tools_existence[32]] = \
                                        (player.slots[tools_existence[32]][0],
                                         None)
                                        if victim.controllable :
                                            print(Texts.OPPO_INITS_STAGE
                                                  .format(your_hp))
                                            if victim.hp == 1 :
                                                print(Texts.R_RECEIVES_STAGE_1)
                                                print(
                                                    Texts.OPPO_RECEIVES_STAGE
                                                    .format(1)
                                                )
                                                player.hp -= your_hp
                                                victim.hp -= 1
                                                parent_game.subgame = \
                                                StageGame(your_hp, 1, True)
                                                sub_game = parent_game.subgame
                                                chosen_game = \
                                                parent_game if \
                                                sub_game is None else sub_game
                                                player = chosen_game.players[0]
                                                victim = chosen_game.players[1]
                                                if isinstance(
                                                    sub_game, StageGame
                                                ) :
                                                    sub_game.gen_bullets()
                                            else :
                                                while True :
                                                    try :
                                                        evil_hp: int = \
                                                        int(input(
                                                            Texts
                                                            .R_RECEIVES_STAGE
                                                            .format(victim.hp)
                                                        ))
                                                        if 0 < evil_hp <= \
                                                           victim.hp :
                                                            print(
                                                            Texts.
                                                            OPPO_RECEIVES_STAGE
                                                            .format(evil_hp)
                                                            )
                                                            player.hp -=your_hp
                                                            victim.hp -=evil_hp
                                                            parent_game\
                                                            .subgame=StageGame(
                                                                your_hp,
                                                                evil_hp, True
                                                            )
                                                            sub_game = \
                                                            parent_game.subgame
                                                            chosen_game = \
                                                            parent_game if \
                                                            sub_game is None \
                                                            else sub_game
                                                            player = \
                                                            chosen_game\
                                                            .players[0]
                                                            victim = \
                                                            chosen_game\
                                                            .players[1]
                                                            if isinstance(
                                                                sub_game,
                                                                StageGame
                                                            ) :
                                                                sub_game\
                                                                .gen_bullets()
                                                            break
                                                    except ValueError :
                                                        pass
                                        else :
                                            evil_hp: int = randint(1,victim.hp)
                                            print(Texts.E_RECEIVES_STAGE
                                                  .format(evil_hp))
                                            player.hp -= your_hp
                                            victim.hp -= evil_hp
                                            parent_game.subgame = StageGame(
                                                your_hp, evil_hp, True
                                            )
                                            sub_game = parent_game.subgame
                                            chosen_game = \
                                            parent_game if sub_game is None \
                                            else sub_game
                                            player = chosen_game.players[0]
                                            victim = chosen_game.players[1]
                                            if isinstance(sub_game, StageGame):
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
                                print(Texts.R_USES_ID33)
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
                            print(Texts.R_USES_ID34)
                        elif to_use == 35 :
                            if any(chosen_game.extra_bullets) :
                                player.slots[tools_existence[35]] = \
                                (player.slots[tools_existence[35]][0], None)
                                for i in chosen_game.extra_bullets :
                                    if i :
                                        chosen_game.bullets.extend(i)
                                        i.clear()
                                print(Texts.R_USES_ID35)
                            else :
                                used = False
                        if used :
                            print(Texts.TOOL_MINUS_1.format(to_use))
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
                        print(Texts.NO_SUCH_TOOL.format(to_use))
            elif operation == 8  and (
                chosen_game.has_tools() or
                chosen_game.count_tools_of_r(None) < len(chosen_game.r_slots)or
                chosen_game.count_tools_of_e(None) < len(chosen_game.e_slots)
            ) :
                player =chosen_game.players[0+(not chosen_game.turn_orders[0])]
                print(Texts.OPPO_TOOL_WAREHOUSE if player.controllable
                      else Texts.E_TOOL_WAREHOUSE)
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
                        print(Texts.TOOL_NAME_MORE.format(
                            k, chosen_game.tools[k][0], v
                        ))
                    else :
                        print(Texts.TOOL_NAME_ONE.format(
                            k, chosen_game.tools[k][0]
                        ))
                    if chosen_game.tools[k][1] is None :
                        print(Texts.TOOL_NO_DESC)
                    else :
                        print(Texts.TOOL_DESC, chosen_game.tools[k][1])
                for slot in player.slots :
                    if slot[1] is not None and slot[0] > 0 :
                        print(Texts.TOOL_NAME_ONE.format(
                            slot[1], chosen_game.tools[slot[1]][0]
                        ))
                        if chosen_game.tools[slot[1]][1] is None :
                            print(Texts.TOOL_NO_DESC)
                        else :
                            print(Texts.TOOL_DESC,
                                  chosen_game.tools[slot[1]][1])
                        print(Texts.SLOT_EXPIRED_AT.format(slot[0]))
                if not e_has_tool :
                    print(Texts.TOOL_WAREHOUSE_EMPTY)
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
                            if nightmare and not victim.controllable :
                                if bullets_i[0] or not randint(0, 3) :
                                    gamesave.add_exp(ceil(
                                        GAMEMODE_SET[gamemode_i][2]
                                    ))
                            elif not debug :
                                if bullets_i[0] or not randint(0, 3) :
                                    gamesave.add_exp()
                            if bullets_i[1] :
                                print(Texts.R_EXPLODES)
                                if bullets_i[0] :
                                    gamesave.exploded_againstshoot_trues += 1
                                    if nightmare and not victim.controllable :
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
                                    print(Texts.R_TRUE_ON_R)
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
                                    print(Texts.R_CUR_HP.format(player.hp))
                                    if isinstance(player, NormalPlayer) and \
                                       random() >= player.hurts / 8. :
                                        player.hurts += 1
                                        assert 0 <= player.hurts < 9
                                else :
                                    gamesave.exploded_againstshoot_falses += 1
                                    print(Texts.R_FALSE_ON_R)
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
                                            print(Texts.OPPO_CATCHES_BULLET
                                                  if victim.controllable
                                                  else Texts.E_CATCHES_BULLET)
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
                                            print(Texts.OPPO_CATCHES_BULLET
                                                  if victim.controllable
                                                  else Texts.E_CATCHES_BULLET)
                                            continue
                                if isinstance(victim, NormalPlayer) and \
                                   victim.bulletproof :
                                    victim.bulletproof[0] -= randint(1, ceil(
                                        (player.attack_boost+1)**0.5
                                    )) if isinstance(player, NormalPlayer) \
                                    else 1
                                    print(Texts.OPPO_BULLETPROOF_DEFENDS
                                          if victim.controllable
                                          else Texts.E_BULLETPROOF_DEFENDS)
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
                                            print(Texts.OPPO_BULLETPROOF_BREAKS
                                                  if victim.controllable else
                                                  Texts.E_BULLETPROOF_BREAKS)
                                elif bullets_i[0] :
                                    if nightmare and not victim.controllable :
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
                                    print(Texts.R_TRUE_ON_E)
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
                                    print((
                                        Texts.OPPO_CUR_HP if
                                        victim.controllable else Texts.E_CUR_HP
                                    ).format(victim.hp))
                                    if isinstance(victim, NormalPlayer) and \
                                       random() >= victim.hurts / 8. :
                                        victim.hurts += 1
                                        assert 0 <= victim.hurts < 9
                                else :
                                    print(Texts.R_FALSE_ON_E)
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
                            print(Texts.R_EXPLODES)
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
                                        print(Texts.OPPO_CATCHES_BULLET
                                              if victim.controllable
                                              else Texts.E_CATCHES_BULLET)
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
                                        print(Texts.OPPO_CATCHES_BULLET
                                              if victim.controllable
                                              else Texts.E_CATCHES_BULLET)
                                        continue
                            if isinstance(victim, NormalPlayer) and \
                               victim.bulletproof :
                                victim.bulletproof[0] -= randint(1, ceil(
                                    (player.attack_boost+1)**0.5
                                )) if isinstance(player, NormalPlayer) else 1
                                print(Texts.OPPO_BULLETPROOF_DEFENDS
                                      if victim.controllable
                                      else Texts.E_BULLETPROOF_DEFENDS)
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
                                        print(Texts.OPPO_BULLETPROOF_BREAKS
                                              if victim.controllable
                                              else Texts.E_BULLETPROOF_BREAKS)
                            elif bullets_i[0] :
                                true_on_e = True
                                print(Texts.R_TRUE_ON_E)
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
                                print((Texts.OPPO_CUR_HP if victim.controllable
                                       else Texts.E_CUR_HP).string
                                      .format(victim.hp))
                                if isinstance(victim, NormalPlayer) and \
                                   random() >= victim.hurts / 8. :
                                    victim.hurts += 1
                                    assert 0 <= victim.hurts < 9
                            else :
                                print(Texts.R_FALSE_ON_E)
                        else :
                            if bullets_i[0] :
                                gamesave.success_selfshoot_trues += 1
                                true_on_r = True
                                print(Texts.R_TRUE_ON_R)
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
                                print(Texts.R_CUR_HP.format(player.hp))
                                if isinstance(player, NormalPlayer) and \
                                   random() >= player.hurts / 8. :
                                    player.hurts += 1
                                    assert 0 <= player.hurts < 9
                            else :
                                gamesave.success_selfshoot_falses += 1
                                print(Texts.R_FALSE_ON_R)
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
                print(Texts.WRONG_OPER_NUM)
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
                elif slot[1] == 2 :
                    will_use = chosen_game.bullets[0] if nightmare else \
                               not randint(0, 1)
                    if isinstance(player, NormalPlayer) and will_use :
                        player.slots[slotid] = (slot[0], None)
                        player.attack_boost += 1
                        print(Texts.E_USES_ID2)
                elif slot[1] == 3 :
                    will_use = \
                    True if nightmare and chosen_game.bullets[0] and \
                            chosen_game.bullets.count(True) == 1 else \
                    not randint(0, 1)
                    if will_use :
                        player.slots[slotid] = (slot[0], None)
                        print(Texts.E_USES_ID3[chosen_game.bullets.pop(0)])
                        if not chosen_game.bullets :
                            break
                elif slot[1] == 4 :
                    will_use = nightmare or not randint(0, 1)
                    if will_use :
                        player.slots[slotid] = (slot[0], None)
                        chosen_game.rel_turn_lap -= 1
                        victim.stopped_turns += 1
                        print(Texts.E_USES_ID4.format(cat_girl))
                elif slot[1] == 5 :
                    will_use = nightmare or not randint(0, 1)
                    if will_use :
                        player.slots[slotid] = (slot[0], None)
                        heal_succeeded: bool = nightmare or (
                            player.hp <= 3 + player.hurts / 4. or
                            random() < 0.5 ** (player.hp-3-player.hurts/4.)
                            if isinstance(player, NormalPlayer) else
                            player.hp <= 3 or random() < 0.5 ** (player.hp-3)
                        )
                        if heal_succeeded :
                            player.hp += 1
                        print(Texts.E_USES_ID5[heal_succeeded])
                elif slot[1] == 6 :
                    will_use = nightmare or not randint(0, 1)
                    if will_use :
                        player.slots[slotid] = (slot[0], None)
                        print(Texts.E_USES_ID6)
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
                        print(Texts.E_USES_ID9)
                        player.bulletproof.insert(0, 3)
                elif slot[1] == 11 :
                    will_use = nightmare or not randint(0, 5)
                    if will_use :
                        player.slots[slotid] = (slot[0], None)
                        dice_sum: int = \
                        randint(1, 6) + randint(1, 6) + randint(1, 6)
                        if debug :
                            print(Texts.E_USES_ID11.format(dice_sum))
                        if dice_sum == 3 :
                            if isinstance(player, NormalPlayer) :
                                player.breakcare_rounds += 2
                        elif dice_sum == 4 :
                            player.hp -= 2
                            print(Texts.E_LOST_2_HP)
                            if player.hp <= 0 :
                                break
                        elif dice_sum == 5 :
                            for bullet_index \
                            in range(2, len(chosen_game.bullets)) :
                                chosen_game.bullets[bullet_index] = \
                                not randint(0, 1)
                        elif dice_sum == 6 :
                            player.hp -= 1
                            print(Texts.E_LOST_1_HP)
                            if player.hp <= 0 :
                                break
                        elif dice_sum == 7 :
                            vanishable_indices: List[int] = []
                            for slotid, slot in enumerate(player.slots) :
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
                            print(Texts.E_GOT_1_HP)
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
                                    print(Texts.E_ATTACK_BOOSTED_2)
                        elif dice_sum == 13 :
                            victim.hp -= 1
                            print(Texts.R_LOST_1_HP)
                            if victim.hp <= 0 :
                                break
                        elif dice_sum == 14 :
                            k: int = 2 - (not randint(0, 2))
                            chosen_game.rel_turn_lap -= k
                            victim.stopped_turns += k
                        elif dice_sum == 15 :
                            victim.hp -= 2
                            print(Texts.R_LOST_2_HP)
                            if victim.hp <= 0 :
                                break
                        elif dice_sum == 18 :
                            victim.hp //= 8
                            print(Texts.R_CRIT)
                            print(Texts.R_CUR_HP.format(victim.hp))
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
                            print(Texts.E_TURNED_INTO_R)
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
                            print(Texts.R_TURNED_INTO_E)
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
                            print(Texts.CLIP_CHANGED)
                elif slot[1] == 16 :
                    will_use = not randint(0, 3)
                    if will_use :
                        player.slots[slotid] = (slot[0], None)
                        shuffle(chosen_game.bullets)
                        print(Texts.E_USES_ID16)
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
                        print(Texts.E_USES_ID22)
                elif slot[1] == 23 :
                    will_use = not randint(0, 2)
                    if will_use :
                        player.slots[slotid] = (slot[0], None)
                        chosen_game.bullets.insert(randint(0, len(
                            chosen_game.bullets
                        )), False)
                        print(Texts.E_USES_ID23)
                elif slot[1] == 24 :
                    will_use = not randint(0, 2)
                    if will_use :
                        player.slots[slotid] = (slot[0], None)
                        chosen_game.bullets.insert(randint(0, len(
                            chosen_game.bullets
                        )), True)
                        print(Texts.E_USES_ID24)
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
                        print(Texts.E_USES_ID25)
                elif slot[1] == 26 :
                    if isinstance(player, NormalPlayer) :
                        will_use = player.hurts > player.begin_band_level + \
                                                  player.mid_band_level and \
                                   not randint(0, 1)
                        if will_use :
                            player.slots[slotid] = (slot[0], None)
                            player.begin_band_level += 1
                            print(Texts.E_USES_ID26)
                elif slot[1] == 27 :
                    will_use = not randint(0, 4)
                    if will_use :
                        player.slots[slotid] = (slot[0], None)
                        if player.hp < 2 :
                            player.hp += 5
                            print(Texts.E_USES_ID27_5)
                        elif player.hp < 5 :
                            player.hp += 4
                            print(Texts.E_USES_ID27_4)
                        elif player.hp < 9 :
                            player.hp += 3
                            print(Texts.E_USES_ID27_3)
                        elif player.hp < 14 :
                            player.hp += 2
                            print(Texts.E_USES_ID27_2)
                        else :
                            player.hp += 1
                            print(Texts.E_USES_ID27_1)
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
                            print(Texts.E_USES_ID3[chosen_game.bullets.pop(0)])
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
                        print(Texts.E_USES_ID4.format(cat_girl))
                elif slot[1] == 32 :
                    will_use = not randint(0, 9)
                    if will_use :
                        evil_hp: int = randint(1, player.hp)
                        print(Texts.E_INITS_STAGE.format(evil_hp))
                        if victim.controllable :
                            if victim.hp == 1 :
                                print(Texts.R_RECEIVES_STAGE_1)
                                victim.hp -= 1
                                player.hp -= evil_hp
                                parent_game.subgame = StageGame(
                                    1, evil_hp, False
                                )
                                sub_game = parent_game.subgame
                                chosen_game = \
                                parent_game if sub_game is None else sub_game
                                player = chosen_game.players[1]
                                victim = chosen_game.players[0]
                                if isinstance(sub_game, StageGame) :
                                    sub_game.gen_bullets()
                            else :
                                while True :
                                    try :
                                        your_hp: int = int(input(
                                            Texts.R_RECEIVES_STAGE
                                            .format(victim.hp)
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
                                            player = chosen_game.players[1]
                                            victim = chosen_game.players[0]
                                            if isinstance(sub_game, StageGame):
                                                sub_game.gen_bullets()
                                            break
                                    except ValueError :
                                        pass
                        else :
                            your_hp = randint(1, victim.hp)
                            print(I18nText(
                                "你以 {0} 生命值应战",
                                en_en="You accepted with {0} HP"
                            ).format(your_hp))
                            victim.hp -= your_hp
                            player.hp -= evil_hp
                            parent_game.subgame = StageGame(
                                your_hp, evil_hp, False
                            )
                            sub_game = parent_game.subgame
                            chosen_game = \
                            parent_game if sub_game is None else sub_game
                            player = chosen_game.players[1]
                            victim = chosen_game.players[0]
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
                        print(Texts.E_USES_ID33)
                elif slot[1] == 34 :
                    will_use = (not (all(chosen_game.bullets[
                        :chosen_game.bullets.count(True)
                    ]) and all(True if x is None else all(x[:x.count(True)])
                               for x in chosen_game.extra_bullets))) \
                    if nightmare else not randint(0, 4)
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
                        print(Texts.E_USES_ID34)
                elif slot[1] == 35 :
                    will_use = \
                    any(chosen_game.extra_bullets) and not randint(0, 4)
                    if will_use :
                        player.slots[slotid] = (slot[0], None)
                        for i in chosen_game.extra_bullets :
                            if i :
                                chosen_game.bullets.extend(i)
                                i.clear()
                        print(Texts.E_USES_ID35)
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
                print(Texts.E_TO_E)
                for bullets_i in shoot_result :
                    if bullets_i is not None :
                        if bullets_i[1] :
                            print(Texts.E_EXPLODES)
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
                                        print(Texts.R_CATCHES_BULLET)
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
                                        print(Texts.R_CATCHES_BULLET)
                                        continue
                            if isinstance(victim, NormalPlayer) and \
                               victim.bulletproof :
                                victim.bulletproof[0] -= \
                                randint(1, ceil((player.attack_boost+1)**0.5))\
                                if isinstance(player, NormalPlayer) else 1
                                print(Texts.R_BULLETPROOF_DEFENDS)
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
                                        print(Texts.R_BULLETPROOF_BREAKS)
                            elif bullets_i[0] :
                                true_on_r = True
                                print(Texts.E_TRUE_ON_R)
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
                                print(Texts.R_CUR_HP.format(victim.hp))
                                if isinstance(victim, NormalPlayer) and \
                                   random() >= victim.hurts / 8. :
                                    victim.hurts += 1
                                    assert 0 <= victim.hurts < 9
                            else :
                                print(Texts.E_FALSE_ON_R)
                        else :
                            if bullets_i[0] :
                                true_on_e = True
                                print(Texts.E_TRUE_ON_E)
                                for _ in range(
                                    base_attack+player.attack_boost if
                                    isinstance(player, NormalPlayer) else
                                    base_attack
                                ) :
                                    player.hp -= \
                                    2 if isinstance(player, NormalPlayer) and \
                                         random() < player.hurts / 8. else 1
                                print(Texts.E_CUR_HP.format(player.hp))
                                if isinstance(player, NormalPlayer) and \
                                   random() >= player.hurts / 8. :
                                    player.hurts += 1
                                    assert 0 <= player.hurts < 9
                            else :
                                print(Texts.E_FALSE_ON_E)
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
                print(Texts.E_TO_R)
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
                                print(Texts.E_EXPLODES)
                                if bullets_i[0] :
                                    true_on_e = True
                                    print(Texts.E_TRUE_ON_E)
                                    for _ in range(
                                        base_attack+player.attack_boost if
                                        isinstance(player, NormalPlayer) else
                                        base_attack
                                    ):
                                        player.hp -= \
                                        2 if isinstance(player, NormalPlayer) \
                                             and random() < player.hurts / 8. \
                                        else 1
                                    print(Texts.E_CUR_HP.format(player.hp))
                                    if isinstance(player, NormalPlayer) and \
                                       random() >= player.hurts / 8. :
                                        player.hurts += 1
                                        assert 0 <= player.hurts < 9
                                else :
                                    print(Texts.E_FALSE_ON_E)
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
                                            print(Texts.R_CATCHES_BULLET)
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
                                            print(Texts.R_CATCHES_BULLET)
                                            continue
                                if isinstance(victim, NormalPlayer) and \
                                   victim.bulletproof :
                                    victim.bulletproof[0] -= randint(1, ceil(
                                        (player.attack_boost+1)**0.5
                                    ))if isinstance(player, NormalPlayer)else 1
                                    print(Texts.R_BULLETPROOF_DEFENDS)
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
                                                        victim\
                                                        .breakcare_rounds += 1
                                                victim.breakcare_potential = 0
                                            print(Texts.R_BULLETPROOF_BREAKS)
                                elif bullets_i[0] :
                                    true_on_r = True
                                    print(Texts.E_TRUE_ON_R)
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
                                    print(Texts.R_CUR_HP.format(victim.hp))
                                    if isinstance(victim, NormalPlayer) and \
                                       random() >= victim.hurts / 8. :
                                        victim.hurts += 1
                                        assert 0 <= victim.hurts < 9
                                else :
                                    print(Texts.E_FALSE_ON_R)
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
    print(Texts.PLAYER_0_WON.format(cat_girl) if chosen_game.players[0].alive
          else (Texts.PLAYER_1_WON.format(cat_girl) if
                chosen_game.players[1].alive else Texts.END_0_0))
elif chosen_game.players[0].alive :
    if chosen_game.e_hp >= 0 :
        print(Texts.R_WON.format(cat_girl))
    elif chosen_game.e_hp == -1 :
        print(Texts.R_WON_1)
    elif chosen_game.e_hp == -2 :
        print(Texts.R_WON_2)
    else :
        print(Texts.R_WON_3)
elif chosen_game.r_hp >= 0 :
    if chosen_game.players[1].alive :
        print(Texts.E_WON.format(cat_girl))
    elif chosen_game.e_hp >= 0 :
        print(Texts.END_0_0)
        gamesave.add_exp(25)
        gamesave.add_coins()
    elif chosen_game.e_hp == -1 :
        print(Texts.END_0_1)
        gamesave.add_exp(80)
        gamesave.add_coins(3)
    elif chosen_game.e_hp == -2 :
        print(Texts.END_0_2.format(cat_girl))
        gamesave.add_exp(400)
        gamesave.add_coins(10)
    else :
        print(Texts.END_0_3.format(cat_girl))
        gamesave.add_exp(1500)
        gamesave.add_coins(32)
elif chosen_game.r_hp == -1 :
    if chosen_game.players[1].alive :
        print(Texts.E_WON_1)
    elif chosen_game.e_hp >= 0 :
        print(Texts.END_1_0)
        gamesave.add_exp(80)
        gamesave.add_coins(3)
    elif chosen_game.e_hp == -1 :
        print(Texts.END_1_1)
        gamesave.add_exp(400)
        gamesave.add_coins(10)
    elif chosen_game.e_hp == -2 :
        print(Texts.END_1_2)
        gamesave.add_exp(1500)
        gamesave.add_coins(32)
    else :
        print(Texts.END_1_3)
        gamesave.add_exp(4800)
        gamesave.add_coins(100)
elif chosen_game.r_hp == -2 :
    if chosen_game.players[1].alive :
        print(Texts.E_WON_2)
    elif chosen_game.e_hp >= 0 :
        print(Texts.END_2_0.format(cat_girl))
        gamesave.add_exp(400)
        gamesave.add_coins(10)
    elif chosen_game.e_hp == -1 :
        print(Texts.END_2_1)
        gamesave.add_exp(1500)
        gamesave.add_coins(32)
    elif chosen_game.e_hp == -2 :
        print(Texts.END_2_2)
        gamesave.add_exp(4800)
        gamesave.add_coins(100)
    else:
        print(Texts.END_2_3)
        gamesave.add_exp(16000)
        gamesave.add_coins(320)
else :
    if chosen_game.players[1].alive :
        print(Texts.E_WON_3)
    elif chosen_game.e_hp >= 0 :
        print(Texts.END_3_0.format(cat_girl))
        gamesave.add_exp(1500)
        gamesave.add_coins(32)
    elif chosen_game.e_hp == -1 :
        print(Texts.END_3_1)
        gamesave.add_exp(4800)
        gamesave.add_coins(100)
    elif chosen_game.e_hp == -2 :
        print(Texts.END_3_2)
        gamesave.add_exp(16000)
        gamesave.add_coins(320)
    else :
        print(Texts.END_3_3)
        gamesave.add_exp(54000)
        gamesave.add_coins(1000)

gamesave.play_periods += 1
gamesave.game_runs += 1
print("================================")
print(Texts.GAME_COUNT_INFO
      .format(total_turn_count, total_round_count, total_period_count))

try :
    with open(gamesave_filename, "wb") as gamesave_file :
        gamesave_file.write(gamesave.serialize())
except OSError as err :
    print(Texts.PROBLEM_SAVING, err)
