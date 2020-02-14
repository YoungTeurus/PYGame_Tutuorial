class A:
    def __init__(self, x):
        self.x = x

class B:
    def __init__(self, y):
        self.y = y

if __name__ == "__main__":
    classes = {
        "A": [A, 1],
        "B": [B, 2]
    }
    selected_class = "B"
    obj = classes[selected_class][0](classes[selected_class][1])
    print(obj.y)