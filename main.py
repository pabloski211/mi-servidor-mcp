import os
import threading
import asyncio
from typing import Dict, Any, Optional

from fastmcp import FastMCP   # tus tools aquí
import httpx
from starlette.applications import Starlette
from starlette.responses import Response, JSONResponse, StreamingResponse, PlainTextResponse
from starlette.requests import Request
from starlette.routing import Route

# ---------- CONFIG ----------
INNER_HOST = "127.0.0.1"
INNER_PORT = int(os.getenv("INNER_PORT", "9000"))  # FastMCP interno
PUBLIC_PORT = int(os.getenv("PORT", "8000"))       # UVicorn/Render

CORS_ALLOW_ORIGINS = os.getenv("CORS_ALLOW_ORIGINS", "*")
CORS_ALLOW_HEADERS = os.getenv("CORS_ALLOW_HEADERS", "Content-Type, Accept, x-api-key")
CORS_ALLOW_METHODS = os.getenv("CORS_ALLOW_METHODS", "GET, POST, OPTIONS")
CORS_MAX_AGE = "86400"

# ---------- MCP (nativo) ----------
mcp = FastMCP("HR MCP Server")

@mcp.tool
def ping(message: str) -> Dict[str, Any]:
    """Simple health check."""
    return {"ok": True, "message": message}

@mcp.tool
def search_candidates(term: str = "") -> Dict[str, Any]:
    """Search candidates by term."""
    return {"results": [], "term": term}

def run_inner_fastmcp():
    # Levanta FastMCP nativo en loopback, puerto interno
    mcp.run(transport="http", host=INNER_HOST, port=INNER_PORT, path="/")

# Arrancamos el FastMCP nativo en un hilo aparte
threading.Thread(target=run_inner_fastmcp, daemon=True).start()

# ---------- ASGI proxy con CORS + OPTIONS ----------
async def preflight(_: Request):
    return Response(status_code=204, headers={
        "Access-Control-Allow-Origin": CORS_ALLOW_ORIGINS,
        "Access-Control-Allow-Methods": CORS_ALLOW_METHODS,
        "Access-Control-Allow-Headers": CORS_ALLOW_HEADERS,
        "Access-Control-Max-Age": CORS_MAX_AGE,
    })

def add_cors_headers(resp: Response) -> Response:
    resp.headers.setdefault("Access-Control-Allow-Origin", CORS_ALLOW_ORIGINS)
    resp.headers.setdefault("Vary", "Origin")
    return resp

async def proxy_post_root(request: Request):
    # Reenvía el JSON-RPC al FastMCP interno
    body = await request.body()
    headers = {
        "Content-Type": "application/json",
        # Respeta lo tiquismiquis del servidor interno:
        "Accept": request.headers.get("accept", "application/json, text/event-stream"),
    }
    # Reenvía también x-api-key / cookies si las hay
    if "x-api-key" in request.headers:
        headers["x-api-key"] = request.headers["x-api-key"]
    cookies = request.headers.get("cookie")

    async with httpx.AsyncClient(timeout=None) as client:
        r = await client.post(
            f"http://{INNER_HOST}:{INNER_PORT}/",
            content=body,
            headers=headers,
            cookies={} if not cookies else {c.split("=")[0].strip(): "=".join(c.split("=")[1:]) for c in cookies.split(";")}
        )
        # Passthrough JSON y cookies de sesión
        resp = Response(
            content=r.content,
            status_code=r.status_code,
            media_type=r.headers.get("content-type", "application/json")
        )
        if "set-cookie" in r.headers:
            resp.headers["set-cookie"] = r.headers["set-cookie"]
        return add_cors_headers(resp)

async def proxy_sse(request: Request):
    # Reenvía SSE manteniendo stream abierto
    headers = {
        "Accept": "text/event-stream",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
    }
    if "x-api-key" in request.headers:
        headers["x-api-key"] = request.headers["x-api-key"]
    cookies = request.headers.get("cookie")

    async def eventgen():
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream(
                "GET", f"http://{INNER_HOST}:{INNER_PORT}/sse",
                headers=headers,
                cookies={} if not cookies else {c.split("=")[0].strip(): "=".join(c.split("=")[1:]) for c in cookies.split(";")}
            ) as r:
                async for chunk in r.aiter_bytes():
                    yield chunk

    resp = StreamingResponse(eventgen(), media_type="text/event-stream", headers={
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "X-Accel-Buffering": "no",
    })
    return add_cors_headers(resp)

routes = [
    Route("/", preflight, methods=["OPTIONS"]),     # CORS preflight
    Route("/", proxy_post_root, methods=["POST"]),  # JSON-RPC
    Route("/sse", preflight, methods=["OPTIONS"]),
    Route("/sse", proxy_sse, methods=["GET"]),      # SSE
]
app = Starlette(routes=routes)

if __name__ == "__main__":
    # Para correr local:
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=PUBLIC_PORT, reload=False)