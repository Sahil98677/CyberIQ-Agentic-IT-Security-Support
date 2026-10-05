from backend.router import heuristic_route


def test_network_route():
    result = heuristic_route("My VPN is not connecting")
    assert "network" in result["intents"]


def test_security_route():
    result = heuristic_route("I received a suspicious login alert")
    assert "security" in result["intents"]


def test_multi_intent_route():
    result = heuristic_route("My VPN is not connecting and I received a suspicious login alert")
    assert set(result["intents"]) == {"network", "security"}
    assert result["priority"] == "high"
