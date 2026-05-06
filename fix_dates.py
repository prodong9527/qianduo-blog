import re

with open('index.html', 'r') as f:
    content = f.read()

# We need to do replacements in reverse order (oldest first) to avoid conflicts
# The cascade: after adding today:
# 05-03 周星驰: 今天->昨天 (already done above)
# 05-02 松下幸之助: 昨天·19:04 -> 2天前
# 05-01 费曼: 昨天·21:34 -> 3天前  
# 04-30 马斯克: 昨天·19:04 -> 4天前
# 04-29 蔡元培: 昨天 -> 5天前
# 04-28 左宗棠: 昨天 -> 6天前
# 04-27: 2天前 -> 3天前
# 04-26: 3天前 -> 4天前
# 04-24: 4天前 -> 5天前
# 04-23: 5天前 -> 6天前
# 04-22: 6天前 -> 7天前
# 04-21: 7天前 -> 8天前
# 04-20: 8天前 -> 9天前
# 04-19: 9天前 -> 10天前
# and so on...

# Do replacements from oldest to newest to avoid conflicts
replacements = [
    # Specific articles with timestamps that need to become day-relative
    ('>昨天 · 21:34</div>', '>3天前</div>'),   # 费曼 05-01
    ('>昨天 · 19:04</div>', '>4天前</div>'),   # 马斯克 04-30
    ('>昨天</div>', '>5天前</div>'),           # 蔡元培 04-29
    ('>2天前</div>', '>3天前</div>'),
    ('>3天前</div>', '>4天前</div>'),
    ('>4天前</div>', '>5天前</div>'),
    ('>5天前</div>', '>6天前</div>'),
    ('>6天前</div>', '>7天前</div>'),
    ('>7天前</div>', '>8天前</div>'),
    ('>8天前</div>', '>9天前</div>'),
    ('>9天前</div>', '>10天前</div>'),
    ('>10天前</div>', '>11天前</div>'),
]

for old, new in replacements:
    content = content.replace(old, new)

# Now fix 松下幸之助 (05-02) specifically - it's still showing as yesterday but is 2 days ago
# It was "昨天 · 19:04" and we've changed it to "4天前" above, but we need it to be "2天前"
# Let me check what it's now...

print("Checking 松下幸之助 area:")
idx = content.find('松下幸之助')
if idx >= 0:
    snippet = content[idx-200:idx+100]
    import re
    matches = re.findall(r'<div class="article-time">[^<]+</div>', snippet)
    for m in matches:
        print(m)

print("\nDone")
with open('index.html', 'w') as f:
    f.write(content)
