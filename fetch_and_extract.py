#!/usr/bin/env python3
"""
Fetch gk100.com pages and extract scores for schools in schools.json.
Usage: python3 fetch_and_extract.py
Reads page content from tmp/ directory files.
"""
import json
import re

def load_data():
    with open('data/schools.json') as f:
        schools = json.load(f)
    with open('data/scores.json') as f:
        scores = json.load(f)
    
    name_to_id = {}
    id_to_name = {}
    for s in schools:
        name_to_id[s['name']] = s['id']
        id_to_name[s['id']] = s['name']
    
    return schools, scores, name_to_id, id_to_name

def extract_from_text(text, name_to_id):
    """Extract school->score mappings from gk100 page text"""
    results = {}  # sid -> (score, name)
    
    lines = text.split('\n')
    
    # Sort names by length (longest first) to prefer more specific matches
    sorted_names = sorted(name_to_id.keys(), key=len, reverse=True)
    
    for i, line in enumerate(lines):
        line_stripped = line.strip()
        if not line_stripped:
            continue
        
        for name in sorted_names:
            sid = name_to_id[name]
            if sid in results:
                continue  # Already found this school
            
            if name not in line_stripped:
                continue
            
            # Verify it's a standalone match (not part of a longer name)
            idx = line_stripped.find(name)
            after = idx + len(name)
            
            # Check if this is a sub-match of a longer school name we care about
            # e.g., "四川大学" inside "四川大学锦城学院"
            # Allow parenthetical suffixes like (深圳), (威海)
            if after < len(line_stripped):
                next_char = line_stripped[after]
                # Skip if followed by typical college/branch suffixes
                skip_suffixes = ['锦城', '锦江', '华西', '珠海学院']
                remaining = line_stripped[after:]
                if any(remaining.startswith(s) for s in skip_suffixes):
                    continue
            
            # Get context: current line + next 4 lines
            context = line_stripped
            for j in range(1, 5):
                if i + j < len(lines):
                    context += ' ' + lines[i + j].strip()
            
            # Find scores (3-digit numbers in reasonable range)
            numbers = re.findall(r'\b(\d{3})\b', context)
            valid_scores = [int(n) for n in numbers if 350 <= int(n) <= 750]
            
            if valid_scores:
                # For gk100 format, scores appear in order: score, rank
                # Take the first valid score
                score = valid_scores[0]
                results[sid] = (score, name)
    
    return results

def update_scores(scores, results, province_key, score_type):
    """Update scores dict with new results"""
    updated = 0
    new_entries = []
    
    for sid, (score, name) in sorted(results.items(), key=lambda x: x[1][0], reverse=True):
        if sid not in scores:
            scores[sid] = {}
        if province_key not in scores[sid]:
            scores[sid][province_key] = {}
        
        # Check if we already have 2025 data for this score_type
        if '2025' in scores[sid][province_key] and score_type in scores[sid][province_key].get('2025', {}):
            continue
        
        if '2025' not in scores[sid][province_key]:
            scores[sid][province_key]['2025'] = {}
        
        scores[sid][province_key]['2025'][score_type] = score
        updated += 1
        new_entries.append((name, sid, score))
    
    return updated, new_entries

def process_file(filepath, province_key, score_type, scores, name_to_id):
    """Process a single fetched text file"""
    with open(filepath) as f:
        text = f.read()
    
    results = extract_from_text(text, name_to_id)
    updated, new_entries = update_scores(scores, results, province_key, score_type)
    
    print(f"\n[{province_key}] ({score_type})")
    print(f"  Matched: {len(results)}, New entries: {updated}")
    if new_entries:
        for name, sid, score in new_entries:
            print(f"    + {name} ({sid}) = {score}")
    
    return updated

def main():
    schools, scores, name_to_id, id_to_name = load_data()
    
    total_updated = 0
    
    # Process files from tmp/ directory
    import os
    import glob
    
    files = sorted(glob.glob('tmp/*.txt'))
    
    for filepath in files:
        basename = os.path.basename(filepath)
        # Expected format: province_scoretype.txt
        # e.g., neimenggu_wulilei.txt, tianjin_zonghe.txt
        parts = basename.replace('.txt', '').split('_', 1)
        province_key = parts[0]
        score_type_map = {
            'wulilei': '物理类',
            'zonghe': '综合',
            'like': '理科',
            'lishilei': '历史类',
        }
        score_type = score_type_map.get(parts[1], '物理类') if len(parts) > 1 else '物理类'
        
        total_updated += process_file(filepath, province_key, score_type, scores, name_to_id)
    
    if total_updated > 0:
        with open('data/scores.json', 'w') as f:
            json.dump(scores, f, ensure_ascii=False, indent=2)
        print(f"\n=== Total updated: {total_updated} entries ===")
        print("Saved to data/scores.json")
    else:
        print("\nNo new entries to add.")
    
    # Show remaining schools without data
    school_ids = {s['id'] for s in schools}
    has_data = {sid for sid in scores if sid in school_ids and any('2025' in scores[sid].get(p, {}) for p in scores[sid])}
    no_data = school_ids - has_data
    print(f"\nSchools with 2025 data: {len(has_data)}/{len(school_ids)}")
    print(f"Still missing: {len(no_data)}")

if __name__ == '__main__':
    main()
