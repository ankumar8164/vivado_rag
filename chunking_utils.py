import re
from langchain.text_splitter import RecursiveCharacterTextSplitter

def remove_headings_and_footer(md_text, heading_patterns=None, footer_pattern = r'^UG\d+'):
    """
    - Drops any line matching one of the heading_patterns.
    - Stops (and drops) everything from the first line matching footer_pattern onward.
    """
    if heading_patterns is None:
        heading_patterns = [
            r'^#{1,6}\s',
            r'^\*Chapter\s',
            r'^###\s',
            r'^#####\s',
            r'^\*\*.*\*\*$',
        ]
    heading_re = re.compile('|'.join(heading_patterns))
    footer_re  = re.compile(footer_pattern)

    out_lines = []
    for line in md_text.splitlines():
        stripped = line.strip()
        if footer_re.match(stripped):
            break
        if heading_re.match(stripped):
            continue
        out_lines.append(line)

    return "\n".join(out_lines)


def chunk_markdown(md_text, chunk_size = 500, chunk_overlap = 100):
    """
    1) Cleans out headings & footers
    2) Splits into overlapping chunks via LangChain
    """
    cleaned = remove_headings_and_footer(md_text)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return splitter.split_text(cleaned)

def remove_markdown_tables(md_text):
    """
    Removes any contiguous block of lines that look like a Markdown table.
    """
    lines = md_text.splitlines()
    filtered = []
    i = 0
    while i < len(lines):
        if '|' in lines[i] and re.match(r'^\s*\|?.*\|\s*$', lines[i]):
            # look for a separator line next
            if i + 1 < len(lines) and re.match(r'^\s*\|?[-\s|:]+\|[-\s|:]+\|?\s*$', lines[i+1]):
                # skip header + separator
                i += 2
                # skip table rows
                while i < len(lines) and '|' in lines[i]:
                    i += 1
                continue
        filtered.append(lines[i])
        i += 1
    return "\n".join(filtered)