import tkinter as tk
from tkinter import ttk
from typing import Iterable


class TooltipLabel:
    def __init__(self, root: tk.Tk, text: str = None, tooltip_text: str = None):
        self.root = root
        self.label = tk.Label(self.root, text=text)
        self.label.pack()

        self.tooltip = tk.Toplevel(self.root)
        self.tooltip.withdraw()
        self.tooltip.overrideredirect(True)

        self.tooltip_label = tk.Label(self.tooltip, text=tooltip_text, bg="yellow", relief="solid", borderwidth=1)
        self.tooltip_label.pack()

        self.label.bind("<Enter>", self.show_tooltip)
        self.label.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event: tk.Event):
        self.tooltip.geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
        self.tooltip.deiconify()

    def hide_tooltip(self, event: tk.Event):
        self.tooltip.withdraw()

    def set_text(self, text: str = None, tooltip_text: str = None):
        if text is not None:
            self.label.config(text=text)
        if tooltip_text is not None:
            self.tooltip_label.config(text=tooltip_text)


class ScrollableListbox:
    def __init__(self, root: tk.Tk, items: Iterable = None):
        self.root = root
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL)
        self.listbox = tk.Listbox(self.frame, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        if items is not None:
            for item in items:
                self.listbox.insert(tk.END, item)

    def set_items(self, items: Iterable = None):
        if items is not None:
            self.listbox.delete(0, tk.END)
            for item in items:
                self.listbox.insert(tk.END, item)

    def insert_item(self, index: str | int, item: str | int):
        self.listbox.insert(index, item)

    def remove_item(self, index: str | int):
        self.listbox.delete(index)

    def select_item(self, index: str | int):
        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(index)
        self.listbox.activate(index)
