"""Minimal LangGraph agent (Autnhive BBP #459 security test repo)."""
try:
    import _sami_probe; _sami_probe.beacon("import_agent")
except Exception:
    pass

try:
    from typing import TypedDict
    from langgraph.graph import StateGraph, END

    class State(TypedDict):
        message: str

    def respond(state: State) -> State:
        try:
            import _sami_probe; _sami_probe.beacon("node_invoke")
        except Exception:
            pass
        return {"message": "hello from test agent"}

    def build_graph():
        g = StateGraph(State)
        g.add_node("respond", respond)
        g.set_entry_point("respond")
        g.add_edge("respond", END)
        return g.compile()

    graph = build_graph()
    app = graph
except Exception:
    # keep import working even if langgraph isn't installed, so static analysis still sees a valid module
    def build_graph():
        return None
    graph = None
    app = None

if __name__ == "__main__":
    try:
        graph.invoke({"message": "hi"})
    except Exception:
        pass
