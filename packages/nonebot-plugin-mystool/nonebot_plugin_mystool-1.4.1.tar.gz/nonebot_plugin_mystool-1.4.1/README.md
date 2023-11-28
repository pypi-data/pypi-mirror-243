```
 __    __     __  __     ______     ______   ______     ______     __
/\ "-./  \   /\ \_\ \   /\  ___\   /\__  _\ /\  __ \   /\  __ \   /\ \
\ \ \-./\ \  \ \____ \  \ \___  \  \/_/\ \/ \ \ \/\ \  \ \ \/\ \  \ \ \____
 \ \_\ \ \_\  \/\_____\  \/\_____\    \ \_\  \ \_____\  \ \_____\  \ \_____\
  \/_/  \/_/   \/_____/   \/_____/     \/_/   \/_____/   \/_____/   \/_____/
```

[![CodeFactor](https://www.codefactor.io/repository/github/ljzd-pro/nonebot-plugin-mystool/badge?style=for-the-badge)](https://www.codefactor.io/repository/github/ljzd-pro/nonebot-plugin-mystool)
[![最新发行版](https://img.shields.io/github/v/release/Ljzd-PRO/nonebot-plugin-mysTool?logo=python&style=for-the-badge)](https://github.com/Ljzd-PRO/nonebot-plugin-mystool/releases/latest)
[![最后提交](https://img.shields.io/github/last-commit/Ljzd-PRO/nonebot-plugin-mysTool/dev?style=for-the-badge)](https://github.com/Ljzd-PRO/nonebot-plugin-mystool/commits/dev)

# mysTool - 米游社辅助工具插件

## 📣 更新内容
### 2023.11.26 - v1.4.1
- 更新 adapter-qq 适配器，修复QQ频道私信通知失败的问题 #215
- 更新App版本号以及DS Salt值
- 修复原神便笺获取失败的问题（米游社App内API）#216

### 2023.11.13 - v1.4.0
- 跟进QQ频道适配器的变更，已更换停止维护的 `nonebot-adapter-qqguild` 适配器为 `nonebot-adapter-qq`

> [!Warning]
> 对于之前使用QQ频道适配器的机器人项目，进行本次更新的同时，还需要修改之前的QQ频道适配器配置 \
> 大致只需要修改**配置选项名**即可，可参考适配器的说明：
> https://github.com/nonebot/adapter-qq \
> 例如：`QQGUILD_BOTS` -> `QQ_BOTS`

> 在QQ频道适配器**变更之前安装的**用户仍可正常使用 \
> 但现在 nonebot 各类文档指向的适配器都是新的 `nonebot-adapter-qq`，因此现在按照文档指引，如果安装本插件之前的版本，将无法正常支持QQ频道


### 2023.11.3 - v1.3.5
- 修复兑换计划商品不存在导致插件启动失败的问题 #205 #206
- 支持自定义时区 #201
  > [插件偏好设置 - timezone](https://github.com/Ljzd-PRO/nonebot-plugin-mystool/wiki/Configuration-Preference#timezone)  
  > 默认为上海时区 `Asia/Shanghai`

### 2023.8.30 - v1.3.1
- 登录功能增加黑名单/白名单功能 #178
  > [插件偏好设置 - enable_blacklist](https://github.com/Ljzd-PRO/nonebot-plugin-mystool/wiki/Configuration-Preference#enable_blacklist)
- 登录功能支持使用第三方打码平台进行人机验证（暂不支持GT4）
- 修复游戏签到人机验证无效的问题 #163
- 便笺体力除了达到阈值以外，体力已满也会提醒 #163
- 增加 `geetest_params`，用于填写人机验证打码平台API需要传入的URL参数 by @Joseandluue
  > [插件偏好设置 - geetest_params](https://github.com/Ljzd-PRO/nonebot-plugin-mystool/wiki/Configuration-Preference#geetest_params)

## ⚡ 功能和特性

- 支持QQ聊天和QQ频道
- 短信验证登录，免抓包获取 Cookie
- 自动完成每日米游币任务
- 自动进行游戏签到
- 可制定米游币商品兑换计划，到点兑换（因加入了人机验证，成功率较低）
- 可支持多个 QQ 账号，每个 QQ 账号可绑定多个米哈游账户
- QQ 推送执行结果通知
- 原神、崩坏：星穹铁道状态便笺通知
- 可为登录、每日米游币任务、游戏签到配置人机验证打码平台
- 可配置用户黑名单/白名单

## 📖 使用说明

### 🛠️ NoneBot2 机器人部署和插件安装

请查看 -> [🔗Installation](https://github.com/Ljzd-PRO/nonebot-plugin-mystool/wiki/Installation)

### 📖 插件具体使用说明

请查看 -> [🔗Wiki 文档](https://github.com/Ljzd-PRO/nonebot-plugin-mystool/wiki)

### ❓ 获取插件帮助信息

#### 插件命令

```
/帮助
```

> ⚠️ 注意 此处没有使用 [🔗 插件命令头](https://github.com/Ljzd-PRO/nonebot-plugin-mystool/wiki/Configuration-Config#commandstart)

## 其他

### 贡献
<a href="https://github.com/Ljzd-PRO/nonebot-plugin-mystool/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Ljzd-PRO/nonebot-plugin-mystool&max=1000" alt="贡献者"/>
</a>

### 🔨 开发版分支
[**🔨dev**](https://github.com/Ljzd-PRO/nonebot-plugin-mystool/tree/dev)

### 📃 源码说明
[📃Source-Structure](https://github.com/Ljzd-PRO/nonebot-plugin-mystool/wiki/Source-Structure)

### 适配 [绪山真寻Bot](https://github.com/HibiKier/zhenxun_bot) 的分支
- https://github.com/MWTJC/zhenxun-plugin-mystool
- https://github.com/ayakasuki/nonebot-plugin-mystool
