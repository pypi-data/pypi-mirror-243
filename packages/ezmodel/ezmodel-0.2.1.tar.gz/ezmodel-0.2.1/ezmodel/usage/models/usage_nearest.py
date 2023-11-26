import matplotlib.pyplot as plt
import numpy as np

from ezmodel.models.knn import KNN
from ezmodel.util.sample_from_func import sine_function

nearest = KNN()

# create some data to test this model on
X, y, _X, _y = sine_function(20, 1000)

# let the model fit the data
nearest.fit(X, y)

# predict the data using the model
y_hat = nearest.predict(_X)

# predict the data using the model
_X = _X[np.argsort(_X[:, 0])]
y_hat = nearest.predict(_X)

plt.scatter(X, y, label="Data")
plt.plot(_X, y_hat, color="black", label="Nearest Neighbors")
plt.legend()
plt.show()
