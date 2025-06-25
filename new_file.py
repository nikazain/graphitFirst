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
        }  #adds the number of the chapter and it's value to the dictionary
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
    if "Sent:" in w:
        current_section = "Cover Letter Sent"
        is_rombik = False
        continue
    if "History:" in w:
        current_section = "Chat History"
        is_rombik = False
        continue
    if is_rombik:
        continue
    if case_num and current_section:
        result[case_num][current_section] += " " + w

import re
chat_messages = {} # dictionary for chat history

for num, data in result.items():
    for section, text in data.items():
        if section != "Chat History":
            continue

        words = text.strip().split()
        messages = [] #will store the message strings in the format speaker : message, they are also split below
        speaker = ""
        msg = ""
        prev = [] # used to track two previous words
        collecting = False # a flag indicating if we are currently collecting a message for a speaker

        for w in words:
            if re.fullmatch(r"\d{1,2}:\d{2}", w) and len(prev) >= 2: # checked that w is an actual timestamp and we have 2 names for the name and surname
                if collecting:
                    messages.append(f"{speaker}: {msg.strip()}")
                speaker = f"{prev[-2]} {prev[-1]}"
                msg = ""
                collecting = True
                continue

            if collecting:
                msg += " " + w
            prev.append(w)
            if len(prev) > 3:
                prev.pop(0)

        if collecting and msg.strip():
            messages.append(f"{speaker}: {msg.strip()}")
                
        chat_messages[num] = [m.replace(": AM ", ": ", 1).replace(": PM ", ": ", 1) for m in messages]

for num, data in result.items():
    if num in chat_messages:
        data["Chat History"] = chat_messages[num]
    else:
        data["Chat History"] = ["No messages found."]

for num, data in result.items():
    print(f"\nCase {num}:")
    for section, content in data.items():
        print(f"  {section}:")
        if isinstance(content, list):
            for msg in content[:3]:  # show first 3 messages
                print("   ", msg)
        else:
            print("   ", content[:50], "...")


