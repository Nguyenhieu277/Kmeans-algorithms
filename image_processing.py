import matplotlib.pyplot as mpl
import numpy as np
from sklearn.cluster import KMeans

img = mpl.imread("a.jpg")

height = img.shape[0]
width = img.shape[1]

img = img.reshape(width * height, 3)

K = int(input())
kmeans = KMeans(n_clusters=K).fit(img)
labels = kmeans.predict(img)
clusters = kmeans.cluster_centers_

newImg = np.zeros_like(img)
for i in range(len(newImg)):
    newImg[i] = clusters[labels[i]]

newImg = newImg.reshape(height, width, 3)
mpl.imshow(newImg)
mpl.show()