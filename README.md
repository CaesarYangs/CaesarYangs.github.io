# Cyrus' Paperbox

一个简单的个人博客：白底、单栏正文、文字导航和文章列表。
原生 HTML、CSS、JavaScript，可直接在 GitHub Pages 发布。无需 Hugo、Jekyll、Node 或构建步骤。

## 本地运行

在仓库根目录执行：

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

使用任意静态文件服务器也可以。必须从仓库根目录提供服务，导航与资源使用站点根路径。
云环境已有 Python、Chromium 和可选的浏览器测试工具，无需额外安装才能运行网站。

## 编辑

- `index.html`：首页简介与文章列表。
- `blogs/`：4 篇博客，正文保存在各自的 `index.html` 中。
- `docs/`：13 篇操作系统和算法笔记。
- `others/`：关于与项目；`resume/`：简历 PDF。
- `assets/css/site.css`：公共排版和手机适配。
- `assets/js/site.js`：年份与旧缓存清理。网站阅读、导航均不依赖 JavaScript。

修改文章时编辑 `<article>` 内的 HTML。`data-post-meta` 标记日期和分类。
新增文章可以复制现有文章文件，修改标题、description、canonical URL、正文和日期，再在首页或栏目列表中添加链接。
导航、RSS 和 sitemap 都是普通静态文件，需要手动同步；没有生成器或搜索索引维护步骤。
保留原有标题的 `id`，以免已分享的锚点失效。

分治、搜索笔记使用仓库内的 KaTeX 渲染公式；参考对应页面的脚本和 `data-math` 标记即可。
外部 GitLab 图片仍保留原地址，当前云环境可能无法加载它们。

## 发布

将仓库推送至 GitHub 后，在 **Settings → Pages** 选择 **Deploy from a branch → main → / (root)**。
保留 `.nojekyll`，GitHub Pages 会直接发布这些文件。根路径配置适用于 `CaesarYangs.github.io`，子目录站点需要调整资源路径。
推送到已配置 Pages 的 main 分支后，GitHub 会按仓库发布设置更新网站。

## 验证（可选）

```sh
python3 -m unittest discover -s tests -v
python3 scripts/check_links.py
# 先启动本地服务器，再使用当前环境的 Playwright 和 Chromium：
python3 tests/browser_smoke.py --output /tmp/paperbox-preview
```

内容基线来自原站的 17 篇正文与 50 个 HTML 地址。博客基线排除了 Hugo 重复生成的标题、日期与标签前言；保留正文、原锚点、代码和图片。以后有意修改原文章时，应人工确认差异后再更新对应基线。
`sw.js` 仅供旧访问者退役原缓存使用，新站不注册 Service Worker，也不会清理同源其他应用的缓存。
