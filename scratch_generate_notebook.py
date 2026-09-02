import json
import os

notebook = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# Dataset Explorer\n",
                "This notebook provides interactive exploration of the synthetic lunar dataset."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import cv2\n",
                "import matplotlib.pyplot as plt\n",
                "from src.visualization.pair_visualizer import PairVisualizerSuite\n",
                "from src.visualization.quality_metrics import QualityAssessor\n",
                "\n",
                "# Assuming dataset is located in 'data/synthetic/'\n",
                "pair_id = 'pair_001'\n",
                "source = cv2.imread(f'data/synthetic/{pair_id}/source.png')\n",
                "reference = cv2.imread(f'data/synthetic/{pair_id}/reference.png')\n",
                "\n",
                "# Compute quality metrics\n",
                "qa = QualityAssessor()\n",
                "metrics = qa.assess_pair(source, reference)\n",
                "for k, v in metrics.items():\n",
                "    print(f'{k}: {v:.2f}')\n"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "vis = PairVisualizerSuite(output_dir='results/visualizations')\n",
                "out_path = vis.create_comparison_grid(source, reference, pair_id)\n",
                "grid_img = cv2.imread(out_path)\n",
                "plt.figure(figsize=(15, 15))\n",
                "plt.imshow(cv2.cvtColor(grid_img, cv2.COLOR_BGR2RGB))\n",
                "plt.axis('off')\n",
                "plt.show()\n"
            ]
        }
    ],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

os.makedirs('notebooks', exist_ok=True)
with open('notebooks/dataset_explorer.ipynb', 'w') as f:
    json.dump(notebook, f, indent=4)

print("Notebook generated successfully.")
