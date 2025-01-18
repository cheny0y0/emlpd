from datetime import date
from math import atan, log
from random import randint, random
from sys import argv
from time import sleep, time
from typing import Callable, Optional

from .gameapi import GameSave, VER_STRING
from .gameinst import CLASSIC_MODE

gamesave: GameSave = GameSave()

EXP_MUL_CALC: Callable[[int], float] = lambda x: (
    (16*(-0.5*log((0.0625*x-120)**2+1)+atan(0.0625*x-120)*(0.0625*x-120))+
     1.5625*x)/32768+1-0.08921291791932255
)*((1+x/65536)**0.5)

print("恶魔轮盘赌（重构版） v"+VER_STRING)
debug: bool = "debug" in argv[1:]
nightmare: bool = "nightmare" in argv[1:]
show_pp: bool = "show_pp" in argv[1:]
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
    print("警告：梦魇模式已激活。恶魔会变得无比强大！！！")
print("“哦！看看，又一个来送死的”")
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

attack_boost: int = 0
r_pp: int = 0
e_pp: int = 0
r_pp_combo: int = 0
e_pp_combo: int = 0
r_bullet_unknown: Optional[bool] = None if debug else True
e_bullet_unknown: Optional[bool] = None if nightmare else True

round_turn_count: int = 0
total_turn_count: int = 0
total_round_count: int = 0

