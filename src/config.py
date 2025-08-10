# -*- coding: utf-8 -*-

"""
Configuration for the v2srt application.
Stores constants, language mappings, and API settings.
"""

class Config:
    """Stores all script-wide configuration constants."""
    DEFAULT_MODEL = "grok-3-mini"
    DEFAULT_BATCH_SIZE = 10
    DEFAULT_SEPARATOR = "[|||]"
    DEFAULT_INPUT_LANG = "ja"
    DEFAULT_OUTPUT_LANG = "zh-cn"
    DEFAULT_WHISPER_MODEL = "large"
    DEFAULT_CONCURRENCY = 5
    MAX_VALIDATION_RETRIES = 3
    API_URL = "https://api.x.ai/v1/chat/completions"

LANG_MAP = {
    'en': 'English', 'zh': 'Chinese', 'ja': 'Japanese', 'es': 'Spanish',
    'fr': 'French', 'de': 'German', 'ru': 'Russian', 'ko': 'Korean',
}
