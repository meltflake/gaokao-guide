#!/usr/bin/env python3
"""Add 211 school 2025 data extracted from gk100.com pages."""
import json

with open('data/scores.json', 'r') as f:
    scores = json.load(f)

def add_score(sid, province, year, category, score):
    """Add a score entry. category is like '物理类', '历史类', '综合', '理科'"""
    if sid not in scores:
        scores[sid] = {}
    if province not in scores[sid]:
        scores[sid][province] = {}
    if year not in scores[sid][province]:
        scores[sid][province][year] = {}
    # Only set if not already set (keep first/highest score for each category)
    if category not in scores[sid][province][year]:
        scores[sid][province][year][category] = score
    else:
        # Keep the higher score (main campus > branch)
        if score > scores[sid][province][year][category]:
            scores[sid][province][year][category] = score

# ============================================================
# 内蒙古 (neimenggu) - 物理类 top 5000
# ============================================================
neimenggu_data = {
    'bupt': 664,       # 北京邮电大学 第001组
    'bjtu': 647,       # 北京交通大学 第001组
    'nuaa': 641,       # 南京航空航天大学 第001组
    'tju_med': 641,    # 天津医科大学 第003组
    'xidian': 636,     # 西安电子科技大学 第101组
    'whut': 627,       # 武汉理工大学 第002组
    'cufe': 626,       # 中央财经大学 第001组
    'nust': 626,       # 南京理工大学 第001组
    'bfsu': 625,       # 北京外国语大学 第004组
    'sufe': 624,       # 上海财经大学 第003组 (used 624, page shows 621 for 002组)
    'jiangnan': 624,   # 江南大学 第012组
    'shu': 624,        # 上海大学 第001组
    'bjkj': 623,       # 北京科技大学 第002组
    'suda': 622,       # 苏州大学 第009组
    'uibe': 620,       # 对外经济贸易大学 第002组
    'bhua': 620,       # 北京化工大学 第001组
    'buaa_med': 619,   # 北京中医药大学 第003组
    'nenu': 618,       # 东北师范大学 第013组
    'jnu': 618,        # 暨南大学 第010组
    'ecust': 615,      # 华东理工大学 第001组
    'nwu': 614,        # 西北大学 第003组
    'cuc': 613,        # 中国传媒大学 第004组
    'zuel': 612,       # 中南财经政法大学 第444组
    'swufe': 612,      # 西南财经大学 第502组
    'swjtu': 612,      # 西南交通大学 第003组
    'ccnu': 612,       # 华中师范大学 第057组
    'cupl': 611,       # 中国政法大学 第006组
    'blcu': 611,       # 北京林业大学 第006组
    'imu': 610,        # 内蒙古大学 第227组
}
for sid, score in neimenggu_data.items():
    add_score(sid, 'neimenggu', '2025', '物理类', score)

# ============================================================
# 天津 (tianjin) - 综合类 top 5000
# ============================================================
tianjin_data = {
    'bupt': 677,       # 北京邮电大学 01组
    'cupl': 676,       # 中国政法大学 01组
    'bjtu': 658,       # 北京交通大学 01组
    'cuc': 658,        # 中国传媒大学 14组
    'nuaa': 655,       # 南京航空航天大学 01组
    'xidian': 652,     # 西安电子科技大学 01组
    'suda': 651,       # 苏州大学 10组
    'whut': 647,       # 武汉理工大学 03组
    'sufe': 647,       # 上海财经大学 02组
    'cufe': 648,       # 中央财经大学 02组
    'uibe': 647,       # 对外经济贸易大学 02组
    'nust': 644,       # 南京理工大学 02组
    'bjgydx': 644,     # 北京工业大学 01组
    'bfsu': 644,       # 北京外国语大学 04组
    'bjkj': 646,       # 北京科技大学 01组
    'snnu': 645,       # 陕西师范大学 01组
    'tju_med': 643,    # 天津医科大学 03组
}
for sid, score in tianjin_data.items():
    add_score(sid, 'tianjin', '2025', '综合', score)