while CLASSIC_MODE.r_hp > 0 and CLASSIC_MODE.e_hp > 0 :
    gametime_time_start: float = time()
    round_turn_count = 0
    total_round_count += 1
    gamesave.play_rounds += 1
    for i in CLASSIC_MODE.round_start_message :
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
    r_send_result: int = CLASSIC_MODE.send_tools_to_r()
    e_send_result: int = CLASSIC_MODE.send_tools_to_e()
    r_pp += r_send_result * 50
    e_pp += e_send_result * 50
    if r_send_result == 2 :
        print("你获得两个道具")
    else :
        r_pp_combo = 0
        if r_send_result == 1 :
            print("很遗憾，你道具数过多，只获得一个道具")
    if e_send_result == 2 :
        print("恶魔获得两个道具")
    else :
        e_pp_combo = 0
        if e_send_result == 1 :
            print("非常开心，恶魔道具数过多，只获得一个道具")
    CLASSIC_MODE.gen_bullets()
    sleep(1)
    print("子弹一共有", len(CLASSIC_MODE.bullets), "发")
    sleep(1)
    print("实弹", CLASSIC_MODE.bullets.count(True), "发 , 空弹",
          CLASSIC_MODE.bullets.count(False), "发")
    shoot_result: Optional[bool]
    gamesave.active_gametime += time() - gametime_time_start
    while CLASSIC_MODE.bullets :
        gametime_time_start = time()
        try :
            with open("emlpd.dat", "wb") as gamesave_file :
                gamesave_file.write(gamesave.serialize())
        except OSError as err :
            print("存档时遇到问题!", err)
        if CLASSIC_MODE.r_hp <= 0 or CLASSIC_MODE.e_hp < -1 or \
           (CLASSIC_MODE.e_hp <= 0 and CLASSIC_MODE.yourturn) :
            break
        if CLASSIC_MODE.rel_turn_lap < 0 :
            print("感觉...头晕晕的...要变成{0}了~".format(cat_girl))
        elif CLASSIC_MODE.rel_turn_lap :
            print("哈哈哈哈，恶魔被敲晕了，还是我的回合！")
        gamesave.active_gametime += time() - gametime_time_start
        if CLASSIC_MODE.yourturn :
            if CLASSIC_MODE.rel_turn_lap < 0 :
                CLASSIC_MODE.yourturn = not CLASSIC_MODE.yourturn
                CLASSIC_MODE.rel_turn_lap += 1
        else :
            if CLASSIC_MODE.rel_turn_lap > 0 :
                CLASSIC_MODE.yourturn = not CLASSIC_MODE.yourturn
                CLASSIC_MODE.rel_turn_lap -= 1
        if CLASSIC_MODE.yourturn :
            if debug :
                for i in CLASSIC_MODE.debug_message :
                    if i[1] is None :
                        if i[2] is None :
                            print(*i[0])
                        else :
                            print(*i[0], end=i[2])
                    elif i[2] is None :
                        print(*i[0], sep=i[1])
                    else :
                        print(*i[0], sep=i[1], end=i[2])
            if show_pp :
                print("当前你的表现分:", r_pp)
                print("当前恶魔表现分:", e_pp)
            print("当前为你的回合")
            print(
                "请选择：1朝对方开枪，0朝自己开枪，7打开道具库，8查看对方道具"
            )
            operation: int = 2
            try :
                operation = int(input())
            except ValueError :
                pass
            if operation == 7 :
                print("道具库：")
                for tool in CLASSIC_MODE.r_tools :
                    print("道具", tool, "：", CLASSIC_MODE.tools[tool][0],
                          sep="")
                    print("作用", CLASSIC_MODE.tools[tool][1], sep="：")
                print("返回请输入任意字母")
                to_use: Optional[int] = None
                try:
                    to_use = int(input("使用道具请按它的对应编号:"))
                except ValueError:
                    pass
                if to_use in CLASSIC_MODE.r_tools :
                    if to_use == 2 :
                        CLASSIC_MODE.r_tools.remove(2)
                        attack_boost += 1
                        print("你使用了小刀，结果会如何呢？真让人期待")
                    elif to_use == 3 :
                        CLASSIC_MODE.r_tools.remove(3)
                        print("你排出了一颗实弹" \
                              if CLASSIC_MODE.bullets.pop(0) \
                              else "你排出了一颗空弹")
                        if r_bullet_unknown is not None :
                            r_bullet_unknown = True
                    elif to_use == 4 :
                        CLASSIC_MODE.r_tools.remove(4)
                        CLASSIC_MODE.rel_turn_lap += 1
                        print("恭喜你，成功敲晕了对方！")
                    elif to_use == 5 :
                        CLASSIC_MODE.r_tools.remove(5)
                        if CLASSIC_MODE.r_hp < 4 or \
                           (random() < 0.5 ** (CLASSIC_MODE.r_hp-3) and
                            not nightmare) :
                            if CLASSIC_MODE.r_hp > 3 :
                                r_pp_combo += 1
                                r_pp += 2 ** (CLASSIC_MODE.r_hp-4) * 500 * \
                                        r_pp_combo
                            CLASSIC_MODE.r_hp += 1
                            gamesave.healed += 1
                            print("你使用了道德的崇高赞许，回复了一点生命")
                        else :
                            print("因为你的不诚实，你并未回复生命，"
                                  "甚至失去了道德的崇高赞许")
                    elif to_use == 6 :
                        CLASSIC_MODE.r_tools.remove(6)
                        if r_bullet_unknown is not None :
                            r_bullet_unknown = False
                        print("当前的子弹为实弹" \
                              if CLASSIC_MODE.bullets[0] \
                              else "当前的子弹为空弹")
            elif operation == 8 :
                print("恶魔的道具库：")
                for tool in CLASSIC_MODE.e_tools :
                    print("道具", tool, "：", CLASSIC_MODE.tools[tool][0],
                          sep="")
                    print("作用", CLASSIC_MODE.tools[tool][1], sep="：")
            elif operation == 1 :
                round_turn_count += 1
                total_turn_count += 1
                gamesave.play_turns += 1
                shoot_result = CLASSIC_MODE.shoot(False, True)
                if shoot_result is not None :
                    if shoot_result :
                        gamesave.success_againstshoot_trues += 1
                    else :
                        gamesave.success_againstshoot_falses += 1
                    if shoot_result :
                        if r_bullet_unknown :
                            if not all(CLASSIC_MODE.bullets) :
                                r_pp_combo += 1
                            r_pp += 840 * CLASSIC_MODE.bullets.count(False) * \
                                    r_pp_combo * (1+attack_boost) // \
                                    (len(CLASSIC_MODE.bullets)+1)
                        print("运气非常好，是个实弹！")
                        CLASSIC_MODE.e_hp -= 1 + attack_boost
                        gamesave.damage_caused_to_e += 1 + attack_boost
                        print("恶魔生命值：", CLASSIC_MODE.e_hp)
                    else :
                        r_pp_combo = 0
                        print("很遗憾，是个空弹")
                if r_bullet_unknown is not None :
                    r_bullet_unknown = True
                attack_boost = 0
            elif operation == 0 :
                round_turn_count += 1
                total_turn_count += 1
                gamesave.play_turns += 1
                shoot_result = CLASSIC_MODE.shoot(True, True)
                if shoot_result is not None :
                    if shoot_result :
                        gamesave.success_selfshoot_trues += 1
                        r_pp_combo = 0
                        print("感觉像是去奈何桥走了一遭，竟然是个实弹！")
                        CLASSIC_MODE.r_hp -= 1 + attack_boost
                        gamesave.damage_caught += 1 + attack_boost
                        gamesave.damage_caused_to_r += 1 + attack_boost
                        print("你的生命值：", CLASSIC_MODE.r_hp)
                    else :
                        gamesave.success_selfshoot_falses += 1
                        if r_bullet_unknown :
                            if any(CLASSIC_MODE.bullets) :
                                r_pp_combo += 1
                            r_pp += 840 * CLASSIC_MODE.bullets.count(True) * \
                                    r_pp_combo * \
                                    (max(4+CLASSIC_MODE.e_tools.count(2)+
                                         CLASSIC_MODE.e_tools.count(4)-
                                         CLASSIC_MODE.r_hp, 1) if
                                     CLASSIC_MODE.rel_turn_lap <= 0 else
                                     max(3-CLASSIC_MODE.r_hp, 1)) // \
                                    (len(CLASSIC_MODE.bullets)+1)
                        print("啊哈！，是个空弹！")
                if r_bullet_unknown is not None :
                    r_bullet_unknown = True
                attack_boost = 0
            else :
                print("请确定输入的数字正确")
        else :
            gametime_time_start = time()
            if not CLASSIC_MODE.bullets :
                break
            for toolid in CLASSIC_MODE.e_tools[:] :
                will_use: bool
                if not CLASSIC_MODE.bullets :
                    break
                if toolid == 3 :
                    will_use = \
                    True if nightmare and CLASSIC_MODE.bullets[0] and \
                            CLASSIC_MODE.bullets.count(True) == 1 else \
                    not randint(0, 1)
                    if will_use :
                        CLASSIC_MODE.e_tools.remove(3)
                        print("恶魔排出了一颗实弹" \
                              if CLASSIC_MODE.bullets.pop(0) \
                              else "恶魔排出了一颗空弹")
                        if e_bullet_unknown is not None :
                            e_bullet_unknown = True
                elif toolid == 2 :
                    will_use = CLASSIC_MODE.bullets[0] if nightmare else \
                                     not randint(0, 1)
                    if will_use :
                        CLASSIC_MODE.e_tools.remove(2)
                        attack_boost += 1
                        print("恶魔使用了小刀，哦吼吼，结果会如何呢？")
                elif toolid == 4 :
                    will_use = nightmare or not randint(0, 1)
                    if will_use :
                        CLASSIC_MODE.e_tools.remove(4)
                        CLASSIC_MODE.rel_turn_lap -= 1
                        print("恭喜恶魔，成功把你变成了{0}！".format(cat_girl))
                elif toolid == 5 :
                    will_use = nightmare or not randint(0, 1)
                    if will_use :
                        CLASSIC_MODE.e_tools.remove(5)
                        if CLASSIC_MODE.e_hp < 4 or nightmare :
                            if CLASSIC_MODE.e_hp > 3 and not nightmare :
                                e_pp_combo += 1
                                e_pp += 2 ** (CLASSIC_MODE.e_hp-4) * 500 * \
                                        e_pp_combo
                            CLASSIC_MODE.e_hp += 1
                            print("恶魔使用了道德的崇高赞许，回复了一点生命")
                        else :
                            print("因为恶魔的不诚实，恶魔并未回复生命，"
                                  "甚至失去了道德的崇高赞许")
                elif toolid == 6 :
                    will_use = nightmare or not randint(0, 1)
                    if will_use :
                        CLASSIC_MODE.e_tools.remove(6)
                        if e_bullet_unknown is not None :
                            e_bullet_unknown = False
                        print("恶魔查看了枪里的子弹并笑了一下")
            if not CLASSIC_MODE.bullets :
                break
            round_turn_count += 1
            total_turn_count += 1
            gamesave.play_turns += 1
            is_to_self: bool = \
            (not CLASSIC_MODE.bullets[0]) if nightmare else not randint(0, 1)
            if is_to_self :
                shoot_result = CLASSIC_MODE.shoot(True, False)
                if shoot_result is not None :
                    print("恶魔将枪口对准了自己")
                    if shoot_result :
                        e_pp_combo = 0
                        print("“砰！”一声枪响，它自杀了，你心里暗喜")
                        CLASSIC_MODE.e_hp -= 1 + attack_boost
                        print("恶魔生命值：", CLASSIC_MODE.e_hp)
                    else :
                        if e_bullet_unknown and CLASSIC_MODE.e_hp > 0 :
                            if any(CLASSIC_MODE.bullets) :
                                e_pp_combo += 1
                            e_pp += 840 * CLASSIC_MODE.bullets.count(True) * \
                                    e_pp_combo * \
                                    (max(4+CLASSIC_MODE.r_tools.count(2)+
                                         CLASSIC_MODE.r_tools.count(4)-
                                         CLASSIC_MODE.e_hp, 1) if
                                     CLASSIC_MODE.rel_turn_lap >= 0 else
                                     max(3-CLASSIC_MODE.e_hp, 1)) // \
                                    (len(CLASSIC_MODE.bullets)+1)
                        print("“啊哈！，是个空弹！”恶魔嘲讽道")
                    if CLASSIC_MODE.e_hp <= 0 :
                        break
            else :
                shoot_result = CLASSIC_MODE.shoot(False, False)
                print("恶魔朝你开了一枪")
                if shoot_result is not None :
                    if shoot_result :
                        if e_bullet_unknown :
                            if not all(CLASSIC_MODE.bullets) :
                                e_pp_combo += 1
                            e_pp += 840 * CLASSIC_MODE.bullets.count(False) * \
                                    (1+attack_boost) // \
                                    (len(CLASSIC_MODE.bullets)+1)
                        print("运气非常差，是个实弹！")
                        CLASSIC_MODE.r_hp -= 1 + attack_boost
                        gamesave.damage_caught += 1 + attack_boost
                        print("你的生命值：", CLASSIC_MODE.r_hp)
                    else :
                        e_pp_combo = 0
                        print("很幸运，是个空弹")
                if CLASSIC_MODE.e_hp < 0 :
                    break
            if e_bullet_unknown is not None :
                e_bullet_unknown = True
            attack_boost = 0
            gamesave.active_gametime += time() - gametime_time_start

