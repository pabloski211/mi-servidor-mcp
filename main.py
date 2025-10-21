# server.py
import os
from typing import Dict, Any
from fastmcp import FastMCP

mcp = FastMCP("HR MCP Server")

@mcp.tool
def ping(message: str) -> Dict[str, Any]:
    """Simple health check."""
    return {"ok": True, "message": message}

@mcp.tool
def search_candidates(term: str = "") -> Dict[str, Any]:
    """Search candidates by term."""
    # TODO: implement real search
    return {"results": [], "term": term}

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    # HTTP “streamable” en raíz → encaja con tu swagger POST /
    mcp.run(transport="http", host="0.0.0.0", port=port, path="/")
    # Nota: el servidor también publica SSE (típicamente en /sse) si el cliente lo usa.