import matplotlib.pyplot as plt
f = open("spiny_L=10,T=1.txt", "r")
print(f.readlines()[100])
plt.imshow(f.readlines()[100])
