# UnlockRecipe
[English](README.md)

---
## 简介
* JEI, REI等mod查看配方时，可能无法查看未解锁的配方
* 使用该插件可以使非op玩家解锁配方
---
## 命令
* `!!recipe`解锁自己的所有配方（仅限玩家）
---
## 配置文件
config.json （默认配置文件）
```json5
{
    "permission": 1,  // 玩家权限等级
    "announce": true,  // 是否在玩家进入游戏时通知玩家
    "announce_once": true  // 是否只通知一次
}
```
announced_players.json (记录已通知的玩家)
```json5
{
  "announced_players": [
    "player1",
    "player2"
    ]
}
```