if CLASSIC_MODE.r_hp > 0 :
    gamesave.add_coins()
    if CLASSIC_MODE.e_hp == 0 :
        print("恭喜你，成功把恶魔变成了{0}！".format(cat_girl))
    elif CLASSIC_MODE.e_hp == -1 :
        print("恭喜你，成功把恶魔打得体无完肤！")
    elif CLASSIC_MODE.e_hp == -2 :
        print("恭喜你，成功把恶魔化作一团灰烬！")
    else :
        print("恭喜你，成功让恶魔原地消失！")
elif CLASSIC_MODE.r_hp == 0 :
    if CLASSIC_MODE.e_hp > 0 :
        print("唉....你被恶魔变成了{0}".format(cat_girl))
    elif CLASSIC_MODE.e_hp == 0 :
        print("你们最后同归于尽了")
        gamesave.add_exp(25)
        gamesave.add_coins()
    elif CLASSIC_MODE.e_hp == -1 :
        print("你让恶魔面目全非，但你也付出了生命的代价")
        gamesave.add_exp(80)
        gamesave.add_coins(3)
    elif CLASSIC_MODE.e_hp == -2 :
        print("恶魔为你化作灰烬，而你成为了{0}".format(cat_girl))
        gamesave.add_exp(400)
        gamesave.add_coins(10)
    else :
        print("你作为{0}看着恶魔消失于世上".format(cat_girl))
        gamesave.add_exp(1500)
        gamesave.add_coins(32)
