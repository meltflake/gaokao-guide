#!/usr/bin/env python3
"""Process fetched gk100 page text and extract scores for schools in schools.json"""
import json
import re
import sys

def load_data():
    with open('data/schools.json') as f:
        schools = json.load(f)
    with open('data/scores.json') as f:
        scores = json.load(f)
    
    name_to_id = {}
    for s in schools:
        name_to_id[s['name']] = s['id']
    
    return schools, scores, name_to_id

def extract_scores(text, name_to_id):
    """Extract school->score from text"""
    results = {}
    
    # Sort by name length descending for longest match first
    sorted_names = sorted(name_to_id.keys(), key=len, reverse=True)
    
    lines = text.split('\n')
    
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        
        for name in sorted_names:
            sid = name_to_id[name]
            if sid in results:
                continue
            
            if name not in line:
                continue
            
            # Skip if it's part of a different school name
            # e.g. "湖北大学" shouldn't match inside "湖北大学知行学院"
            idx = line.find(name)
            after = idx + len(name)
            if after < len(line):
                rest = line[after:]
                # Skip independent college suffixes
                bad_suffixes = ['知行', '锦城', '锦江', '文理学院', '城市学院', '珠海学院', '(珠海校区)', '学院', '附属']
                if any(rest.startswith(s) for s in bad_suffixes):
                    # But allow "(深圳)", "(威海)", "(保定)" etc that are in our schools.json
                    if not any(f'({loc})' in name for loc in ['深圳', '威海', '保定', '华东', '武汉', '北京']):
                        continue
            
            # Get context for number extraction
            context_lines = [line]
            for j in range(1, 6):
                if i + j < len(lines):
                    context_lines.append(lines[i + j].strip())
            context = ' '.join(context_lines)
            
            # Find 3-digit numbers
            numbers = re.findall(r'\b(\d{3})\b', context)
            valid = [int(n) for n in numbers if 350 <= int(n) <= 750]
            
            if valid:
                results[sid] = (valid[0], name)
    
    return results

def update_scores(scores, results, province, score_type):
    """Update scores.json with new results"""
    new_count = 0
    
    for sid, (score, name) in results.items():
        if sid not in scores:
            scores[sid] = {}
        if province not in scores[sid]:
            scores[sid][province] = {}
        if '2025' not in scores[sid][province]:
            scores[sid][province]['2025'] = {}
        
        if score_type not in scores[sid][province]['2025']:
            scores[sid][province]['2025'][score_type] = score
            new_count += 1
            print(f"  + {name} ({sid}) [{province}] = {score} ({score_type})")
    
    return new_count

def main():
    """Process a text file. Usage: python3 process_pages.py <file> <province> <score_type>"""
    if len(sys.argv) < 4:
        print("Usage: python3 process_pages.py <file> <province> <score_type>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    province = sys.argv[2]
    score_type = sys.argv[3]
    
    schools, scores, name_to_id = load_data()
    
    with open(filepath) as f:
        text = f.read()
    
    results = extract_scores(text, name_to_id)
    new_count = update_scores(scores, results, province, score_type)
    
    print(f"\nMatched: {len(results)}, New: {new_count}")
    
    if new_count > 0:
        with open('data/scores.json', 'w') as f:
            json.dump(scores, f, ensure_ascii=False, indent=2)
        print("Saved!")

if __name__ == '__main__':
    main()
