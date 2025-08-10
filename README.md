# v2srt: A Universal AI Subtitle Translator

A robust command-line tool to automatically transcribe audio/video files using Whisper and translate subtitles using any standard, OpenAI-compatible Large Language Model (LLM). This tool is designed for accuracy, speed, and resilience, featuring intelligent self-correction mechanisms.

---

## English

### Key Features

-   **Universal LLM Support**: Connect to any OpenAI-compatible API endpoint. Tested with Grok, adaptable for GPT-4, Claude, and others.
-   **High-Quality Transcription**: Utilizes OpenAI's Whisper to generate accurate SRT subtitle files from video or audio sources.
-   **Advanced AI Translation**: Employs large language models for nuanced and context-aware translation.
-   **Intelligent Self-Correction & Robust Error Handling**:
    -   **Format Correction**: If the AI fails to use the correct subtitle separator, the tool automatically re-prompts, explaining the formatting error to the AI and retrying up to 3 times.
    -   **Language Correction**: If the AI responds in the wrong language, the tool detects the mismatch, informs the AI of its mistake, and retries up to 3 times.
-   **Heuristic Language Detection**:
    -   Features a sophisticated, multi-layered validation system to prevent false negatives, especially for CJK (Chinese, Japanese, Korean) languages.
    -   Explicitly checks if the AI simply returned the original source language, marking it as a failure.
-   **Optimized Prompt Engineering**: Uses an advanced two-step prompt that separates the translation task from the formatting task, significantly improving reliability.
-   **Concurrent Processing**: Fully supports multi-threaded requests to significantly speed up the translation of large files.
-   **Flexible Input**: Accepts existing SRT files for translation-only tasks, or video/audio files for a full transcription-and-translation workflow.
-   **Rich Debugging**: A `--debug` mode provides detailed, step-by-step logs of the entire process.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/abysmli/v2srt
    cd v2srt
    ```

2.  **Install System Dependencies (ffmpeg)**: Whisper requires `ffmpeg` to be installed on your system for audio/video processing.
    -   On Debian/Ubuntu: `sudo apt update && sudo apt install ffmpeg`
    -   On macOS (using Homebrew): `brew install ffmpeg`

3.  **Install Whisper:** Please follow the [official installation instructions](https://github.com/openai/whisper#setup).

4.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Configuration

An API key for your chosen translation service is required. You can set it in one of two ways:

1.  **Environment Variable (Recommended)**:
    ```bash
    export LLM_API_KEY="your_api_key_here" 
    # Note: The variable name is historical. It can hold any key.
    ```
2.  **Command-Line Argument**: Use the `-k` or `--api-key` flag.

### Usage

The tool is run via the `main.py` module.

```
usage: main.py [-h] (-i <file> | -v <file> | -a <file>) ...

v2srt: A Universal AI Subtitle Translator.

options:
  -h, --help            show this help message and exit

... (full help output available via -h) ...
```

### Examples

-   **Translate a Japanese SRT file to Chinese using the default model:**
    ```bash
    python3 -m src.main -i subtitles.srt -il ja -ol zh-cn
    ```

-   **Transcribe a video and translate using a specific model and 10 parallel threads:**
    ```bash
    python3 -m src.main -v video.mp4 -ol en -m 'some-other-model' -c 10
    ```

-   **Connect to a different, OpenAI-compatible LLM service (e.g., OpenAI's API):**
    ```bash
    python3 -m src.main -v video.mp4 -ol de \
      --api-url "https://api.openai.com/v1/chat/completions" \
      --api-key "YOUR_OPENAI_KEY" \
      -m "gpt-4"
    ```

---

## 中文

### 主要功能

-   **通用 LLM 支持**：可连接到任何兼容 OpenAI 标准的 API 服务。已在 Grok 上测试，同样适用于 GPT-4, Claude 等其他模型。
-   **高质量语音转录**：集成 OpenAI Whisper，从视频或音频文件精确生成 SRT 字幕。
-   **先进的 AI 翻译**：利用强大的大型语言模型进行细致入微且具备上下文感知能力的翻译。
-   **智能自我修正与强大的容错机制**：
    -   **格式修正**：如果 AI 未能正确使用字幕分割符，工具会自动重新发送请求，向 AI 解释其格式错误，并最多重试3次。
    -   **语言修正**：如果 AI 返回了错误的语言，工具能检测到不匹配，告知 AI 它犯的错误，并最多重试3次。
-   **启发式语言检测**：
    -   采用先进的多层防御验证系统，以防止错误的否定判断，特别是针对经常混淆的中、日、韩（CJK）语言。
    -   能明确检查出 AI 是否仅仅返回了原文（未翻译），并将其判定为失败。
-   **优化的提示工程**：使用先进的两步提示法，将“内容翻译”和“格式应用”任务分离，极大地提升了 AI 输出结果的稳定性和可靠性。
-   **高效率并发处理**：完全支持多线程请求，显著加快大型文件的翻译速度。
-   **灵活的输入方式**：既可以接收已有的 SRT 文件进行纯翻译，也可以接收视频/音频文件，完成“转录+翻译”的完整工作流。
-   **丰富的调试模式**：通过 `--debug` 标志可以启用详细的日志，分步展示完整的请求、响应和验证过程。

### 安装

1.  **克隆代码仓库：**
    ```bash
    git clone https://github.com/abysmli/v2srt
    cd v2srt
    ```

2.  **安装系统依赖 (ffmpeg)**：Whisper 依赖 `ffmpeg` 来处理音视频文件。
    -   在 Debian/Ubuntu 上: `sudo apt update && sudo apt install ffmpeg`
    -   在 macOS 上 (使用 Homebrew): `brew install ffmpeg`

3.  **安装 Whisper：** 请遵循 [官方安装指南](https://github.com/openai/whisper#setup) 进行安装。

4.  **安装 Python 依赖包：**
    ```bash
    pip install -r requirements.txt
    ```

### 配置

程序需要您选择的翻译服务所对应的 API 密钥。您可以通过以下两种方式之一进行设置：

1.  **环境变量 (推荐)**：
    ```bash
    export LLM_API_KEY="在这里填入你的API密钥"
    # 提示：变量名是历史遗留的，但它可以用于存放任何服务的密钥。
    ```
2.  **命令行参数**：在运行脚本时，使用 `-k` 或 `--api-key` 标志。

### 使用方法

通过 `main.py` 模块来运行此脚本。

```
usage: main.py [-h] (-i <file> | -v <file> | -a <file>) ...

v2srt: A Universal AI Subtitle Translator.

... (运行 -h 查看完整帮助信息) ...
```

### 示例

-   **使用默认 AI 模型翻译一个已有的日语 SRT 文件到中文：**
    ```bash
    python3 -m src.main -i subtitles.srt -il ja -ol zh-cn
    ```

-   **转录一个视频，并使用特定模型和 10 个并发线程进行翻译：**
    ```bash
    python3 -m src.main -v video.mp4 -ol en -m 'some-other-model' -c 10
    ```

-   **连接到另一个兼容 OpenAI 的 LLM 服务（例如 OpenAI 的 API）：**
    ```bash
    python3 -m src.main -v video.mp4 -ol de \
      --api-url "https://api.openai.com/v1/chat/completions" \
      --api-key "YOUR_OPENAI_KEY" \
      -m "gpt-4"
    ```