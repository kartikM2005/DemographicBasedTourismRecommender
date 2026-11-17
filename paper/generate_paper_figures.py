import os
os.environ["MPLCONFIGDIR"] = os.path.join(os.getcwd(), "paper")

import matplotlib.pyplot as plt
import numpy as np

def generate_benchmark_chart():
    models = ['Baseline KNN (k=5)', 'Decision Tree (CART)', 'Random Forest (B=100)', 'KNN-Stacking (Proposed)']
    accuracy = [77.03, 85.37, 85.57, 85.98]
    precision = [77.52, 85.34, 85.81, 86.06]
    recall = [77.03, 85.37, 85.57, 85.98]
    f1_score = [76.36, 85.25, 84.90, 85.62]

    x = np.arange(len(models))
    width = 0.18

    fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
    
    rects1 = ax.bar(x - 1.5*width, accuracy, width, label='Accuracy (%)', color='#612D53')
    rects2 = ax.bar(x - 0.5*width, precision, width, label='Precision (%)', color='#853953')
    rects3 = ax.bar(x + 0.5*width, recall, width, label='Recall (%)', color='#B85C6E')
    rects4 = ax.bar(x + 1.5*width, f1_score, width, label='F1-Score (%)', color='#DDA7A5')

    ax.set_ylabel('Performance Metric (%)', fontsize=11, fontweight='bold')
    ax.set_title('Comparative Evaluation: Standalone Baselines vs. Proposed KNN-Stacking Ensemble', fontsize=11, fontweight='bold', pad=12)
    ax.set_xticks(x)
    ax.set_xticklabels(models, fontsize=9.5, fontweight='bold')
    ax.set_ylim(70, 92)
    ax.legend(loc='upper left', frameon=True, framealpha=0.9, fontsize=9)
    ax.grid(axis='y', linestyle='--', alpha=0.5)

    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height:.1f}%',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=7.5, fontweight='semibold')

    autolabel(rects1)
    autolabel(rects2)
    autolabel(rects3)
    autolabel(rects4)

    plt.tight_layout()
    output_path = os.path.join("paper", "figure2_benchmark_comparison.png")
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"Generated {output_path}")

def generate_architecture_diagram():
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    ax.axis('off')

    boxes = [
        {"text": "1. User Input Vector\n(Age, Gender, Budget,\nDuration, Group, Season)", "pos": (0.08, 0.5), "color": "#EAD8E2", "edge": "#612D53"},
        {"text": "2. Preprocessing\n(Z-Score Scaling &\nCategorical Encoding)", "pos": (0.28, 0.5), "color": "#F3EBF0", "edge": "#853953"},
        {"text": "3. Level-0 Base Classifiers\n• KNN (k=5)\n• CART Decision Tree\n• Random Forest (B=100)", "pos": (0.49, 0.5), "color": "#E2E8F0", "edge": "#475569"},
        {"text": "4. Level-1 Meta-Learner\n(Logistic Regression\nStacking Optimization)", "pos": (0.71, 0.5), "color": "#FEF3C7", "edge": "#D97706"},
        {"text": "5. XAI Scoring &\nLive Telemetry\n• Weather/Hazards\n• Ranked Top-N List\n• Smart Budget Split", "pos": (0.92, 0.5), "color": "#D1FAE5", "edge": "#059669"}
    ]

    for b in boxes:
        x, y = b["pos"]
        ax.text(x, y, b["text"], ha='center', va='center', fontsize=8.5, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.7', facecolor=b["color"], edgecolor=b["edge"], linewidth=1.8))

    for i in range(len(boxes) - 1):
        x1 = boxes[i]["pos"][0] + 0.075
        x2 = boxes[i+1]["pos"][0] - 0.075
        ax.annotate('', xy=(x2, 0.5), xytext=(x1, 0.5),
                    arrowprops=dict(arrowstyle='->', lw=2, color='#612D53'))

    ax.set_title('Pipelined System Architecture: Context-Aware KNN-Stacking Tourism Recommendation Framework',
                 fontsize=11, fontweight='bold', pad=15)

    plt.tight_layout()
    output_path = os.path.join("paper", "figure1_architecture.png")
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"Generated {output_path}")

if __name__ == '__main__':
    generate_benchmark_chart()
    generate_architecture_diagram()
