# 恶魔轮盘赌（重构版）
## 正常玩法
### 运行
需要 Python 3.6 或更高版本的 Python。  
在终端输入 `python -m emlpd`。
### 游戏规则介绍
你需要根据游戏界面给你的提示来打败恶魔。要打败恶魔，需要让恶魔的生命值变为 0
或以下，且自己的生命值在 0 以上。  
每一回合之初游戏都会告诉你主弹夹内实弹与空弹各有几发。每一轮，
你可以选择朝自己开枪，也可以朝对方开枪。
若朝自己开枪且射出的全部子弹都为空弹且全部未炸膛，则下一轮还是你开枪，
否则轮到对面开枪。  
若射出了 1 发实弹，则它会造成 1 点的基础伤害（可能被防御）。  
射出的每一发子弹都有 5% 的概率炸膛（即让子弹作用方相反；可使用道具改变）。  
若某一方的负伤数为 _n_(0≤_n_≤8,_n_∈N)，则对于该方受到的每一点实弹伤害，都有
_n_/8 的概率导致额外受到 1 点生命值伤害，有 1-_n_/8 的概率导致负伤数加 1。
负伤数初始为 0。  
若某一方的体力为 _m_(0≤_m_≤32,_m_∈N)，负伤数为 _n_(0≤_n_≤8,_n_∈N)，若 _m_>0，
则该方每开一次枪都会消耗 1 体力。每一轮该方都有 1/(_n_+1) 的概率回复 1 体力。
当 _m_<8 时，该方有 1-_m_/8 的概率晕一轮。  
如果某一方晕了 _n_(_n_∈N₊) 轮，那么若原本下一轮应轮到该方开枪，
则下一轮变为仍是另一方开枪，且该方晕的轮数变为 _n_-1。
#### 游戏周期
##### 轮
开枪 1 次称为 1 轮。
##### 回合
发放 1 次新弹夹称为 1 回合。
##### 周目
更换 1 个新恶魔称为 1 周目。
##### 局
游戏运行 1 次称为 1 局。
#### 道具说明
##### 道具 0：良枪(一)
若对面使用了**破枪**，则将你的叠加破枪数减 1，否则将你的叠加良枪(一)数加 1。  
_详见 道具 21：**破枪**_
##### 道具 1：良枪(二)
若对面使用了**破枪**，则将你的叠加破枪数减 1，否则将你的叠加良枪(二)数加 1。  
_详见 道具 21：**破枪**_
##### 道具 2：小刀
若本轮使用了 _n_(_n_∈N) 个**小刀**，对本轮射出的每一发实弹都附加 _n_
点额外伤害。
##### 道具 3：开挂(一)
将主弹夹的最外部的 1 发子弹退出（让其消失），并告诉这发子弹的实空。
##### 道具 4：超级小木锤
让对方晕的轮数加 1。
##### 道具 5：道德的崇高赞许
设当前你的生命值为 _m_(_m_∈N₊)，负伤数为 _n_(0≤_n_≤8,_n_∈N)，当 _m_≤3+_n_/3
时，你有 100% 的概率加 1 点生命值；当 _m_>3+_n_/3 时，你有
pow(2,3+_n_/3-_m_) 的概率加 1 点生命值。
##### 道具 6：透视镜
告诉你各弹夹的最外部的 1 发子弹的实空（最上方一条是主弹夹的）。
##### 道具 7：拿来主义
若对方有 _n_(_n_∈N)个非 OP 道具，则有 1/_n_ 的概率随机等可能地获得一个非 OP
道具，有 1-1/_n_ 的概率随机等可能地将对方的 1 个非 OP 道具拿来。
两者互为对立事件。
##### 道具 8：你的就是我的
此为 OP 道具。  
将对方的道具库与你共用，届时你无法使用你的道具库中的道具。有 30% 的概率共用
1 回合，50% 的概率共用 2 回合，20% 的概率共用 3 回合。三者互斥。
##### 道具 9：防<ruby>弹<rt>dàn</rt></ruby>衣
将一件耐久指数为 3 的防弹衣加在最外层。在你有至少 1 件防弹衣时，
当一发子弹射到你，设本轮的额外伤害为 _n_(_n_∈N)，最外层防弹衣会先减少
randint(1,ceil(√(_n_+1))) 点耐久指数。随后，设最外层防弹衣耐久指数为
_m_(_m_∈Z)，若 _m_<0，则该防弹衣有 1-pow(2,_m_) 的概率消失。  
若有 1 件防弹衣消失，你的破防潜能会加 1；若防弹衣消失后你没有穿上的防弹衣，
那么你的每一点破防潜能都有 15% 的概率转变为破防回合数，有 85% 的概率无事发生。
若破防回合数大于 0，则接下来的回合你将不能使用任何道具，
并且会随机朝自己或对方开枪，每过 1 回合破防回合数减 1。
##### 道具 10：反甲
_未实装_
##### 道具 11：<ruby>骰<rt>tóu</rt></ruby>子
令 _m_=randint(1,6)+randint(1,6)+randint(1,6)。当 _m_=3 时，你会破防 2
回合；当 _m_=4 时，你会减 2 点生命值，并告诉你；当 _m_=5 时，
主弹夹从外至里从第 3 发子弹开始的空实状态会随机变化；当 _m_=6 时，你会减 1
点生命值，并告诉你；当 _m_=7 时，你的一个非 OP 道具会消失；当 _m_=10 时，
你会加 1 点生命值，并告诉你；当 _m_=12 时，你本轮额外伤害会加 2 点，并有
50% 的概率告诉你；当 _m_=13 时，对面会减 1 点生命值，并告诉你；当 _m_=14
时，对面有 1/3 的概率多晕 1 轮，2/3 的概率多晕 2 轮，两者互为对立事件；当
_m_=15 时，对面会减 2 点生命值，并告诉你；当 _m_=18 时，
对面的生命值会变为原来的 1/8（向下取整），并告诉你。
##### 道具 12：槽位延期
设你现在有 _n_(_n_∈N)个临时槽位。当 _n_=0 时，不会使用道具；当 _n_>0 时，
对于每个临时槽位，都有 100% 的概率延期 1 回合。
##### 道具 13：镜子
此为 OP 道具。  
对于生命值、负伤数、体力、道具库、叠加良枪(一)、叠加良枪(二)、本轮额外伤害、
防弹衣、叠加接弹套、 叠加双发射手、叠加连发射手、叠加破枪、叠加绷带，有 50%
的概率，你的变为对方的，并告诉“你变成了恶魔的样子”；50%
的概率，对方的变为你的，并告诉“恶魔变成了你的样子”。两者互为对立事件。
并将双方晕的轮数变为 0。
##### 道具 14：接<ruby>弹<rt>dàn</rt></ruby>套
会将你的叠加接弹套数加 1。设你现在有 _n_(_n_∈N₊)个叠加接弹套，对面的额外伤害为
_m_(_m_∈N)，若对面射来 1 发实弹，你有 (1-pow(0.8,_n_))/(1+_m_)
的概率接住之（免受该实弹的伤害并告诉你“你接住了一颗子弹”）
并将其放在主弹夹的末尾，且叠加接弹套数变为 0；若对面射来 1 发空弹，你有
0.8/(1+_m_) 的概率接住之（告诉你“你接住了一颗子弹”）并将其放在主弹夹的末尾，
且叠加接弹套数减 1。
##### 道具 15：填实
设现在主弹夹有 _n_(_n_∈N₊)发子弹，则对于主弹夹内的每发空弹都有 1/_n_
的概率变为实弹。若至少有 1 发空弹变为实弹，则会提示“弹夹有变动”。
##### 道具 16：重整弹药
将主弹夹内的所有子弹暂时拿出，并一发发放回主弹夹。你可以指定每发子弹放在何处，
但放回的是实弹还是空弹只有放入后才会显示。例如下面的情况：`0实1空2实3实4空5`，
输入 `0` 会将一发子弹放入主弹夹最外处；输入 `5` 会将一发子弹放入主弹夹最里处；
输入 `3` 会将一发子弹放入例中两发连续实弹的位置。所有子弹放入后会提示
“你重整了一下弹药”。
##### 道具 17：双发射手
会将你的叠加双发射手数加 1。  
_详见 道具 18：**连发射手**_
##### 道具 18：连发射手
会将你的叠加连发射手数加 1。  
设你现在有 _m_(_m_∈N)个叠加双发射手，_n_(_n_∈N)个叠加连发射手，主弹夹子弹数为
_r_(_r_∈N₊)，若朝对方开枪，则至少会射出 min(_r_,1+_m_) 发子弹，并有
1-pow(2,-_n_) 的概率多射出 1 发子弹（若弹夹内还有子弹）。换而言之，当 _n_>0
时，你有 min(1,pow(1-pow(2,-_n_),_r_-1-_m_)) 的概率清空弹夹。设主弹夹射出了
_s_(_s_∈N₊) 发子弹，若 _s_>_n_，则叠加连发射手数变为 0；若 _s_≤_n_，
则叠加连发射手数减 _s_。每多射出 1 发子弹（由叠加双发射手），叠加双发射手数减
1。
##### 道具 19：硬币
_未实装_
##### 道具 20：燃烧弹
_未实装_
##### 道具 21：破枪
将对面的叠加破枪数加 1。  
设你的叠加良枪(一)数为 _m_(_m_∈N)，叠加良枪(二)数为 _n_(_n_∈N)，叠加破枪数为
_r_(_r_∈N)。若朝自己开枪，当 _r_>0 时，有 100% 的概率炸膛；当 _r_=0 且 _m_>0
时，有 0% 的概率炸膛；否则，有 5% 的概率炸膛。若朝对方开枪，当 _r_>0 时，
对于射出的每发子弹有 100% 的概率炸膛；当 _r_=0 且 _n_>0
时，对于射出的每发子弹有 0% 的概率炸膛；否则，对于射出的每发子弹有 5%
的概率炸膛。
##### 道具 22：取出子弹
在主弹夹内取出 1
发由你指定位置的子弹并将其变为道具**实弹**或**空弹**，并告诉你。
##### 道具 23：空弹
在主弹夹内放入 1 发由你指定位置的空弹，并告诉你。
##### 道具 24：实弹
在主弹夹内放入 1 发由你指定位置的实弹，并告诉你。
##### 道具 25：神秘子弹
在主弹夹内放入 1 发由你指定位置的神秘子弹，并告诉你。  
所谓“神秘子弹”，是指该子弹的实空未知，且有 50% 概率影响紧挨该子弹里部的 1
发子弹的实空（若有）。
##### 道具 26：绷带
2 回合后让你的负伤数减 1。若当前正在使用的绷带数大于负伤数，则不会使用。
##### 道具 27：医疗包
若你的生命值小于 2，则会回复 5 点生命值；若你的生命值小于 5，则会回复 4
点生命值；若你的生命值小于 9，则会回复 3 点生命值；若你的生命值小于
14，则会回复 2 点生命值；若你的生命值大于等于 14，则会回复 1 点生命值。
此外，若你的负伤数等于 0，则会回复 2 点生命值；若你的负伤数小于 4，则会回复 1
点生命值。根据生命值回复的生命值会告诉你，而根据负伤数回复的生命值不会告诉你。
##### 道具 28：开挂(二)
立即发放一批新弹夹（不保留现有弹夹）。
##### 道具 29：双枪会给出答案
此为 OP 道具。  
添加 1 异或 2 个额外弹夹。添加伊始是复制已有弹夹到新额外弹夹。不会提示。
##### 道具 30：所有或一无所有
此为 OP 道具。  
有 50% 的概率将双方的道具库、防弹衣清空，额外伤害归零。
##### 道具 31：超级大木锤
此为 OP 道具。  
设当前主弹夹内有 _n_(_n_∈N₊)发子弹，让对方晕的轮数加 _n_。
##### 道具 32：不死不休
_未实装_
##### 道具 33：枪筒维修
_未实装_
### 游戏模式介绍
#### 1. 普通模式
只有 1 个周目。  
你和恶魔的初始生命值分别为 1 和 10。  
会发放除 ID10 的所有道具。
#### 2. 无限模式(一)
只有 1 个周目。  
你和恶魔的初始生命值分别为 2 和 (2⁶⁴-1)。  
会发放除 ID10、ID11、ID13 的所有道具。
#### 3. 小刀狂欢
只有 1 个周目。  
你和恶魔的初始生命值分别为 1 和 10。  
只会发放 ID2、ID3 道具。
#### 4. 骰子王国
只有 1 个周目。  
你和恶魔的初始生命值分别为 50 和 randint(50,90)。  
只会发放 ID11 道具。
#### 5. 无限模式(二)
有无穷多个周目。  
你的初始生命值为 2。设当前为第 _n_(_n_∈N₊)周目，恶魔的初始生命值为 (_n_+9)。  
会发放除 ID10 的所有道具。
#### 6. 连射派对
只有 1 个周目。  
你和恶魔的初始生命值分别为 40 和 200。  
只会发放 ID0、ID1、ID2、ID9、ID15、ID17、ID18、ID21、ID27、ID28、ID29 道具。
#### 7. 炸膛测试
只有 1 个周目。  
你和恶魔的初始生命值分别为 10 和 50。  
只会发放 ID5、ID9、ID21 道具。
#### 8. 赤手空“枪”
只有 1 个周目。  
你和恶魔的初始生命值分别为 20 和 50。  
不会发放任何道具。
### 自定义游戏模式
预设的游戏模式在 [emlpd.gameinst](emlpd/gameinst.py) 中，由 `GAMEMODE_SET`
定义。这是 `GAMEMODE_SET` 的默认设置：

