# mihomo-rules

适用于 mihomo（Clash Meta）的规则集。以 [MetaCubeX/meta-rules-dat](https://github.com/MetaCubeX/meta-rules-dat) 为上游，每日同步并叠加本仓库的增补与删减，编译为 mrs 格式发布。每日北京时间 7:30 更新。

## 规则集地址

规则集发布于 `meta` 分支：

| 类型 | 地址 | behavior |
|---|---|---|
| 域名 | `https://raw.githubusercontent.com/uhovohu/mihomo-rules/meta/geo/geosite/<名称>.mrs` | `domain` |
| IP | `https://raw.githubusercontent.com/uhovohu/mihomo-rules/meta/geo/geoip/<名称>.mrs` | `ipcidr` |

每个规则集另附同名 `.yaml` 文本版本，文件头注明其构成（上游来源、扣除项与增补项）。

示例：

```yaml
rule-providers:
  google:
    type: http
    behavior: domain
    format: mrs
    url: https://raw.githubusercontent.com/uhovohu/mihomo-rules/meta/geo/geosite/google.mrs
    interval: 86400
```

## 配置示例

[uhovohu/clash](https://github.com/uhovohu/clash) 提供基于本规则集的完整配置：

| 配置 | 说明 |
|---|---|
| [uhovohu-mihomo.yaml](https://github.com/uhovohu/clash/blob/main/uhovohu-mihomo.yaml) | 完整版，含链式代理 |
| [uhovohu-mihomo-nolink.yaml](https://github.com/uhovohu/clash/blob/main/uhovohu-mihomo-nolink.yaml) | 完整版，不含链式代理 |
| [uhovohu-mihomo-lite.yaml](https://github.com/uhovohu/clash/blob/main/uhovohu-mihomo-lite.yaml) | 精简版，含链式代理 |
| [uhovohu-mihomo-nolink-lite.yaml](https://github.com/uhovohu/clash/blob/main/uhovohu-mihomo-nolink-lite.yaml) | 精简版，不含链式代理 |

## 规则集列表

来源说明：

| 标记 | 含义 |
|---|---|
| 上游 | 取自上游同名规则集，可能含少量增补或删减 |
| 上游 − X | 取自上游，并扣除规则集 X 已包含的条目 |
| 本仓库 | 上游无对应规则集，由本仓库维护 |
| 外部 | 转发自其他项目的规则集 |

标注「合集」的规则集已扣除各厂商规则集中的条目，仅保留无独立规则集的部分。

### geosite（域名）

#### 一、拦截

| 名称 | 说明 | 来源 |
|---|---|---|
| icloudprivaterelay | iCloud 专用代理（Private Relay）入口 | 上游 |
| reject | 其他拦截项：国内 App 的日志上报和遥测（美团、京东、字节等）、交易所推送、国内 DoH、个别 STUN 和 NTP | 本仓库 |
| awavenue | 秋风广告规则（AWAvenue），以国内 App 广告为主 | 外部（TG-Twilight/AWAvenue-Ads-Rule） |
| ads-misc | 其他广告追踪、营销追踪、广告投放和受众数据、国内广告 SDK、统计上报、反广告拦截脚本，如 DoubleClick、AppsFlyer、Marketo、穿山甲、Amplitude | 本仓库 |
| category-httpdns-cn | 国内 HTTPDNS 接口：阿里、百度、腾讯、美团等 | 上游 |
| win-spy | Windows 遥测和广告 | 上游 |

#### 二、内网与连通性检测

| 名称 | 说明 | 来源 |
|---|---|---|
| private | 局域网和保留域名：`localhost`、`.local`、`in-addr.arpa`、路由器管理地址等 | 上游 |
| connectivity-check | 联网检测地址（合集，保留微软部分） | 上游 |
| sniffer-skip-misc | 米家设备连接域名 | 本仓库 |

#### 三、交易所

| 名称 | 说明 | 来源 |
|---|---|---|
| bybit | Bybit | 上游 |
| binance | Binance 币安，含专属风控 | 上游 |
| coinbase | Coinbase：主站、App 后端、Wallet 跳转、Base 链 | 本仓库 |
| bitget | Bitget | 本仓库 |
| huobi | HTX（火币） | 上游 |
| okx | OKX | 上游 |
| tradingview | TradingView | 本仓库 |
| bookmap | Bookmap | 本仓库 |
| category-cryptocurrency | 其他加密货币相关：交易所、钱包、行情、区块浏览器（合集） | 上游 − binance、bybit、okx、huobi、coinbase |

#### 四、海外商家

| 名称 | 说明 | 来源 |
|---|---|---|
| adobe@!cn | Adobe 海外部分 | 上游 − adobe@cn |
| tesla@!cn | Tesla 海外部分 | 上游 − tesla@cn |
| bytedance@!cn | 字节跳动海外部分：TikTok、CapCut、Lark 国际版等 | 上游 |
| disney@!cn | Disney 海外部分，含 Disney+、Hulu、ESPN | 上游 − disney@cn |
| steam@!cn | Steam 海外部分 | 上游 − steam@cn |
| taptap@!cn | TapTap 海外部分 | 上游 |
| bilibili@!cn | 哔哩哔哩海外部分 | 上游 |
| category-ip-geo-detect@!cn | IP 检测：查 IP、测速、泄露与指纹检测、纯净度评分（国内外站点均在此） | 本仓库 |
| cloudflare@!cn | Cloudflare 海外部分 | 上游 − cloudflare@cn |
| vercel | Vercel：Next.js、Turborepo、vercel.app 托管站、Grep | 上游 |
| amazon@!cn | Amazon 海外部分，含 AWS（Prime Video、Twitch 另有文件） | 上游 − amazon@cn、primevideo、twitch |
| linkedin@!cn | LinkedIn 海外部分 | 上游 − linkedin@cn |
| paypal@!cn | PayPal 海外部分，含 Braintree | 上游 − paypal@cn |
| jiguang@!cn | 极光推送海外版 EngageLab | 本仓库 |
| category-cas@!cn | 海外证书机构：证书吊销查询（OCSP、CRL）等 | 上游 − category-cas@cn |
| akamai@!cn | Akamai 海外部分 | 上游 − akamai@cn |
| youtube | YouTube | 上游 |
| google | Google 全系服务：搜索、Gmail、Play、Firebase、Gemini 等（YouTube、Android 另有文件） | 上游 − youtube、android |
| amp | Google AMP 加速页 | 上游 |
| openai | OpenAI：ChatGPT、API、Sora | 上游 |
| anthropic | Anthropic：Claude、Claude Code，含 CDN、认证、监控上报、客服组件 | 本仓库 |
| perplexity | Perplexity | 上游 |
| groq | Groq | 上游 |
| cerebras | Cerebras | 上游 |
| huggingface | Hugging Face | 上游 |
| cursor | Cursor | 上游 |
| elevenlabs | ElevenLabs | 上游 |
| comfy | ComfyUI 官网和插件库 | 上游 |
| windsurf | Windsurf | 上游 |
| poe | Poe | 上游 |
| manus | Manus | 上游 |
| jetbrains-ai | JetBrains AI | 上游 |
| youmind | YouMind | 上游 |
| category-ai-chat-!cn | 其他海外 AI 服务（合集） | 上游 |
| github | GitHub：主站、raw、头像、Copilot、npm | 上游 |
| vscode | VS Code：网页版、插件市场、设置同步、Webview | 本仓库 |
| github1s | GitHub1s（以网页版 VS Code 浏览仓库） | 上游 |
| python | Python 官网、PyPI 包仓库与下载服务器 | 上游 |
| category-dev | 开发者网站：编程语言、包仓库、开发工具、文档查询（合集） | 上游 |
| discord | Discord | 上游 |
| telegram | Telegram | 上游 |
| reddit | Reddit | 上游 |
| tumblr | Tumblr | 上游 |
| line | LINE | 上游 |
| truthsocial | Truth Social | 本仓库 |
| meta | Meta：Facebook、Instagram、WhatsApp、Threads、Llama | 上游 |
| x | X（Twitter）、xAI / Grok | 上游 |
| spacex | SpaceX、Starlink | 上游 |
| neuralink | Neuralink | 上游 |
| theboringcompany | The Boring Company | 上游 |
| netflix | Netflix | 上游 |
| primevideo | Prime Video | 上游 |
| twitch | Twitch | 上游 |
| dazn | DAZN 体育直播 | 上游 |
| hbo | HBO、Max | 上游 |
| vimeo | Vimeo | 上游 |
| rumble | Rumble | 上游 |
| plex | Plex | 上游 |
| emby | 部分公开 Emby 服务 | 本仓库 |
| spotify | Spotify | 上游 |
| steamunlocked | SteamUnlocked | 上游 |
| steaminventoryhelper | Steam Inventory Helper 插件 | 上游 |
| epicgames | Epic Games | 上游 |
| coinpoker | CoinPoker：主站、后端、监控和 App 用到的第三方服务 | 本仓库 |
| biliintl | 哔哩哔哩国际版 | 上游 |
| ookla-speedtest | Speedtest by Ookla | 上游 |
| nodeseek | NodeSeek 论坛 | 上游 |
| vps | VPS 商家、VPS 比价、中转面板官网 | 本仓库 |
| forum | VPS 及网络技术论坛 | 本仓库 |
| airport | 代理服务测评站点 | 本仓库 |
| proxy-misc | 其他海外网站：划词翻译、BlackBerry、油猴、部分 Mac 软件作者站点 | 本仓库 |
| microsoft | Microsoft 全系服务：Windows、Office、Bing、Azure、Copilot（GitHub、VS Code 另有文件） | 上游 − github、vscode、connectivity-check |
| apple | Apple 全系服务：iCloud、App Store、Apple Music、系统更新、推送，含 CDN 别名 | 上游 |
| appleakamai | Apple 设备使用的 Akamai 别名（iCloud 邮件、推送等） | 本仓库 |
| android | Android | 上游 |
| f-droid | F-Droid | 上游 |
| apkpure | APKPure | 上游 |
| apkmirror | APKMirror | 上游 |
| apkcombo | APKCombo | 上游 |
| wise | Wise | 上游 |
| pay | 海外支付和配套：Stripe、Adyen、Paddle 等收银台，3D 验证、风控反欺诈、人机验证、KYC | 本仓库 |
| getui | 个推 | 上游 |
| jiguang | 极光推送 | 上游 |
| category-stun | STUN 服务器 | 上游 |
| saas@!cn | 海外通用第三方服务：多个 App 共用的 SDK、SaaS 接口，如 Sentry 公共入口、RevenueCat、OneTrust、Branch、jsDelivr | 本仓库 |
| adobe@cn | Adobe 国内部分 | 上游 |
| tesla@cn | Tesla 国内部分 | 上游 |
| bytedance@cn | 字节跳动国内部分：抖音、头条、西瓜、飞书、火山引擎等，含抖音 PCDN | 上游 − bytedance@!cn |
| disney@cn | Disney 国内部分 | 上游 |
| steam@cn | Steam 国内部分 | 上游 |
| taptap@cn | TapTap 国内部分 | 上游 − taptap@!cn |
| bilibili@cn | 哔哩哔哩国内部分 | 上游 − bilibili@!cn |
| cloudflare@cn | Cloudflare 国内部分 | 上游 |
| amazon@cn | Amazon 国内部分 | 上游 |
| linkedin@cn | LinkedIn 国内部分 | 上游 |
| paypal@cn | PayPal 国内部分 | 上游 |
| category-cas@cn | 国内证书机构 | 上游 |
| stun@cn | 国内公共 STUN：搜狐、电信、联通和几所高校 | 本仓库 |
| akamai@cn | Akamai 国内部分 | 上游 |

#### 五、国内商家

| 名称 | 说明 | 来源 |
|---|---|---|
| tencent@!cn | 腾讯海外部分 | 上游 |
| alibaba@!cn | 阿里海外部分 | 上游 |
| huawei@!cn | 华为海外部分 | 上游 |
| xiaomi@!cn | 小米海外部分 | 上游 |
| netease@!cn | 网易海外部分 | 上游 |
| jd@!cn | 京东海外部分 | 上游 |
| xiaohongshu@!cn | 小红书海外部分（RedNote） | 上游 |
| chinamobile@!cn | 中国移动海外部分 | 上游 |
| chinaunicom@!cn | 中国联通海外部分 | 上游 |
| chinatelecom@!cn | 中国电信海外部分 | 上游 |
| wechat | 微信：QQ 主域、微信自有域、支付、多媒体 CDN、小程序、推送 | 本仓库 |
| honor | 荣耀 | 上游 |
| meituan | 美团 | 上游 |
| baidu | 百度，含百度网盘 | 上游 |
| kuaishou | 快手 | 上游 |
| xunlei | 迅雷 | 上游 |
| meitu | 美图 | 上游 |
| smzdm | 什么值得买 | 上游 |
| zhihu | 知乎 | 上游 |
| pinduoduo | 拼多多 | 上游 |
| deepseek | DeepSeek | 上游 |
| category-ai-cn | 其他国内 AI 服务（合集） | 上游 |
| yy | YY、多玩、欢聚 | 上游 |
| tendcloud | TalkingData 统计 | 上游 |
| wasu | 华数 | 上游 |
| geetest | 极验验证码 | 上游 |
| ishumei | 数美风控 | 上游 |
| cn-misc | 上游没有单独文件的国内小应用和服务，如金十数据、Bark 推送、Go 镜像 | 本仓库 |
| cn-misc-realip | 其他国内服务：向日葵远控、微店、唯品会、税务、公安一网通办 | 本仓库 |
| saas@cn | 国内通用第三方服务：多个 App 共用的 SDK、SaaS 接口，如 MobTech、DCloud、网易易盾 | 本仓库 |
| tencent@cn | 腾讯国内部分（微信另有文件） | 上游 − tencent@!cn、wechat |
| alibaba@cn | 阿里国内部分：淘宝、支付宝、阿里云、高德等 | 上游 − alibaba@!cn |
| huawei@cn | 华为国内部分 | 上游 − huawei@!cn |
| xiaomi@cn | 小米国内部分 | 上游 − xiaomi@!cn |
| netease@cn | 网易国内部分 | 上游 − netease@!cn |
| jd@cn | 京东国内部分 | 上游 − jd@!cn |
| xiaohongshu@cn | 小红书国内部分 | 上游 − xiaohongshu@!cn |
| chinamobile@cn | 中国移动国内部分 | 上游 − chinamobile@!cn |
| chinaunicom@cn | 中国联通国内部分 | 上游 − chinaunicom@!cn |
| chinatelecom@cn | 中国电信国内部分 | 上游 − chinatelecom@!cn |
| nvidia@cn | NVIDIA 国内部分 | 上游 |
| intel@cn | Intel 国内部分 | 上游 |
| amd@cn | AMD 国内部分 | 上游 |
| synology@cn | 群晖国内部分 | 上游 |

#### 六、国内分类

| 名称 | 说明 | 来源 |
|---|---|---|
| category-cdn-cn | 国内 CDN（合集） | 上游 |
| category-dev-cn | 国内开发者网站（合集） | 上游 |
| category-bank-cn | 国内银行（合集） | 上游 |
| category-securities-cn | 国内证券（合集） | 上游 |
| category-ntp@!cn | 海外时间服务器，如 `pool.ntp.org`（合集） | 上游 − category-ntp@cn |
| category-ntp@cn | 国内时间服务器（合集） | 上游 |
| category-netdisk-cn | 国内网盘：115、123 盘、蓝奏云、坚果云等（合集） | 上游 |
| category-games-cn | 国内游戏（合集） | 上游 |
| category-finance@cn | 国内金融（合集） | 上游 |

#### 七、通用总表

| 名称 | 说明 | 来源 |
|---|---|---|
| geolocation-!cn | 海外常见域名总表 | 上游 |
| cn | 国内域名总表 | 上游 |
| geolocation-cn | 国内常见域名总表 | 上游 |

### geoip（IP）

| 名称 | 说明 | 来源 |
|---|---|---|
| reject | 其他拦截 IP：联通、电信、移动的部分地址，美团位置上报等 | 本仓库 |
| private | 局域网和保留地址 | 上游 |
| ipv6-all | 全部 IPv6 地址（`::/0`） | 本仓库 |
| sniffer-skip-ip | 国内大厂（腾讯、抖音、小红书等）、国际 CDN 的部分 IP | 本仓库 |
| proxy-misc | 其他海外 IP：甲骨文、Clouvider / Gcore、Dropbox | 本仓库 |
| nodeseek | NodeSeek 邮件服务器 | 本仓库 |
| cn-misc | 其他国内 IP：中国联通、哈啰单车 | 本仓库 |
| amazon | 部分 CloudFront 地址 | 本仓库 |
| bybit | Bybit 服务器 | 本仓库 |
| binance | Binance 服务器（阿里云、腾讯云、AWS 东京） | 本仓库 |
| bitget | Bitget 服务器 | 本仓库 |
| htx | HTX（火币）服务器 | 本仓库 |
| okx | OKX 服务器 | 本仓库 |
| bookmap | Bookmap 服务器 | 本仓库 |
| openai | ChatGPT App 直接连的 Azure 地址 | 本仓库 |
| category-cryptocurrency | 加密货币类 App 的服务器地址（CoinGlass） | 本仓库 |
| google | Google | 上游 |
| anthropic | Anthropic（AS399358） | 本仓库 |
| discord | Discord 语音（AS49544） | 本仓库 |
| telegram | Telegram | 上游 |
| twitter | X（Twitter） | 上游 |
| netflix | Netflix | 上游 |
| bilibili | 哔哩哔哩国内机房 | 上游 |
| cloudflare | Cloudflare | 上游 |
| apple | Apple（`17.0.0.0/8` 等） | 本仓库 |
| wechat | 微信：官方 API、媒体 CDN、小程序、支付、核心通信 | 本仓库 |
| jingdongcloud | 京东云 | 本仓库 |
| cn | 国内 IP 总表 | 上游 |

## 许可证

GPL-3.0
