from math import ceil
from random import choice, randint, random, shuffle
from sys import argv
from time import sleep, time
from typing import Dict, Iterator, List, Optional, Tuple, TYPE_CHECKING

from .gameapi import Game, GameSave, ShootResult, VER_STRING
from .gameinst import GAMEMODE_SET

gamesave: GameSave = GameSave()
gamemode_i: int = 1

print("恶魔轮盘赌（重构版） v"+VER_STRING)
debug: bool = "debug" in argv[1:]
nightmare: bool = "nightmare" in argv[1:]
skipthread: bool = "skipthread" in argv[1:]

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

while 1 :
    gamemode: str = input("""\
输入0以查看统计信息。
请选择游戏模式:
1.普通模式
2.无限模式(一)
3.小刀狂欢
4.骰子王国
5.无限模式(二)
6.连射派对""")
    try :
        gamemode_i = int(gamemode)
    except ValueError :
        pass
    else :
        if gamemode_i in (1, 2, 3, 4, 5, 6) :
            break
        if not gamemode_i :
            for k, v in gamesave.__dict__.items() :
                print(k, v, sep=": ")

IDENTITIES: Dict[int, Tuple[str, str, int]] = {
    1: ("工人", "加2血/25%免伤/去掉小刀", 0),
    2: ("老兵", "加1攻/回血概率up10%/对面加攻", 0),
    3: ("狙击手", "", 0),
    4: ("圣女", "", 20)
}

chosen_games: Iterator[Game] = iter(GAMEMODE_SET[gamemode_i][0])
r_hurts: int = 0
e_hurts: int = 0
r_stamina: int = 32
e_stamina: int = 32
r_selfshoot_promises: int = 0
e_selfshoot_promises: int = 0
r_againstshoot_promises: int = 0
e_againstshoot_promises: int = 0
r_attack_boost: int = 0
e_attack_boost: int = 0
r_bulletproof: List[int] = []
e_bulletproof: List[int] = []
r_bullet_catcher_level: int = 0
e_bullet_catcher_level: int = 0
r_multishoot_level: int = 0
e_multishoot_level: int = 0
r_comboshoot_level: int = 0
e_comboshoot_level: int = 0
r_cursed_shoot_level: int = 0
e_cursed_shoot_level: int = 0
r_0band_level: int = 0
e_0band_level: int = 0
r_1band_level: int = 0
e_1band_level: int = 0
r_breakcare_rounds: int = 0
e_breakcare_rounds: int = 0
r_breakcare_potential: int = 0
e_breakcare_potential: int = 0
base_attack: int = 1

bullets_upgrade: int = 0

true_on_r: bool = False
true_on_e: bool = False

chosen_game: Game = next(chosen_games)

round_turn_count: int = 0
period_turn_count: int = 0
total_turn_count: int = 0
period_round_count: int = 0
total_round_count: int = 0
total_period_count: int = 1