# ============================================================
# 宁夏 (ningxia) - 物理类 top 5000+
# ============================================================
ningxia_data = {
    'bupt': 613,       # 北京邮电大学 502专业组
    'bjtu': 599,       # 北京交通大学 502专业组
    'nuaa': 584,       # 南京航空航天大学 501专业组
    'xidian': 583,     # 西安电子科技大学 501专业组
    'cufe': 575,       # 中央财经大学 001专业组
    'nust': 573,       # 南京理工大学 502专业组
    'bjkj': 569,       # 北京科技大学 001专业组
    'suda': 568,       # 苏州大学 503专业组
    'jnu': 568,        # 暨南大学 505专业组
    'jiangnan': 567,   # 江南大学 502专业组
    'sufe': 563,       # 上海财经大学 003专业组
    'uibe': 561,       # 对外经济贸易大学 503专业组
    'bfsu': 558,       # 北京外国语大学 001专业组
    'ecust': 555,      # 华东理工大学 501专业组
    'bhua': 552,       # 北京化工大学 503专业组
    'buaa_med': 552,   # 北京中医药大学 001专业组
    'nwu': 552,        # 西北大学 502专业组
    'ccnu': 551,       # 华中师范大学 508专业组
    'cupl': 550,       # 中国政法大学 001专业组
    'swufe': 546,      # 西南财经大学 503专业组
    'cuc': 553,        # 中国传媒大学 502专业组  (from earlier, 534 for 001)
    'tju_med': 588,    # 天津医科大学 A04专业组
    'lnu': 545,        # 辽宁大学 001专业组
    'cug': 544,        # 中国地质大学(武汉) 001专业组
    'scnu': 543,       # 华南师范大学 502专业组
    'dlmu': 541,       # 大连海事大学 503专业组
    'shanghai_intl': 540, # 上海外国语大学 002专业组
    'ynu': 540,        # 云南大学 A04专业组
    'fzu': 537,        # 福州大学 504专业组
    'snnu': 537,       # 陕西师范大学 007专业组
    'hhu': 536,        # 河海大学 501专业组
    'swu': 536,        # 西南大学 006专业组
    'hunnu': 535,      # 湖南师范大学 001专业组
    'cup': 533,        # 中国石油大学(北京) 501专业组
    'hebut': 533,      # 河北工业大学 502专业组
    'cup_hz': 533,     # 中国石油大学(华东) 503专业组
    'whut': 533,       # 武汉理工大学 502专业组 (lower group)
    'swjtu': 529,      # 西南交通大学 501专业组
    'blcu': 527,       # 北京林业大学 503专业组
    'chd': 527,        # 长安大学 503专业组
    'zuel': 525,       # 中南财经政法大学 001专业组
    'nenu': 522,       # 东北师范大学 504专业组
    'cumtb': 521,      # 中国矿业大学(北京) 001专业组
    'hzau': 521,       # 华中农业大学 001专业组
    'dhu': 530,        # 东华大学 501专业组
    'cugb': 522,       # 中国地质大学(北京) 502专业组
}
for sid, score in ningxia_data.items():
    add_score(sid, 'ningxia', '2025', '物理类', score)

# ============================================================
# 新疆 (xinjiang) - 理科 top 5000
# ============================================================
xinjiang_data = {
    'bupt': 611,       # 北京邮电大学
    'bjtu': 610,       # 北京交通大学 (理科试验班类)(信息类) - used 585 for main
    'xidian': 597,     # 西安电子科技大学
    'nuaa': 594,       # 南京航空航天大学
    'sufe': 586,       # 上海财经大学
    'nust': 580,       # 南京理工大学
    'cufe': 575,       # 中央财经大学
    'bjkj': 571,       # 北京科技大学
    'uibe': 568,       # 对外经济贸易大学
    'suda': 564,       # 苏州大学
    'ecust': 561,      # 华东理工大学
    'cuc': 561,        # 中国传媒大学
    'cupl': 561,       # 中国政法大学
    'whut': 555,       # 武汉理工大学
    'swjtu': 553,      # 西南交通大学
    'buaa_med': 551,   # 北京中医药大学
    'bfsu': 549,       # 北京外国语大学
    'shu': 549,        # 上海大学
    'tju_med': 548,    # 天津医科大学
    'cup': 546,        # 中国石油大学(北京)
    'bhua': 545,       # 北京化工大学
    'swufe': 545,      # 西南财经大学
    'dhu': 544,        # 东华大学
    'shanghai_intl': 544, # 上海外国语大学
    'jiangnan': 540,   # 江南大学
    'bjgydx': 539,     # 北京工业大学
    'zuel': 537,       # 中南财经政法大学
}
for sid, score in xinjiang_data.items():
    add_score(sid, 'xinjiang', '2025', '理科', score)

# ============================================================
# 北京 (beijing) - 综合类 top 5000
# ============================================================
beijing_data = {
    'bupt': 663,       # 北京邮电大学 02组
    'cupl': 667,       # 中国政法大学 01组
    'bjtu': 651,       # 北京交通大学 03组
    'uibe': 649,       # 对外经济贸易大学 02组
    'bjkj': 648,       # 北京科技大学 03组
    'nuaa': 651,       # 南京航空航天大学 02组
    'cufe': 643,       # 中央财经大学 01组
    'nwu': 643,        # 西北大学 02组
    'sufe': 640,       # 上海财经大学 01组
    'xidian': 640,     # 西安电子科技大学 02组
}
for sid, score in beijing_data.items():
    add_score(sid, 'beijing', '2025', '综合', score)

