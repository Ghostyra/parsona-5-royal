def sep_string(string):
    for i in range(len(string)-1):
        if string[i].islower() and string[i+1].isupper():
            string = string[:i+1] + "/" + string[i+1:]
    return string


def edit_effects(string):
    short_eff = {"Phys":"Physical", "Elec":"Electricity", "?":"-", "Nuke":"Nuclear", "Psi":"Psy",
                 "Psychic":"Psy", "Dark":"Darkness", "Electric":"Electricity", "Null":"-"}
    edit_string = ""
    words = string.split()
    for word in words:
        word = word.strip(",")
        if word == "&":
            continue
        elif word in short_eff.keys():
            edit_string += short_eff[word] + "/"
        else:
            edit_string += word + "/"
    return edit_string.rstrip("/")