```python3
from typing import Dict, Iterable, Optional, Tuple, Union
from emlpd.gameapi import Game

normal_mode: Game = ...
infinite_mode: Game = ...
xiaodao_party: Game = ...
dice_kingdom: Game = ...
class InfiniteMode2: ...
combo_party: Game = ...
exploded_test: Game = ...
onlybyhand: Game = ...

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
你需要新建一个 Python 脚本，在其中创建一个 `Game` 对象（在
[emlpd.gameapi](emlpd/gameapi.py) 中），然后将其添加到 `GAMEMODE_SET`
中，例如：
```python3
from emlpd.gameapi import Game
from emlpd.gameinst import GAMEMODE_SET, gen_tools_from_generic_tools

my_gamemode: Game = Game( # 参数详情见 Game.__doc__
    2,
    10,
    8,
    0,
    10,
    100,
    90,
    gen_tools_from_generic_tools(
        (0, 1, 21) # 包含预定道具 ID，可为空；见 emlpd.gameinst.GENERIC_TOOLS
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
        2: 4
    },
    7,
    False
)

GAMEMODE_SET[
    9 # 游戏模式 ID
] = (
    (my_gamemode,), # 一个包含 Game 的可迭代对象
    1, # 指定每回合各方最多发放的道具数
    2.75, # 指定经验乘数
    "游戏模式名字",
    "游戏模式介绍"
)