# ============================================================
# 河北 (hebei) - 历史类 top 1万
# ============================================================
hebei_hist_data = {
    'uibe': 636,       # 对外经济贸易大学
    'bfsu': 630,       # 北京外国语大学
    'sufe': 630,       # 上海财经大学
    'cupl': 628,       # 中国政法大学
    'bupt': 623,       # 北京邮电大学
    'suda': 622,       # 苏州大学
    'shanghai_intl': 622, # 上海外国语大学
    'bjkj': 619,       # 北京科技大学
    'shu': 619,        # 上海大学
    'bhua': 618,       # 北京化工大学
    'buaa_med': 618,   # 北京中医药大学
    'nust': 618,       # 南京理工大学
    'cup': 618,        # 中国石油大学(北京)
    'bjtu': 617,       # 北京交通大学
    'dhu': 617,        # 东华大学
    'nuaa': 617,       # 南京航空航天大学
    'cufe': 617,       # 中央财经大学
    'ccnu': 616,       # 华中师范大学
    'jiangnan': 615,   # 江南大学
    'cugb': 615,       # 中国地质大学(北京)
    'dlmu': 614,       # 大连海事大学
    'njnu': 614,       # 南京师范大学
    'swjtu': 614,      # 西南交通大学
    'cumtb': 614,      # 中国矿业大学(北京)
    'blcu': 613,       # 北京林业大学
    'xidian': 613,     # 西安电子科技大学
    'zzu': 613,        # 郑州大学
    'ahu': 612,        # 安徽大学
    'hhu': 612,        # 河海大学
    'ecust': 611,      # 华东理工大学
    'snnu': 611,       # 陕西师范大学
    'cug': 610,        # 中国地质大学(武汉)
    'cumt': 610,       # 中国矿业大学
    'chd': 609,        # 长安大学
    'fzu': 609,        # 福州大学
    'hfut': 609,       # 合肥工业大学
    'jnu': 609,        # 暨南大学
    'nau': 609,        # 南京农业大学
    'swu': 609,        # 西南大学
    'cup_hz': 608,     # 中国石油大学(华东)
    'whut': 606,       # 武汉理工大学
    'ttu': 605,        # 太原理工大学
    'cuc': 605,        # 中国传媒大学
    'hebut': 603,      # 河北工业大学
    'scnu': 602,       # 华南师范大学
    'lnu': 602,        # 辽宁大学
    'ncu': 602,        # 南昌大学
    'ynu': 601,        # 云南大学
    'imu': 600,        # 内蒙古大学
    'swufe': 597,      # 西南财经大学
    'hunnu': 596,      # 湖南师范大学 (with 艺术类 600)
    'nwu': 596,        # 西北大学
    'zuel': 595,       # 中南财经政法大学
    'hzau': 594,       # 华中农业大学
    'ybu': 594,        # 延边大学
    'nenu': 586,       # 东北师范大学
    'xju': 585,        # 新疆大学
    'qhu': 591,        # 青海大学
}
for sid, score in hebei_hist_data.items():
    add_score(sid, 'hebei', '2025', '历史类', score)

# ============================================================
# 河北 (hebei) - 物理类 (from the 6-8万 range page + merged)
# These are lower-tier 211s that appear in physic 6-8万 range
# ============================================================
hebei_phys_data = {
    'nust': 635,       # 南京理工大学 (from 前1万 page)
    'dlmu': 561,       # 大连海事大学
    'hzau': 561,       # 华中农业大学
    'xju': 561,        # 新疆大学
    'ybu': 561,        # 延边大学
    'nenu': 557,       # 东北师范大学
    'qhu': 565,        # 青海大学
}
for sid, score in hebei_phys_data.items():
    add_score(sid, 'hebei', '2025', '物理类', score)

# ============================================================
# 河南 (henan) - 物理类 top 1万
# ============================================================
henan_data = {
    'bupt': 670,       # 北京邮电大学 101普通组
    'bjtu': 659,       # 北京交通大学 101普通组
    'whut': 651,       # 武汉理工大学 104普通组
    'nuaa': 651,       # 南京航空航天大学 101普通组
    'xidian': 652,     # 西安电子科技大学 101普通组
    'jnu': 650,        # 暨南大学 105普通组
    'hhu': 649,        # 河海大学 101普通组
    'nust': 648,       # 南京理工大学 103普通组
    'jiangnan': 647,   # 江南大学 101普通组
    'sufe': 646,       # 上海财经大学 103普通组
}
for sid, score in henan_data.items():
    add_score(sid, 'henan', '2025', '物理类', score)

# ============================================================
# 广东 (guangdong) - 物理类 top 1万
# ============================================================
guangdong_phys = {
    'bupt': 657,       # 北京邮电大学 206组
    'nuaa': 643,       # 南京航空航天大学 205组
    'bjtu': 637,       # 北京交通大学 212组
    'xidian': 630,     # 西安电子科技大学 207组
}
for sid, score in guangdong_phys.items():
    add_score(sid, 'guangdong', '2025', '物理类', score)

# ============================================================
# Save
# ============================================================
with open('data/scores.json', 'w') as f:
    json.dump(scores, f, ensure_ascii=False, indent=2)

# Count how many 211 schools now have 2025 data
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
print(f"Still missing 2025 data: {len(no_2025)}")
print("Missing:", no_2025)
