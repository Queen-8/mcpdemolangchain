from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


@mcp.tool()   
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

# The transport is the protocol that the MCP server will use to communicate with the client.
# In this case, we are using the stdio transport, which is a simple text-based protocol that allows the MCP server to communicate with the client over the console.
# The transport="stdio" argument tells the MCP server to use the stdio transport.
# Use standard input and output(stdin and stdout) to receive and respond to tool function calls.
if __name__ == "__main__":
    # run the MCP server with stdio transport 
    mcp.run(transport="stdio")  