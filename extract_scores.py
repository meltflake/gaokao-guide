#!/usr/bin/env python3
"""Extract 2025 scores from gk100.com pages for all schools in schools.json"""
import json
import re
import sys

def load_data():
    with open('data/schools.json') as f:
        schools = json.load(f)
    with open('data/scores.json') as f:
        scores = json.load(f)
    # Build name -> id mapping with various name forms
    name_to_id = {}
    for s in schools:
        name = s['name']
        sid = s['id']
        name_to_id[name] = sid
        # Also add without parentheses content variations
        # e.g. "哈尔滨工业大学(深圳)" -> try matching
    return schools, scores, name_to_id

def extract_scores_from_text(text, name_to_id, province_key, score_type):
    """Extract school scores from fetched text content.
    Returns dict of {school_id: score}
    """
    results = {}
    
    # Try to find score patterns - typically in table format
    # Common patterns:
    # 1. "学校名 ... 分数" in table rows
    # 2. "学校名\t分数" or similar
    
    lines = text.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Try to match any school name in this line
        for name, sid in name_to_id.items():
            if name in line:
                # Try to extract a score (3-digit number, typically 400-700+)
                # Look for numbers in the line
                numbers = re.findall(r'\b(\d{3})\b', line)
                if numbers:
                    # Filter for reasonable score range
                    valid_scores = [int(n) for n in numbers if 350 <= int(n) <= 750]
                    if valid_scores:
                        # Take the first reasonable score (usually the min/投档线)
                        score = valid_scores[0]
                        results[sid] = score
                        print(f"  Found: {name} ({sid}) = {score}")
    
    return results

def main():
    schools, scores, name_to_id = load_data()
    
    # Read extracted text from stdin or file
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            text = f.read()
    else:
        text = sys.stdin.read()
    
    # Province and score type from args
    province_key = sys.argv[2] if len(sys.argv) > 2 else 'test'
    score_type = sys.argv[3] if len(sys.argv) > 3 else '物理类'
    
    results = extract_scores_from_text(text, name_to_id, province_key, score_type)
    
    # Update scores
    updated = 0
    for sid, score in results.items():
        if sid not in scores:
            scores[sid] = {}
        if province_key not in scores[sid]:
            scores[sid][province_key] = {}
        if '2025' not in scores[sid][province_key]:
            scores[sid][province_key]['2025'] = {}
            scores[sid][province_key]['2025'][score_type] = score
            updated += 1
        elif score_type not in scores[sid][province_key]['2025']:
            scores[sid][province_key]['2025'][score_type] = score
            updated += 1
    
    print(f"\nTotal found: {len(results)}, Updated: {updated}")
    
    if updated > 0:
        with open('data/scores.json', 'w') as f:
            json.dump(scores, f, ensure_ascii=False, indent=2)
        print("Saved to scores.json")

if __name__ == '__main__':
    main()
