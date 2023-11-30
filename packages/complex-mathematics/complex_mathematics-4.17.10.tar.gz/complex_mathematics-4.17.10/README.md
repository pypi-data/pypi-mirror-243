# complex_mathematics

![Version](https://img.shields.io/badge/version-4.15.8-blue)

---

**complex_mathematics is a Python module that can be used for many complex math related problems, with concepts from many different topics in mathematics, such as calculus, linear algebra, geometry, algebra, statistics, and more. It also has machine learning algorithms such as linear regression and K-Nearest-Neighbors.**

---

**To get started:**

Install with:

`pip install complex_mathematics`

---

**Linear Algebra:**

`from complex_mathematics.linalg import BLANK`

Eigenvectors:

The eigenvector class has one parameter, the matrix

The eigenvalues attribute holds the eigenvalues

The eigenvectors attribute holds the eigenvectors

```
from complex_mathematics.linalg import eigenvector
import numpy as np

mat = np.array([[1, 0, 0], [0, 2, 0], [0, 0, 3]])

eig = eigenvector(mat) #eigenvector(matrix)

print(eig.eigenvalues)
print(eig.eigenvectors)
```

Matrix Inverse:

The matrix inverse function has one parameter, the matrix

It returns the inverse

```
from complex_mathematics.linalg import inverse
import numpy as np

matrix = np.array([[1, 2], [3, 4]])

inv = inverse(matrix)

print(inv)
```

---

**Machine Learning:**

`from complex_mathematics.ml import BLANK`

Linear Regression:

The LinearRegression class has four parameters, the learning rate with a default 0.01, the max iterations with a default 10000, the tolerance, and optimization method with a default of batch gradient descent

Batch Gradient Descent:

```
import numpy as np
import random
from complex_mathematics.ml import LinearRegression


X = np.array([[i] for i in range(-50, 51)])
y = np.array([2*i + 1 + random.uniform(-1, 1) for i in range(-50, 51)])

model = LinearRegression(learning_rate = 0.00001)

model.fit(X, y)

print(model.predict(np.array([10])))
```

Normal Equations:

```
import numpy as np
import random
from complex_mathematics.ml import LinearRegression
    

X = np.array([i for i in range(-50, 51)])
y = np.array([2*i + 1 + random.uniform(-1, 1) for i in range(-50, 51)])

model = LinearRegression(optimization_method = "NormalEquations")

model.fit(X, y)

print(model.predict(np.array([10])))
```

K-Means Clustering:

The KMeans class has four parameters, the dataset, the number of centroids(k), the max iterations, with a default of 100, and the tolerance, with a default of 10^-4

```
from complex_mathematics.ml import KMeans
import numpy as np

data = np.array([
    [2, 3, 4],
    [3, 5, 6],
    [4, 4, 5],
    [2, 6, 3],
    [7, 2, 1],
    [6, 4, 2],
    [8, 5, 4],
    [9, 4, 3]
])

model = KMeans(data, 6) #KMeans(data, k, max_iters=100, tolerance=1e-4)

print(model.centroids, model.labels)
```

Tokenizer:

The tokenizer function has two parameters, the string that will be tokenized, and the delimiter, with a default of " "

```
from complex_mathematics.ml import tokenizer

print(tokenizer("This should have 5 tokens")) #tokenizer(string, delimiter = " ")
```

Logarithmic Regression:

Logarithmic regression fits a logarithmic line to data, of the form f(x) = a*ln(x)+b

Unfortunately, for now, the class only takes in two dimensional lists, so for those of you wanting to use numpy arrays and multi-dimensional datasets, sorry

It takes in two parameters, the x values and the y values

```
from complex_mathematics.ml import LogarithmicRegression


X = [2, 3, 4, 5, 6]
y = [0.117, 0.152, 0.193, 0.232, 0.266]

model = LogarithmicRegression(X, y)
print(model.a, model.b)
```

Polynomial Regression:

Polynomial regression fits an n degree polynomial function

The PolynomialRegression class has three parameters, the degree, the learning rate with a default 0.001, and the max iterations with a default 10000

```
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from complex_mathematics.ml import PolynomialRegression

np.random.seed(0)
X = np.random.rand(80, 2)
y = np.sum(X, axis=1) + np.random.normal(0, 0.1, X.shape[0])

poly_reg = PolynomialRegression(degree=2)

poly_reg.fit(X, y)

x1_test = np.linspace(0, 1, 20)
x2_test = np.linspace(0, 1, 20)
X1_test, X2_test = np.meshgrid(x1_test, x2_test)
X_test = np.column_stack((X1_test.ravel(), X2_test.ravel()))

y_pred = poly_reg.predict(X_test)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
scatter = ax.scatter(X[:, 0], X[:, 1], y, c='gray', label='Actual Data')

surface = ax.plot_surface(X1_test, X2_test, y_pred.reshape(X1_test.shape), color='red', alpha=0.5, label='Polynomial Regression')

ax.set_xlabel('Feature 1')
ax.set_ylabel('Feature 2')
ax.set_zlabel('Target')

plt.show()
```

---

**Algebra:**

`from complex_mathematics.algebra import BLANK`

Quadratic Equation Solver:

The quadratic function has one parameter, the equation in string form

It returns the solutions in a numpy array

```
from complex_mathematics.algebra import quadratic

print(quadratic("-x^2-x+12"))
```

Polynomial Solver:

The polynomial solver has one parameter, a numpy array of the coefficients of the equation

It returns the solutions in a numpy array

```
import numpy as np
from complex_mathematics.algebra import solve

coefs = np.array([1, 0, -16])

print(solve(coefs)) #solve(coefs, step=0.01, tolerance=1e-8, srange=100)
```

Natural Log:

The natural log function takes in one parameter, the number

```
from complex_mathematics.algebra import ln

print(ln(15))
```

E to the x power:

The exp() function takes in one parameter, the number

```
from complex_mathematics.algebra import exp

print(exp(3))
```

Common Logarithm:

The log() function takes in one parameter, the number

```
from complex_mathematics.algebra import log

print(log(3))
```

Parametric Equation Grapher:

The parametric_graph() function takes in 4 parameters, the x function, the y function, the t minimum, and the t maximum.

```
from complex_mathematics.algebra import parametric_graph
import numpy as np

def x(t):
  return ((np.cos(t))**3)*(5*(np.sin(t))**2-(np.cos(t))**2)

def y(t):
  return ((np.sin(t))**3)*(5*(np.cos(t))**2-(np.sin(t))**2)

parametric_graph(x, y, 0, 6.28)
```

---

**Statistics:**

`from complex_mathematics.stats import BLANK`

Percent Change:

The percent change function has two parameters, the previous value and the new value

It returns the percent change

```
from complex_mathematics.stats import pchange

print(pchange(100, 110)) #pchange(a, b)
```

Mean:

The mean function has one parameter, the data

It returns the mean of the data

```
import numpy as np
from complex_mathematics.stats import mean

a = np.array([5, 15, 20, 25])

print(mean(a)) #mean(data)
```

Median:

The median function has one parameter, the data

It returns the median of the data

```
import numpy as np
from complex_mathematics.stats import median

a = np.array([5, 15, 20, 25])

print(median(a)) #median(data)
```

Standard Deviation:

The standard deviation function has one parameter, the data

It returns the standard deviation of the data

```
import numpy as np
from complex_mathematics.stats import sd

print(sd(np.array([1, 2, 4, 8, 16]))) #sd(data)
```

Factors:

The factor function has one parameter, the number that is to be factored

It returns a numpy array of the factors of that number

It includes negative factors

```
from complex_mathematics.stats import factor

print(factor(80))
```

Gaussian Calculator:

The gaussian function takes in one parameter, the data, and gives you function that calculates the probability of a number appearing based on the frequency of numbers in the data.

```
from complex_mathematics.stats import gaussian
import numpy as np
import matplotlib.pyplot as plt


data = np.array([1, 2, 2, 3, 3, 3, 4, 4, 5])

p = gaussian(data)

x = np.arange(0, 6, 0.1) 

y = np.apply_along_axis(p, 0, x)

plt.plot(x, y)

plt.show()
```

---

**Complex Numbers:**

`from complex_mathematics.complex import BLANK`

Complex Number:

The complex number class has two parameters, the real part and the imaginary part

It has three functions: mod(), which gives the modulus of the number; arg(), which gives the argument of the number; and conjugate(), which gives the conjugate of the number.

```
from complex_mathematics.complex import complex

num = complex(4, 6)

print(num.mod())
print(num.arg())
print(num.conjugate())
```

Complex Multiplication:

The complex multiplication function has two parameters, the two complex numbers that will be multiplied.

```
from complex_mathematics.complex import complex
from complex_mathematics.complex import cmultiply

num1 = complex(4, 6)
num2 = complex(1, 2)

res = cmultiply(num1, num2)

print(res.a, res.bi)
```

<!-- LICENSE -->
## License

Distributed under the MIT License. See [LICENSE](https://github.com/Arnav-MaIhotra/complex_mathematics/blob/main/LICENSE) for more information.
