my_file = open("file.txt", "w+")

for i in range(1500):
    my_file.write(str(i)+'\n')
