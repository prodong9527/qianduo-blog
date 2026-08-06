#!/usr/bin/env python3
"""Fix relative dates in index.html - only update the relative date label, preserve the time."""

import re
from datetime import datetime

TODAY = datetime(2026, 8, 3)  # Today is 2026-08-03

def get_relative_label(date_str):
    """Convert YYYY-MM-DD to relative date prefix."""
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        diff = (TODAY - dt).days
        if diff == 0:
            return "今天"
        elif diff == 1:
            return "昨天"
        elif diff == 2:
            return "2 天前"
        elif diff == 3:
            return "3 天前"
        elif diff == 4:
            return "4 天前"
        elif diff == 5:
            return "5 天前"
        elif diff == 6:
            return "6 天前"
        elif diff >= 7 and diff <= 14:
            return f"{diff} 天前"
        elif diff >= 15:
            return f"{diff}天前"
        else:
            return f"{diff}天前"  # future
    except:
        return None

# Known article dates and their times (extracted from current index.html)
article_times = {
    "2026-08-03": "19:04",
    "2026-08-02": "19:05",
    "2026-08-01": "11:00",
    "2026-07-31": "19:05",
    "2026-07-30": "19:03",
    "2026-07-29": "19:05",
    "2026-07-28": "19:04",
    "2026-07-27": "19:03",
    "2026-07-26": "19:04",
    "2026-07-24": "19:03",
    "2026-07-23": "19:00",
    "2026-07-22": "19:02",
    "2026-07-21": "19:05",
    "2026-07-20": "19:05",
    "2026-07-19": "11:00",
    "2026-07-18": "11:00",
    "2026-07-17": "19:02",
    "2026-07-16": "19:03",
    "2026-07-06": "19:05",
    "2026-07-02": "19:05",
    "2026-07-09": "19:05",
    "2026-07-08": "19:03",
    "2026-06-30": "19:03",
    "2026-06-29": "19:05",
    "2026-06-28": "19:05",
    "2026-06-27": "19:03",
    "2026-06-26": "19:04",
    "2026-06-25": "19:03",
    "2026-06-24": "19:04",
    "2026-06-23": "19:05",
    "2026-06-22": "19:03",
    "2026-06-21": "19:05",
    "2026-06-19": "11:00",
    "2026-06-18": "19:03",
    "2026-06-17": "11:00",
}

def fix_dates_in_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    updated = 0
    for article_date, time_str in article_times.items():
        label = get_relative_label(article_date)
        if label is None:
            continue
        
        new_text = f"{label} · {time_str}"
        
        # Pattern: within the specific article block, find and update the article-time div
        # We need to match the article, then find the article-time div inside it
        article_block_pattern = rf'(<article id="{article_date}"[^>]*>.*?<div class="article-time">)([^<]+)</div>'
        
        def replacer(m):
            return m.group(1) + new_text + '</div>'
        
        content, n = re.subn(article_block_pattern, replacer, content, count=1, flags=re.DOTALL)
        if n > 0:
            print(f"✓ Updated {article_date} -> {new_text}")
            updated += n
        else:
            print(f"✗ Article {article_date} not found in index.html")
    
    with open(filepath, 'w') as f:
        f.write(content)
    
    print(f"\nTotal articles updated: {updated}")

if __name__ == '__main__':
    fix_dates_in_file('/root/.openclaw/workspace/qianduo-blog/index.html')