import emlpd.__main__ # type: ignore # import 不能省去！
```
随后运行上述脚本，即可看到：
```text
游戏模式 9 : 游戏模式名字
介绍: 游戏模式介绍
```
输入 `9` 即可进入自定义游戏模式。
## 经典玩法
### 运行
需要 Python 3.6 或更高版本的 Python。  
在终端输入 `python -m emlpd.classic`。
### 游戏规则介绍
你需要根据游戏界面给你的提示来打败恶魔。要打败恶魔，需要让恶魔的生命值变为 0
或以下，且自己的生命值在 0 以上。  
每一回合之初游戏都会告诉你实弹与空弹各有几发。每一轮，你可以选择朝自己开枪，
也可以朝对方开枪。若朝自己开枪且射出的子弹为空弹，则下一轮还是你开枪，
否则轮到对面开枪。  
若射出了 1 发实弹，则它会造成 1 点的基础伤害。  
如果某一方晕了 _n_(_n_∈N₊) 轮，那么若原本下一轮应轮到该方开枪，
则下一轮变为仍是另一方开枪，且该方晕的轮数变为 _n_-1。
#### 游戏周期
##### 轮
开枪 1 次称为 1 轮。
##### 回合
发放 1 次新弹夹称为 1 回合。
##### 局
游戏运行 1 次称为 1 局。
#### 道具说明
##### 道具 2：小刀
若本轮使用了 _n_(_n_∈N) 个**小刀**，对本轮射出的实弹都附加 _n_
点额外伤害。
##### 道具 3：开挂
将弹夹的最外部的 1 发子弹退出（让其消失），并告诉这发子弹的实空。
##### 道具 4：超级小木锤
让对方晕的轮数加 1。
##### 道具 5：道德的崇高赞许
设当前你的生命值为 _m_(_m_∈N₊)，当 _m_≤3 时，你有 100% 的概率加 1 点生命值；当
_m_>3 时，你有 pow(2,3-_m_) 的概率加 1 点生命值。
##### 道具 6：透视镜
告诉你弹夹的最外部的 1 发子弹的实空。