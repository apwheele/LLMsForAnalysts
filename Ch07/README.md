# Gemimg MCP Server

An MCP (Model Context Protocol) server that enables Claude Code to generate images using Google's Gemini image generation API through the [gemimg](https://github.com/minimaxir/gemimg) library.

## Features

- Generate images from text prompts
- Support for custom aspect ratios (16:9, 1:1, 9:16, etc.)
- Returns images directly in Claude Code
- Leverages Google's Gemini 2.0 Flash model

## Installation

1. Install dependencies:

```bash
pip install gemimg mcp
```

2. Set up your Gemini API key. You can do this in one of three ways:

   **Option A: Environment variable**
   ```bash
   export GEMINI_API_KEY="your-api-key-here"
   ```

   **Option B: .env file**
   Create a `.env` file in your working directory:
   ```
   GEMINI_API_KEY=your-api-key-here
   ```

   **Option C: System-wide configuration**
   Add to your shell profile (~/.bashrc, ~/.zshrc, etc.)

3. Get a Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey)

## Configuration

Add this server to your Claude Code configuration. Edit your MCP settings file:

**For Claude Desktop:**
Edit `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "gemimg": {
      "command": "python",
      "args": ["/path/to/gemimg-mcp-server/server.py"],
      "env": {
        "GEMINI_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

**For Claude Code CLI:**
Edit `~/.config/claude-code/mcp_settings.json`:

```json
{
  "mcpServers": {
    "gemimg": {
      "command": "python",
      "args": ["/path/to/gemimg-mcp-server/server.py"],
      "env": {
        "GEMINI_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

Replace `/path/to/gemimg-mcp-server/server.py` with the actual path to the server.py file.

## Usage

Once configured, you can ask Claude Code to generate images:

```
Generate an image of a futuristic city at sunset
```

```
Create a 16:9 landscape image of mountains reflected in a lake
```

```
Make an image of a cute robot reading a book
```

Claude Code will use the `generate_image` tool to create images based on your prompts.

## Tool Parameters

The `generate_image` tool accepts:

- `prompt` (required): Text description of the image to generate
- `aspect_ratio` (optional): Aspect ratio like "16:9", "1:1", "9:16". Default: "1:1"
- `model` (optional): Gemini model name. Default: "gemini-2.0-flash-exp"

## Troubleshooting

**"gemimg library not installed"**
- Run: `pip install gemimg`

**"Failed to initialize GemImg client"**
- Make sure your `GEMINI_API_KEY` is set correctly
- Verify your API key is valid at [Google AI Studio](https://aistudio.google.com/apikey)

**"Error generating image"**
- Check your internet connection
- Verify your API key has not exceeded quota
- Ensure the prompt follows Google's content policies

## License

MIT License - feel free to modify and distribute as needed.
