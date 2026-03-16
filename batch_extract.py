#!/usr/bin/env python3
"""Parse gk100.com fetched text and extract scores for schools in schools.json"""
import json
import re
import sys
import os

def load_data():
    with open('data/schools.json') as f:
        schools = json.load(f)
    with open('data/scores.json') as f:
        scores = json.load(f)
    
    # Build name -> id mapping
    name_to_id = {}
    for s in schools:
        name = s['name']
        sid = s['id']
        name_to_id[name] = sid
    
    return schools, scores, name_to_id

def parse_gk100_table(text, name_to_id):
    """Parse gk100 format: school name, group, score, rank in table"""
    results = {}  # sid -> (score, rank)
    
    lines = text.split('\n')
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        
        # Check if this line contains a school name we're looking for
        matched_name = None
        matched_sid = None
        
        for name, sid in name_to_id.items():
            if name in line:
                # Make sure it's not a substring of another school
                # e.g. "四川大学" should not match "四川大学(锦江学院)"
                # But "哈尔滨工业大学(深圳)" should match
                idx = line.find(name)
                # Check the character after the name
                after_idx = idx + len(name)
                if after_idx < len(line):
                    next_char = line[after_idx]
                    # If followed by Chinese characters that are NOT parentheses, skip
                    if next_char not in '(\uff08 \t\n' and ord(next_char) > 127 and next_char not in '第组':
                        continue
                
                if matched_name is None or len(name) > len(matched_name):
                    matched_name = name
                    matched_sid = sid
        
        if matched_name and matched_sid:
            # Look for score in this line and nearby lines
            # Score is typically a 3-digit number between 350-750
            search_text = line
            # Also check next few lines (table rows might span)
            for j in range(1, 5):
                if i + j < len(lines):
                    search_text += ' ' + lines[i + j].strip()
            
            numbers = re.findall(r'\b(\d{3,4})\b', search_text)
            scores_found = []
            ranks_found = []
            
            for n in numbers:
                val = int(n)
                if 350 <= val <= 750:
                    scores_found.append(val)
                elif 10 <= val <= 9999:
                    ranks_found.append(val)
            
            if scores_found:
                # Take the highest score for this school (first occurrence is usually correct)
                score = scores_found[0]
                
                # Only update if we don't have this school yet, or if new score is higher
                if matched_sid not in results or score > results[matched_sid][0]:
                    results[matched_sid] = (score, matched_name)
        
        i += 1
    
    return results

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 batch_extract.py <text_file> <province_key> [score_type]")
        print("  province_key: e.g., neimenggu, tianjin, beijing, etc.")
        print("  score_type: e.g., 物理类, 综合, 理科 (default: 物理类)")
        sys.exit(1)
    
    text_file = sys.argv[1]
    province_key = sys.argv[2]
    score_type = sys.argv[3] if len(sys.argv) > 3 else '物理类'
    
    schools, scores, name_to_id = load_data()
    
    with open(text_file) as f:
        text = f.read()
    
    results = parse_gk100_table(text, name_to_id)
    
    updated = 0
    already_have = 0
    new_schools = []
    
    for sid, (score, name) in sorted(results.items(), key=lambda x: x[1][0], reverse=True):
        if sid not in scores:
            scores[sid] = {}
        if province_key not in scores[sid]:
            scores[sid][province_key] = {}
        
        if '2025' in scores[sid][province_key] and score_type in scores[sid][province_key]['2025']:
            already_have += 1
            continue
        
        if '2025' not in scores[sid][province_key]:
            scores[sid][province_key]['2025'] = {}
        
        scores[sid][province_key]['2025'][score_type] = score
        updated += 1
        new_schools.append(f"  {name} ({sid}) = {score}")
    
    print(f"\nProvince: {province_key}, Type: {score_type}")
    print(f"Total matched: {len(results)}, New: {updated}, Already had: {already_have}")
    
    if new_schools:
        print("\nNewly added:")
        for s in new_schools:
            print(s)
    
    if updated > 0:
        with open('data/scores.json', 'w') as f:
            json.dump(scores, f, ensure_ascii=False, indent=2)
        print(f"\nSaved {updated} new entries to scores.json")

if __name__ == '__main__':
    main()
