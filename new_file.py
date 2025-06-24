with open("cases.txt", "r") as file:
    content = file.read()
words = content.strip().split() 
result = {}
case_num = None #number of the current case
is_case = False 
for w in words:
    if w == "CASE":
        is_case = True
        continue
    if is_case:
        case_num = w.lstrip("#")  # strip the #
        result[case_num] = ""  #adds the number of the chapter and it's value to the dictionary
        is_case = False
        continue
    if case_num:
        result[case_num] += " " + w
    
for num, text in result.items():
    print(f"Case {num}: {text[:60]}...")




