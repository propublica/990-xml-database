with open("./name_match_eins.txt") as f:
    name_match_eins = []
    for line in f:
        name_match_eins.append(line.strip())

with open("./name_state_match_eins.txt") as f:
    name_state_match_eins = []
    for line in f:
        name_state_match_eins.append(line.strip())

combined_eins = set()
combined_eins.update(name_match_eins, name_state_match_eins)

with open("./all_immigration_eins.txt", "w") as f:
    for ein in combined_eins:
        f.write(f"{ein}\n")
