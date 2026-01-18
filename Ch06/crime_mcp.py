# dallas_crime_mcp.py
# /// script
# dependencies = [
#   "mcp",
#   "pandas",
#   "matplotlib",
#   "tabulate"
# ]
# ///

from mcp.server import Server
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

# load the dallas crime data in the same folder as script
dallas = pd.read_csv('DallasCrime.csv.zip')

# get categories for enums
nibrs_cats = pd.unique(dallas['nibrs']).tolist()
loc_cats = pd.unique(dallas['location']).tolist()

def month_trends(nibrs=None, location=None):
    """Get monthly crime trends as a formatted table."""
    dal = dallas.copy()
    if nibrs:
        dal = dal[dal['nibrs'] == nibrs]
    if location:
        dal = dal[dal['location'] == location]
    gb = dal.groupby(['Year','Month'], as_index=False).size()
    pb = gb.pivot(index='Month', columns='Year', values='size')
    return pb.to_markdown()

def top_addresses(nibrs=None, location=None, k=10):
    """Get top repeat crime addresses."""
    dal = dallas.copy()
    if nibrs:
        dal = dal[dal['nibrs'] == nibrs]
    if location:
        dal = dal[dal['location'] == location]
    vc = dal['address'].value_counts().head(k)
    return vc.to_markdown()

def plot_monthly_trends(nibrs=None, location=None):
    """Create line chart of monthly crime trends."""
    dal = dallas.copy()
    if nibrs:
        dal = dal[dal['nibrs'] == nibrs]
    if location:
        dal = dal[dal['location'] == location]
    gb = dal.groupby(['Year', 'Month'], as_index=False).size()
    gb['Day'] = 1
    gb['Mo-Yr'] = pd.to_datetime(gb[['Year','Month','Day']])
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(gb['Mo-Yr'], gb['size'], marker='o')
    ax.set_ylabel('Incident Count')
    title = f'Monthly Trends'
    if nibrs:
        title += f' - {nibrs}'
    if location:
        title += f' at {location}'
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
    plt.close(fig)
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return img_base64

# create MCP server
server = Server("dallas-crime-analysis")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools."""
    return [
        types.Tool(
            name="month_trends",
            description="Get monthly crime trends by year",
            inputSchema={
                "type": "object",
                "properties": {
                    "nibrs": {
                        "type": "string",
                        "description": "NIBRS offense type",
                        "enum": nibrs_cats
                    },
                    "location": {
                        "type": "string",
                        "description": "Location category",
                        "enum": loc_cats
                    }
                }
            }
        ),
        types.Tool(
            name="top_addresses",
            description="Get top repeat crime addresses",
            inputSchema={
                "type": "object",
                "properties": {
                    "nibrs": {
                        "type": "string",
                        "description": "NIBRS offense type",
                        "enum": nibrs_cats
                    },
                    "location": {
                        "type": "string",
                        "description": "Location category",
                        "enum": loc_cats
                    },
                    "k": {
                        "type": "integer",
                        "description": "Number of addresses to return",
                        "default": 10
                    }
                }
            }
        ),
        types.Tool(
            name="plot_monthly_trends",
            description="Create chart of monthly crime trends",
            inputSchema={
                "type": "object",
                "properties": {
                    "nibrs": {
                        "type": "string",
                        "description": "NIBRS offense type",
                        "enum": nibrs_cats
                    },
                    "location": {
                        "type": "string",
                        "description": "Location category",
                        "enum": loc_cats
                    }
                }
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict
) -> list[types.TextContent | types.ImageContent]:
    """Handle tool execution."""
    if name == "month_trends":
        result = month_trends(**arguments)
        return [types.TextContent(type="text", text=result)]

    elif name == "top_addresses":
        result = top_addresses(**arguments)
        return [types.TextContent(type="text", text=result)]

    elif name == "plot_monthly_trends":
        img_base64 = plot_monthly_trends(**arguments)
        return [types.ImageContent(
            type="image",
            data=img_base64,
            mimeType="image/png"
        )]

    raise ValueError(f"Unknown tool: {name}")

async def main():
    """Run the MCP server."""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="dallas-crime-analysis",
                server_version="1.0.0",
                capabilities=types.ServerCapabilities(
                    tools=types.ToolsCapability()
                )
            )
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())