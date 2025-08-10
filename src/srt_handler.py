# -*- coding: utf-8 -*-

"""
Handles parsing and writing of SRT (SubRip Text) files.
"""

from .utils import cprint, Colors

def parse_srt(file_path):
    """
    Parses an SRT file and returns a list of subtitle blocks.
    Each block is a dictionary containing index, timestamp, and text.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        blocks = content.strip().split('\n\n')
        parsed_blocks = []
        for block in blocks:
            lines = block.split('\n')
            if len(lines) >= 3:
                parsed_blocks.append({
                    'index': lines[0],
                    'timestamp': lines[1],
                    'text': '\n'.join(lines[2:])
                })
        return parsed_blocks
    except FileNotFoundError:
        cprint(Colors.FAIL, f"Error: Could not find SRT file to parse at '{file_path}'")
        return []
    except Exception as e:
        cprint(Colors.FAIL, f"An error occurred while parsing the SRT file: {e}")
        return []

def write_srt_block(file_handle, block, translated_text):
    """Writes a single translated subtitle block to the output file."""
    file_handle.write(f"{block['index']}\n")
    file_handle.write(f"{block['timestamp']}\n")
    file_handle.write(f"{translated_text}\n\n")

