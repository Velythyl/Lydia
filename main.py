def is_foundation(c):
    return not c[0].isupper()

def all_foundation(l):
    for c in l:
        if not is_foundation(c):
            return False
    return True

def all_calculated(c, classes):
    for x in c.deps:
        if not is_foundation(x) and not classes[x].calculated:
            return False
    return True

def isnt_foundation(c):
    return not is_foundation(c)

class Node:
    def __init__(self, name, deps):
        self.name = name
        self.deps = deps
        self.refs = set(deps)
        self.calculated = False

    def print_line(self,classes):
        bla = []
        for d in self.deps:
            if not is_foundation(d):
                bla.append("ref("+classes[d].name+")")

        print(f"""{self.name}: |{{{','.join(self.deps)}}} U {' U '.join(bla)}| = |{self.refs}| = {len(self.refs)}""")

def calculate(node, dico, visited):
    if node in visited:
        return None

    if all_calculated(node, classes) and node.calculated:
        return

    if all_foundation(node.deps):
        node.calculated = True
        return

    for x in node.deps:
        if is_foundation(x):
            continue
        calculate(dico[x], dico, visited + [node])
        if not dico[x].calculated:
            return

    for x in node.deps:
        if is_foundation(x):
            continue
        node.refs = node.refs.union(dico[x].refs)
    node.calculated = True

def calc_all(classes):
    while True:
        for c in classes:
            calculate(c, classes, [])

        done = True
        for c in classes:
            if c.calculated == False:
                done = False

        if done:
            break

class MyList(list):
    def __getitem__(self, key):
        if isinstance(key, str):
            for x in self:
                if x.name == key:
                    return x
            return None

        for i, n in enumerate(self):
            if i == key:
                return n

if __name__ == "__main__":
    x = None
    classes = MyList()
    while x != "done":
        x = input("Class:comma-sep-deps OR 'done'")
        if x == "done":
            break
        if x == "":
            continue
        tableau = x.split(":")
        classes.append(Node(tableau[0], tableau[1].split(",")))

    calc_all(classes)
    for c in classes:
        c.print_line(classes)
