import pandas as pd
import re

def load_questions_from_csv(csv_path, question_col = 'Question', pages_col = 'Pages',max_page = 358):
    df = pd.read_csv(csv_path, dtype=str)

    results = []
    for _, row in df.iterrows():
        q = str(row.get(question_col, '')).strip()
        pages_raw = str(row.get(pages_col, '')).strip()
        if not q or not pages_raw:
            continue
        
        nums = re.findall(r'\b\d{1,3}\b', pages_raw)
        pages = [int(n) for n in nums if 1 <= int(n) <= max_page]

        if pages:
            results.append((q, pages))

    return results