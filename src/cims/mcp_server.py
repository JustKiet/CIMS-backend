from cims.tools.area import AreaToolset
from cims.tools.field import FieldToolset
from cims.tools.level import LevelToolset
from cims.tools.expertise import ExpertiseToolset
from cims.tools.candidate import CandidateToolset
from cims.tools.customer import CustomerToolset
from cims.tools.project import ProjectToolset
from cims.config import settings

from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    name="CIMS (Candidate Information Management System) MCP Toolkit",
    host=settings.MCP_HOST,
    port=settings.MCP_PORT,
)

mcp.add_tool(
    fn=AreaToolset.get_areas,
)

mcp.add_tool(
    fn=FieldToolset.get_fields,
)

mcp.add_tool(
    fn=LevelToolset.get_levels,
)

mcp.add_tool(
    fn=ExpertiseToolset.get_expertises,
)

mcp.add_tool(
    fn=CandidateToolset.get_candidates,
)

mcp.add_tool(
    fn=CandidateToolset.get_candidate,
)

mcp.add_tool(
    fn=CustomerToolset.get_customers,
)

mcp.add_tool(
    fn=CustomerToolset.get_customer,
)

mcp.add_tool(
    fn=ProjectToolset.get_projects,
)

mcp.add_tool(
    fn=ProjectToolset.get_project,
)

mcp.add_tool(
    fn=CandidateToolset.search_candidates,
)

mcp.add_tool(
    fn=CustomerToolset.search_customers,
)

mcp.add_tool(
    fn=ProjectToolset.search_projects,
)

if __name__ == "__main__":
    mcp.run(transport="sse")