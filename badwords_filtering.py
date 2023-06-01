ko_data = []

def get_data(filename):
    global ko_data
    
    with open("./DB/" + filename, encoding='UTF-8') as f:
        lines = f.readlines()
    data = []
    for d in lines:
        data.append(d.strip())
    data.sort(key= lambda x : len(x))
    ko_data = data

def bad2star(line):
    global ko_data
    
    used_badword = []
    for badword in ko_data:
        if badword in line:
            line = line.replace(badword,'*'*len(badword))
            used_badword.append(badword)
    return (line, used_badword)
