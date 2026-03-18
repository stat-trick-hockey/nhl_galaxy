import json
import numpy as np
import umap
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans
import os

# Ensure output folder exists
os.makedirs("docs", exist_ok=True)

goals = json.load(open("data/goals.json"))

shot_types = [g.get("shotType") or "unknown" for g in goals]

enc = LabelEncoder()
enc.fit(shot_types)

X = []
for g in goals:
    X.append([
        g.get("x") or 0,
        g.get("y") or 0,
        enc.transform([g.get("shotType") or "unknown"])[0],
        g.get("period") or 0
    ])

X = np.array(X)

reducer = umap.UMAP(n_components=3, random_state=42)
embedding = reducer.fit_transform(X)

kmeans = KMeans(n_clusters=8, random_state=42)
clusters = kmeans.fit_predict(embedding)

for i, g in enumerate(goals):
    g["gx"] = float(embedding[i][0])
    g["gy"] = float(embedding[i][1])
    g["gz"] = float(embedding[i][2])
    g["cluster"] = int(clusters[i])

with open("docs/embedded_goals.json", "w") as f:
    json.dump(goals, f)

print("Galaxy data saved to docs/embedded_goals.json")
