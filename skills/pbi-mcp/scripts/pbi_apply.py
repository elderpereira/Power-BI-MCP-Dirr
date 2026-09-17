import asyncio, json, os, sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

NAME = sys.argv[1] if len(sys.argv) > 1 else "Matriz Mensal CIM"
HERE = os.path.dirname(os.path.abspath(__file__))
PATH = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "medida_matriz.dax")
MODE = sys.argv[3] if len(sys.argv) > 3 else "validate"

expr = open(PATH, encoding="utf-8").read()

async def main():
    p = StdioServerParameters(command="npx.cmd",
        args=["-y", "@microsoft/powerbi-modeling-mcp@latest", "--start"])
    PORT = sys.argv[4] if len(sys.argv) > 4 else "51237"
    async with stdio_client(p) as (r, w):
        async with ClientSession(r, w) as s:
            await s.initialize()
            async def call(tool, req):
                res = await s.call_tool(tool, {"request": req})
                return "\n".join(getattr(c, "text", str(c)) for c in res.content)

            await call("connection_operations", {"operation": "Connect", "dataSource": "localhost:" + PORT})

            if MODE in ("validate", "both"):
                q = "EVALUATE ROW(\"h\", " + expr.strip() + ")"
                out = await call("dax_query_operations",
                                 {"operation": "Validate", "query": q, "timeoutSeconds": 60})
                print("VALIDATE:", out[:2500])

            if MODE in ("create", "both"):
                out = await call("measure_operations", {"operation": "Create", "definitions": [
                    {"name": NAME, "tableName": "#Medidas", "expression": expr}]})
                print("CREATE:", out[:1500])

            if MODE == "update":
                out = await call("measure_operations", {"operation": "Update", "definitions": [
                    {"name": NAME, "tableName": "#Medidas", "expression": expr}]})
                print("UPDATE:", out[:1500])

            if MODE == "render":
                q = "EVALUATE ROW(\"h\", " + expr.strip() + ")"
                out = await call("dax_query_operations",
                                 {"operation": "Execute", "query": q, "resultMode": "Inline",
                                  "timeoutSeconds": 120})
                d = json.loads(out)
                html = d["data"]["rows"][0]["[h]"]
                open(os.path.join(HERE, "preview.html"), "w", encoding="utf-8").write(html)
                print("RENDER OK, chars:", len(html))

asyncio.run(main())
