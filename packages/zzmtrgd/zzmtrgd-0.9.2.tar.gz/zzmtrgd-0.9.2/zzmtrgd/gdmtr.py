import numpy as np
import pandas as pd


class GDMTR():
    def __init__(self, epochs = 500, learning_rate = 0.01, beta1 = 0.9, beta2 = 0, epsilon = 1e-8, t = 0, convergence = 1e-6, verbose = False):

        super(GDMTR, self).__init__()
        self.epochs = epochs
        self.learning_rate = learning_rate
        self.beta1 = beta1 
        self.beta2 = beta2
        self.epsilon = epsilon            
        self.t = t
        self.verbose = verbose
        self.history = []
        self.convergence_threshold = convergence
        self.weights = None
        self.bias = None
        self.n_features = None
        self.n_targets = None

    def l_history(self):
        return self.history    
    

    def adam_optimizer(self, weights, biases, gradients_w, gradients_b):

        # Initializing empty arrays
        m_w = np.zeros_like(weights)
        v_w = np.zeros_like(weights)
        m_b = np.zeros_like(biases)
        v_b = np.zeros_like(biases)
        
        self.t += 1

        # Update moments for weights
        m_w = self.beta1 * m_w + (1 - self.beta1) * gradients_w
        v_w = self.beta2 * v_w + (1 - self.beta2) * (gradients_w ** 2)

        # Update moments for biases
        m_b = self.beta1 * m_b + (1 - self.beta1) * gradients_b
        v_b = self.beta2 * v_b + (1 - self.beta2) * (gradients_b ** 2)

        # Bias correction
        m_w_hat = m_w / (1 - self.beta1 ** self.t)
        v_w_hat = v_w / (1 - self.beta2 ** self.t)
        m_b_hat = m_b / (1 - self.beta1 ** self.t)
        v_b_hat = v_b / (1 - self.beta2 ** self.t)

        # Update weights
        weights -= self.learning_rate * m_w_hat / (np.sqrt(v_w_hat) + self.epsilon)

        # Update biases
        biases -= self.learning_rate * m_b_hat / (np.sqrt(v_b_hat) + self.epsilon)

        return weights, biases    


    def fit(self, features, targets):
            
        # Checking input formats
        if isinstance(features, pd.DataFrame):
            features = features.values
        if isinstance(targets, pd.DataFrame):
            targets = targets.values
            
        # Initialize data shapes
        n_samples = features.shape[0] # Data points
        self.n_features = features.shape[1] # Features size
        self.n_targets = targets.shape[1] # Targets size
        
        # Initilize parameters
        w = np.zeros((self.n_features,self.n_targets)) # Weight matrix
        b = np.random.rand(self.n_targets) #Bias vector
        
        # Iterate training
        for epoch in range(self.epochs):

            # Make prediction
            y_pred = np.dot(features, w) + b

            # Calculating the loss (aRRMSE)
            rmse = np.sqrt(np.mean((targets - y_pred)**2))

            # Calculate Relative RMSE
            relative_rmse = rmse / np.sqrt(np.mean(targets**2))

            # Calculate Average Relative RMSE
            loss = np.mean(relative_rmse)
            
            # Calculate the gradients for each target variable
            dw = np.dot(features.T, (y_pred - targets)) / n_samples
            db = np.mean(y_pred - targets, axis=0)

            # Update parameters for each target variable
            self.weights, self.bias = self.adam_optimizer(w, b, dw, db)
            # Print the losses if verbose set to True
            if self.verbose == True:
                print(f'Epoch [{epoch}/{self.epochs}], Loss: {loss}')

            # Stop condition if reach convergence
            if epoch > 0 and np.abs(loss - self.history[-1]) < self.convergence_threshold:
                print(f"Converged after {epoch} iterations.")
                break
            self.history.append(loss) 

    def predict(self, x):
        y_pred = np.dot(x, self.weights) + self.bias
        #for i in range(self.n_targets):
            # Filling the prediction vector
            #y_pred.append(self.bias[i] + np.sum(x * self.weights[0][i]))
        return y_pred
        

    



