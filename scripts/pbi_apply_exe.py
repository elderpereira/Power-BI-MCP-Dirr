import asyncio, json, sys, os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Detecta o .exe na pasta "mcp-server" relativa à raiz da skill
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
MCP_EXE = os.path.join(SKILL_DIR, "mcp-server", "powerbi-modeling-mcp.exe")

# Fallback: caminho alternativo (VSCode extensions)
if not os.path.exists(MCP_EXE):
    HOME = os.path.expanduser("~")
    ALT_PATH = os.path.join(
        HOME, ".vscode", "extensions",
        "analysis-services.powerbi-modeling-mcp-0.4.0-win32-x64",
        "server", "powerbi-modeling-mcp.exe"
    )
    if os.path.exists(ALT_PATH):
        MCP_EXE = ALT_PATH

if not os.path.exists(MCP_EXE):
    print(f"ERRO: powerbi-modeling-mcp.exe não encontrado.")
    print(f"Procurado em: {MCP_EXE}")
    print(f"Solucao: copie o .exe para a pasta 'mcp-server/' junto com este script")
    sys.exit(1)

NAME = sys.argv[1] if len(sys.argv) > 1 else "Medida"
PATH = sys.argv[2] if len(sys.argv) > 2 else r"medida.dax"
MODE = sys.argv[3] if len(sys.argv) > 3 else "validate"
PORT = sys.argv[4] if len(sys.argv) > 4 else "54887"

expr = open(PATH, encoding="utf-8").read()

async def main():
    p = StdioServerParameters(command=MCP_EXE, args=["--start"])
    async with stdio_client(p) as (r, w):
        async with ClientSession(r, w) as s:
            await s.initialize()
            async def call(tool, req):
                res = await s.call_tool(tool, {"request": req})
                return "\n".join(getattr(c, "text", str(c)) for c in res.content)

            await call("connection_operations", {"operation": "Connect", "dataSource": "localhost:" + PORT})

            if MODE in ("validate", "both"):
                q = "EVALUATE ROW(\"h\", " + expr.strip() + ")"
                out = await call("dax_query_operations", {"operation": "Validate", "query": q})
                print("VALIDATE:", out[:1500])

            if MODE == "update":
                out = await call("measure_operations", {"operation": "Update", "definitions": [{"name": NAME, "tableName": "#Medidas", "expression": expr}]})
                print("UPDATE:", out[:800])

            if MODE == "render":
                q = "EVALUATE ROW(\"h\", " + expr.strip() + ")"
                out = await call("dax_query_operations", {"operation": "Execute", "query": q, "resultMode": "Inline", "timeoutSeconds": 120})
                d = json.loads(out)
                html = d["data"]["rows"][0]["[h]"][0]
                open(r"preview.html", "w", encoding="utf-8").write(html)
                print("RENDER OK")

asyncio.run(main())