elif CLASSIC_MODE.r_hp == -1 :
    if CLASSIC_MODE.e_hp > 0 :
        print("唉....你被恶魔打得体无完肤")
    elif CLASSIC_MODE.e_hp == 0 :
        print("恶魔让你面目全非，但他也付出了生命的代价")
        gamesave.add_exp(80)
        gamesave.add_coins(3)
    elif CLASSIC_MODE.e_hp == -1 :
        print("二人幸终……")
        gamesave.add_exp(400)
        gamesave.add_coins(10)
    elif CLASSIC_MODE.e_hp == -2 :
        print("恶魔为你化作灰烬，而你也面目狼狈……")
        gamesave.add_exp(1500)
        gamesave.add_coins(32)
    else :
        print("你用残缺的身躯彻底送走了恶魔")
        gamesave.add_exp(4800)
        gamesave.add_coins(100)
elif CLASSIC_MODE.r_hp == -2 :
    if CLASSIC_MODE.e_hp > 0 :
        print("唉....你被恶魔化作一团灰烬")
    elif CLASSIC_MODE.e_hp == 0 :
        print("你为恶魔化作灰烬，而它成为了{0}".format(cat_girl))
        gamesave.add_exp(400)
        gamesave.add_coins(10)
    elif CLASSIC_MODE.e_hp == -1 :
        print("你为恶魔化作灰烬，而它也面目狼狈……")
        gamesave.add_exp(1500)
        gamesave.add_coins(32)
    elif CLASSIC_MODE.e_hp == -2 :
        print("你们化作了两团灰烬")
        gamesave.add_exp(4800)
        gamesave.add_coins(100)
    else:
        print("")
        gamesave.add_exp(16000)
        gamesave.add_coins(320)
