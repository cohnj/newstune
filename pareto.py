# import matplotlib
# matplotlib.use('Agg')
# import matplotlib.pyplot as plt 

def pareto_frontier(Xs, Ys, maxX = True, maxY = True):
# Sort the list in either ascending or descending order of X
    myList = sorted([[Xs[i], Ys[i]] for i in range(len(Xs))], reverse=maxX)
# Start the Pareto frontier with the first value in the sorted list
    p_front = [myList[0]]    
# Loop through the sorted list
    for pair in myList[1:]:
        if maxY: 
            if pair[1] >= p_front[-1][1]: # Look for higher values of Y…
                p_front.append(pair) # … and add them to the Pareto frontier
        else:
            if pair[1] <= p_front[-1][1]: # Look for lower values of Y…
                p_front.append(pair) # … and add them to the Pareto frontier
# Turn resulting pairs back into a list of Xs and Ys
    p_frontX = [pair[0] for pair in p_front]
    p_frontY = [pair[1] for pair in p_front]
    return p_frontX, p_frontY

# plt.scatter(Xs, Ys)
# plt.plot(p_frontX, p_frontY)
# plt.plot(x2, y2)
# plt.plot(x3, y3)
# plt.plot(x4, y4)
# plt.plot(x5, y5)
# plt.plot(x6, y6)
# plt.plot(x7, y7)
# plt.plot(x8, y8)
# plt.plot(x9, y9)
# plt.plot(x10, y10)
# plt.show()

#y=[2.56422, 3.77284,3.52623,3.51468,3.02199]
#z=[0.15, 0.3, 0.45, 0.6, 0.75]


# plt.scatter(p_frontX, p_frontY)
# plt.plot(p_frontX, p_frontY)

# n=[1,2,3,4,5,6,7,8,9,10][::-1]

# #fig, ax = plt.subplots()

# for i, txt in enumerate(n):
#     plt.annotate(txt, (p_frontX[i],p_frontY[i]))

# plt.show()

dominant = []
visited = []
for j in range(10):   
    Xs = [f[0] for f in filtered if f not in visited]
    Ys = [f[1] for f in filtered if f not in visited]
    p_frontX, p_frontY = pareto_frontier(Xs,Ys)
    for i in range(len(p_frontX)):
        for f in filtered:
            if f[0] == p_frontX[i] and f[1] == p_frontY[i] and f not in visited:
                median_score = f[0] * -1
                #median_score = 0
                if f[0] > 0.0 and f[1] > 0.0:
                    dominant.append((j,median_score,f[0],f[1],f[2]))
                visited.append(f)


dominant.sort()
for i in range(len(dominant)): print dominant[i][0],dominant[i][2],dominant[i][3],dominant[i][-1]
#for i in range(len(dominant)): print dominant[i][0],dominant[i][-1]


#dominant = list(set(dominant))
#dominant.sort()

# import matplotlib.pyplot as plt   
# Xs, Ys = # get your data from somewhere to go here
# # Find lowest values for cost and highest for savings
# p_front = pareto_frontier(Xs, Ys, maxX = False, maxY = True) 
# # Plot a scatter graph of all results
# plt.scatter(Xs, Ys)
# # Then plot the Pareto frontier on top
# plt.plot(p_front[0], p_front[1])
# plt.show()




