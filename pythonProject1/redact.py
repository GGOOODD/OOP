import re

with open("test.txt", encoding="UTF-8") as f:
    lines = f.readlines()

pattern = re.compile("^[а-я]{13,50}$")
with open("test.txt", "w") as f:
    for line in lines:
        result = pattern.search(line)
        if result is None:
            f.write(line)
