import tkinter


class Listboxc:
    class ListboxObject:
        def __init__(self, pos, text, obj):
            self.pos = pos
            self.text = text
            self.object = obj

    def __init__(self, frame):
        self.listbox = tkinter.Listbox(frame)
        self.listbox.pack(fill='x', expand='true')
        self.listbox.insert(0, "a list entry")

        self.objects = dict()

    def getLast(self):
        return self.listbox.size()

    def addElement(self, text, obj, idx=None):
        if idx is None:
            idx = self.getLast()
        item = Listboxc.ListboxObject(idx, text, obj)
        self.objects[idx] = item
        self.listbox.insert(idx, item.text)

    def clear(self):
        self.listbox.delete(0, self.getLast())

    def getObject(self, pos):
        return self.objects[pos].object

    def getCurrent(self):
        return self.getObject(self.listbox.curselection()[0])
