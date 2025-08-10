# -*- coding: utf-8 -*- 

"""
Handles the translation of text batches using an external API,
including language validation and retry mechanisms.
"""

import json
import re
import subprocess
import time
from .utils import cprint, Colors
from .config import Config, LANG_MAP

try:
    from langdetect import detect_langs, LangDetectException
    LANGDETECT_AVAILABLE = True
except ImportError:
    LANGDETECT_AVAILABLE = False

class Translator:
    """
    Manages API calls to the translation service.
    """
    def __init__(self, args):
        self.api_url = args.api_url
        self.api_key = args.api_key
        self.model = args.model
        self.separator = args.separator
        self.input_lang = args.input_lang
        self.output_lang = args.output_lang
        self.debug = args.debug
        if not LANGDETECT_AVAILABLE:
            cprint(Colors.WARNING, "Warning: 'langdetect' library not found. Language validation will be skipped.")
            cprint(Colors.WARNING, "To enable this feature, please run: pip install langdetect")

    def _validate_language(self, text_batch, batch_index):
        """
        Validates language using a multi-layered defense strategy.
        """
        if not LANGDETECT_AVAILABLE:
            return True

        try:
            combined_text = " ".join(text_batch).strip()
            if not combined_text: return True

            if self.debug:
                cprint(Colors.INFO, f"--- Debug: Validating language for Batch #{batch_index} ---")
                cprint(Colors.INFO, f"Text for detection (first 200 chars): '{combined_text[:200]}...'")

            detected_results = detect_langs(combined_text)
            if not detected_results:
                if self.debug: cprint(Colors.WARNING, f"Language detection returned no results for Batch #{batch_index}. Skipping validation.")
                return True

            top_lang = detected_results[0].lang

            # 1st Defense: Check if the AI returned the original language.
            if top_lang.startswith(self.input_lang):
                if self.debug: cprint(Colors.FAIL, f"Language validation FAILED for Batch #{batch_index}! AI returned the original language '{self.input_lang}'.")
                return False

            # 2nd Defense: Check if the top guess is the target language.
            if top_lang.startswith(self.output_lang):
                if self.debug: cprint(Colors.OKGREEN, f"Language validation PASSED for Batch #{batch_index} (Top Guess: '{top_lang}')")
                return True

            # 3rd Defense (Heuristic): For CJK confusion, check possibilities.
            # This rule is now more robust, triggering if the target is any 'zh' variant.
            if self.output_lang.startswith('zh') and top_lang in ['ko', 'ja']:
                all_detected_langs = {result.lang for result in detected_results}
                if 'zh-cn' in all_detected_langs or 'zh-tw' in all_detected_langs:
                    if self.debug:
                        cprint(Colors.WARNING, f"Heuristic Pass for Batch #{batch_index}: Top guess was '{top_lang}', but a 'zh' variant was also detected. Accepting.")
                        cprint(Colors.WARNING, f"Full detection list: {detected_results}")
                    return True
            
            # If all defenses are passed, it's a definitive failure.
            if self.debug:
                cprint(Colors.FAIL, f"Language validation FAILED for Batch #{batch_index}! (Expected: '{self.output_lang}', Top Guess: '{top_lang}')")
                cprint(Colors.FAIL, f"Full detection list: {detected_results}")
            return False

        except LangDetectException:
            if self.debug: cprint(Colors.WARNING, f"Could not detect language for Batch #{batch_index}. Skipping validation.")
            return True

    def translate_batch(self, indexed_batch, network_retry_count=0, validation_retry_count=0, separator_retry_count=0):
        batch_index, text_batch = indexed_batch
        if not text_batch: return {'translations': [], 'input_tokens': 0, 'output_tokens': 0}
        error_result = {'translations': [f"---TRANSLATION_ERROR---\n{text}" for text in text_batch], 'input_tokens': 0, 'output_tokens': 0}
        clean_text_to_translate = "\n".join(text_batch)
        structure_template = f" {self.separator} ".join(text_batch)
        from_lang, to_lang = LANG_MAP.get(self.input_lang, self.input_lang), LANG_MAP.get(self.output_lang, self.output_lang)
        common_rules = "Your task is to translate a list of subtitles and format the output precisely. Do not add any extra explanations, introductory text, or markdown."

        if validation_retry_count > 0:
            prompt = f"""You are an expert translator. Your previous translation attempt was WRONG because you used the wrong language.
You MUST translate the following {from_lang} text into {to_lang}. Do not use any other language.
{common_rules}

1. First, translate this block of text:
{clean_text_to_translate}

2. Second, take your translation and format it EXACTLY like this template, using '{self.separator}' as the separator:
{structure_template}
"""
        elif separator_retry_count > 0:
            prompt = f"""You are an expert translator. Your previous attempt FAILED because you did not format the output correctly.
You MUST use the exact separator string '{self.separator}' between each and every translated subtitle.
The number of separators in your output must be exactly one less than the number of subtitles.
{common_rules}

1. First, translate this block of text:
{clean_text_to_translate}

2. Second, take your translation and format it EXACTLY like this template, using '{self.separator}' as the separator:
{structure_template}
"""
        else:
            prompt = f"""You are a highly skilled translator specializing in subtitle files.
You MUST translate the following {from_lang} text into {to_lang}. Do not use any other language.
{common_rules}

1. First, translate the following text, where each line is a separate subtitle:
{clean_text_to_translate}

2. Second, you MUST format your entire response as a single block of text. Use the following template for structure, placing the exact separator string '{self.separator}' between each corresponding translated subtitle:
{structure_template}
"""

        data = {"messages": [{"role": "user", "content": prompt}], "model": self.model}
        if self.debug: cprint(Colors.WARNING, f"\n--- Debug: Sending Batch #{batch_index} (Network: {network_retry_count + 1}, Lang-Validation: {validation_retry_count + 1}, Format-Validation: {separator_retry_count + 1}) ---")

        try:
            response = subprocess.run(
                ['curl', '-s', '-X', 'POST', self.api_url, '-H', f"Authorization: Bearer {self.api_key}", '-H', 'Content-Type: application/json', '-d', json.dumps(data)],
                capture_output=True, text=True, check=True, encoding='utf-8'
            )
            response_json = json.loads(response.stdout)
            usage = response_json.get("usage", {})
            input_tokens, output_tokens = usage.get("prompt_tokens", 0), usage.get("completion_tokens", 0)
            translated_content = re.sub(r'^```(json|text)?\s*|\s*```$', '', response_json["choices"][0]["message"]["content"].strip())
            translated_batch = [text.strip() for text in translated_content.split(self.separator)]

            if self.debug:
                cprint(Colors.WARNING, f"\n--- Debug: Received Response for Batch #{batch_index} ---")
                for i, text in enumerate(translated_batch): print(f"  {batch_index}-{i+1}: {text.strip()}")
            
            if len(translated_batch) != len(text_batch):
                if separator_retry_count < Config.MAX_VALIDATION_RETRIES:
                    cprint(Colors.FAIL, f"Retrying Batch #{batch_index} due to separator mismatch (Expected: {len(text_batch)}, Got: {len(translated_batch)})... (Attempt {separator_retry_count + 2}/{Config.MAX_VALIDATION_RETRIES + 1})")
                    time.sleep(1)
                    return self.translate_batch(indexed_batch, network_retry_count, validation_retry_count, separator_retry_count + 1)
                else:
                    cprint(Colors.FAIL, f"Max format retries reached for Batch #{batch_index}. Accepting translation as is.")
            
            if not self._validate_language(translated_batch, batch_index):
                if validation_retry_count < Config.MAX_VALIDATION_RETRIES:
                    cprint(Colors.FAIL, f"Retrying Batch #{batch_index} due to language mismatch... (Attempt {validation_retry_count + 2}/{Config.MAX_VALIDATION_RETRIES + 1})")
                    time.sleep(1)
                    return self.translate_batch(indexed_batch, network_retry_count, validation_retry_count + 1, 0)
                else:
                    cprint(Colors.FAIL, f"Max language validation retries reached for Batch #{batch_index}. Accepting translation as is.")

            return {'translations': translated_batch, 'input_tokens': input_tokens, 'output_tokens': output_tokens}

        except (subprocess.CalledProcessError, json.JSONDecodeError, IndexError, KeyError) as e:
            cprint(Colors.FAIL, f"\nError during translation of Batch #{batch_index}: {e}")
            if 'response' in locals(): cprint(Colors.FAIL, f"Response from API: {response.stdout}")
            if network_retry_count < 1:
                cprint(Colors.WARNING, "Retrying after network/API error...")
                time.sleep(1)
                return self.translate_batch(indexed_batch, network_retry_count + 1, validation_retry_count, separator_retry_count)
            return error_result
