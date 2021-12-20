import tkinter as tk

charges = []


class Charge:
    def __init__(self, q, pos, item, record):
        self.q = q  # charge
        self.pos = pos  # position
        self.item = item  # item in canvas
        self.record = record  # record in table


def _create_circle(self, x, y, r, **kwargs):  # x=xCoordinate, y=yCoordinate, r=radius
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
