import asyncio, json, os, sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

HERE = os.path.dirname(os.path.abspath(__file__))
PORT = sys.argv[1] if len(sys.argv) > 1 else "53307"

async def main():
    p = StdioServerParameters(command="npx.cmd",
        args=["-y", "@microsoft/powerbi-modeling-mcp@latest", "--start"])
    async with stdio_client(p) as (r, w):
        async with ClientSession(r, w) as s:
            await s.initialize()
            await s.call_tool("connection_operations", {"request": {
                "operation": "Connect", "dataSource": "localhost:" + PORT}})
            NAME = sys.argv[2] if len(sys.argv) > 2 else "Dashboard CIM HTML"
            res = await s.call_tool("measure_operations", {"request": {
                "operation": "Get",
                "references": [{"name": NAME, "tableName": "#Medidas"}]}})
            txt = "\n".join(getattr(c, "text", str(c)) for c in res.content)
            open(os.path.join(HERE, "medida_atual.json"), "w", encoding="utf-8").write(txt)
            print("len:", len(txt))
            print(txt[:6000])

asyncio.run(main())
