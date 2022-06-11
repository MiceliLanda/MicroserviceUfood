
# # def solution(n):
# # 	num_list = list(str(n))
# # 	a = 0
# # 	print(num_list)
# # 	for i in num_list:
# # 		a+=int(i)
# # 	# print(a)

# # solution(29)

# # def solution(a, b, k):
# # 	c = list(reversed(b))
# # 	c = str(c)
# # 	b = str(b)
# # 	cont = 0
# # 	data = 0
# # 	for i in range(len(b)):
# # 		print([i])

# def solution(a, b, k):
# 	c = list(reversed(b))
# 	cont = 0
# 	data = 0
# 	for i in range(len(c)):
# 		data = str(a[i])+  str(c[i])
# 		print(data)
# 		if int(data) < k:
# 			cont += 1
# 	return cont

# a=[16, 1, 4, 2, 14]
# b= [7, 11, 2, 0, 15]
# k= 743

# solution(a,b,k)


# matrix = [[9, 7, 4, 5], [1, 6, 2, -6], [12, 20, 2, 0], [-5, -6, 7, -2]]

# def solution(arr):
#     newString = ''
#     for i in range(len(arr)):
#         temp = list(arr[i])
#         test = temp[1::]
#         arr[i]=test[1::]
#         newString+=temp[0]
#         print(newString)


arr = (["Daisy", "Rose", "Hyacinth", "Poppy"])
# solution(arr)
# obtain first letter from each string in the list and put them in a new list for the list is empty
# for i in range(len(arr)):
""" cont = 0
newString = ''
while True:
    if arr[cont]:
        newString+=arr[cont][0]
        arr[cont]=arr[cont][1::]
        cont+=1
        # print(arr,newString)

        if cont == len(arr):
            cont=0
    elif arr[cont]:
        arr.pop(cont)
    else:
        break
print(newString) """

# matrix= [[9, 7, 4, 5, 3],
#         [1, 6, 2, -6, 2],
#         [12, 20, 2, 0, 1],
#         [-5, -6, 7, -2, 0],
#         [1, 6, 2, -6, 2]]

matrix= [[9, 1, 2, 0],
        [8, 4, 3, 1]]


#extract only border of matri4

a = [matrix[0][1:3],matrix[1][1:3]]
import numpy as np# 
print(a)
lista2 = [4,2,3,1]

lista = np.reshape(sorted(lista2),(2,2))
print(lista)


