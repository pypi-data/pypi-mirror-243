import numpy as np
import math


class LinearRegression:
    def __init__(self, learning_rate=0.01, max_iters=10000, tolerance = 1e-10, optimization_method = "GradientDescent"):
        self.learning_rate = learning_rate
        self.max_iters = max_iters
        self.tolerance = tolerance
        self.om = optimization_method
        self.params = None

    def fit(self, X, y):
        
        if self.om == "GradientDescent":
          self.params = np.zeros(X.shape[1]+1)
          X = np.c_[np.ones((X.shape[0], 1)), X]
          perror = 0

          for _ in range(self.max_iters):
              gradient = X.T.dot(X.dot(self.params)-y)
              self.params -= self.learning_rate*gradient
              error = 0.5*(X.dot(self.params)-y).dot(X.dot(self.params)-y)
              if abs(perror-error) < self.tolerance:
                  break
              else:
                  perror = error

        elif self.om == "NormalEquations":
          X = np.c_[np.ones((X.shape[0], 1)), X]

          des = np.linalg.inv(X.T.dot(X)).dot(X.T.dot(y))
          self.params = des

    def predict(self, X):
        return X.dot(self.params[1:])+self.params[0]

  

class KMeans:
  def __init__(self, data, k, max_iters=100, tolerance=1e-4):
    def dist(p1, p2):
      return math.sqrt(np.sum((p1 - p2) ** 2))
    n_samples, n_features = data.shape
    centroids = data[np.random.choice(n_samples, k, replace=False)]
    old_centroids = np.zeros((k, n_features))
    labels = np.zeros(n_samples)

    for _ in range(max_iters):
      for i in range(n_samples):
        distances = [dist(data[i], centroid) for centroid in centroids]
        labels[i] = np.argmin(distances)

      old_centroids[:] = centroids

      for i in range(k):
        cluster_points = data[labels == i]
        if len(cluster_points) > 0:
          centroids[i] = np.mean(cluster_points, axis=0)

      if np.allclose(centroids, old_centroids, rtol=tolerance):
        break

    self.centroids = centroids
    self.labels = labels


def tokenizer(string, delimiter = " "):
  tokens = string.split(delimiter)
  return tokens

class LogarithmicRegression:
  def __init__(self, X, y):
    lnx = [math.log(i, math.e) for i in X]
    lny = [math.log(i, math.e) for i in y]

    slope = 0

    slope = (lny[0]-lny[-1])/(lnx[0]-lnx[-1])
    
    bias = sum(lny)/len(lny)-slope*sum(lnx)/len(lnx)
    self.a, self.b = slope, bias

  

class PolynomialRegression:
    def __init__(self, degree=2, learning_rate=0.001, max_iters=10000):
        self.degree = degree
        self.learning_rate = learning_rate
        self.max_iters = max_iters
        self.params = None

    def _create_polynomial_features(self, X):
        num_samples, num_features = X.shape
        poly_features = []

        for i in range(num_features):
            for j in range(self.degree + 1):
                poly_features.append(X[:, i]**j)

        return np.column_stack(poly_features)

    def _compute_gradient(self, X, y, y_pred):
        error = y_pred - y
        gradient = np.dot(X.T, error) / X.shape[0]
        return gradient

    def fit(self, X, y):
        X_poly = self._create_polynomial_features(X)
        self.params = np.random.randn(X_poly.shape[1])

        for _ in range(self.max_iters):
            y_pred = np.dot(X_poly, self.params)
            gradient = self._compute_gradient(X_poly, y, y_pred)
            self.params -= self.learning_rate * gradient

    def predict(self, X):
        X_poly = self._create_polynomial_features(X)
        return np.dot(X_poly, self.params)
    
def outliers(df, outlier_coefficient):
    XY = df.values

    dists = []

    for i in XY:
        dist = []
        for j in XY:
            if np.array_equal(i, j):
                continue
            mag = math.sqrt((i-j).dot(i-j))
            dist.append(mag)
        dists.append(dist)

    dists = np.array(dists)

    avg_dists = np.zeros(dists.shape[0])

    count = 0

    for i in dists:
        m = np.mean(i)
        avg_dists[count] = m
        count += 1

    q1 = np.percentile(avg_dists, 25)
    q3 = np.percentile(avg_dists, 75)

    IQR = q3-q1

    max_ = q3+outlier_coefficient*IQR

    count = 0

    indices = []

    for i in avg_dists:
        if i > max_:
            indices.append(count)
        count += 1

    return np.array(indices)