while 1 :
    gametime_time_start: float = time()
    if chosen_game.r_hp <= 0 or chosen_game.e_hp <= 0 :
        try :
            if chosen_game.r_hp <= 0 :
                r_bulletproof.clear()
            if chosen_game.e_hp <= 0 :
                e_bulletproof.clear()
            if chosen_game.e_hp <= 0 :
                if nightmare :
                    gamesave.add_exp(ceil(10*(2-chosen_game.e_hp)*\
                                          GAMEMODE_SET[gamemode_i][2]))
                elif not debug :
                    gamesave.add_exp(10*(2-chosen_game.e_hp))
                if not debug :
                    gamesave.add_coins()
            try :
                with open("emlpd.dat", "wb") as gamesave_file :
                    gamesave_file.write(gamesave.serialize())
            except OSError as err :
                print("存档时遇到问题!", err)
            chosen_game = next(chosen_games)
            total_period_count += 1
            gamesave.play_periods += 1
            print("================")
            print("本周目持续了", period_turn_count, "轮,")
            print(period_round_count, "回合,")
            round_turn_count = 0
            period_turn_count = 0
            period_round_count = 0
            base_attack = 1
            r_stamina += (32-r_stamina) // 2
            e_stamina += (32-e_stamina) // 2
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
    while r_1band_level > 0 and r_hurts > 0 :
        r_hurts -= 1
        r_1band_level -= 1
    r_1band_level += r_0band_level
    r_0band_level = 0
    while e_1band_level > 0 and e_hurts > 0 :
        e_hurts -= 1
        e_1band_level -= 1
    e_1band_level += e_0band_level
    e_0band_level = 0
    if r_breakcare_rounds > 0 :
        r_breakcare_rounds -= 1
    if e_breakcare_rounds > 0 :
        e_breakcare_rounds -= 1
    print("当前你的生命值为:", chosen_game.r_hp)
    print("当前你的负伤数为:", r_hurts)
    print("当前恶魔生命值为:", chosen_game.e_hp)
    print("当前恶魔负伤数为:", e_hurts)
    sleep(1)
    r_expired_slots: List[Optional[int]] = chosen_game.expire_r_slots()
    e_expired_slots: List[Optional[int]] = chosen_game.expire_e_slots()
    for tool_id in r_expired_slots :
        if tool_id is not None :
            print("非常可惜,随着槽位的到期,你的", chosen_game.tools[tool_id][0], "也不翼而飞")
    for tool_id in e_expired_slots :
        if tool_id is not None :
            print("非常高兴,随着槽位的到期,恶魔的", chosen_game.tools[tool_id][0], "不翼而飞")
    sleep(1)
    r_new_slot: Optional[int] = chosen_game.send_r_slot()
    e_new_slot: Optional[int] = chosen_game.send_e_slot(1., {5: 1}) if \
                                nightmare else chosen_game.send_e_slot()
    if r_new_slot is not None :
        print("你获得1个有效期", r_new_slot, "回合的空槽位")
    if e_new_slot is not None :
        print("恶魔获得1个有效期", e_new_slot, "回合的空槽位")
    print("你获得", chosen_game.send_tools_to_r(GAMEMODE_SET[gamemode_i][1]),
          "个道具")
    print("恶魔获得", chosen_game.send_tools_to_e(GAMEMODE_SET[gamemode_i][1]),
          "个道具")
    chosen_game.gen_bullets()
    sleep(1)
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
        if chosen_game.r_hp <= 0 or chosen_game.e_hp <= 0 :
            break
        if chosen_game.rel_turn_lap < 0 :
            print("感觉...头晕晕的...要变成猫娘了~")
        elif chosen_game.rel_turn_lap :
            print("哈哈哈哈,恶魔被敲晕了,还是我的回合!")
        gamesave.active_gametime += time() - gametime_time_start
        if chosen_game.yourturn :
            if chosen_game.rel_turn_lap < 0 :
                chosen_game.yourturn = not chosen_game.yourturn
                chosen_game.rel_turn_lap += 1
        else :
            if chosen_game.rel_turn_lap > 0 :
                chosen_game.yourturn = not chosen_game.yourturn
                chosen_game.rel_turn_lap -= 1
        if chosen_game.yourturn :
            if debug :
                print("当前弹夹:", chosen_game.bullets)
                print("当前额外弹夹:", chosen_game.extra_bullets)
                print("你的体力:", r_stamina)
                print("恶魔体力:", e_stamina)
                print("当前相对套轮数:", chosen_game.rel_turn_lap)
                print("你的防弹衣:", r_bulletproof)
                print("恶魔的防弹衣:", e_bulletproof)
                print("你的叠加接弹套:", r_bullet_catcher_level)
                print("恶魔的叠加接弹套:", e_bullet_catcher_level)
                print("你的叠加双发射手:", r_multishoot_level)
                print("恶魔的叠加双发射手:", e_multishoot_level)
                print("你的叠加连发射手:", r_comboshoot_level)
                print("恶魔的叠加连发射手:", e_comboshoot_level)
                print("你的破枪数:", r_cursed_shoot_level)
                print("恶魔的破枪数:", e_cursed_shoot_level)
                print("你的破防回合数:", r_breakcare_rounds)
                print("恶魔的破防回合数:", e_breakcare_rounds)
                print("你的破防潜能:", r_breakcare_potential)
                print("恶魔的破防潜能:", e_breakcare_potential)
            print("当前为你的回合")
            operation: int = 2
            if r_breakcare_rounds > 0 :
                operation = randint(0, 1)
            else :
                print("请选择:1朝对方开枪,0朝自己开枪,7打开道具库,8查看对方道具")
                try :
                    operation = int(input())
                except ValueError :
                    pass
            if operation == 7 :
                print("道具库:")
                tools_existence: Dict[int, int] = {}
                permaslots: Dict[int, int] = {}
                for slotid, slot in enumerate(chosen_game.r_slots) :
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
                    print("作用:", chosen_game.tools[k][1])
                for slot in chosen_game.e_slots :
                    if slot[1] is not None and slot[0] > 0 :
                        print("道具", slot[1], ":", chosen_game.tools[slot[1]][0])
                        print("作用:", chosen_game.tools[slot[1]][1])
                        print("还有", slot[0], "回合到期")
                if not tools_existence :
                    print("(空)")
                while tools_existence :
                    print("返回请输入任意字母")
                    to_use: Optional[int] = None
                    try:
                        to_use = int(input("使用道具请按它的对应编号:"))
                    except ValueError:
                        break
                    if to_use in tools_existence :
                        used: bool = True
                        if to_use == 0 :
                            chosen_game.r_slots[tools_existence[0]] = \
                            (chosen_game.r_slots[tools_existence[0]][0], None)
                            if r_cursed_shoot_level > 0 :
                                r_cursed_shoot_level -= 1
                            else :
                                r_selfshoot_promises += 1
                        elif to_use == 1 :
                            chosen_game.r_slots[tools_existence[1]] = \
                            (chosen_game.r_slots[tools_existence[1]][0], None)
                            if r_cursed_shoot_level > 0 :
                                r_cursed_shoot_level -= 1
                            else :
                                r_againstshoot_promises += 1
                        elif to_use == 2 :
                            chosen_game.r_slots[tools_existence[2]] = \
                            (chosen_game.r_slots[tools_existence[2]][0], None)
                            r_attack_boost += 1
                            print("你使用了小刀,结果会如何呢?真让人期待")
                        elif to_use == 3 :
                            chosen_game.r_slots[tools_existence[3]] = \
                            (chosen_game.r_slots[tools_existence[3]][0], None)
                            if chosen_game.bullets.pop(0) :
                                print("你排出了一颗实弹")
                            else :
                                print("你排出了一颗空弹")
                        elif to_use == 4 :
                            chosen_game.r_slots[tools_existence[4]] = \
                            (chosen_game.r_slots[tools_existence[4]][0], None)
                            chosen_game.rel_turn_lap += 1
                            print("恭喜你,成功敲晕了对方!")
                        elif to_use == 5 :
                            chosen_game.r_slots[tools_existence[5]] = \
                            (chosen_game.r_slots[tools_existence[5]][0], None)
                            if chosen_game.r_hp <= 3 + r_hurts / 4. or \
                               (random() < 0.5 ** (chosen_game.r_hp-3-r_hurts/\
                                                   4.) and not nightmare) :
                                chosen_game.r_hp += 1
                                gamesave.healed += 1
                                print("你使用了道德的崇高赞许,回复了1点生命")
                            else :
                                print("因为你的不诚实,你并未回复生命,"
                                      "甚至失去了道德的崇高赞许")
                        elif to_use == 6 :
                            chosen_game.r_slots[tools_existence[6]] = \
                            (chosen_game.r_slots[tools_existence[6]][0], None)
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
                            chosen_game.r_slots[tools_existence[7]] = \
                            (chosen_game.r_slots[tools_existence[7]][0], None)
                            nonlimit_tool_slotids: List[int] = []
                            for slotid, slot in enumerate(chosen_game.e_slots):
                                if slot[1] is not None :
                                    if chosen_game.tools_sending_limit_in_game[
                                        slot[1]
                                    ] <= 0 :
                                        nonlimit_tool_slotids.append(slotid)
                            bring_tool_id: Optional[int] = None
                            if random() < 1 / (len(nonlimit_tool_slotids)+1) :
                                nonlimit_toolids: List[int] = []
                                for tool_id in chosen_game.tools :
                                    if chosen_game.tools_sending_limit_in_game[
                                        tool_id
                                    ] <= 0 :
                                        nonlimit_toolids.append(tool_id)
                                bring_tool_id = choice(nonlimit_toolids)
                            else :
                                taken_slotid: int = \
                                choice(nonlimit_tool_slotids)
                                bring_tool_id = \
                                chosen_game.e_slots[taken_slotid][1]
                                chosen_game.e_slots[taken_slotid] = \
                                (chosen_game.e_slots[taken_slotid][0], None)
                            if bring_tool_id is None :
                                assert 0
                            for slotid, slot in enumerate(chosen_game.r_slots):
                                if slot[1] is None :
                                    chosen_game.r_slots[slotid] = \
                                    (chosen_game.r_slots[slotid][0],
                                     bring_tool_id)
                                    print("+1 道具", bring_tool_id)
                                    break
                            else :
                                assert False
                        elif to_use == 8 :
                            if chosen_game.slots_sharing is None :
                                chosen_game.r_slots[tools_existence[8]] = \
                                (chosen_game.r_slots[tools_existence[8]][0],
                                 None)
                                new_keep_rounds: int = \
                                choice([1, 1, 1, 2, 2, 2, 2, 2, 3, 3])
                                chosen_game.slots_sharing = \
                                (not 0, new_keep_rounds, chosen_game.r_slots)
                                chosen_game.r_slots = chosen_game.e_slots
                            elif chosen_game.slots_sharing[0] :
                                chosen_game.r_slots[tools_existence[8]] = \
                                (chosen_game.r_slots[tools_existence[8]][0],
                                 None)
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
                                (not 0, new_keep_rounds, chosen_game.r_slots)
                        elif to_use == 9 :
                            chosen_game.r_slots[tools_existence[9]] = \
                            (chosen_game.r_slots[tools_existence[9]][0], None)
                            print("你穿上了一件防弹衣")
                            r_bulletproof.insert(0, 3)
                        elif to_use == 11 :
                            chosen_game.r_slots[tools_existence[11]] = \
                            (chosen_game.r_slots[tools_existence[11]][0], None)
                            dice_sum: int = \
                            randint(1, 6) + randint(1, 6) + randint(1, 6)
                            if debug :
                                print("你摇出了", dice_sum, "点")
                            if dice_sum == 3 :
                                r_breakcare_rounds += 2
                            elif dice_sum == 4 :
                                chosen_game.r_hp -= 2
                                print("你失去了2点生命")
                            elif dice_sum == 5 :
                                for bullet_index \
                                in range(2, len(chosen_game.bullets)) :
                                    chosen_game.bullets[bullet_index] = \
                                    not randint(0, 1)
                            elif dice_sum == 6 :
                                chosen_game.r_hp -= 1
                                print("你失去了1点生命")
                            elif dice_sum == 7 :
                                vanishable_indices: List[int] = []
                                for slotid, slot in \
                                    enumerate(chosen_game.r_slots) :
                                    if slot[1] is not None :
                                        if chosen_game.\
                                           tools_sending_limit_in_game[
                                            slot[1]
                                        ] <= 0 :
                                            vanishable_indices.append(slotid)
                                if vanishable_indices :
                                    vanish_index: int = \
                                    choice(vanishable_indices)
                                    chosen_game.r_slots[vanish_index] = \
                                    (chosen_game.r_slots[vanish_index][0],None)
                            elif dice_sum == 8 :
                                pass
                            elif dice_sum == 10 :
                                chosen_game.r_hp += 1
                                gamesave.healed += 1
                                print("你获得了1点生命")
                            elif dice_sum == 12 :
                                r_attack_boost += 2
                                if randint(0, 1) :
                                    print("你的攻击力提高了2点")
                            elif dice_sum == 13 :
                                chosen_game.e_hp -= 1
                                print("恶魔失去了1点生命")
                            elif dice_sum == 14 :
                                chosen_game.rel_turn_lap += \
                                2 - (not randint(0, 2))
                            elif dice_sum == 15 :
                                chosen_game.e_hp -= 2
                                print("恶魔失去了2点生命")
                            elif dice_sum == 18 :
                                chosen_game.e_hp //= 8
                                print("恶魔受到暴击!!!")
                                print("恶魔生命值:", chosen_game.e_hp)
                                gamesave.add_exp(6)
                        elif to_use == 12 :
                            temporary_slots: List[int] = []
                            for slotid in range(len(chosen_game.r_slots)) :
                                if chosen_game.r_slots[slotid][0] > 0 :
                                    temporary_slots.append(slotid)
                            if temporary_slots :
                                chosen_game.r_slots[tools_existence[12]] = \
                                (chosen_game.r_slots[tools_existence[12]][0],
                                 None)
                                delay_prob: float = len(temporary_slots) ** 0.5
                                for slotid in temporary_slots :
                                    if random() < delay_prob :
                                        chosen_game.r_slots[slotid] = \
                                        (chosen_game.r_slots[slotid][0]+1,
                                         chosen_game.r_slots[slotid][1])
                            else :
                                used = False
                        elif to_use == 13 :
                            chosen_game.r_slots[tools_existence[13]] = \
                            (chosen_game.r_slots[tools_existence[13]][0], None)
                            if randint(0, 1) :
                                print("你变成了恶魔的样子")
                                chosen_game.r_hp = chosen_game.e_hp
                                chosen_game.r_slots.clear()
                                chosen_game.r_slots.extend(chosen_game.e_slots)
                                chosen_game.r_sending_total.clear()
                                chosen_game.r_sending_total.update(
                                    chosen_game.e_sending_total.copy()
                                )
                                r_attack_boost = e_attack_boost
                                r_bulletproof.clear()
                                r_bulletproof.extend(e_bulletproof)
                                r_bullet_catcher_level = e_bullet_catcher_level
                                r_selfshoot_promises = e_selfshoot_promises
                                r_againstshoot_promises = \
                                e_againstshoot_promises
                                r_multishoot_level = e_multishoot_level
                                r_comboshoot_level = e_comboshoot_level
                                r_cursed_shoot_level = e_cursed_shoot_level
                                r_hurts = e_hurts
                                r_stamina = e_stamina
                                r_0band_level = e_0band_level
                                r_1band_level = e_1band_level
                            else :
                                print("恶魔变成了你的样子")
                                chosen_game.e_hp = chosen_game.r_hp
                                chosen_game.e_slots.clear()
                                chosen_game.e_slots.extend(chosen_game.r_slots)
                                chosen_game.e_sending_total.clear()
                                chosen_game.e_sending_total.update(
                                    chosen_game.r_sending_total.copy()
                                )
                                e_attack_boost = r_attack_boost
                                e_bulletproof.clear()
                                e_bulletproof.extend(r_bulletproof)
                                e_bullet_catcher_level = r_bullet_catcher_level
                                e_selfshoot_promises = r_selfshoot_promises
                                e_againstshoot_promises = \
                                r_againstshoot_promises
                                e_multishoot_level = r_multishoot_level
                                e_comboshoot_level = r_comboshoot_level
                                e_cursed_shoot_level = r_cursed_shoot_level
                                e_hurts = r_hurts
                                e_stamina = r_stamina
                                e_0band_level = r_0band_level
                                e_1band_level = r_1band_level
                            chosen_game.rel_turn_lap = 0
                        elif to_use == 14 :
                            chosen_game.r_slots[tools_existence[14]] = \
                            (chosen_game.r_slots[tools_existence[14]][0], None)
                            r_bullet_catcher_level += 1
                        elif to_use == 15 :
                            chosen_game.r_slots[tools_existence[15]] = \
                            (chosen_game.r_slots[tools_existence[15]][0], None)
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
                            chosen_game.r_slots[tools_existence[16]] = \
                            (chosen_game.r_slots[tools_existence[16]][0], None)
                            former_bullets: List[bool] = chosen_game.bullets[:]
                            chosen_game.bullets.clear()
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
                                        pass
                                chosen_game.bullets.insert(
                                    insertion, former_bullets.pop(randint(
                                        0, len(former_bullets)-1
                                    ))
                                )
                            print("你重整了一下弹药")
                        elif to_use == 17 :
                            chosen_game.r_slots[tools_existence[17]] = \
                            (chosen_game.r_slots[tools_existence[17]][0], None)
                            r_multishoot_level += 1
                        elif to_use == 18 :
                            chosen_game.r_slots[tools_existence[18]] = \
                            (chosen_game.r_slots[tools_existence[18]][0], None)
                            r_comboshoot_level += 1
                        elif to_use == 21 :
                            chosen_game.r_slots[tools_existence[21]] = \
                            (chosen_game.r_slots[tools_existence[21]][0], None)
                            e_cursed_shoot_level += 1
                        elif to_use == 22 :
                            try :
                                bullet_i_to_pick: int = \
                                int(input("请输入要取出子弹的编号"
                                          "(0~{0},0为当前子弹,输入其它以取消):"
                                          .format(len(chosen_game.bullets)-1)))
                                if 0 <= bullet_i_to_pick < \
                                    len(chosen_game.bullets) :
                                    chosen_game.r_slots[tools_existence[22]] =\
                                    (chosen_game.r_slots[tools_existence[22]][
                                        0
                                    ], 24 if \
                                    chosen_game.bullets.pop(bullet_i_to_pick) \
                                    else 23)
                                    print("你取出了一颗子弹")
                                    print("+1 道具", chosen_game.r_slots[
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
                                    chosen_game.r_slots[tools_existence[23]] =\
                                    (chosen_game.r_slots[tools_existence[23]][
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
                                    chosen_game.r_slots[tools_existence[24]] =\
                                    (chosen_game.r_slots[tools_existence[24]][
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
                                    chosen_game.r_slots[tools_existence[25]] =\
                                    (chosen_game.r_slots[tools_existence[25]][
                                        0
                                    ], None)
                                    chosen_game.bullets.insert(bullet_i_to_ins,
                                                               not randint(0, 1))
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
                            if r_hurts > r_0band_level + r_1band_level :
                                chosen_game.r_slots[tools_existence[26]] = \
                                (chosen_game.r_slots[tools_existence[26]][0],
                                 None)
                                r_0band_level += 1
                                print("你使用了绷带")
                            else :
                                used = False
                        elif to_use == 27 :
                            chosen_game.r_slots[tools_existence[27]] = \
                            (chosen_game.r_slots[tools_existence[27]][0], None)
                            if chosen_game.r_hp < 2 :
                                chosen_game.r_hp += 5
                                gamesave.healed += 5
                                print("你使用了医疗包,回复了5点生命")
                            elif chosen_game.r_hp < 5 :
                                chosen_game.r_hp += 4
                                gamesave.healed += 4
                                print("你使用了医疗包,回复了4点生命")
                            elif chosen_game.r_hp < 9 :
                                chosen_game.r_hp += 3
                                gamesave.healed += 3
                                print("你使用了医疗包,回复了3点生命")
                            elif chosen_game.r_hp < 14 :
                                chosen_game.r_hp += 2
                                gamesave.healed += 2
                                print("你使用了医疗包,回复了2点生命")
                            else :
                                chosen_game.r_hp += 1
                                gamesave.healed += 1
                                print("你使用了医疗包,回复了1点生命")
                            if r_hurts < 1 :
                                chosen_game.r_hp += 2
                                gamesave.healed += 2
                            elif r_hurts < 4 :
                                chosen_game.r_hp += 1
                                gamesave.healed += 1
                            r_hurts = 0
                        elif to_use == 28 :
                            chosen_game.r_slots[tools_existence[28]] = \
                            (chosen_game.r_slots[tools_existence[28]][0], None)
                            while chosen_game.bullets :
                                print("你排出了一颗实弹" if \
                                      chosen_game.bullets.pop(0) else \
                                      "你排出了一颗空弹")
                        elif to_use == 29 :
                            chosen_game.r_slots[tools_existence[29]] = \
                            (chosen_game.r_slots[tools_existence[29]][0], None)
                            chosen_game.copy_bullets_for_new()
                        elif to_use == 30 :
                            chosen_game.r_slots[tools_existence[30]] = \
                            (chosen_game.r_slots[tools_existence[30]][0], None)
                            if randint(0, 1) :
                                for slotid, slot in \
                                enumerate(chosen_game.r_slots) :
                                    chosen_game.r_slots[slotid]=(slot[0], None)
                                for slotid, slot in \
                                enumerate(chosen_game.e_slots) :
                                    chosen_game.e_slots[slotid]=(slot[0], None)
                                r_attack_boost = 0
                                e_attack_boost = 0
                                r_bulletproof.clear()
                                e_bulletproof.clear()
                            else :
                                pass
                        elif to_use == 31 :
                            chosen_game.r_slots[tools_existence[31]] = \
                            (chosen_game.r_slots[tools_existence[31]][0], None)
                            chosen_game.rel_turn_lap += \
                            len(chosen_game.bullets)
                            print("恭喜你,成功敲晕了对方!")
                        if used :
                            print("-1 道具", to_use)
                        if not chosen_game.bullets :
                            break
                        tools_existence.clear()
                        permaslots.clear()
                        for slotid, slot in enumerate(chosen_game.r_slots) :
                            if slot[1] is not None :
                                if slot[0] <= 0 :
                                    if slot[1] in permaslots :
                                        permaslots[slot[1]] += 1
                                    else :
                                        permaslots[slot[1]] = 1
                                tools_existence[slot[1]] = slotid
                    else :
                        print("道具", to_use, "不存在或未拥有")
            elif operation == 8 :
                print("恶魔的道具库:")
                permaslots: Dict[int, int] = {}
                for slot in chosen_game.e_slots :
                    if slot[1] is not None and slot[0] <= 0 :
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
                    print("作用:", chosen_game.tools[k][1])
                for slot in chosen_game.e_slots :
                    if slot[1] is not None and slot[0] > 0 :
                        print("道具", slot[1], ":",
                              chosen_game.tools[slot[1]][0])
                        print("作用:", chosen_game.tools[slot[1]][1])
                        print("还有", slot[0], "回合到期")
            elif operation == 1 :
                round_turn_count += 1
                period_turn_count += 1
                total_turn_count += 1
                gamesave.play_turns += 1
                if r_stamina > 0 :
                    r_stamina -= 1
                true_on_r = False
                true_on_e = False
                shoot_combo_addition = 0
                comboshoot_consume_num = 0
                while shoot_combo_addition < len(chosen_game.bullets) :
                    comboshoot_consume_num += 1
                    if random() >= 0.5 ** r_comboshoot_level :
                        shoot_combo_addition += 1
                    else :
                        break
                if shoot_combo_addition == len(chosen_game.bullets) :
                    chosen_game.rel_turn_lap += 1
                r_comboshoot_level -= comboshoot_consume_num
                if r_comboshoot_level < 0 :
                    r_comboshoot_level = 0
                if r_cursed_shoot_level > 0 :
                    shoots_result = chosen_game.shoots(
                        False, True, 1.,
                        shoot_combo_addition+r_multishoot_level+1 \
                        if shoot_combo_addition+r_multishoot_level<\
                           len(chosen_game.bullets) \
                        else len(chosen_game.bullets)
                    )
                    r_cursed_shoot_level -= 1
                elif r_againstshoot_promises > 0 :
                    shoots_result = chosen_game.shoots(
                        False, True, 0.,
                        shoot_combo_addition+r_multishoot_level+1 \
                        if shoot_combo_addition+r_multishoot_level<\
                           len(chosen_game.bullets) \
                        else len(chosen_game.bullets)
                    )
                    r_againstshoot_promises -= 1
                else :
                    shoots_result = chosen_game.shoots(
                        False, True,
                        combo=shoot_combo_addition+r_multishoot_level+1 \
                        if shoot_combo_addition+r_multishoot_level<\
                           len(chosen_game.bullets) \
                        else len(chosen_game.bullets)
                    )
                base_shoot = True
                for shoot_result in shoots_result :
                    if shoot_result[0] is not None :
                        if base_shoot :
                            base_shoot = False
                        elif shoot_combo_addition :
                            shoot_combo_addition -= 1
                        else :
                            r_multishoot_level -= 1
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
                                        gamesave.add_exp(
                                            ceil((base_attack+r_attack_boost)*\
                                                 GAMEMODE_SET[gamemode_i][2]/2)
                                        )
                                    elif not debug :
                                        gamesave.add_exp((base_attack+\
                                                          r_attack_boost)//2)
                                    true_on_r = True
                                    print("感觉像是去奈何桥走了一遭,竟然是个实弹!")
                                    for _ in range(base_attack+r_attack_boost):
                                        if random() < r_hurts / 8. :
                                            chosen_game.r_hp -= 2
                                            gamesave.damage_caused_to_r += 2
                                            gamesave.damage_caught += 2
                                        else :
                                            chosen_game.r_hp -= 1
                                            gamesave.damage_caused_to_r += 1
                                            gamesave.damage_caught += 1
                                    print("你的生命值:", chosen_game.r_hp)
                                    if random() >= r_hurts / 8. :
                                        r_hurts += 1
                                        assert 0 <= r_hurts < 9
                                else :
                                    gamesave.exploded_againstshoot_falses += 1
                                    print("啊哈!,是个空弹!")
                            else :
                                if bullets_i[0] :
                                    gamesave.success_againstshoot_trues += 1
                                else :
                                    gamesave.success_againstshoot_falses += 1
                                if e_bullet_catcher_level :
                                    if bullets_i[0] :
                                        if random() < \
                                           (1-0.8**e_bullet_catcher_level) / \
                                           (1+r_attack_boost) :
                                            e_bullet_catcher_level = 0
                                            chosen_game.bullets.append(True)
                                            if e_stamina > 0 :
                                                e_stamina -= 1
                                            print("恶魔接住了一颗子弹")
                                            continue
                                    else :
                                        if random() < 0.8 / (1+r_attack_boost):
                                            e_bullet_catcher_level -= 1
                                            chosen_game.bullets.append(False)
                                            if e_stamina > 0 :
                                                e_stamina -= 1
                                            print("恶魔接住了一颗子弹")
                                            continue
                                if e_bulletproof :
                                    e_bulletproof[0] -= \
                                    randint(1, ceil((r_attack_boost+1)**0.5))
                                    print("恶魔的防弹衣承受了这次撞击")
                                    if e_bulletproof[0] <= 0 :
                                        if random() >= 2**(e_bulletproof[0]-1):
                                            del e_bulletproof[0]
                                            e_breakcare_potential += 1
                                            if not e_bulletproof :
                                                for _ in \
                                                range(e_breakcare_potential) :
                                                    if random() < 0.15 :
                                                        e_breakcare_rounds += 1
                                                e_breakcare_potential = 0
                                            print("恶魔的一件防弹衣爆了")
                                elif bullets_i[0] :
                                    if nightmare :
                                        gamesave.add_exp(
                                            ceil((base_attack+\
                                                  r_attack_boost)/2)
                                        )
                                    elif not debug :
                                        gamesave.add_exp((base_attack+\
                                                          r_attack_boost)//2)
                                    true_on_e = True
                                    print("运气非常好,是个实弹!")
                                    for _ in range(base_attack+r_attack_boost):
                                        if random() < e_hurts / 8. :
                                            chosen_game.e_hp -= 2
                                            gamesave.damage_caused_to_e += 2
                                        else :
                                            chosen_game.e_hp -= 1
                                            gamesave.damage_caused_to_e += 1
                                    print("恶魔生命值:", chosen_game.e_hp)
                                    if random() >= e_hurts / 8. :
                                        e_hurts += 1
                                        assert 0 <= e_hurts < 9
                                else :
                                    print("很遗憾,是个空弹")
                if not true_on_r and r_stamina < 32 and \
                   random() < 1. / (r_hurts+1) :
                    r_stamina += 1
                if not true_on_e and e_stamina < 32 and \
                   random() < 1. / (e_hurts+1) :
                    e_stamina += 1
                if r_stamina < 8 and random() < 1 - (r_stamina/8.) :
                    chosen_game.rel_turn_lap -= 1
                if e_stamina < 8 and random() < 1 - (e_stamina/8.) :
                    chosen_game.rel_turn_lap += 1
                r_attack_boost = 0
            elif operation == 0 :
                round_turn_count += 1
                period_turn_count += 1
                total_turn_count += 1
                gamesave.play_turns += 1
                true_on_r = False
                true_on_e = False
                if r_stamina > 0 :
                    r_stamina -= 1
                if r_selfshoot_promises :
                    shoot_result = chosen_game.shoot(True, True, 0.)
                    r_selfshoot_promises -= 1
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
                            if e_bullet_catcher_level :
                                if bullets_i[0] :
                                    if random() < \
                                       (1-0.8**e_bullet_catcher_level) / \
                                       (1+r_attack_boost):
                                        e_bullet_catcher_level = 0
                                        chosen_game.bullets.append(True)
                                        if e_stamina > 0 :
                                            e_stamina -= 1
                                        print("恶魔接住了一颗子弹")
                                        continue
                                else :
                                    if random() < 0.8 / (1+r_attack_boost) :
                                        e_bullet_catcher_level -= 1
                                        chosen_game.bullets.append(False)
                                        if e_stamina > 0 :
                                            e_stamina -= 1
                                        print("恶魔接住了一颗子弹")
                                        continue
                            if e_bulletproof :
                                e_bulletproof[0] -= \
                                randint(1, ceil((r_attack_boost+1)**0.5))
                                print("恶魔的防弹衣承受了这次撞击")
                                if e_bulletproof[0] <= 0 :
                                    if random() >= 2 ** (e_bulletproof[0]-1) :
                                        del e_bulletproof[0]
                                        e_breakcare_potential += 1
                                        if not e_bulletproof :
                                            for _ in \
                                            range(e_breakcare_potential) :
                                                if random() < 0.15 :
                                                    e_breakcare_rounds += 1
                                            e_breakcare_potential = 0
                                        print("恶魔的一件防弹衣爆了")
                            elif bullets_i[0] :
                                true_on_e = True
                                print("运气非常好,是个实弹!")
                                for _ in range(base_attack+r_attack_boost) :
                                    if random() < e_hurts / 8. :
                                        chosen_game.e_hp -= 2
                                        gamesave.damage_caused_to_e += 2
                                    else :
                                        chosen_game.e_hp -= 1
                                        gamesave.damage_caused_to_e += 1
                                print("恶魔生命值:", chosen_game.e_hp)
                                if random() >= e_hurts / 8. :
                                    e_hurts += 1
                                    assert 0 <= e_hurts < 9
                            else :
                                print("很遗憾,是个空弹")
                        else :
                            if bullets_i[0] :
                                gamesave.success_selfshoot_trues += 1
                                true_on_r = True
                                print("感觉像是去奈何桥走了一遭,竟然是个实弹!")
                                for _ in range(base_attack+r_attack_boost) :
                                    if random() < r_hurts / 8. :
                                        chosen_game.r_hp -= 2
                                        gamesave.damage_caused_to_r += 2
                                        gamesave.damage_caught += 2
                                    else :
                                        chosen_game.r_hp -= 1
                                        gamesave.damage_caused_to_r += 1
                                        gamesave.damage_caught += 1
                                print("你的生命值:", chosen_game.r_hp)
                                if random() >= r_hurts / 8. :
                                    r_hurts += 1
                                    assert 0 <= r_hurts < 9
                            else :
                                gamesave.success_selfshoot_falses += 1
                                print("啊哈!,是个空弹!")
                if not true_on_r and r_stamina < 32 and \
                   random() < 1. / (r_hurts+1) :
                    r_stamina += 1
                if not true_on_e and e_stamina < 32 and \
                   random() < 1. / (e_hurts+1) :
                    e_stamina += 1
                if r_stamina < 8 and random() < 1 - (r_stamina/8.) :
                    chosen_game.rel_turn_lap -= 1
                if e_stamina < 8 and random() < 1 - (e_stamina/8.) :
                    chosen_game.rel_turn_lap += 1
                r_attack_boost = 0
            else :
                print("请确定输入的数字正确")
        else :
            gametime_time_start = time()
            if not chosen_game.bullets :
                break
            for slotid, slot in enumerate(chosen_game.e_slots) :
                will_use: bool
                if e_breakcare_rounds > 0 or not chosen_game.bullets :
                    break
                if slot[1] == 0 :
                    will_use = nightmare or not randint(0, 3)
                    if will_use :
                        chosen_game.e_slots[slotid] = (slot[0], None)
                        if e_cursed_shoot_level > 0 :
                            e_cursed_shoot_level -= 1
                        else :
                            e_selfshoot_promises += 1
                elif slot[1] == 1 :
                    will_use = nightmare or not randint(0, 3)
                    if will_use :
                        chosen_game.e_slots[slotid] = (slot[0], None)
                        if e_cursed_shoot_level > 0 :
                            e_cursed_shoot_level -= 1
                        else :
                            e_againstshoot_promises += 1
                elif slot[1] == 3 :
                    will_use = \
                    True if nightmare and chosen_game.bullets[0] and \
                            chosen_game.bullets.count(True) == 1 else \
                    not randint(0, 1)
                    if will_use :
                        chosen_game.e_slots[slotid] = (slot[0], None)
                        if chosen_game.bullets.pop(0) :
                            print("恶魔排出了一颗实弹")
                        else:
                            print("恶魔排出了一颗空弹")
                        if not chosen_game.bullets :
                            break
                elif slot[1] == 2 :
                    will_use = chosen_game.bullets[0] if nightmare else \
                                     not randint(0, 1)
                    if will_use :
                        chosen_game.e_slots[slotid] = (slot[0], None)
                        e_attack_boost += 1
                        print("恶魔使用了小刀,哦吼吼,结果会如何呢?")
                elif slot[1] == 4 :
                    will_use = nightmare or not randint(0, 1)
                    if will_use :
                        chosen_game.e_slots[slotid] = (slot[0], None)
                        chosen_game.rel_turn_lap -= 1
                        print("恭喜恶魔,成功把你变成了猫娘!")
                elif slot[1] == 5 :
                    will_use = nightmare or not randint(0, 1)
                    if will_use :
                        chosen_game.e_slots[slotid] = (slot[0], None)
                        if nightmare or\
                           chosen_game.r_hp <= 3 + r_hurts / 4. or \
                           random() < 0.5 ** (chosen_game.r_hp-3-r_hurts/4.) :
                            chosen_game.e_hp += 1
                            print("恶魔使用了道德的崇高赞许,回复了1点生命")
                        else :
                            print("因为恶魔的不诚实,恶魔并未回复生命,"
                                  "甚至失去了道德的崇高赞许")
                elif slot[1] == 6 :
                    will_use = nightmare or not randint(0, 1)
                    if will_use :
                        chosen_game.e_slots[slotid] = (slot[0], None)
                        print("恶魔查看了枪里的子弹并笑了一下")
                elif slot[1] == 7 :
                    will_use = not randint(0, 3)
                    if will_use :
                        chosen_game.e_slots[slotid] = (slot[0], None)
                        nonlimit_tool_slotids: List[int] = []
                        for slotid, slot in enumerate(chosen_game.r_slots) :
                            if slot[1] is not None :
                                if chosen_game.tools_sending_limit_in_game[
                                    slot[1]
                                ] <= 0 :
                                    nonlimit_tool_slotids.append(slotid)
                        bring_tool_id: Optional[int] = None
                        if random() < 1 / (len(nonlimit_tool_slotids)+1) :
                            nonlimit_toolids: List[int] = []
                            for tool_id in chosen_game.tools :
                                if chosen_game.tools_sending_limit_in_game[
                                    tool_id
                                ] <= 0 :
                                    nonlimit_toolids.append(tool_id)
                            bring_tool_id = choice(nonlimit_toolids)
                        else :
                            taken_slotid: int = choice(nonlimit_tool_slotids)
                            bring_tool_id = \
                            chosen_game.r_slots[taken_slotid][1]
                            chosen_game.r_slots[taken_slotid] = \
                            (chosen_game.r_slots[taken_slotid][0], None)
                        if bring_tool_id is None :
                            assert 0
                        for slotid, slot in enumerate(chosen_game.e_slots) :
                            if slot[1] is None :
                                chosen_game.e_slots[slotid] = \
                                (chosen_game.e_slots[slotid][0], bring_tool_id)
                                break
                        else :
                            assert False
                elif slot[1] == 8 :
                    will_use = not randint(0, 7)
                    if will_use :
                        if chosen_game.slots_sharing is None :
                            chosen_game.e_slots[slotid] = (slot[0], None)
                            new_keep_rounds: int = \
                            choice([1, 1, 1, 2, 2, 2, 2, 2, 3, 3])
                            chosen_game.slots_sharing = \
                            (not 1, new_keep_rounds, chosen_game.e_slots)
                            chosen_game.e_slots = chosen_game.r_slots
                        elif not chosen_game.slots_sharing[0] :
                            chosen_game.e_slots[slotid] = (slot[0], None)
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
                            (not 1, new_keep_rounds, chosen_game.e_slots)
                elif slot[1] == 9 :
                    will_use = nightmare or not randint(0, 1)
                    if will_use :
                        chosen_game.e_slots[slotid] = (slot[0], None)
                        print("恶魔穿上了一件防弹衣")
                        e_bulletproof.insert(0, 3)
                elif slot[1] == 11 :
                    will_use = nightmare or not randint(0, 5)
                    if will_use :
                        chosen_game.e_slots[slotid] = (slot[0], None)
                        dice_sum: int = \
                        randint(1, 6) + randint(1, 6) + randint(1, 6)
                        if debug :
                            print("恶魔摇出了", dice_sum, "点")
                        if dice_sum == 3 :
                            e_breakcare_rounds += 2
                        elif dice_sum == 4 :
                            chosen_game.e_hp -= 2
                            print("恶魔失去了2点生命")
                        elif dice_sum == 5 :
                            for bullet_index \
                            in range(2, len(chosen_game.bullets)) :
                                chosen_game.bullets[bullet_index] = \
                                not randint(0, 1)
                        elif dice_sum == 6 :
                            chosen_game.e_hp -= 1
                            print("恶魔失去了1点生命")
                        elif dice_sum == 7 :
                            vanishable_indices: List[int] = []
                            for slotid,slot in enumerate(chosen_game.e_slots) :
                                if slot[1] is not None :
                                    if chosen_game.tools_sending_limit_in_game[
                                        slot[1]
                                    ] <= 0 :
                                        vanishable_indices.append(slotid)
                            if vanishable_indices :
                                vanish_index: int = choice(vanishable_indices)
                                chosen_game.e_slots[vanish_index] = \
                                (chosen_game.e_slots[vanish_index][0], None)
                        elif dice_sum == 8 :
                            pass
                        elif dice_sum == 10 :
                            chosen_game.e_hp += 1
                            print("恶魔获得了1点生命")
                        elif dice_sum == 12 :
                            e_attack_boost += 2
                            if randint(0, 1) :
                                print("恶魔的攻击力提高了2点")
                        elif dice_sum == 13 :
                            chosen_game.r_hp -= 1
                            print("你失去了1点生命")
                            if chosen_game.r_hp <= 0 :
                                break
                        elif dice_sum == 14 :
                            chosen_game.rel_turn_lap -= 2 - (not randint(0, 2))
                        elif dice_sum == 15 :
                            chosen_game.r_hp -= 2
                            print("你失去了2点生命")
                            if chosen_game.r_hp <= 0 :
                                break
                        elif dice_sum == 18 :
                            chosen_game.r_hp //= 8
                            print("你受到暴击!!!")
                            print("你的生命值:", chosen_game.r_hp)
                elif slot[1] == 12 :
                    will_use = not randint(0, 1)
                    if will_use :
                        temporary_slots: List[int] = []
                        for slotid in range(len(chosen_game.e_slots)) :
                            if chosen_game.e_slots[slotid][0] > 0 :
                                temporary_slots.append(slotid)
                        if temporary_slots :
                            chosen_game.e_slots[slotid] = (slot[0], None)
                            delay_prob: float = len(temporary_slots) ** 0.5
                            for slotid in temporary_slots :
                                if random() < delay_prob :
                                    chosen_game.e_slots[slotid] = \
                                    (chosen_game.e_slots[slotid][0]+1,
                                     chosen_game.e_slots[slotid][1])
                elif slot[1] == 13 :
                    will_use = not randint(0, 7) and \
                                     abs(chosen_game.r_hp-chosen_game.e_hp) > 1
                    if will_use :
                        chosen_game.e_slots[slotid] = (slot[0], None)
                        if randint(0, 1) :
                            print("你变成了恶魔的样子")
                            chosen_game.r_hp = chosen_game.e_hp
                            chosen_game.r_slots.clear()
                            chosen_game.r_slots.extend(chosen_game.e_slots)
                            chosen_game.r_sending_total.clear()
                            chosen_game.r_sending_total.update(
                                chosen_game.e_sending_total.copy()
                            )
                            r_attack_boost = e_attack_boost
                            r_bulletproof.clear()
                            r_bulletproof.extend(e_bulletproof)
                            r_bullet_catcher_level = e_bullet_catcher_level
                            r_selfshoot_promises = e_selfshoot_promises
                            r_againstshoot_promises = e_againstshoot_promises
                            r_multishoot_level = e_multishoot_level
                            r_comboshoot_level = e_comboshoot_level
                            r_cursed_shoot_level = e_cursed_shoot_level
                            r_hurts = e_hurts
                            r_stamina = e_stamina
                            r_0band_level = e_0band_level
                            r_1band_level = e_1band_level
                        else :
                            print("恶魔变成了你的样子")
                            chosen_game.e_hp = chosen_game.r_hp
                            chosen_game.e_slots.clear()
                            chosen_game.e_slots.extend(chosen_game.r_slots)
                            chosen_game.e_sending_total.clear()
                            chosen_game.e_sending_total.update(
                                chosen_game.r_sending_total.copy()
                            )
                            e_attack_boost = r_attack_boost
                            e_bulletproof.clear()
                            e_bulletproof.extend(r_bulletproof)
                            e_bullet_catcher_level = r_bullet_catcher_level
                            e_selfshoot_promises = r_selfshoot_promises
                            e_againstshoot_promises = r_againstshoot_promises
                            e_multishoot_level = r_multishoot_level
                            e_comboshoot_level = r_comboshoot_level
                            e_cursed_shoot_level = r_cursed_shoot_level
                            e_hurts = r_hurts
                            e_stamina = r_stamina
                            e_0band_level = r_0band_level
                            e_1band_level = r_1band_level
                        chosen_game.rel_turn_lap = 0
                elif slot[1] == 14 :
                    will_use = not randint(0, 2)
                    if will_use :
                        chosen_game.e_slots[slotid] = (slot[0], None)
                        e_bullet_catcher_level += 1
                elif slot[1] == 15 :
                    will_use = not randint(0, 3)
                    if will_use :
                        chosen_game.e_slots[slotid] = (slot[0], None)
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
                        chosen_game.e_slots[slotid] = (slot[0], None)
                        shuffle(chosen_game.bullets)
                        print("恶魔重整了一下弹药")
                elif slot[1] == 17 :
                    will_use = all(chosen_game.bullets[:e_multishoot_level+2])\
                               if nightmare else not randint(0, 3)
                    if will_use :
                        chosen_game.e_slots[slotid] = (slot[0], None)
                        e_multishoot_level += 1
                elif slot[1] == 18 :
                    will_use = not randint(0, 3)
                    if will_use :
                        chosen_game.e_slots[slotid] = (slot[0], None)
                        e_comboshoot_level += 1
                elif slot[1] == 21 :
                    will_use = nightmare or not randint(0, 2)
                    if will_use :
                        chosen_game.e_slots[slotid] = (slot[0], None)
                        r_cursed_shoot_level += 1
                elif slot[1] == 22 :
                    will_use = not randint(0, 2)
                    if will_use :
                        chosen_game.e_slots[slotid] = (
                            slot[0], 24 if chosen_game.bullets.pop(randint(
                                0, len(chosen_game.bullets)-1
                            )) else 23
                        )
                        print("恶魔取出了一颗子弹")
                elif slot[1] == 23 :
                    will_use = not randint(0, 2)
                    if will_use :
                        chosen_game.e_slots[slotid] = (slot[0], None)
                        chosen_game.bullets.insert(randint(0, len(
                            chosen_game.bullets
                        )), False)
                        print("恶魔放入了一颗空弹")
                elif slot[1] == 24 :
                    will_use = not randint(0, 2)
                    if will_use :
                        chosen_game.e_slots[slotid] = (slot[0], None)
                        chosen_game.bullets.insert(randint(0, len(
                            chosen_game.bullets
                        )), True)
                        print("恶魔放入了一颗实弹")
                elif slot[1] == 25 :
                    will_use = not randint(0, 2)
                    if will_use :
                        chosen_game.e_slots[slotid] = (slot[0], None)
                        bullet_i_to_ins: int = randint(0, len(
                            chosen_game.bullets
                        ))
                        chosen_game.bullets.insert(bullet_i_to_ins, True)
                        if bullet_i_to_ins < len(chosen_game.bullets) - 1 :
                            chosen_game.bullets[bullet_i_to_ins+1] = \
                            not randint(0, 1)
                        print("恶魔放入了一颗神秘子弹")
                elif slot[1] == 26 :
                    will_use = e_hurts > e_0band_level + e_1band_level and \
                               not randint(0, 1)
                    if will_use :
                        chosen_game.e_slots[slotid] = (slot[0], None)
                        e_0band_level += 1
                        print("恶魔使用了绷带")
                elif slot[1] == 27 :
                    will_use = not randint(0, 4)
                    if will_use :
                        chosen_game.e_slots[slotid] = (slot[0], None)
                        if chosen_game.e_hp < 2 :
                            chosen_game.e_hp += 5
                            print("恶魔使用了医疗包,回复了5点生命")
                        elif chosen_game.e_hp < 5 :
                            chosen_game.e_hp += 4
                            print("恶魔使用了医疗包,回复了4点生命")
                        elif chosen_game.e_hp < 9 :
                            chosen_game.e_hp += 3
                            print("恶魔使用了医疗包,回复了3点生命")
                        elif chosen_game.e_hp < 14 :
                            chosen_game.e_hp += 2
                            print("恶魔使用了医疗包,回复了2点生命")
                        else :
                            chosen_game.e_hp += 1
                            print("恶魔使用了医疗包,回复了1点生命")
                        if e_hurts < 1 :
                            chosen_game.e_hp += 2
                        elif e_hurts < 4 :
                            chosen_game.e_hp += 1
                        e_hurts = 0
                elif slot[1] == 28 :
                    will_use = not (not chosen_game.bullets.count(True) >> 1 \
                                    if nightmare else randint(0, 5))
                    if will_use :
                        chosen_game.e_slots[slotid] = (slot[0], None)
                        while chosen_game.bullets :
                            print("恶魔排出了一颗实弹" if chosen_game.bullets.pop(0) \
                                  else "恶魔排出了一颗空弹")
                elif slot[1] == 29 :
                    will_use = not randint(0, 7)
                    if will_use :
                        chosen_game.e_slots[slotid] = (slot[0], None)
                        chosen_game.copy_bullets_for_new()
                elif slot[1] == 31 :
                    will_use = nightmare or not randint(0, 5)
                    if will_use :
                        chosen_game.e_slots[slotid] = (slot[0], None)
                        chosen_game.rel_turn_lap -= len(chosen_game.bullets)
                        print("恭喜恶魔,成功把你变成了猫娘!")
            if not chosen_game.bullets :
                break
            round_turn_count += 1
            period_turn_count += 1
            total_turn_count += 1
            gamesave.play_turns += 1
            true_on_r = False
            true_on_e = False
            if e_stamina > 0 :
                e_stamina -= 1
            is_to_self: bool = ((not e_cursed_shoot_level) !=
                                chosen_game.bullets[0]) if \
                               nightmare and e_breakcare_rounds <= 0 else \
                               not randint(0, 1)
            if is_to_self :
                if e_cursed_shoot_level > 0 :
                    shoot_result = chosen_game.shoot(True, False, 1.)
                    e_cursed_shoot_level -= 1
                elif e_selfshoot_promises > 0 :
                    shoot_result = chosen_game.shoot(True, False, 0.)
                    e_selfshoot_promises -= 1
                else :
                    shoot_result = chosen_game.shoot(True, False)
                print("恶魔将枪口对准了自己")
                for bullets_i in shoot_result :
                    if bullets_i is not None :
                        if bullets_i[1] :
                            print("啊哦,子弹居然炸膛了!")
                            if r_bullet_catcher_level :
                                if bullets_i[0] :
                                    if random() < \
                                       (1-0.8**r_bullet_catcher_level) / \
                                       (1+e_attack_boost):
                                        gamesave.bullets_caught += 1
                                        r_bullet_catcher_level = 0
                                        chosen_game.bullets.append(True)
                                        if r_stamina > 0 :
                                            r_stamina -= 1
                                        print("你接住了一颗子弹")
                                        continue
                                else :
                                    if random() < 0.8 / (1+e_attack_boost) :
                                        gamesave.bullets_caught += 1
                                        r_bullet_catcher_level -= 1
                                        chosen_game.bullets.append(False)
                                        if r_stamina > 0 :
                                            r_stamina -= 1
                                        print("你接住了一颗子弹")
                                        continue
                            if r_bulletproof :
                                r_bulletproof[0] -= \
                                randint(1, ceil((e_attack_boost+1)**0.5))
                                print("你的防弹衣承受了这次撞击")
                                if r_bulletproof[0] <= 0 :
                                    if random() >= 2 ** (r_bulletproof[0]-1) :
                                        del r_bulletproof[0]
                                        r_breakcare_potential += 1
                                        if not r_bulletproof :
                                            for _ in \
                                            range(r_breakcare_potential) :
                                                if random() < 0.15 :
                                                    r_breakcare_rounds += 1
                                            r_breakcare_potential = 0
                                        print("你的一件防弹衣爆了")
                            elif bullets_i[0] :
                                true_on_r = True
                                print("运气非常差,是个实弹!")
                                for _ in range(base_attack+e_attack_boost) :
                                    if random() < r_hurts / 8. :
                                        chosen_game.r_hp -= 2
                                        gamesave.damage_caught += 2
                                    else :
                                        chosen_game.r_hp -= 1
                                        gamesave.damage_caught += 1
                                print("你的生命值:", chosen_game.r_hp)
                                if random() >= r_hurts / 8. :
                                    r_hurts += 1
                                    assert 0 <= r_hurts < 9
                            else :
                                print("很幸运,是个空弹")
                        else :
                            if bullets_i[0] :
                                true_on_e = True
                                print("“砰!”一声枪响,它自杀了,你心里暗喜")
                                for _ in range(base_attack+e_attack_boost) :
                                    chosen_game.e_hp -= \
                                    2 if random() < e_hurts / 8. else 1
                                print("恶魔生命值:", chosen_game.e_hp)
                                if random() >= e_hurts / 8. :
                                    e_hurts += 1
                                    assert 0 <= e_hurts < 9
                            else :
                                print("“啊哈!,是个空弹!”恶魔嘲讽道")
            else :
                shoot_combo_addition = 0
                comboshoot_consume_num = 0
                while shoot_combo_addition < len(chosen_game.bullets) :
                    comboshoot_consume_num += 1
                    if random() >= 0.5 ** e_comboshoot_level :
                        shoot_combo_addition += 1
                    else :
                        break
                if shoot_combo_addition == len(chosen_game.bullets) :
                    chosen_game.rel_turn_lap -= 1
                e_comboshoot_level -= comboshoot_consume_num
                if e_comboshoot_level < 0 :
                    e_comboshoot_level = 0
                if e_cursed_shoot_level > 0 :
                    shoots_result = chosen_game.shoots(
                        False, False, 1.,
                        shoot_combo_addition+e_multishoot_level+1 \
                        if shoot_combo_addition+e_multishoot_level<\
                           len(chosen_game.bullets) \
                        else len(chosen_game.bullets)
                    )
                    e_cursed_shoot_level -= 1
                elif e_againstshoot_promises > 0 or nightmare :
                    shoots_result = chosen_game.shoots(
                        False, False, 0.,
                        shoot_combo_addition+e_multishoot_level+1 \
                        if shoot_combo_addition+e_multishoot_level<\
                           len(chosen_game.bullets) \
                        else len(chosen_game.bullets)
                    )
                    if e_againstshoot_promises :
                        e_againstshoot_promises -= 1
                else :
                    shoots_result = chosen_game.shoots(
                        False, False,
                        combo=shoot_combo_addition+e_multishoot_level+1 \
                        if shoot_combo_addition+e_multishoot_level<\
                           len(chosen_game.bullets) \
                        else len(chosen_game.bullets)
                    )
                base_shoot = True
                print("恶魔朝你开了一枪")
                for shoot_result in shoots_result :
                    if shoot_result[0] is not None :
                        if base_shoot :
                            base_shoot = False
                        elif shoot_combo_addition :
                            shoot_combo_addition -= 1
                        else :
                            e_multishoot_level -= 1
                    for bullets_i in shoot_result :
                        if bullets_i is not None :
                            if bullets_i[1] :
                                print("啊哦,子弹居然炸膛了!")
                                if bullets_i[0] :
                                    true_on_e = True
                                    print("“砰!”一声枪响,它自杀了,你心里暗喜")
                                    for _ in range(base_attack+e_attack_boost):
                                        chosen_game.e_hp -= \
                                        2 if random() < e_hurts / 8. else 1
                                    print("恶魔生命值:", chosen_game.e_hp)
                                    if random() >= e_hurts / 8. :
                                        e_hurts += 1
                                        assert 0 <= e_hurts < 9
                                else :
                                    print("“啊哈!,是个空弹!”恶魔嘲讽道")
                            else :
                                if r_bullet_catcher_level :
                                    if bullets_i[0] :
                                        if random() < \
                                           (1-0.8**r_bullet_catcher_level) / \
                                           (1+e_attack_boost):
                                            gamesave.bullets_caught += 1
                                            r_bullet_catcher_level = 0
                                            chosen_game.bullets.append(True)
                                            if r_stamina > 0 :
                                                r_stamina -= 1
                                            print("你接住了一颗子弹")
                                            continue
                                    else :
                                        if random() < 0.8 / (1+e_attack_boost):
                                            gamesave.bullets_caught += 1
                                            r_bullet_catcher_level -= 1
                                            chosen_game.bullets.append(False)
                                            if r_stamina > 0 :
                                                r_stamina -= 1
                                            print("你接住了一颗子弹")
                                            continue
                                if r_bulletproof :
                                    r_bulletproof[0] -= \
                                    randint(1, ceil((e_attack_boost+1)**0.5))
                                    print("你的防弹衣承受了这次撞击")
                                    if r_bulletproof[0] <= 0 :
                                        if random() >= 2**(r_bulletproof[0]-1):
                                            del r_bulletproof[0]
                                            r_breakcare_potential += 1
                                            if not r_bulletproof :
                                                for _ in \
                                                range(r_breakcare_potential) :
                                                    if random() < 0.15 :
                                                        r_breakcare_rounds += 1
                                                r_breakcare_potential = 0
                                            print("你的一件防弹衣爆了")
                                elif bullets_i[0] :
                                    true_on_r = True
                                    print("运气非常差,是个实弹!")
                                    for _ in range(base_attack+e_attack_boost):
                                        if random() < r_hurts / 8. :
                                            chosen_game.r_hp -= 2
                                            gamesave.damage_caught += 2
                                        else :
                                            chosen_game.r_hp -= 1
                                            gamesave.damage_caught += 1
                                    print("你的生命值:", chosen_game.r_hp)
                                    if random() >= r_hurts / 8. :
                                        r_hurts += 1
                                        assert 0 <= r_hurts < 9
                                else :
                                    print("很幸运,是个空弹")
            if not true_on_r and r_stamina < 32 and \
               random() < 1. / (r_hurts+1) :
                r_stamina += 1
            if not true_on_e and e_stamina < 32 and \
               random() < 1. / (e_hurts+1) :
                e_stamina += 1
            if r_stamina < 8 and random() < 1 - (r_stamina/8.) :
                chosen_game.rel_turn_lap -= 1
            if e_stamina < 8 and random() < 1 - (e_stamina/8.) :
                chosen_game.rel_turn_lap += 1
            e_attack_boost = 0
            gamesave.active_gametime += time() - gametime_time_start
        if not debug :
            gamesave.add_exp()

if chosen_game.r_hp > 0 :
    if chosen_game.e_hp == 0 :
        print("恭喜你，成功把恶魔变成了猫娘！")
    elif chosen_game.e_hp == -1 :
        print("恭喜你，成功把恶魔打得体无完肤！")
    elif chosen_game.e_hp == -2 :
        print("恭喜你，成功把恶魔化作一团灰烬！")
    else :
        print("恭喜你，成功让恶魔原地消失！")
elif chosen_game.r_hp == 0 :
    if chosen_game.e_hp > 0 :
        print("唉....你被恶魔变成了猫娘")
    elif chosen_game.e_hp == 0 :
        print("你们最后同归于尽了")
        gamesave.add_exp(25)
        gamesave.add_coins()
    elif chosen_game.e_hp == -1 :
        print("你让恶魔面目全非，但你也付出了生命的代价")
        gamesave.add_exp(80)
        gamesave.add_coins(3)
    elif chosen_game.e_hp == -2 :
        print("恶魔为你化作灰烬，而你成为了猫娘")
        gamesave.add_exp(400)
        gamesave.add_coins(10)
    else :
        print("你作为猫娘看着恶魔消失于世上")
        gamesave.add_exp(1500)
        gamesave.add_coins(32)
elif chosen_game.r_hp == -1 :
    if chosen_game.e_hp > 0 :
        print("唉....你被恶魔打得体无完肤")
    elif chosen_game.e_hp == 0 :
        print("恶魔让你面目全非，但他也付出了生命的代价")
        gamesave.add_exp(80)
        gamesave.add_coins(3)
    elif chosen_game.e_hp == -1 :
        print("二人幸终……")
        gamesave.add_exp(400)
        gamesave.add_coins(10)
    elif chosen_game.e_hp == -2 :
        print("恶魔为你化作灰烬，而你也面目狼狈……")
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
        print("你为恶魔化作灰烬，而它成为了猫娘")
        gamesave.add_exp(400)
        gamesave.add_coins(10)
    elif chosen_game.e_hp == -1 :
        print("你为恶魔化作灰烬，而它也面目狼狈……")
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
        print("恶魔作为猫娘看着你消失于世上")
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
