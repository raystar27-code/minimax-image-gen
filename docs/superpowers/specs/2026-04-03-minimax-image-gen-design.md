# MiniMax Image Generation Skill Design

## Overview
A reusable skill for OpenClaw (or other agents) to generate images using the MiniMax API. The skill provides a CLI tool that handles API authentication, request construction, image downloading, and local file storage.

## User Review Required
> [!IMPORTANT]
> The skill requires a MiniMax API Key (`MINIMAX_API_KEY`) to be set in a `.env` file or as an environment variable.

## Proposed Design

### Component: CLI Tool (Python)
A Python script (`minimax_gen.py`) will serve as the core executor.

#### Input Arguments
- `--prompt` (Required): The text description for the image.
- `--aspect_ratio` (Optional, default "1:1"): The aspect ratio (e.g., 16:9, 3:2).
- `--model` (Optional, default "image-01"): The MiniMax model to use.
- `--output_dir` (Optional, default "./outputs"): Where to save the generated image.

#### Logic Flow
1. Load environment variables from `.env` using `python-dotenv`.
2. Construct the POST request to `https://api.minimaxi.com/v1/image_generation`.
3. Set `response_format` to `url`.
4. Parse the response to extract the image URL.
5. Download the image and save it to the specified `output_dir` with a unique timestamp-based filename.
6. Print the absolute path of the saved file to `stdout` for OpenClaw to consume.

### Component: Skill Documentation (SKILL.md)
A `SKILL.md` compliant with the `writing-skills` format, teaching OpenClaw how to use the CLI tool.

#### Structure
- **Description**: Use when you need to generate an image from text using MiniMax.
- **Example Usage**: `python minimax_gen.py --prompt "A futuristic city"`
- **Response Handling**: Extract the file path from the output to send to the user.

## Open Questions
- Do you want to support generating multiple images (`n > 1`) in a single call? (Currently planned for 1 image).
- Should the `prompt_optimizer` be enabled by default? (I suggest yes for better AI generation).

## Verification Plan
1. **Manual Test**: Run the script with a sample prompt and verify the image is downloaded correctly.
2. **Integration Test**: Mock an OpenClaw call to see if it can parse the output path.
