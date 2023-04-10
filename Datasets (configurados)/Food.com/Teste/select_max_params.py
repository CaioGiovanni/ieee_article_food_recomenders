import os, glob

maxPrecision, maxHR, maxF1 = 0.0, 0.0, 0.0
max_files = ['', '', '']
types_1 = ['Cosine', 'Euclidian']
types_2 = ['1.2', '1.3', '2.3']
initial_path = os.getcwd()

for x in range(1,6):
    for type_1 in types_1:
        for type_2 in types_2:
            os.chdir(initial_path)
            os.chdir(os.path.join(os.getcwd(), str(x), type_1, type_2))
            print(os.getcwd())
            for file in glob.glob("*.txt"):
                with open(file) as f:
                    line = f.readline()
                    line_splited = line.split("	")
                    if float(line_splited[6]) >= maxPrecision:
                        maxPrecision = float(line_splited[6])
                        max_files[0] = file + ' ||| ' + type_1 + ' ||| ' + type_2 + ' ||| ' + str(x)
                    if float(line_splited[7]) >= maxHR:
                        maxHR = float(line_splited[7])
                        max_files[1] = file + ' ||| ' + type_1 + ' ||| ' + type_2 + ' ||| ' + str(x)
                    if float(line_splited[8]) >= maxF1:
                        maxF1 = float(line_splited[8])
                        max_files[2] = file + ' ||| ' + type_1 + ' ||| ' + type_2 + ' ||| ' + str(x)

print(maxPrecision)
print(maxHR)
print(maxF1)
for x in max_files:
    print(x)

