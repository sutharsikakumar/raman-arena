import numpy as np
import matplotlib.pyplot as plt

models = ['a','b','c','d','e','f','g','h','i']

mos2_elo = [51.7, 86.8, 100.0, 49.0, 36.0, 65.2, 0.0, 64.6, 7.5]
graphene_elo = [36.1, 57.6, 79.1, 14.4, 100.0, 99.6, 0.0, 14.4, 57.6]
hbn_elo = [14.4, 95.2, 51.2, 100.0, 71.6, 71.2, 0.0, 21.2, 21.7]
wse2_elo = [35.3, 43.9, 51.1, 57.9, 100.0, 99.5, 5.2, 13.1, 43.5]

x = np.arange(len(models))
width = 0.2

plt.figure(figsize=(24, 12))

# 🎨 APPLY COLORS HERE
bars1 = plt.bar(x - 1.5*width, mos2_elo, width, label='MoS₂', color='#281C59')
bars2 = plt.bar(x - 0.5*width, graphene_elo, width, label='Graphene', color='#4E8D9C')
bars3 = plt.bar(x + 0.5*width, hbn_elo, width, label='h-BN', color='#85C79A')
bars4 = plt.bar(x + 1.5*width, wse2_elo, width, label='WSe₂', color='#EDF7BD')

plt.xlabel("Model")
plt.ylabel("ELO Rating")
plt.title("Raman Classification ELO Rankings by Model")

plt.xticks(x, models)
plt.legend()

# Start ELO line
plt.axhline(y=50, linestyle='--', color='gray')
plt.text(len(models)-1, 52, "Start ELO (50)", ha='right', fontsize=9)

# Value labels
def add_labels(bars):
    for bar in bars:
        height = bar.get_height()
        if height > 0:
            plt.text(
                bar.get_x() + bar.get_width()/2,
                height + 2,
                f"{int(height)}",
                ha='center',
                fontsize=8
            )

add_labels(bars1)
add_labels(bars2)
add_labels(bars3)
add_labels(bars4)

plt.tight_layout()
plt.show()