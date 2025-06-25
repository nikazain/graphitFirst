import re
import json

with open("cases.txt", "r") as file:
    content = file.read()
words = content.strip().split() 
result = {}
case_num = None #number of the current case
is_case = False 
current_section = None #tracks the section that we are in
is_rombik = False

for w in words:
    if w == "CASE":
        is_case = True
        continue
    if is_case:
        case_num = w.lstrip("#")  # strip the #
        result[case_num] = {
            "Project Description": "",
            "Cover Letter Sent": "",
            "Chat History": ""
        } 
        current_section = None #reset the current section
        is_case = False
        continue
    if w == "###":
        is_rombik = True
        continue
    if "Description:" in w:
        current_section = "Project Description"
        is_rombik = False
        continue
    elif "Sent:" in w:
        current_section = "Cover Letter Sent"
        is_rombik = False
        continue
    elif "History:" in w:
        current_section = "Chat History"
        is_rombik = False
        continue
    if is_rombik:
        continue
    if case_num and current_section:
        result[case_num][current_section] += " " + w

for num, data in result.items():
    for section, text in data.items():
        if section != "Chat History":
            continue

        words = text.strip().split()
        # words.append("00:00")
        messages = []
        speaker = ""
        msg_collect = ""
        after_timestamp = False
        prev = [] 
        
        for w in words:
            if re.fullmatch(r"\d{1,2}:\d{2}", w) and len(prev) >= 2: 
                    if speaker: # basically if a speaker exists
                        msg_clean = re.sub(r"^(AM|PM)\s+", "", ' '.join(msg_collect.strip().replace('--- ##', '').strip().split()[:-2]))
                        messages.append(f"{speaker}: {msg_clean}")
                    speaker = f"{prev[-2]} {prev[-1]}"
                    msg_collect = ""
                    prev = []
            elif speaker: #runs if the current code is not a timestamp and if speaker is set
                msg_collect += " " + w
            prev.append(w)
            if len(prev) > 2:
                prev.pop(0)
        if msg_collect:
            msg_clean = re.sub(r"^(AM|PM)\s+", "", msg_collect.strip().replace('--- ##', '').strip())
            messages.append(f"{speaker}: {msg_clean}")
         
        data["Chat History"] = messages

### Printing Output ###
for num, data in result.items():
    print(f"\nCase {num}:")
    for section, content in data.items():
        print(f"  {section}:")
        if isinstance(content, list):
            for msg_collect in content:
                print("   ", msg_collect)
        else:
            print("   ", content[:50], "...")

with open("parsed_cases.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

