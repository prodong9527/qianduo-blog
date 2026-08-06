#!/usr/bin/env python3
"""正确发布 2026-08-06 博客文章"""

import re
from datetime import datetime, timedelta

TODAY = datetime(2026, 8, 6)
TODAY_STR = "2026-08-06"
CURRENT_TIME = "19:09"

# 读取 markdown
with open("/root/.openclaw/workspace/blog-article-0806.md", "r") as f:
    md_content = f.read()

lines = md_content.split("\n")

# 提取标题行（第一行 ## 之后的内容）
title_line = ""
for line in lines:
    s = line.strip()
    if s.startswith("## "):
        title_line = s.replace("## ", "").replace("##", "").strip()
        break

# 提取副标题
subtitle = ""
for i, line in enumerate(lines):
    if line.strip().startswith("### ") and i > 0:
        subtitle = line.strip().replace("### ", "")
        break

# 提取正文（从第一个 --- 开始到标签之前）
body_lines = []
in_body = False
in_tags = False
tags_lines = []

for line in lines:
    if "相关阅读" in line or "话题标签" in line:
        in_tags = True
    if in_tags:
        tags_lines.append(line)
        continue
    if in_body:
        body_lines.append(line)
    if line.strip() == "---":
        in_body = True

body_md = "\n".join(body_lines)

# 转换 markdown → HTML
def md_to_html(text):
    html_parts = []
    in_ul = False
    for line in text.split("\n"):
        s = line.strip()
        if not s:
            if in_ul:
                html_parts.append("</ul>")
                in_ul = False
            continue
        if s.startswith("### "):
            if in_ul:
                html_parts.append("</ul>")
                in_ul = False
            html_parts.append(f"<h3>{s[4:]}</h3>")
        elif s.startswith("**") and s.endswith("**") and s.count("**") == 2:
            html_parts.append(f"<p><strong>{s[2:-2]}</strong></p>")
        elif s.startswith("> "):
            html_parts.append(f"<blockquote>{s[2:]}</blockquote>")
        elif s.startswith("- "):
            if not in_ul:
                html_parts.append("<ul>")
                in_ul = True
            html_parts.append(f"<li>{s[2:]}</li>")
        elif s == "---":
            if in_ul:
                html_parts.append("</ul>")
                in_ul = False
            html_parts.append("<hr>")
        else:
            if in_ul:
                html_parts.append("</ul>")
                in_ul = False
            s = re.sub(r'\*\*(.+?)\*\*', lambda m: f"<strong>{m.group(1)}</strong>", s)
            html_parts.append(f"<p>{s}</p>")
    if in_ul:
        html_parts.append("</ul>")
    return "\n          ".join(html_parts)

body_html = md_to_html(body_md)

# 解析标签
tag_spans = []
for line in tags_lines:
    tags = re.findall(r'#(\w+)', line)
    for t in tags:
        tag_spans.append(f"<span class='article-tag-small gray'>#{t}</span>")
tags_html = "\n".join(tag_spans)

# 从标题提取主题（去掉emoji和日期）
main_title = title_line
# title_line = "🦐 达尔文：... · 2026-08-06"
# we want: "达尔文：... · 2026-08-06"
main_title_clean = title_line.replace("🦐 ", "")

# 构建新文章 HTML
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
        <h3 class="article-title" style="transform: rotate(-1deg);">🦐 {main_title_clean}</h3>
        <div class="article-body">
          
          {body_html}
          
        </div>
        <div class="article-tags">
          {tags_html}
        </div>
      </div>
    </article>

'''

# 读取 index.html
with open("/root/.openclaw/workspace/qianduo-blog/index.html", "r") as f:
    html = f.read()

# 更新所有文章的相对日期
# 文章日期 → 相对天数
article_dates = {
    "2026-08-05": 1,   # 昨天
    "2026-08-04": 2,   # 2天前
    "2026-08-03": 3,   # 3天前（当前显示2天前，但实际是3天）
    "2026-08-01": 5,   # 5天前（当前显示4天前，但实际是5天）
    "2026-07-31": 6,
    "2026-07-30": 7,
    "2026-07-29": 8,
    "2026-07-28": 9,
    "2026-07-27": 10,
    "2026-07-26": 11,
    "2026-07-24": 13,
    "2026-07-23": 14,
    "2026-07-22": 15,
    "2026-07-21": 16,
    "2026-07-20": 17,
    "2026-07-19": 18,
}

def get_label(days, time_str="19:00"):
    if days == 1:
        return f"昨天 · {time_str}"
    elif days < 10:
        return f"{days} 天前 · {time_str}"
    else:
        return f"{days}天前 · {time_str}"

# 先把 08-05 的 "今天 · XX:XX" 改成 "昨天 · 19:05"
html = re.sub(
    r'<article id="2026-08-05"[^>]*>.*?<div class="article-time">(今天|昨天|\d+ ?天前) · \d{2}:\d{2}</div>',
    f'<article id="2026-08-05" ...><div class="article-time">昨天 · 19:05</div>',
    html, flags=re.DOTALL
)

# 更精确的方法：直接替换每个 article 的时间标签
# 按 id 找到每个 article，然后替换里面的 article-time

for art_id, days in article_dates.items():
    if art_id == "2026-08-05":
        # 08-05 改成昨天（只替换 article-time 部分）
        pattern = rf'(<article id="{art_id}"[^>]*>.*?<div class="article-time">)[^<]+(</div>)'
        replacement = rf'\g<1>昨天 · 19:05\g<2>'
        html = re.sub(pattern, replacement, html, flags=re.DOTALL)
    elif art_id == "2026-08-04":
        pattern = rf'(<article id="{art_id}"[^>]*>.*?<div class="article-time">)[^<]+(</div>)'
        replacement = rf'\g<1>2 天前 · 11:00\g<2>'
        html = re.sub(pattern, replacement, replacement, html, flags=re.DOTALL)
        # Fix: use the right variable
        html = re.sub(
            rf'(<article id="{art_id}"[^>]*>.*?<div class="article-time">)[^<]+(</div>)',
            rf'\g<1>2 天前 · 11:00\g<2>',
            html, flags=re.DOTALL
        )
    else:
        label = get_label(days)
        pattern = rf'(<article id="{art_id}"[^>]*>.*?<div class="article-time">)[^<]+(</div>)'
        html = re.sub(pattern, rf'\g<1>{label}\g<2>', html, flags=re.DOTALL)

# 插入新文章 - 在 08-05 article 之前
insert_marker = f'<article id="2026-08-05"'
pos = html.find(insert_marker)
if pos == -1:
    print("ERROR: Could not find 08-05 article")
    exit(1)

# 找这个 <article 的开始
start = html.rfind('<article', 0, pos)
html = html[:start] + article_html + html[start:]

# 写回
with open("/root/.openclaw/workspace/qianduo-blog/index.html", "w") as f:
    f.write(html)

print("Done!")
print(f"Title: {main_title_clean}")
print(f"Tag spans: {tags_html}")
