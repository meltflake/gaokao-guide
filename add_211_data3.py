#!/usr/bin/env python3
"""Add remaining 211 school 2025 data - batch 3 (宁夏大学, etc)."""
import json

with open('data/scores.json', 'r') as f:
    scores = json.load(f)

def add_score(sid, province, year, category, score):
    if sid not in scores:
        scores[sid] = {}
    if province not in scores[sid]:
        scores[sid][province] = {}
    if year not in scores[sid][province]:
        scores[sid][province][year] = {}
    if category not in scores[sid][province][year]:
        scores[sid][province][year][category] = score
    elif score > scores[sid][province][year][category]:
        scores[sid][province][year][category] = score

# ============================================================
# 宁夏大学 (nxu) - from dakao100.com 2025 data
# ============================================================
nxu_data = {
    'ningxia': {'物理类': 492, '历史类': 523},
    'hebei': {'物理类': 570, '历史类': 581},
    'guangdong': {'物理类': 552, '历史类': 577},
    'tianjin': {'综合': 610},
    'shandong': {'综合': 538},
    'neimenggu': {'物理类': 585, '历史类': 597},
    'xinjiang': {'理科': 430},
}
for prov, cats in nxu_data.items():
    for cat, score in cats.items():
        add_score('nxu', prov, '2025', cat, score)

# ============================================================
# 石河子大学 (shihezi) - lower tier, estimate based on similar schools
# In xinjiang as local school it would have lower scores
# Skip - no reliable 2025 data found
# ============================================================

# ============================================================
# 西藏大学 (xbmu) - lowest tier 211
# Skip - no reliable 2025 data found
# ============================================================

# ============================================================
# Save
# ============================================================
with open('data/scores.json', 'w') as f:
    json.dump(scores, f, ensure_ascii=False, indent=2)

ids_211 = ['bjtu','bupt','bjkj','bhua','bjgydx','bfsu','blcu','cupl','cufe','uibe','cuc','buaa_med','xidian','nuaa','nust','hhu','jiangnan','suda','ecust','sufe','shanghai_intl','shu','dhu','nenu','dlmu','swjtu','swu','swufe','whut','ccnu','hzau','zuel','scnu','jnu','hunnu','snnu','nwu','chd','fzu','ncu','zzu','gxu','ynu','gzu','hainanu','imu','nxu','xju','shihezi','ybu','xbmu','qhu','hfut','ahu','nau','njnu','ttu','hebut','cup','cup_hz','cumt','cumtb','cug','cugb','tju_med','lnu']

has_2025 = set()
for s in ids_211:
    if s in scores:
        for prov, pdata in scores[s].items():
            if '2025' in pdata:
                has_2025.add(s)
                break

no_2025 = [s for s in ids_211 if s not in has_2025]
print(f"211 schools with 2025 data: {len(has_2025)}/{len(ids_211)}")
print(f"Still missing: {len(no_2025)}: {no_2025}")
