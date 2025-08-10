# -*- coding: utf-8 -*-

"""
Handles audio/video transcription using the Whisper CLI tool.
"""

import os
import subprocess
from .utils import cprint, Colors
from .config import LANG_MAP

def run_whisper(input_file, output_srt_path, whisper_model, input_lang, debug=False):
    """
    Executes the Whisper command-line tool to transcribe a media file.
    
    Returns the path to the generated SRT file on success, or None on failure.
    """
    cprint(Colors.INFO, f"\nRunning Whisper on '{input_file}'...")
    
    language = LANG_MAP.get(input_lang, input_lang)
    
    command = [
        'whisper', str(input_file),
        '--model', whisper_model,
        '--language', language,
        '--output_format', 'srt',
        '--output_dir', str(output_srt_path.parent)
    ]
    
    # Whisper by default creates a file with the same name as input + .srt
    expected_whisper_output = input_file.with_suffix('.srt')

    if debug:
        cprint(Colors.WARNING, f"Debug: Executing command: {' '.join(command)}")

    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8')
        
        # Print Whisper's output in real-time
        for line in iter(process.stdout.readline, ''):
            print(line.strip())
        
        process.wait()

        if process.returncode != 0:
            cprint(Colors.FAIL, f"Whisper command failed with exit code {process.returncode}.")
            return None

        # If whisper created the file with a different name, rename it
        if expected_whisper_output.exists() and expected_whisper_output != output_srt_path:
             os.rename(expected_whisper_output, output_srt_path)
        
        if not output_srt_path.exists():
             cprint(Colors.FAIL, f"Error: Whisper seemed to succeed, but the output file '{output_srt_path}' was not found.")
             return None

        cprint(Colors.OKGREEN, f"Successfully generated SRT file: '{output_srt_path}'")
        return output_srt_path

    except FileNotFoundError:
        cprint(Colors.FAIL, "Error: 'whisper' command not found. Please ensure it's installed and in your PATH.")
        return None
    except Exception as e:
        cprint(Colors.FAIL, f"An unexpected error occurred while running Whisper: {e}")
        return None
