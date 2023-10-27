
def clean_data(data):
    return [x for x in data if x != None]


def show_list(data):
    show = []
    for group in data:
        show.append([str(x) for x in group])
    return show