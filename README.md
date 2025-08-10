# v2srt: AI-Powered Subtitle Transcription and Translation

A robust command-line tool to automatically transcribe audio/video files using Whisper and translate the subtitles into a target language using a powerful AI model (e.g., Grok). This tool is designed for accuracy, speed, and resilience, featuring intelligent self-correction mechanisms.

---

## English

### Key Features

-   **High-Quality Transcription**: Utilizes OpenAI's Whisper to generate accurate SRT subtitle files from video or audio sources.
-   **Advanced AI Translation**: Employs large language models for nuanced and context-aware translation.
-   **Intelligent Self-Correction & Robust Error Handling**:
    -   **Format Correction**: If the AI fails to use the correct subtitle separator, the tool will automatically re-prompt, explaining the formatting error to the AI and retrying up to 3 times.
    -   **Language Correction**: If the AI responds in the wrong language (e.g., returns English when Chinese was requested), the tool detects the mismatch, informs the AI of its mistake, and retries up to 3 times.
-   **Heuristic Language Detection**:
    -   Features a sophisticated, multi-layered validation system to prevent false negatives, especially for CJK (Chinese, Japanese, Korean) languages which often confuse statistical detection models.
    -   Explicitly checks if the AI simply returned the original source language, marking it as a failure.
-   **Optimized Prompt Engineering**: Uses an advanced two-step prompt that separates the translation task from the formatting task, significantly improving the reliability and consistency of the AI's output.
-   **Concurrent Processing**: Fully supports multi-threaded requests to significantly speed up the translation of large files. The number of parallel workers is configurable.
-   **Flexible Input**: Accepts existing SRT files for translation-only tasks, or video/audio files for a full transcription-and-translation workflow.
-   **Rich Debugging**: A `--debug` mode provides detailed, step-by-step logs of the entire process, including prompts sent, responses received, and validation results.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/abysmli/v2srt
    cd v2srt
    ```

2.  **Install System Dependencies (ffmpeg)**: Whisper requires `ffmpeg` to be installed on your system for audio/video processing.

    -   On Debian/Ubuntu:
        ```bash
        sudo apt update && sudo apt install ffmpeg
        ```
    -   On macOS (using Homebrew):
        ```bash
        brew install ffmpeg
        ```

3.  **Install Whisper:** This tool requires OpenAI's Whisper to be installed. Please follow the [official installation instructions](https://github.com/openai/whisper#setup).

4.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    The `requirements.txt` file includes `tqdm` for progress bars and `langdetect` for language validation.

### Configuration

The API key for the translation service is required. You can set it in one of two ways:

1.  **Environment Variable (Recommended)**:
    ```bash
    export XAI_API_KEY="your_api_key_here"
    ```
2.  **Command-Line Argument**: Use the `-k` or `--api-key` flag when running the script.

### Usage

The script is run via the `main.py` module. Here is the full help information:

```
usage: main.py [-h] (-i <file> | -v <file> | -a <file>) [-o <file>]
               [-ot <file>] [-il <code>] [-ol <code>] [-m <name>]
               [-wm {tiny,base,small,medium,large,large-v2,large-v3}]
               [-k <key>] [-b <N>] [-c <N>] [-s <str>] [-d] [--version]

v2srt: Transcribe and Translate Subtitles.

options:
  -h, --help            show this help message and exit

Input/Output:
  -i <file>, --input-srt <file>
                        Path to an existing SRT file to translate.
  -v <file>, --input-video <file>
                        Path to a video file to transcribe and then translate.
  -a <file>, --input-audio <file>
                        Path to an audio file to transcribe and then translate.
  -o <file>, --output-srt <file>
                        Path to save the generated (untranslated) SRT file from transcription.
  -ot <file>, --output-translated <file>
                        Path to save the final translated SRT file.

Language & Model:
  -il <code>, --input-lang <code>
                        Input language code (e.g., 'en', 'ja'). Default: ja
  -ol <code>, --output-lang <code>
                        Output language code (e.g., 'en', 'zh-cn'). Default: zh-cn
  -m <name>, --model <name>
                        Translation model to use. Default: grok-3-mini
  -wm {tiny,base,small,medium,large,large-v2,large-v3}, --whisper-model {tiny,base,small,medium,large,large-v2,large-v3}
                        Whisper model for transcription. Default: large

API & Performance:
  -k <key>, --api-key <key>
                        Your translation API key. Defaults to XAI_API_KEY env var.
  -b <N>, --batch-size <N>
                        Number of subtitles to send in each API request. Default: 10
  -c <N>, --concurrency <N>
                        Number of parallel API requests to make. Default: 5
  -s <str>, --separator <str>
                        Unique separator for batching subtitles. Default: '[|||]'

Miscellaneous:
  -d, --debug           Enable debug mode for verbose request/response logging.
  --version             show program's version number and exit
