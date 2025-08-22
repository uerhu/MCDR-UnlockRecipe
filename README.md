# UnlockRecipe
[中文](README_cn.md)

---
## Introduction
* JEI, REI and other mods cannot view locked recipes when browsing recipes
* Use this plugin to unlock recipes for non-op players
---
## Command
* `!!recipe`unlock recipes for oneself（Only for player）
---
## Configuration
config.json （default configuration file）
```json5
{
    "permission": 1,  // player permission level
    "announce": true,  // whether to notify players when they enter the game
    "announce_once": true  // whether to notify only once
}
```
announced_players.json (record notified players)
```json5
{
  "announced_players": [
    "player1",
    "player2"
    ]
}
```
