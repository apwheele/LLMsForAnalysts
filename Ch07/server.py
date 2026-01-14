#!/usr/bin/env python3
"""
MCP Server for generating images using Google's Gemini API via gemimg library.
"""

import os
import sys
import base64
from io import BytesIO
from typing import Optional

try:
    from gemimg import GemImg
except ImportError:
    print("Error: gemimg library not installed. Run: pip install gemimg", file=sys.stderr)
    sys.exit(1)

from mcp.server import Server
from mcp.types import Tool, TextContent, ImageContent
import mcp.server.stdio

# Initialize the MCP server
app = Server("gemimg-server")

# Initialize GemImg client (API key will be loaded from environment)
try:
    gemimg_client = GemImg(model="gemini-3-pro-image-preview")
except Exception as e:
    print(f"Warning: Failed to initialize GemImg client: {e}", file=sys.stderr)
    print("Make sure GEMINI_API_KEY is set in your environment or .env file", file=sys.stderr)
    gemimg_client = None


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="generate_image",
            description=(
                "Generate an image from a text prompt using Google's Gemini image generation API. "
                "Returns the generated image as a base64-encoded PNG. "
                "Supports aspect ratio specification (e.g., '16:9', '1:1', '9:16')."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "Text description of the image to generate",
                    },
                    "aspect_ratio": {
                        "type": "string",
                        "description": "Optional aspect ratio (e.g., '16:9', '1:1', '9:16'). Default is '1:1'.",
                    },
                    "model": {
                        "type": "string",
                        "description": "Optional model name. Default is 'gemini-3-pro-image-preview'.",
                    },
                    "save_dir": {
                        "type": "string",
                        "description": "Directory path where the generated image should be saved. Default is current working directory.",
                    },
                    "image_size": {
                        "type": "string",
                        "description": "Image size: '1K' (1024px), '2K' (2048px), or '4K' (4096px). Default is '4K'.",
                        "enum": ["1K", "2K", "4K"],
                    },
                    "style_images": {
                        "type": "array",
                        "description": "Optional list of file paths to images to use for style/composition guidance.",
                        "items": {
                            "type": "string"
                        },
                    },
                    "n_images": {
                        "type": "integer",
                        "description": "Number of images to generate. Default is 1",
                    }
                },
                "required": ["prompt"],
            },
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent | ImageContent]:
    """Handle tool calls."""
    if name != "generate_image":
        raise ValueError(f"Unknown tool: {name}")

    if gemimg_client is None:
        return [
            TextContent(
                type="text",
                text="Error: GemImg client not initialized. Please set GEMINI_API_KEY environment variable.",
            )
        ]

    prompt = arguments.get("prompt")
    if not prompt:
        return [TextContent(type="text", text="Error: prompt is required")]

    aspect_ratio = arguments.get("aspect_ratio", "1:1")
    model = arguments.get("model","gemini-3-pro-image-preview")
    save_dir = arguments.get("save_dir")
    image_size = arguments.get("image_size", "4K")
    style_images = arguments.get("style_images")
    n_images = int(arguments.get("n_images","1"))

    try:
        # Update client model if specified
        if model:
            gemimg_client.model = model

        # Prepare generate parameters
        generate_params = {
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "save": True,
        }

        # Add save_dir if specified
        if save_dir:
            os.makedirs(save_dir, exist_ok=True)
            generate_params["save_dir"] = save_dir

        # Add style_images if specified (gemimg expects them as input_images parameter)
        if style_images:
            generate_params["input_images"] = style_images

        # Generate image
        gl = []
        for _ in range(n_images):
            gen = gemimg_client.generate(**generate_params)
            gl.append(gen)

        # Convert PIL Image to base64 PNG
        #buffer = BytesIO()
        #gen.image.save(buffer, format="PNG")
        #image_bytes = buffer.getvalue()
        #image_base64 = base64.b64encode(image_bytes).decode("utf-8")

        # Build result message
        result_text = f"Generated image for prompt: '{prompt}' (aspect ratio: {aspect_ratio}, size: {image_size})"
        if save_dir:
            result_text += f"\nSaved {n_images} to: {save_dir}"
        if style_images:
            result_text += f"\nUsing {len(style_images)} style image(s)"

        # Return both text description and the image
        #ImageContent(
        #        type="image",
        #        data=image_base64,
        #        mimeType="image/png",
        #    ),
        return [
            TextContent(
                type="text",
                text=result_text,
            )
        ]

    except Exception as e:
        return [
            TextContent(
                type="text",
                text=f"Error generating image: {str(e)}",
            )
        ]


async def main():
    """Run the MCP server."""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options(),
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
