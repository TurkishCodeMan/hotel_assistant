from IPython.display import Image, display
from langchain_core.runnables.graph import CurveStyle, MermaidDrawMethod, NodeStyles
from agent_graph.graph import build_graph

# Grafiği oluştur
workflow = build_graph()
graph = workflow.get_graph()

# Mermaid kaynak kodunu al ve dosyaya yaz
mermaid_source = graph.draw_mermaid()
with open("graph_source.md", "w") as f:
    f.write(mermaid_source)

print("Grafik kaynak kodu 'graph_source.md' dosyasına kaydedildi.")
print("\nMermaid kaynak kodu:")
print(mermaid_source)