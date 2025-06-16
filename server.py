from mcp.server.fastmcp import FastMCP
from mock_confluence_service import pages

mcp = FastMCP()


@mcp.tool()
def get_confluence_page_by_id(page_id: str) -> str:
    """
    Use this tool to get the content of a Confluence page given its id.
    This page contains information about the team's projects, their status, tech stack, etc.

    Args:
        page_id (str): The id of the Confluence page to get.

    Returns:
        str: The content of the Confluence page.
    """
    # get the page from the pages list
    page = next((page for page in pages if page["id"] == page_id), None)
    if page:
        return page["content"]
    else:
        return f"Page with id {page_id} not found."


@mcp.tool()
def get_confluence_pages() -> list[dict]:
    """
    Use this tool to get the list of pages in the Confluence instance.
    These pages contain information about the team's projects, their status, tech stack, etc.
    
    Returns:
        list[dict]: A list of Confluence pages with their id and title.
    """
    return [{"id": page["id"], "title": page["title"]} for page in pages]
