import matplotlib.pyplot as plt

#f = open('input.txt', 'r')
f = open('export_elpho_drug_ISZ.txt', 'r')
#f = open('export elpho drug ISZ+RIF.txt', 'r')
pairs = f.readlines()
x_axis = []
y_axis = []

for pair in pairs:
    values = pair.split()
    x_axis.append(float(values[0]))
    y_axis.append(float(values[1]))

plt.plot(x_axis, y_axis)
plt.show()
