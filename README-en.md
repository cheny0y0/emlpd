# Evil's Mutual Linear Probability Detection
## Regular Gameplay
### Run
Python 3.6 or above is required.  
type `python -m emlpd` in the terminal.
### Game Rule Introduction
You need to follow the hints given to you in the game interface to defeat Evil.
To defeat the Evil, you need to make the Evil's HP 0 or less and your HP 0 or
more.  
At the beginning of each round, the game will tell you the counts of true and
false bullets are in the main clip. Each turn, you can choose to shoot at
yourself or the opposite.   
If you shoot at yourself and all the bullets are false bullets and do not
explode, you will shoot again in the next turn, otherwise the opposite will
shoot.  
If 1 true bullet is shot, it causes 1 point of base damage (may be defended
against).  
Each shot has a chance of exploding (i.e., making the bullet act to the
opposite; can be changed with a tool), see Tool 21: **Pò Qiāng**.  
If a side has a hurting point of _n_(0≤_n_≤8,_n_∈**N**), then for each point of
true bullet damage to the opposite, there is a probability of _n_/8 that it
will result in an additional HP of damage, and a probability of 1-_n_/8 that it
will result in a hurting point plus 1. Hurting point is initially 0.  
If a side has _m_(0≤_m_≤32,_m_∈**N***) and a hurting point of
_n_(0≤_n_≤8,_n_∈**N***), and if _m_>0, then this side's stamina decrease by 1
for each shot. Each turn this side's stamina has a 1/(_n_+1) probability of
increasing by 1. When _m_<8, there is a probability of 1-_m_/8 of that this
side will get dazed for a round.  
If a side have _n_(_n_∈**N₊**) dazing turns, then if it would have been this
side to shoot in the next turn, then the opposite still shoots in the next turn
and the number of this side's dazing turns becomes _n_-1.
#### Game Cycles
##### Turn
Shooting 1 time is called 1 turn.
##### Round
Giving 1 new clips is called 1 round.
##### Period
Changing 1 new Evil is called 1 period.
##### Game
Game running 1 time is called 1 game.
#### Tools' Descriptions
##### Tool 0: Liáng Qiāng(Yī)
Decrease your stacked badguns by 1 if **Pò Qiāng** is used by the opposite,
otherwide increase your stacked goodgun(foo) by 1.  
_See Tool 21: **Pò Qiāng**_
##### Tool 1: Liáng Qiāng(Èr)
Decrease your stacked badguns by 1 if **Pò Qiāng** is used by the opposite,
otherwide increase your stacked goodgun(bar) by 1.  
_See Tool 21: **Pò Qiāng**_
##### Tool 2: Xiǎo Dāo
If _n_(_n_∈**N**) **Xiǎo Dāo**s is used this turn, attach _n_ points of
additional damage for each true bullets shot this turn.
##### Tool 3: Kāi Guà(Yī)
Let the outermost bullet of the main clip quit(make it disappear), and tell you
whether the bullet was true or false.
##### Tool 4: Chāo Jí Xiǎo Mù Chuí
Let the number of the opposite's dazing round increase by 1.
##### Tool 5: Dào Dé De Chóng Gāo Zàn Xǔ
Suppose your current HP is _m_(_m_∈**N₊**), hurting point is
_n_(0≤_n_≤8,_n_∈**N**), if _m_≤3+_n_/3, there is a probability of 100% that
your HP will increase by 1; if _m_>3+_n_/3, there is a probability of
pow(2,3+_n_/3-_m_) that your HP will increase by 1.
##### Tool 6: Tòu Shì Jìng
Tells you whether it is true or false of the outermost bullet of each clip (the
top message describes the main clip's).
##### Tool 7: Ná Lái Zhǔ Yì
If the opposite has _n_(_n_∈**N**) non-OP tools, there is a probability of
1/_n_ of gaining a non-OP tool equally likely, and a probability of 1-1/_n_ of
fetching 1 non-OP tool from the opposite equally likely.  
The two are opposite events.
##### Tool 8: Nǐ De Jiù Shì Wǒ De
This is an OP tool.  
Share the opposite's tool warehouse with you, and you will not be able to use
the tools in your warehouse at that time. There is a 30% chance of sharing 1
round, a 50% chance of sharing 2 rounds, and a 20% chance of sharing 3 rounds.
All three are mutually exclusive.
##### Tool 9: Fáng Dàn Yī
Append a bulletproof wearing with a durability exponent of 3 to the outermost
layer. When you have at least 1 bulletproof wearing, when a bullet is shot at
you, suppose the extra damage value of the turn is _n_(_n_∈**N**), the
outermost bulletproof wearing will first reduce randint(1,ceil(√(_n_+1)))
points of durability exponent. Subsequently, suppose the durability exponent of
the outermost bulletproof wearing is _m_(_m_∈**Z**), if _m_<0, the bulletproof
wearing has a probability of 1-pow(2,_m_) of disappearing.  
If 1 bulletproof wearing disappears, your break care potential increases by 1;
if there is no bulletproof weareing after the bulletproof wearing disappears,
each point of your break care potential has a probability of 15% of turning
into a point of break care round, and a probability of 85% of nothing
happening. If the point of break care rounds is greater than 0, you will not be
able to use any tools in the following rounds, and you will randomly shoot at
either yourself or the opposite, and the point of break care rounds will
decrease by 1 for every 1 round that passes.
##### Tool 10: Fǎn Jiǎ
_Not Implemented Yet_
##### Tool 11: Tóu Zi
Let _m_=randint(1,6)+randint(1,6)+randint(1,6). If _m_=3, you break care for 2
rounds; if _m_=4, your HP will decrease by 2 and tell you so; if _m_=5, the
true-false state of the bullets in the main clip changes randomly from the
outside to the inside from the 3rd bullet; if _m_=6, your HP will decrease by 1
and tell you so; if _m_=7, one of your non-OP tools disappears; if _m_=9, your
stamina will increase by 1 until reaching the maximum; if _m_=10, your HP will
increase by 1 and tell you so; if _m_=11, your stamina will increase by 2 until
reaching the maximum; if _m_=12, your additional damage for the current turn
will increase by 2, and there is a probability of 50% that you will be told so;
if _m_=13, the opposite's HP will decrease by 1 and tell you so; if _m_=14, the
opposite has a probability of 1/3 of being dazed for 1 more turn, and a
probability of 2/3 of being dazed for 2 more turns, which are opposite events;
if _m_=15, the opposite's HP will decrease by 2 and tell you so; if _m_=18, the
opposite's HP will become 1/8th of what it was originally (floored), and tell
you so.
##### Tool 12: Cáo Wèi Yán Qī
Suppose you currently have _n_(_n_∈**N**) temporary slots. If _n_=0, this tool
will not be used; if _n_>0, for each temporary slot, there is a 100%
probability of postponing 1 round.
##### Tool 13: Jìng Zi
This is an OP tool.  
For HP, hurting point, stamina, tool warehouse, stacked goodgun(foo), stacked
goodgun(bar), additional damage of current turn, bulletproof wearings, stacked
bullet catcher, stacked repeater, stacked combo shooter, stacked badgun,
stacked bandage, there is a probability of 50% that yours become the
opposite's, and tells “你变成了恶魔的样子”; there is a probability of 50% that
the opposite's become yours, and tells “恶魔变成了你的样子”. The two are
opposite event.  
And you and the opposite's dazing rounds will become 0.
##### Tool 14: Jiē Dàn Tào
Let your stacked bullet catcher increase by 1. Suppose you currently have
_n_(_n_∈**N₊**) stacked bullet catchers, the opposite's additional damage is
_m_(_m_∈**N**), if the opposite shoots 1 true bullet, there is a probability of
(1-pow(0.8,_n_))/(1+_m_) that you will catch it(avoids the damage from the
bullet and tells you “你接住了一颗子弹”) and put it into the tail of the main
clip, and let your stacked bullet catcher be 0; if the opposite shoots 1 false
bullet, there is a probability of 0.8/(1+_m_) that you will catch it(tells you
“你接住了一颗子弹”) and put it into the tail of the main clip, and let your
stacked bullet catcher decrease by 1.
##### Tool 15: Tián Shí
Suppose there are _n_(_n_ ∈ **N₊**) bullets in the main clip now, then for
each false bullet in the main clip there is a probability of 1/_n_ that it will
become a true bullet. If at least one false bullet becomes a true bullet, the
message “弹夹有变动” will be displayed.
##### Tool 16: Chóng Zhěng Dàn Yào
Temporarily take all bullets in the main clip out and put them back to the main
clip one by one. You can specify where to put each bullet, but whether it is a
true bullet or a false bullet that is put back in will only be shown when it is
put in. For example, in the following case: `0实1空2实3实4空5`, inputting `0`
will place one bullet in the outermost part of the main clip, inputting `5`
will place one bullet in the innermost part of the main clip, and inputting `3`
will place one bullet in the location of the two continuous true bullets in the
example. After all bullets have been put, the message “你重整了一下弹药” will
be displayed.
##### Tool 17: Shuāng Fā Shè Shǒu
Let your stacked repeater count increase by 1.  
_See Tool 18: **Lián Fā Shè Shǒu**_
##### Tool 18: Lián Fā Shè Shǒu
Let your stacked combo shooter count increase by 1.  
Suppose currently you have _m_(_m_∈**N**) stacked repeaters, _n_(_n_∈**N**)
stacked combo shooters, amount of the bullets in main clip is _r_(_r_∈**N₊**),
if you shoot at the opposite, then at least min(_r_,1+_m_) bullets will be
shot, and there will be a probability of 1-2⁻ⁿ shooting 1 more bullet(if there
exists a bullet in the clip). In other words, when _n_>0, there is a
probability of min(1,pow(1-2⁻ⁿ,_r_-1-_m_)) of clearing the clip. Suppose
_s_(_s_∈**N₊**) bullets are shot from the main clip, if _s_>_n_, then your
stacked combo shooter will become 0; if _s_≤_n_, then your stacked combo
shooter will decrease by _s_. For each additional shot bullet(by stacked
repeater), it makes stacked repeater count decrease by 1.
##### Tool 19: Yìng Bì
_Not Implemented Yet_
##### Tool 20: Rán Shāo Dàn
_Not Implemented Yet_
##### Tool 21: Pò Qiāng
Increase the opposite's stacked badgun by 1。  
Suppose the current explosion exponent is _h_(_h_∈**N**), your stacked
goodgun(foo) count is _m_(_m_∈**N**), your stacked goodgun(bar) count is
_n_(_n_∈**N**), and your stacked badgun number is _r_(_r_∈**N**). If shooting
at oneself, when _r_>0, there is a 100% probability of exploding for each
bullet shot; when _r_=0 and _m_>0, there is a 0% probability of exploding for
each bullet shot; otherwise, there is a probability of 1-pow(1535/1536,_h_+60)
of exploding for each bullet shot. If shooting at the opposite, when _r_>0,
there is a 100% probability of exploding for each bullet shot; when _r_=0 and
_n_>0, there is a 0% probability of exploding for each bullet shot; otherwise,
there is a probability of 1-pow(1535/1536,_h_+60) of exploding for each bullet
shot. The explosion exponent increases by 1 when each bullet shot (whether
exploded or not).
##### Tool 22: Qǔ Chū Zǐ Dàn
Take 1 bullet from the location you specified out from the main clip and change
it to a tool **Shí Dàn** or **Kōng Dàn** and tell you so.
##### Tool 23: Kōng Dàn
Put 1 false bullet into a location specified by you in the main clip and tell
you so.
##### Tool 24: Shí Dàn
Put 1 true bullet into a location specified by you in the main clip and tell
you so.
##### Tool 25: Shén Mì Zǐ Dàn
Put 1 mysterious bullet into a location specified by you in the main clip and
tell you so.  
A “mysterious bullet” is a bullet whose true-false state is unknown and which
has a probability of 50% of affecting the true-false state of the bullet next
to the bullet put directioned inside (if exists).
##### Tool 26: Bēng Dài
Decrease your hurting point by 1 after 2 rounds. If the number of current
pending bandages is greater than or equal to your hurting point, this tool will
not be used.
##### Tool 27: Yī Liáo Bāo
If you have less than 2 HP, make you regain 5 HP; if you have less than 5 HP,
make you regain 4 HP; if you have less than 9 HP, make you regain 3 HP; if you
have less than 14 HP, make you regain 2 HP; if you have more than or equal to
14 HP, make you regain 1 HP. Additionally, if you have 0 hurting points, make
you get 2 HP back, and if you have less than 4 hurting points, make you get 1
HP back. HP regained based on HP are told to you, while HP regained based on
hurting points are not told to you.
##### Tool 28: Kāi Guà(Èr)
Instantly give a batch of new clips(current clips will not be retained).
##### Tool 29: Shuāng Qiāng Huì Gěi Chū Dá Àn
This is an OP tool.  
Add 1 xor 2 extra clips. Just added by copying existing clips to new extra
clips. It will not prompt.
##### Tool 30: Suǒ Yǒu Huò Yì Wú Suǒ Yǒu
This is an OP tool.  
There is a probability of 50% that both sides' tool warehouses and bulletproof
wearings will be cleared, and the additional damage will become zero.
##### Tool 31: Chāo Jí Dà Mù Chuí
This is an OP tool.  
Suppose currently the main clip contains _n_(_n_∈**N₊**) bullets, make the
opposite's dazing rounds increase by _n_.
##### Tool 32: Bù Sǐ Bù Xiū
_Not Implemented Yet_
##### Tool 33: Qiāng Tǒng Wéi Xiū
Make the explosion exponent 2/3 of what it was and tell you “你维修了一下枪筒”.
If the explosion exponent is less than or equal to 0, this tool will not be
used.
### Game Mode Introduction
#### 1. Pǔ Tōng Mó Shì
Only 1 period.  
Your and the Evil's initial HP respectively are 1 and 10.  
All tools except ID10 will be sent.  
Each side has 8 permanent slots.
#### 2. Wú Xiàn Mó Shì(Yī)
Only 1 period.  
Your and the Evil's initial HP respectively are 2 and (2⁶⁴-1).  
All tools except ID10, ID11 and ID13 will be sent.  
Each side has 9 permanent slots.
#### 3. Xiǎo Dāo Kuáng Huān
Only 1 period.  
Your and the Evil's initial HP respectively are 1 and 10.  
Only tool ID2 and ID3 will be sent.  
Each side has 100 permanent slots.  
No temporary slot will be sent.
#### 4. Tóu Zi Wáng Guó
Only 1 period.  
Your and the Evil's initial HP respectively are 50 and randint(50,90).  
Only tool ID11 will be sent.  
Each side has 100 permanent slots.  
No temporary slot will be sent.
#### 5. Wú Xiàn Mó Shì(Èr)
There are infinite periods.  
Your initial HP is 2. Suppose the current period is Period _n_(_n_∈**N₊**), the
Evil's initial HP is (_n_+9).  
All tools except ID10 will be sent.  
Each side has 9 permanent slots.。
#### 6. Lián Shè Pài Duì
Only 1 period.  
Your and the Evil's initial HP respectively are 40 and 200.  
Only tool ID0, ID1, ID2, ID9, ID15, ID17, ID18, ID21, ID27, ID28 and ID29 will
be sent.  
Each side has 12 permanent slots.
#### 7. Zhà Táng Cè Shì
Only 1 period.  
Your and the Evil's initial HP respectively are 10 and 50.  
Only tool ID5, ID9, ID21 will be sent.  
Each side has 6 permanent slots.
#### 8. Chì Shǒu Kōng “Qiāng”
Only 1 period.  
Your and the Evil's initial HP respectively are 18 and 50.  
No tools will be sent.  
Each side has 0 permanent slots.  
No temporary slot will be sent.
### Custom Game Mode
Predefined game modes are in [emlpd.gameinst](emlpd/gameinst.py), defined by `GAMEMODE_SET`.
This is the default setting of `GAMEMODE_SET`:

```python3
from typing import Dict, Iterable, Optional, Tuple, Union
from emlpd.gameapi import Game

class NormalGame(Game): ...

normal_mode: NormalGame = ...
infinite_mode: NormalGame = ...
xiaodao_party: NormalGame = ...
dice_kingdom: NormalGame = ...
class InfiniteMode2: ...
combo_party: NormalGame = ...
exploded_test: NormalGame = ...
onlybyhand: NormalGame = ...

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
```
You need to create a Python script, create a `Game` object(which is defined in
[emlpd.gameapi](emlpd/gameapi.py)) in it, and add it into `GAMEMODE_SET`, for example:
```python3
from emlpd.gameapi import Game
from emlpd.gameinst import GAMEMODE_SET, gen_tools_from_generic_tools

my_gamemode: Game = Game( # For parameters' detail, see Game.__doc__
    2,
    10,
    8,
    0,
    10,
    100,
    90,
    gen_tools_from_generic_tools(
        (0, 1, 21) # Include predefined tools' IDs, can be empty; see
                   # emlpd.gameinst.GENERIC_TOOLS
    ),
    {
        0: 1,
        1: 1,
        21: 2
    },
    {
        0: 0,
        1: 0,
        21: 0
    },
    {
        0: 2,
        1: 2,
        21: 4
    },
    7,
    False
)

GAMEMODE_SET[
    9 # Game mode ID
] = (
    (my_gamemode,), # An iterable includes Game
    1, # Specify the maximal tools sent per round for both side
    2.75, # Specify the EXP multiplier
    "Game Mode Name",
    "Game Mode Description"
)

import emlpd.__main__ # type: ignore # import cannot be omitted!
```
And run the script above, you will see:
```text
游戏模式 9 : Game Mode Name
介绍: Game Mode Description
```
Input `9` for entering custom game mode.
## Classic Gameplay
### Run
Python 3.6 or above is required.  
type `python -m emlpd.classic` in the terminal.
### Game Rule Introduction
你需要根据游戏界面给你的提示来打败恶魔。要打败恶魔，需要让恶魔的生命值变为 0
或以下，且自己的生命值在 0 以上。  
每一回合之初游戏都会告诉你实弹与空弹各有几发。每一轮，你可以选择朝自己开枪，
也可以朝对方开枪。若朝自己开枪且射出的子弹为空弹，则下一轮还是你开枪，
否则轮到对面开枪。  
若射出了 1 发实弹，则它会造成 1 点的基础伤害。  
如果某一方晕了 _n_(_n_∈**N₊**) 轮，那么若原本下一轮应轮到该方开枪，
则下一轮变为仍是另一方开枪，且该方晕的轮数变为 _n_-1。
#### Game Cycles
##### Turn
Shooting 1 time is called 1 turn.
##### Round
Giving 1 new clips is called 1 round.
##### Game
Game running 1 time is called 1 game.
#### Tools' Descriptions
##### Tool 2: 小刀
若本轮使用了 _n_(_n_∈**N**) 个**小刀**，对本轮射出的实弹都附加 _n_
点额外伤害。
##### Tool 3: 开挂
将弹夹的最外部的 1 发子弹退出（让其消失），并告诉这发子弹的实空。
##### Tool 4: 超级小木锤
让对方晕的轮数加 1。
##### Tool 5: 道德的崇高赞许
设当前你的生命值为 _m_(_m_∈**N₊**)，当 _m_≤3 时，你有 100% 的概率加 1 点生命值；当
_m_>3 时，你有 pow(2,3-_m_) 的概率加 1 点生命值。
##### Tool 6: 透视镜
告诉你弹夹的最外部的 1 发子弹的实空。