```

### Examples

-   **Translate an existing Japanese SRT file to Chinese:**
    ```bash
    python3 -m src.main -i subtitles.srt -il ja -ol zh-cn
    ```

-   **Transcribe a video, then translate the resulting SRT file:**
    ```bash
    python3 -m src.main -v video.mp4 -ol zh-cn
    ```

-   **Transcribe and translate, specifying a different Whisper model and batch size:**
    ```bash
    python3 -m src.main -v video.mp4 -ol en -wm small -b 5
    ```

-   **Use 10 parallel threads for faster translation:**
    ```bash
    python3 -m src.main -v video.mp4 -ol zh-cn -c 10
    ```

---

## 中文

### 主要功能

-   **高质量语音转录**：集成 OpenAI Whisper，从视频或音频文件精确生成 SRT 字幕。
-   **先进的 AI 翻译**：利用强大的大型语言模型进行 nuanced (细致入微) 和具备上下文感知能力的翻译。
-   **智能自我修正与强大的容错机制**：
    -   **格式修正**：如果 AI 未能正确使用字幕分割符，工具会自动重新发送请求，向 AI 解释其格式错误，并最多重试3次。
    -   **语言修正**：如果 AI 返回了错误的语言（例如，要求中文却返回了英文），工具能检测到语言不匹配，告知 AI 它犯的错误，并最多重试3次。
-   **启发式语言检测**：
    -   采用先进的多层防御验证系统，以防止错误的否定判断，特别是针对经常混淆统计检测模型的中、日、韩（CJK）语言。
    -   能明确检查出 AI 是否仅仅返回了原文（未翻译），并将其判定为失败。
-   **优化的提示工程 (Prompt Engineering)**：使用先进的两步提示法，将“内容翻译”任务和“格式应用”任务分离，极大地提升了 AI 输出结果的稳定性和可靠性。
-   **高效率并发处理**：完全支持多线程请求，显著加快大型文件的翻译速度。并发线程数可由用户配置。
-   **灵活的输入方式**：既可以接收已有的 SRT 文件进行纯翻译，也可以接收视频/音频文件，完成“转录+翻译”的完整工作流。
-   **丰富的调试模式**：通过 `--debug` 标志可以启用详细的日志，分步展示完整的请求、响应和验证过程。

### 安装

1.  **克隆代码仓库：**
    ```bash
    git clone https://github.com/abysmli/v2srt
    cd v2srt
    ```

2.  **安装系统依赖 (ffmpeg)**：Whisper 依赖 `ffmpeg` 来处理音视频文件。请确保您的系统上已安装此程序。

    -   在 Debian/Ubuntu 上:
        ```bash
        sudo apt update && sudo apt install ffmpeg
        ```
    -   在 macOS 上 (使用 Homebrew):
        ```bash
        brew install ffmpeg
        ```

3.  **安装 Whisper：** 本工具依赖 OpenAI Whisper。请遵循 [官方安装指南](https://github.com/openai/whisper#setup) 进行安装。

4.  **安装 Python 依赖包：**
    ```bash
    pip install -r requirements.txt
    ```
    `requirements.txt` 文件包含了 `tqdm` (用于进度条) 和 `langdetect` (用于语言验证)。

### 配置

程序需要翻译服务的 API 密钥。您可以通过以下两种方式之一进行设置：

1.  **环境变量 (推荐)**：
    ```bash
    export XAI_API_KEY="在这里填入你的API密钥"
    ```
2.  **命令行参数**：在运行脚本时，使用 `-k` 或 `--api-key` 标志。

### 使用方法

通过 `main.py` 模块来运行此脚本。以下是完整的帮助信息：

```
usage: main.py [-h] (-i <file> | -v <file> | -a <file>) [-o <file>]
               [-ot <file>] [-il <code>] [-ol <code>] [-m <name>]
               [-wm {tiny,base,small,medium,large,large-v2,large-v3}]
               [-k <key>] [-b <N>] [-c <N>] [-s <str>] [-d] [--version]

v2srt: Transcribe and Translate Subtitles.

options:
  -h, --help            show this help message and exit

Input/Output:
  -i <file>, --input-srt <file>
                        Path to an existing SRT file to translate.
  -v <file>, --input-video <file>
                        Path to a video file to transcribe and then translate.
  -a <file>, --input-audio <file>
                        Path to an audio file to transcribe and then translate.
  -o <file>, --output-srt <file>
                        Path to save the generated (untranslated) SRT file from transcription.
  -ot <file>, --output-translated <file>
                        Path to save the final translated SRT file.

Language & Model:
  -il <code>, --input-lang <code>
                        Input language code (e.g., 'en', 'ja'). Default: ja
  -ol <code>, --output-lang <code>
                        Output language code (e.g., 'en', 'zh-cn'). Default: zh-cn
  -m <name>, --model <name>
                        Translation model to use. Default: grok-3-mini
  -wm {tiny,base,small,medium,large,large-v2,large-v3}, --whisper-model {tiny,base,small,medium,large,large-v2,large-v3}
                        Whisper model for transcription. Default: large

API & Performance:
  -k <key>, --api-key <key>
                        Your translation API key. Defaults to XAI_API_KEY env var.
  -b <N>, --batch-size <N>
                        Number of subtitles to send in each API request. Default: 10
  -c <N>, --concurrency <N>
                        Number of parallel API requests to make. Default: 5
  -s <str>, --separator <str>
                        Unique separator for batching subtitles. Default: '[|||]'

Miscellaneous:
  -d, --debug           Enable debug mode for verbose request/response logging.
  --version             show program's version number and exit
```

### 示例

-   **翻译一个已有的日语 SRT 文件到中文：**
    ```bash
    python3 -m src.main -i subtitles.srt -il ja -ol zh-cn
    ```

-   **转录一个视频，并翻译生成的 SRT 文件：**
    ```bash
    python3 -m src.main -v video.mp4 -ol zh-cn
    ```

-   **转录并翻译，同时指定一个不同的 Whisper 模型和批处理大小：**
    ```bash
    python3 -m src.main -v video.mp4 -ol en -wm small -b 5
    ```

-   **使用 10 个并发线程来加速翻译：**
    ```bash
    python3 -m src.main -v video.mp4 -ol zh-cn -c 10
    ```