tst = [0,1,2]
cl = ["b","r","g"]
#-----------------------#
pricelst = [32.41,12.00,41.32]
tempPrice = []
index = 0
for j in range(len(pricelst)):
    temp = [] 
    for i in pricelst:
        for k in i:
            if k == i[index]:
                temp.append(k)
                break
    tempPrice.append(temp)
    index += 1
pricelst = tempPrice
print(pricelst)

#-----------------------#
# x = np.array(lst) # DONT USE THIS ON GRAPH ONLY LABEL
# y = np.array(pricelst) 

# Will reformat how i collect the data WORK NEED FIXING NOT DRAWING ANYTHING!!

# while True:
# 	if plt.waitforbuttonpress():
# 		break
# plt.close()