else :
    if CLASSIC_MODE.e_hp > 0 :
        print("唉....恶魔让你人间蒸发了")
    elif CLASSIC_MODE.e_hp == 0 :
        print("恶魔作为{0}看着你消失于世上".format(cat_girl))
        gamesave.add_exp(1500)
        gamesave.add_coins(32)
    elif CLASSIC_MODE.e_hp == -1 :
        print()
        gamesave.add_exp(4800)
        gamesave.add_coins(100)
    elif CLASSIC_MODE.e_hp == -2 :
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
print(total_round_count, "回合")

if CLASSIC_MODE.e_hp < 0 :
    r_pp -= CLASSIC_MODE.e_hp * 320
if CLASSIC_MODE.r_hp < 0 :
    e_pp -= CLASSIC_MODE.r_hp * 320

if show_pp :
    print("表现分:", r_pp, "-", e_pp)

if r_pp > e_pp :
    earned_exp: int = \
    round((r_pp-e_pp)*log(total_turn_count)*EXP_MUL_CALC(r_pp)/128.)
    gamesave.add_exp(earned_exp)
    print("你获得了", earned_exp, "经验")

try :
    with open("emlpd.dat", "wb") as gamesave_file :
        gamesave_file.write(gamesave.serialize())
except OSError as err :
    print("存档时遇到问题!", err)
