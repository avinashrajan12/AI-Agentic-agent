"""Generates docs/schema.png (architecture diagram). Run: python docs/make_schema.py"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(figsize=(10, 6)); ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 6)
def box(x, y, w, h, t, c):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05", fc=c, ec="black"))
    ax.text(x+w/2, y+h/2, t, ha="center", va="center", fontsize=9)
def arrow(x1, y1, x2, y2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="->", lw=1.5))
box(0.3, 2.5, 1.8, 1, "User\n(CLI input)", "#cfe8ff")
box(3.0, 2.5, 2.2, 1, "Agent Loop\n(Plan-Act-Observe)", "#ffe9a8")
box(6.2, 4.2, 3.4, 1, "LLM: Claude API\n(reasoning + tool selection)", "#d6f5d6")
box(6.2, 2.5, 3.4, 1, "Tool Executor", "#f5d6f5")
box(6.2, 0.3, 1.6, 1.4, "Calculator\nDateTime\nWikipedia", "#eeeeee")
box(8.0, 0.3, 1.6, 1.4, "Notes\n(Long-term\nmemory)", "#eeeeee")
box(3.0, 0.5, 2.2, 1, "Short-term memory\n(messages list)", "#eeeeee")
arrow(2.1, 3.0, 3.0, 3.0); arrow(5.2, 3.2, 6.2, 4.4); arrow(6.2, 4.2, 5.2, 3.3)
arrow(5.2, 3.0, 6.2, 3.0); arrow(7.0, 2.5, 7.0, 1.7); arrow(8.6, 2.5, 8.6, 1.7)
arrow(4.1, 2.5, 4.1, 1.5)
ax.text(5, 5.7, "Agentic AI Agent - Architecture", ha="center", fontsize=13, weight="bold")
plt.savefig("docs/schema.png", dpi=150, bbox_inches="tight")
