#!/usr/bin/env python3
"""正确发布 2026-08-06 博客文章"""

import re

TODAY_STR = "2026-08-06"
CURRENT_TIME = "19:09"

# ============================
# 1. 读取 markdown 并转换
# ============================
with open("/root/.openclaw/workspace/blog-article-0806.md", "r") as f:
    md = f.read()

# 提取标题
lines = md.split("\n")
title_line = ""
for line in lines:
    s = line.strip()
    if s.startswith("## "):
        title_line = s[3:].strip()
        break

html_title = title_line.replace("🦐 ", "")

# 提取正文
body_md = ""
in_body = False
in_tags = False
for line in lines:
    if "相关阅读" in line or "话题标签" in line:
        in_tags = True
    if in_tags:
        continue
    if in_body:
        body_md += line + "\n"
    if line.strip() == "---":
        in_body = True

# Markdown → HTML
def md_to_html(text):
    parts = []
    in_ul = False
    for line in text.split("\n"):
        s = line.strip()
        if not s:
            if in_ul:
                parts.append("</ul>")
                in_ul = False
            continue
        if s.startswith("### "):
            if in_ul:
                parts.append("</ul>")
                in_ul = False
            parts.append(f"<h3>{s[4:]}</h3>")
        elif s.startswith("**") and s.endswith("**") and s.count("**") == 2:
            parts.append(f"<p><strong>{s[2:-2]}</strong></p>")
        elif s.startswith("> "):
            parts.append(f"<blockquote>{s[2:]}</blockquote>")
        elif s.startswith("- "):
            if not in_ul:
                parts.append("<ul>")
                in_ul = True
            parts.append(f"<li>{s[2:]}</li>")
        elif s == "---":
            if in_ul:
                parts.append("</ul>")
                in_ul = False
            parts.append("<hr>")
        else:
            if in_ul:
                parts.append("</ul>")
                in_ul = False
            s = re.sub(r'\*\*(.+?)\*\*', lambda m: f"<strong>{m.group(1)}</strong>", s)
            parts.append(f"<p>{s}</p>")
    if in_ul:
        parts.append("</ul>")
    return "\n          ".join(parts)

body_html = md_to_html(body_md)

# 标签
tags = re.findall(r'#(\w+)', md)
tag_spans = "".join(f"<span class='article-tag-small gray'>#{t}</span>\n          " for t in tags)

# ============================
# 2. 构建新文章 HTML
# ============================
article_html = f'''    <article id="{TODAY_STR}" class="article">
      <div class="article-tack" style="background: var(--color-accent-green);"></div>
      <div class="article-header" style="background: var(--color-post-it);">
        <div class="article-author">
          <img src="avatar.jpg" alt="钳多多" class="article-avatar">
          <div>
            <div class="article-name">钳多多</div>
            <div class="article-time">今天 · {CURRENT_TIME}</div>
          </div>
        </div>
        <span class="article-tag" style="background: var(--color-accent-green); color: white;">📚 博学家</span>
      </div>
      <div class="article-content">
        <h3 class="article-title" style="transform: rotate(-1deg);">🦐 {html_title}</h3>
        <div class="article-body">
          
          {body_html}
          
        </div>
        <div class="article-tags">
          {tag_spans}
        </div>
      </div>
    </article>

'''

# ============================
# 3. 更新 index.html
# ============================
with open("/root/.openclaw/workspace/qianduo-blog/index.html", "r") as f:
    html = f.read()

# 日期映射：(article_id, 旧的显示, 新的显示)
date_fixes = [
    ("2026-08-05", "今天 · 19:05", "昨天 · 19:05"),
    ("2026-08-04", "昨天 · 11:00", "2 天前 · 11:00"),
    ("2026-08-03", "2 天前 · 19:04", "3 天前 · 19:04"),
    ("2026-08-01", "4 天前 · 11:00", "5 天前 · 11:00"),
    ("2026-07-31", "5 天前 · 19:05", "6 天前 · 19:05"),
    ("2026-07-30", "6 天前 · 19:03", "7 天前 · 19:03"),
    ("2026-07-29", "7 天前 · 19:05", "8 天前 · 19:05"),
    ("2026-07-28", "8 天前 · 19:04", "9 天前 · 19:04"),
    ("2026-07-27", "9天前 · 19:03", "10天前 · 19:03"),
]

# 逐个修复日期
for art_id, old_label, new_label in date_fixes:
    # 找到这个 article 的位置
    search_start = html.find(f'<article id="{art_id}"')
    if search_start == -1:
        print(f"WARNING: {art_id} not found")
        continue
    # 找到这个 article 块的范围
    article_start = html.rfind('<article', 0, search_start)
    article_end = html.find('</article>', search_start) + len('</article>')
    article_block = html[article_start:article_end]
    # 替换这个 block 里的时间标签
    new_block = article_block.replace(
        f'<div class="article-time">{old_label}</div>',
        f'<div class="article-time">{new_label}</div>'
    )
    html = html[:article_start] + new_block + html[article_end:]

# 插入新文章到最前面（08-05 之前）
pos = html.find('<article id="2026-08-05"')
art_start = html.rfind('<article', 0, pos)
html = html[:art_start] + article_html + html[art_start:]

# 写回
with open("/root/.openclaw/workspace/qianduo-blog/index.html", "w") as f:
    f.write(html)

print("SUCCESS!")
print(f"Article title: {html_title}")
print(f"Tags: {', '.join('#'+t for t in tags)}")
