def print_cons(cons,title=""):
    if title != "":
        print(title)
    for c in cons:
        print(c)
        
def print_deg(any):
    print(any)

def print_for_geo_gebra(cons):
    for c in cons:
        print(str(c).replace("<","").replace(">",""))