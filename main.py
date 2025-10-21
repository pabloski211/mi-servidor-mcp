# server_proxy_stateless.py  (ASGI proxy + auto initialize)
import os, threading, json
from fastmcp import FastMCP
import httpx
from starlette.applications import Starlette
from starlette.responses import Response, StreamingResponse
from starlette.requests import Request
from starlette.routing import Route

INNER_HOST = "127.0.0.1"
INNER_PORT = int(os.getenv("INNER_PORT", "9000"))
PUBLIC_PORT = int(os.getenv("PORT", "8000"))

mcp = FastMCP("HR MCP Server")

@mcp.tool
def ping(message: str): return {"ok": True, "message": message}

def run_inner():
    mcp.run(transport="http", host=INNER_HOST, port=INNER_PORT, path="/")
threading.Thread(target=run_inner, daemon=True).start()

def cors_headers():
    return {
        "Access-Control-Allow-Origin": os.getenv("CORS_ALLOW_ORIGINS","*"),
        "Access-Control-Allow-Methods": os.getenv("CORS_ALLOW_METHODS","GET, POST, OPTIONS"),
        "Access-Control-Allow-Headers": os.getenv("CORS_ALLOW_HEADERS","Content-Type, Accept, x-api-key, x-session-id"),
        "Access-Control-Max-Age": "86400",
    }

async def preflight(_: Request):
    return Response(status_code=204, headers=cors_headers())

async def proxy_post_root(request: Request):
    body = await request.body()
    headers = {"Content-Type":"application/json","Accept":"application/json, text/event-stream"}
    if "x-api-key" in request.headers: headers["x-api-key"] = request.headers["x-api-key"]
    session_id = request.headers.get("x-session-id")
    cookies_hdr = request.headers.get("cookie")

    async with httpx.AsyncClient(timeout=None) as client:
        # 1) Si no hay cookie ni x-session-id → auto-initialize
        set_cookie = None
        if not cookies_hdr and not session_id:
            init_body = {
                "jsonrpc":"2.0","id":"init-auto","method":"initialize",
                "params":{"protocolVersion":"1.0","clientInfo":{"name":"proxy","version":"1.0"},"capabilities":{"tools":{"listChanged":True}}}
            }
            r0 = await client.post(f"http://{INNER_HOST}:{INNER_PORT}/", json=init_body, headers=headers)
            set_cookie = r0.headers.get("set-cookie")

        # 2) Ejecutar la request original contra el inner server
        r = await client.post(
            f"http://{INNER_HOST}:{INNER_PORT}/",
            content=body, headers=headers,
            cookies=None  # usamos Set-Cookie del paso 1 si lo hubo
        )

        # 3) Responder al cliente + CORS + sesión opcional
        resp = Response(r.content, status_code=r.status_code, media_type=r.headers.get("content-type","application/json"))
        h = cors_headers()
        for k,v in h.items(): resp.headers.setdefault(k,v)
        # si el inner nos dio cookie en init, pásala al cliente
        if set_cookie: resp.headers["set-cookie"] = set_cookie
        # opcional: proxyear un x-session-id sintético
        return resp

async def proxy_sse(request: Request):
    headers = {"Accept":"text/event-stream","Cache-Control":"no-cache","Connection":"keep-alive"}
    async def gen():
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream("GET", f"http://{INNER_HOST}:{INNER_PORT}/sse", headers=headers) as r:
                async for chunk in r.aiter_bytes(): yield chunk
    resp = StreamingResponse(gen(), media_type="text/event-stream", headers={"Cache-Control":"no-cache","Connection":"keep-alive","X-Accel-Buffering":"no"})
    for k,v in cors_headers().items(): resp.headers.setdefault(k,v)
    return resp

app = Starlette(routes=[
    Route("/", preflight, methods=["OPTIONS"]),
    Route("/", proxy_post_root, methods=["POST"]),
    Route("/sse", preflight, methods=["OPTIONS"]),
    Route("/sse", proxy_sse, methods=["GET"]),
])

# Run: uvicorn server_proxy_stateless:app --host 0.0.0.0 --port $PORT