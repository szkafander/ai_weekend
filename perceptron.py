#%% single-layer perceptron
import matplotlib.pyplot as pl
import numpy as np

from sklearn.datasets import make_classification

n_samples = 200
n_input_features = 2

# generate data
x, y = make_classification(
        n_samples=n_samples,
        n_features=n_input_features, 
        n_redundant=0, 
        n_informative=2,
        n_clusters_per_class=1,
        class_sep=0.5
    )

y = np.expand_dims(y, 1)

# perceptron class
class Perceptron:
    
    def __init__(
            self, 
            n_features: int = 2,
            n_outputs: int = 1
        ) -> None:
        self.n_features = n_features
        self.n_outputs = n_outputs
        self.weights = np.random.randn(n_features, n_outputs)
        self.biases = np.random.randn(1, n_outputs)
        self.activations = "uninitialized"
    
    def predict(self, x: np.ndarray) -> np.ndarray:
        self.activations = np.matmul(x, self.weights) + self.biases
        return sigmoid(self.activations)
    
    def train(self, x: np.ndarray, y: np.ndarray) -> None:
        pass

# plot data
def plot_preds(
        x: np.ndarray, 
        y: np.ndarray,
        model: Perceptron
    ) -> None:
    
    min_x_0 = min(x[:,0])
    max_x_0 = max(x[:,0])
    min_x_1 = min(x[:,1])
    max_x_1 = max(x[:,1])
    
    gx_0, gx_1 = np.meshgrid(
            np.linspace(min_x_0, max_x_0, 50),
            np.linspace(min_x_1, max_x_1, 50)
        )
    
    gx = np.c_[gx_0.ravel(), gx_1.ravel()]
    
    preds = model.predict(gx)
    
    pl.imshow(
            np.flipud(np.reshape(preds, gx_0.shape)),
            extent=[min_x_0, max_x_0, min_x_1, max_x_1]
        )
    
    y_ = y.flatten()
    
    pl.plot(
            x[y_==0, 0],
            x[y_==0, 1],
            "o"
        )
    pl.plot(
            x[y_==1, 0],
            x[y_==1, 1],
            "o"
        )

sigmoid = lambda x: 1 / (1 + np.exp(-x))
d_sigmoid_d_x = lambda x: sigmoid(x) * (1 - sigmoid(x))

# perceptron model
weights = np.random.randn(n_input_features, 1)

n_epochs = 100000
learning_rate = 0.01

perceptron = Perceptron(n_features=2, n_outputs=1)

#pl.subplot(1, 2, 1)
#plot_preds(x, y, perceptron)

y_ = y.ravel()

for i in range(n_epochs):
    
    # forward pass
    output = perceptron.predict(x)
    
    o_ = output.ravel()
    
    # error
    error = output - y
    
    # gradient
    delta_w = np.matmul(x.T, error * d_sigmoid_d_x(perceptron.activations))
    delta_b = np.sum(error)
    
    # descend
    perceptron.weights -= 1/n_samples * learning_rate * delta_w
    perceptron.biases -= 1/n_samples * learning_rate * delta_b
    
    if i % 3000 == 0:
        pl.subplot(1,2,1)
        pl.cla()
        plot_preds(x, y, perceptron)
        pl.subplot(1,2,2)
        pl.cla()
        pl.hist(output[y==0])
        pl.hist(output[y==1])
        pl.pause(0.01)

#pl.subplot(1, 2, 2)
#plot_preds(x, y, perceptron)