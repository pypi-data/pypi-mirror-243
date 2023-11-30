a = open(r"C:\Users\faizi\OneDrive\Рабочий стол\out.txt", "r")
res = []
for l in a.readlines():
    r = l.split("|")[0]
    try:
        r = int(r)
        res.append(r)
    except:
        pass

print(tuple(res))