# leoknox.me — Leo 的三语个人主页

英文 / 繁体中文 / 简体中文。沿用暖白、陶土橙与深蓝的个人小册子风格，内容围绕性格、思维方式、习惯、兴趣和个人原则。

纯 HTML + CSS + JavaScript，无构建依赖。仅本地修改，未上传 Sites、未部署、未改 Cloudflare/DNS。

## 本地预览

双击 `preview.command`，访问 http://127.0.0.1:5680/ 。Ctrl+C 停止服务。

也可在本站目录运行：

```sh
python3 -m http.server 5680 --bind 127.0.0.1
```

| 语言 | 本地路径 | 正式规范地址 |
| --- | --- | --- |
| English（默认） | `/` | `https://leoknox.me/` |
| 繁體中文 | `/zh-hant/` | `https://leoknox.me/zh-hant/` |
| 简体中文 | `/zh-hans/` | `https://leoknox.me/zh-hans/` |

## 内容更新

基于用户本次提供的自我画像材料重新编写，包含：

- 好奇与动手、独立判断、幽默与整活。
- 观察分析 → 归纳 → 提炼 → 迁移 → 验证 → 修正 → 反馈的思维循环。
- 记录和复盘、数字环境自主、训练记录与状态观察、日常体验。
- 八项兴趣：技术与互联网、Minecraft、数码画面、旅行与城市、AI、社会文化与幽默、健身、咖啡。
- 七项原则：事实、独立、验证、开放、成长、尊重、务实。

这是用于本人审阅的第一人称自我介绍，不是人格测评或专业能力认证。没有加入具体学校、生日、所在地、家庭、身体数据、旅行轨迹或项目履历。没有下载或使用补充材料中的第三方示意图，也没有把其图片当成本人的照片。

## 语言行为

- 访问根路径始终返回完整英文 HTML；直接访问中文路径始终返回对应语言。
- 三个版本均完整预渲染，内容不是靠 JavaScript 临时翻译或请求接口获取。禁用 JS 时八项兴趣都会展开，内容仍可阅读。
- 根据浏览器语言显示可关闭的切换建议，**不自动跳转，不按 IP 定位**。
- 浏览器首选语言按顺序匹配受支持语言。`zh-Hant` 与 TW/HK/MO 识别为繁体；`zh-Hans`、CN/SG 和未指定地区的 `zh` 使用简体；英文或无匹配时为英文。
- 用户主动选择的语言保存在本机 localStorage，后续用于建议，不强制覆盖地址。关闭提示的选择仅在当前会话 sessionStorage 中保存。
- 语言链接均是真实 HTML 超链接。切换时保留当前锚点；拒绝本地存储不会影响切换。
- 页面没有发送语言偏好、分析事件或其他资料的网络请求。

## 友情链接与邮箱

三种语言都包含：

- `https://leoknox.dev/`：项目与开发。
- `https://agent.leoknox.us/`：服务器监控。

仅展示用户指定的链接，不嵌入监控数据或声称在线状态已验证。外链同标签页打开；没有自动访问、登录或调用监控服务。

每页包含 `leo@leosoffice.com`。复制反馈已本地化；mailto 由用户的邮件客户端处理，本站不自动发信。

## 多语言 SEO

- `lang="en"` / `zh-Hant` / `zh-Hans`。
- 每种语言有自己的 title、description、canonical、JSON-LD、Open Graph/Twitter 文案与 1200×630 PNG 分享图。
- 每版 canonical 指向自己，不把中文 canonical 指向英文。
- 三版均有互相对应、包含自身的 `hreflang="en"`、`zh-Hant`、`zh-Hans`；`x-default` 指向英文根路径。
- sitemap.xml 列出三个规范首页。站点地图与 canonical 一致。
- ProfilePage / Person JSON-LD；404 为英文，noindex，不伪造与首页等价的 hreflang。
- 真实语言切换链接、静态完整正文，无 meta refresh、无语言重定向。

此方案遵循 Google 建议：不同语言使用不同 URL，并避免按推测语言强制重定向。多语言配置不保证收录或排名。

## 文件

```text
index.html                English
zh-hant/index.html        繁體中文
zh-hans/index.html        简体中文
404.html                  English error page
assets/style.css          共享样式
assets/main.js            菜单、兴趣、复制与语言提示
assets/language.mjs        浏览器语言匹配
assets/og-*.png           三种语言分享图
content/*.json            各语言文案对照参考
```

网页直接使用各版 HTML，不在运行时读取 content JSON；JSON 是文案参考快照，修改后需同步对应 HTML。`_headers` 使用严格 CSP，修改内联 JSON-LD 后要更新 script SHA-256 hash。

## 将来部署（尚未执行）

Cloudflare Pages 无构建静态站：上传 index.html、zh-hant/、zh-hans/、404.html、assets/、robots.txt、sitemap.xml、_headers、_redirects。文档、content/、preview.command、cloudflare-redirect-rule.json 不必上传。

在 Pages Custom domains 中绑定 `leoknox.me` 和 `www.leoknox.me`，按实际托管项目给出的目标配置 DNS（根域名名称显示为 `@`），并确认两者 HTTPS 证书有效。

域名级 Redirect Rules → Single Redirect：

```text
匹配：(http.host eq "www.leoknox.me") or (http.host eq "leoknox.me" and not ssl)
目标：concat("https://leoknox.me", http.request.uri.path)
状态码：301
Preserve query string：启用
```

`cloudflare-redirect-rule.json` 是单条规则参考对象，不是完整 ruleset API 请求，本地文件不会执行云端修改。Pages `_redirects` 不支持来源主机名匹配的域名级跳转，www 需在域名规则中配置。

若有默认生产 `*.pages.dev` 地址，另行跳转到正式域名，并处理预览分支访问或 noindex。Python 本地服务不执行 Pages 响应头、301 文件或自定义 404。

上线后验证：三个规范页面 200；HTTP/www 301 保留路径与查询参数且无循环；无效 URL 真正返回 404；SEO 文件与图像可访问；随后在真实 Search Console/Bing 账号中验证域名并提交站点地图。本次没有执行这些云端步骤。

## 官方参考

- [Google 多语言与多地区站点](https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites)
- [Google 本地化版本标注](https://developers.google.com/search/docs/specialty/international/localized-versions)
- [Cloudflare Pages 自定义域名](https://developers.cloudflare.com/pages/configuration/custom-domains/)
- [Pages 重定向](https://developers.cloudflare.com/pages/configuration/redirects/)
- [Redirect Rules](https://developers.cloudflare.com/rules/url-forwarding/single-redirects/settings/)
