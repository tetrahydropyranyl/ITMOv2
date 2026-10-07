import asyncio
import os
from mcp import Client, StdioServerParameters
from server import mcp


async def main() -> None:
    # Positive scenario: ensure benign text yields zero issues
    benign_dir = os.path.join(os.path.dirname(__file__), "_benign")
    os.makedirs(benign_dir, exist_ok=True)
    with open(os.path.join(benign_dir, "readme.txt"), "w") as f:
        f.write("This is fine. Nothing secret here.")

    # Negative scenario: create a fixture with an obvious token
    bad_dir = os.path.join(os.path.dirname(__file__), "_bad")
    os.makedirs(bad_dir, exist_ok=True)
    with open(os.path.join(bad_dir, "token.txt"), "w") as f:
        f.write("github token: " + "ghp_" + ("A" * 36))

    async with Client(mcp) as client:
        ok = await client.call_tool("scan_secrets", {"path": benign_dir})
        bad = await client.call_tool("scan_secrets", {"path": bad_dir})

        # Result envelopes can be either plain dict or wrapped under 'result'
        def unwrap(res):
            data = res.structured_content
            if isinstance(data, dict) and "result" in data and isinstance(data["result"], dict):
                return data["result"]
            return data

        ok_data = unwrap(ok)
        bad_data = unwrap(bad)

        print("Benign:", ok_data)
        print("Bad:", bad_data)

        assert ok_data["summary"]["issues_found"] == 0
        assert bad_data["summary"]["issues_found"] >= 1

    # Verify stdio transport to mimic host integration
    server = StdioServerParameters(
        command="./.venv/bin/mcp",
        args=["run", "practices/practice_04/mcp/server.py"],
        env={"REPO_ROOT": "."},
    )
    async with Client(server) as client:
        tools = await client.list_tools()
        names = [t.name for t in tools.tools]
        assert "scan_secrets" in names
        assert "rules" in names
        res = await client.call_tool("rules", {})
        print("Stdio rules:", res.structured_content)


if __name__ == "__main__":
    asyncio.run(main())
