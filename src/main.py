#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
v2str: Automated Subtitle Translation (Refactored)

This is the main entry point for the v2str application. It orchestrates
the process of transcription and translation based on user commands.
"""

import time
from concurrent.futures import ThreadPoolExecutor

from .cli import setup_arg_parser
from .config import LANG_MAP
from .srt_handler import parse_srt, write_srt_block
from .transcription import run_whisper
from .translation import Translator
from .utils import cprint, Colors, TQDM_AVAILABLE

if TQDM_AVAILABLE:
    from tqdm import tqdm

class V2SrtProcessor:
    """
    Orchestrates the transcription and translation workflow.
    """
    def __init__(self, args):
        self.args = args
        self.translator = Translator(args)
        self.source_srt_path = None
        self.translated_srt_path = None
        self.total_input_tokens = 0
        self.total_output_tokens = 0

    def run(self):
        """
        Executes the main logic of the application.
        """
        cprint(Colors.BOLD, "Starting v2str process...")
        
        if not self._determine_paths():
            return

        cprint(Colors.INFO, f"\nSource SRT: '{self.source_srt_path}'")
        cprint(Colors.INFO, f"Translated output: '{self.translated_srt_path}'")
        
        all_blocks = parse_srt(self.source_srt_path)
        if not all_blocks:
            cprint(Colors.FAIL, "No subtitle blocks found in the source file. Exiting.")
            return

        self._translate_and_write_srt(all_blocks)
        
        cprint(Colors.OKGREEN, f"\n{Colors.BOLD}Batch SRT translation complete. Output saved to '{self.translated_srt_path}'")
        
        self._print_token_summary()

    def _determine_paths(self):
        """
        Determines the source and destination paths for SRT files.
        If input is a media file, it runs transcription first.
        """
        media_file = self.args.input_video or self.args.input_audio

        if self.args.input_srt:
            if not self.args.input_srt.is_file():
                cprint(Colors.FAIL, f"Error: Input SRT file not found at '{self.args.input_srt}'")
                return False
            self.source_srt_path = self.args.input_srt
        elif media_file:
            if not media_file.is_file():
                cprint(Colors.FAIL, f"Error: Input media file not found at '{media_file}'")
                return False
            
            output_srt_path = self.args.output_srt or media_file.with_suffix('.srt')
            self.source_srt_path = run_whisper(
                media_file, 
                output_srt_path, 
                self.args.whisper_model, 
                self.args.input_lang,
                self.args.debug
            )
            if not self.source_srt_path:
                cprint(Colors.FAIL, "Exiting due to Whisper failure.")
                return False
        
        self.translated_srt_path = self.args.output_translated or \
            self.source_srt_path.with_suffix(f'.tr{self.source_srt_path.suffix}')
            
        return True

    def _translate_and_write_srt(self, all_blocks):
        """
        Manages the batching, concurrent translation, and writing of results.
        """
        from_lang_name = LANG_MAP.get(self.args.input_lang, self.args.input_lang)
        to_lang_name = LANG_MAP.get(self.args.output_lang, self.args.output_lang)
        cprint(Colors.INFO, f"\nTranslating {len(all_blocks)} subtitles from {from_lang_name} to {to_lang_name}...")
        cprint(Colors.INFO, f"Using model '{self.args.model}' with a concurrency of {self.args.concurrency}.")

        batches = [all_blocks[i:i + self.args.batch_size] for i in range(0, len(all_blocks), self.args.batch_size)]
        text_batches_with_indices = [(i + 1, [block['text'] for block in batch]) for i, batch in enumerate(batches)]
        
        progress_bar = None
        if TQDM_AVAILABLE:
            progress_bar = tqdm(total=len(batches), desc="Translating Batches", unit="batch")

        with open(self.translated_srt_path, 'w', encoding='utf-8') as outfile:
            with ThreadPoolExecutor(max_workers=self.args.concurrency) as executor:
                future_translations = executor.map(self.translator.translate_batch, text_batches_with_indices)
                
                for i, result_data in enumerate(future_translations):
                    translated_texts = result_data['translations']
                    self.total_input_tokens += result_data['input_tokens']
                    self.total_output_tokens += result_data['output_tokens']
                    
                    original_batch_blocks = batches[i]
                    
                    if len(translated_texts) == len(original_batch_blocks):
                        for block, translated_text in zip(original_batch_blocks, translated_texts):
                            write_srt_block(outfile, block, translated_text)
                    else:
                        cprint(Colors.FAIL, "Error: Mismatch in batch sizes. Writing error messages.")
                        for block in original_batch_blocks:
                            write_srt_block(outfile, block, f"---TRANSLATION_ERROR---\n{block['text']}")
                    
                    outfile.flush()
                    
                    token_info = f" | Tokens (In: {result_data['input_tokens']:,}, Out: {result_data['output_tokens']:,})"
                    
                    if progress_bar:
                        progress_bar.set_postfix_str(token_info)
                        progress_bar.update(1)
                    else:
                        cprint(Colors.INFO, f"Completed batch {i+1}/{len(batches)}{token_info}")

                    # A small delay might still be useful in concurrent mode to avoid overwhelming APIs
                    time.sleep(0.1)
        
        if progress_bar:
            progress_bar.close()

    def _print_token_summary(self):
        """Prints the total token usage for the session."""
        total_tokens = self.total_input_tokens + self.total_output_tokens
        cprint(Colors.OKGREEN, f"{Colors.BOLD}Total Tokens Used (from API):")
        cprint(Colors.INFO, f"  Input:   {self.total_input_tokens:,} tokens")
        cprint(Colors.INFO, f"  Output:  {self.total_output_tokens:,} tokens")
        cprint(Colors.BOLD, f"  Total:   {total_tokens:,} tokens")

def main():
    """
    Main function to run the script.
    """
    parser = setup_arg_parser()
    args = parser.parse_args()

    if not args.api_key:
        cprint(Colors.FAIL, "Error: API key not provided. Use -k/--api-key or set XAI_API_KEY env var.")
        exit(1)

    try:
        processor = V2SrtProcessor(args)
        processor.run()
    except KeyboardInterrupt:
        cprint(Colors.FAIL, "\n\nProcess interrupted by user. Exiting.")
        exit(1)
    except Exception as e:
        cprint(Colors.FAIL, f"\nAn unexpected critical error occurred: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        exit(1)

if __name__ == "__main__":
    main()
