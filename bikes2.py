#http://blog.cambridgecoding.com/2016/01/10/from-simple-regression-to-multiple-regression-with-decision-trees/
import pandas as pd
from sklearn.tree import DecisionTreeRegressor
import numpy as np
 
bikes = pd.read_csv('bikes.csv')
regressor = DecisionTreeRegressor(max_depth=20)
regressor.fit(bikes[['temperature', 'humidity']], bikes['count'])

from sklearn.tree import export_graphviz
export_graphviz(regressor, out_file='tree2.dot', feature_names=['temperature','humidity'])

nx = 30
ny = 30
# creating a grid of points
x_temperature = np.linspace(-5, 40, nx) # min temperature -5, max 40
y_humidity = np.linspace(20, 80, ny) # min humidity 20, max 80
xx, yy = np.meshgrid(x_temperature, y_humidity)
# evaluating the regressor on all the points
z_bikes = regressor.predict(np.array([xx.flatten(), yy.flatten()]).T)
zz = np.reshape(z_bikes, (nx, ny))

from matplotlib import pyplot as plt
 
fig = plt.figure(figsize=(8, 8))
# plotting the predictions
plt.pcolormesh(x_temperature, y_humidity, zz, cmap=plt.cm.YlOrRd)
plt.colorbar(label='bikes predicted') # add a colorbar on the right
# plotting also the observations
plt.scatter(bikes['temperature'], bikes['humidity'], s=bikes['count']/25.0, c='g')
# setting the limit for each axis
plt.xlim(np.min(x_temperature), np.max(x_temperature))
plt.ylim(np.min(y_humidity), np.max(y_humidity))
plt.xlabel('temperature')
plt.ylabel('humidity')
#lt.show()

from sklearn.metrics import mean_absolute_error
print "mean absolute error (given data): ", mean_absolute_error(bikes['count'], regressor.predict(bikes[['temperature', 'humidity']]))

from sklearn.cross_validation import cross_val_score
scores = -cross_val_score(regressor, bikes[['temperature', 'humidity']],
bikes['count'], scoring='mean_absolute_error', cv=10)

print "Cross-Validation (some data not given): ", scores.mean()
