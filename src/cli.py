# -*- coding: utf-8 -*-

"""
Command-line interface setup for the v2srt application.
"""

import argparse
import os
from pathlib import Path
from .config import Config
from .utils import Colors

def setup_arg_parser():
    """
    Initializes and configures the argument parser for the command-line interface.
    """
    parser = argparse.ArgumentParser(
        description=f"{Colors.BOLD}v2srt: Transcribe and Translate Subtitles.{Colors.ENDC}",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=f"""
{Colors.BOLD}Examples:{Colors.ENDC}
  {Colors.INFO}# Translate an existing Japanese SRT file to Chinese{Colors.ENDC}
  python -m src.main -i subtitles.srt -il ja -ol zh-cn

  {Colors.INFO}# Transcribe a video, then translate the resulting SRT file{Colors.ENDC}
  python -m src.main -v video.mp4 -ol zh-cn

  {Colors.INFO}# Transcribe and translate, specifying a different Whisper model and batch size{Colors.ENDC}
  python -m src.main -v video.mp4 -ol en -wm small -b 5

  {Colors.INFO}# Use 10 parallel threads for faster translation{Colors.ENDC}
  python -m src.main -v video.mp4 -ol zh-cn -c 10
"""
    )
    io_group = parser.add_argument_group(f"{Colors.BOLD}Input/Output{Colors.ENDC}")
    lang_group = parser.add_argument_group(f"{Colors.BOLD}Language & Model{Colors.ENDC}")
    api_group = parser.add_argument_group(f"{Colors.BOLD}API & Performance{Colors.ENDC}")
    misc_group = parser.add_argument_group(f"{Colors.BOLD}Miscellaneous{Colors.ENDC}")

    input_group = io_group.add_mutually_exclusive_group(required=True)
    input_group.add_argument('-i', '--input-srt', type=Path, metavar="<file>", help="Path to an existing SRT file to translate.")
    input_group.add_argument('-v', '--input-video', type=Path, metavar="<file>", help="Path to a video file to transcribe and then translate.")
    input_group.add_argument('-a', '--input-audio', type=Path, metavar="<file>", help="Path to an audio file to transcribe and then translate.")
    io_group.add_argument('-o', '--output-srt', type=Path, metavar="<file>", help="Path to save the generated (untranslated) SRT file from transcription.")
    io_group.add_argument('-ot', '--output-translated', type=Path, metavar="<file>", help="Path to save the final translated SRT file.")

    lang_group.add_argument('-il', '--input-lang', type=str, default=Config.DEFAULT_INPUT_LANG, metavar="<code>", help=f"Input language code (e.g., 'en', 'ja'). Default: {Config.DEFAULT_INPUT_LANG}")
    lang_group.add_argument('-ol', '--output-lang', type=str, default=Config.DEFAULT_OUTPUT_LANG, metavar="<code>", help=f"Output language code (e.g., 'en', 'zh-cn'). Default: {Config.DEFAULT_OUTPUT_LANG}")
    lang_group.add_argument('-m', '--model', type=str, default=Config.DEFAULT_MODEL, metavar="<name>", help=f"Translation model to use. Default: {Config.DEFAULT_MODEL}")
    lang_group.add_argument('-wm', '--whisper-model', type=str, default=Config.DEFAULT_WHISPER_MODEL, choices=['tiny', 'base', 'small', 'medium', 'large', 'large-v2', 'large-v3'], help=f"Whisper model for transcription. Default: {Config.DEFAULT_WHISPER_MODEL}")

    api_group.add_argument('-k', '--api-key', type=str, default=os.getenv('XAI_API_KEY'), metavar="<key>", help="Your translation API key. Defaults to XAI_API_KEY env var.")
    api_group.add_argument('-b', '--batch-size', type=int, default=Config.DEFAULT_BATCH_SIZE, metavar="<N>", help=f"Number of subtitles to send in each API request. Default: {Config.DEFAULT_BATCH_SIZE}")
    api_group.add_argument('-c', '--concurrency', type=int, default=Config.DEFAULT_CONCURRENCY, metavar="<N>", help=f"Number of parallel API requests to make. Default: {Config.DEFAULT_CONCURRENCY}")
    api_group.add_argument('-s', '--separator', type=str, default=Config.DEFAULT_SEPARATOR, metavar="<str>", help=f"Unique separator for batching subtitles. Default: '{Config.DEFAULT_SEPARATOR}'")

    misc_group.add_argument('-d', '--debug', action='store_true', help="Enable debug mode for verbose request/response logging.")
    misc_group.add_argument('--version', action='version', version='%(prog)s 2.3')
    
    return parser
