# server_gateway.py
import os
import json
import asyncio
from typing import Any, Callable, Dict, List, Optional

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, Response, StreamingResponse, PlainTextResponse
from starlette.routing import Route

# ------------------ Config CORS ------------------
CORS_ALLOW_ORIGINS = os.getenv("CORS_ALLOW_ORIGINS", "*")
CORS_ALLOW_METHODS = os.getenv("CORS_ALLOW_METHODS", "GET, POST, OPTIONS")
CORS_ALLOW_HEADERS = os.getenv("CORS_ALLOW_HEADERS", "Content-Type, Accept, x-api-key")
CORS_MAX_AGE = "86400"

def cors_headers() -> Dict[str, str]:
    return {
        "Access-Control-Allow-Origin": CORS_ALLOW_ORIGINS,
        "Access-Control-Allow-Methods": CORS_ALLOW_METHODS,
        "Access-Control-Allow-Headers": CORS_ALLOW_HEADERS,
        "Access-Control-Max-Age": CORS_MAX_AGE,
    }

def with_cors(resp: Response) -> Response:
    h = cors_headers()
    for k, v in h.items():
        resp.headers.setdefault(k, v)
    resp.headers.setdefault("Vary", "Origin")
    return resp

# ------------------ Registro de tools ------------------
TOOLS: Dict[str, Callable[..., Any]] = {}

def tool(name: str):
    def deco(fn: Callable[..., Any]):
        TOOLS[name] = fn
        return fn
    return deco

@tool("ping")
def ping(message: str) -> Dict[str, Any]:
    return {"ok": True, "message": message}

@tool("search_candidates")
def search_candidates(term: str = "") -> Dict[str, Any]:
    return {"results": [], "term": term}

# ------------------ JSON-RPC helpers ------------------
def jrpc_result(req_id: Any, result: Any) -> JSONResponse:
    return JSONResponse({"jsonrpc": "2.0", "id": req_id, "result": result})

def jrpc_error(req_id: Any, code: int, message: str, data: Any = "") -> JSONResponse:
    return JSONResponse({"jsonrpc": "2.0", "id": req_id, "error": {"code": code, "message": message, "data": data}}, status_code=400)

async def handle_initialize(req_id: Any, params: dict) -> JSONResponse:
    # Sin sesión: siempre OK
    result = {
        "protocolVersion": params.get("protocolVersion", "1.0"),
        "capabilities": params.get("capabilities", {}),
        "serverInfo": {"name": "stateless-mcp-gateway", "version": "1.0.0"},
    }
    return jrpc_result(req_id, result)

async def handle_tools_list(req_id: Any, params: dict) -> JSONResponse:
    out = []
    for name, fn in TOOLS.items():
        doc = (fn.__doc__ or "").strip()
        out.append({"name": name, "description": doc, "inputSchema": {"type": "object"}})
    return jrpc_result(req_id, {"tools": out})

async def handle_tools_call(req_id: Any, params: dict) -> JSONResponse:
    name = params.get("name")
    args = params.get("arguments") or {}
    if not name or name not in TOOLS:
        return jrpc_error(req_id, -32602, f"Unknown tool '{name}'")
    fn = TOOLS[name]
    try:
        if asyncio.iscoroutinefunction(fn):
            res = await fn(**args)
        else:
            res = fn(**args)
        return jrpc_result(req_id, {"content": res})
    except TypeError as e:
        return jrpc_error(req_id, -32602, "Invalid tool arguments", str(e))
    except Exception as e:
        return jrpc_error(req_id, -32000, "Tool execution error", str(e))

METHODS = {
    "initialize": handle_initialize,
    "tools/list": handle_tools_list,
    "tools/call": handle_tools_call,
}

# ------------------ ASGI handlers ------------------
async def preflight(_: Request):
    return with_cors(Response(status_code=204))

async def post_root(request: Request):
    # Acepta cualquier Accept; prioriza application/json
    try:
        body = await request.body()
        data = json.loads(body.decode("utf-8") or "{}")
    except Exception as e:
        return with_cors(jrpc_error("server-error", -32700, f"Parse error: {e}"))

    if not isinstance(data, dict):
        return with_cors(jrpc_error("server-error", -32600, "Invalid request: expected JSON object"))

    method = data.get("method")
    req_id = data.get("id")
    params = data.get("params", {})

    if not method or "jsonrpc" not in data:
        return with_cors(jrpc_error(req_id or "server-error", -32600, "Missing jsonrpc or method"))

    handler = METHODS.get(method)
    if not handler:
        return with_cors(jrpc_error(req_id, -32601, f"Method not found: {method}"))

    resp = await handler(req_id, params)
    return with_cors(resp)

async def sse(_: Request):
    async def gen():
        # Heartbeat cada 15s
        yield b": ok\n\n"
    return with_cors(StreamingResponse(gen(), media_type="text/event-stream", headers={
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "X-Accel-Buffering": "no",
    }))

routes = [
    Route("/", preflight, methods=["OPTIONS"]),
    Route("/", post_root, methods=["POST"]),
    Route("/sse", preflight, methods=["OPTIONS"]),
    Route("/sse", sse, methods=["GET"]),
]

app = Starlette(routes=routes)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("server_gateway:app", host="0.0.0.0", port=port)