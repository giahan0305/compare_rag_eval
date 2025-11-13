#!/usr/bin/env python3
"""
Convert results_multi.json to the CSV format required by open-rag-eval toolkit.
"""

import json
import csv

def convert_json_to_csv(json_file, csv_file):
    """Convert results_multi.json to CSV format for evaluation."""
    
    # Read the JSON file
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Prepare CSV rows
    csv_rows = []
    
    for result in data['results']:
        testcase_id = result['testcase_id']
        question = result['question']
        generated_answer = result['actual_output']
        
        # Extract context/sources
        sources = result.get('sources', [])
        
        # If there are sources, create one row per source
        if sources:
            for idx, source in enumerate(sources, start=1):
                row = {
                    'query_id': testcase_id,
                    'query': question,
                    'query_run': 1,  # Default to 1 as there's only one run per query
                    'passage_id': f"[{idx}]",
                    'passage': source.get('content', ''),
                    'generated_answer': generated_answer if idx == 1 else ''  # Only include answer in first row
                }
                csv_rows.append(row)
        else:
            # If no sources, create a single row with empty passage
            row = {
                'query_id': testcase_id,
                'query': question,
                'query_run': 1,
                'passage_id': '[1]',
                'passage': '',
                'generated_answer': generated_answer
            }
            csv_rows.append(row)
    
    # Write to CSV
    fieldnames = ['query_id', 'query', 'query_run', 'passage_id', 'passage', 'generated_answer']
    
    with open(csv_file, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_rows)
    
    print(f"✅ Converted {len(data['results'])} queries to {csv_file}")
    print(f"   Total rows: {len(csv_rows)}")
