from mcp.server.fastmcp import FastMCP

# Serveur MCP HTTP autonome pour les vols
# Pour le lancer séparément : python mcp_http_server.py
# (utilisé comme alternative à agentMCPDistant.py qui l'incorpore en interne)

mcp = FastMCP("travel_server", host="127.0.0.1", port=8000)


@mcp.tool()
def search_flights(origin: str, destination: str, date: str) -> str:
    """Search for available flights between two cities on a given date."""
    return (
        f"Flights from {origin} to {destination} on {date}:\n"
        f"- AT 601 | 08:00 → 09:15 | Direct | 850 MAD\n"
        f"- AT 603 | 14:30 → 15:45 | Direct | 920 MAD\n"
        f"- AT 605 | 19:00 → 20:15 | Direct | 780 MAD"
    )


@mcp.tool()
def get_flight_price(flight_number: str) -> str:
    """Get the price and details of a specific flight."""
    prices = {
        "AT 601": "850 MAD - Economy class, 1 bag included",
        "AT 603": "920 MAD - Economy class, 1 bag included",
        "AT 605": "780 MAD - Economy class, carry-on only",
    }
    return prices.get(flight_number, f"Flight {flight_number} not found")


if __name__ == "__main__":
    print("Démarrage du serveur MCP HTTP sur http://127.0.0.1:8000/mcp ...")
    mcp.run(transport="streamable-http")