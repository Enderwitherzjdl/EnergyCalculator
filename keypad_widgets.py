# keypad_widgets.py
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QFont

def add_digit_buttons(parent, layout):
    buttons = {
        (0, 0): '7', (0, 1): '8', (0, 2): '9',
        (1, 0): '4', (1, 1): '5', (1, 2): '6',
        (2, 0): '1', (2, 1): '2', (2, 2): '3',
        (3, 0, 1, 2): '0',
        (3, 2): '.',
    }
    for pos, text in buttons.items():
        if len(pos) == 2:
            row, col = pos
            rowspan, colspan = 1, 1
        else:
            row, col, rowspan, colspan = pos
        btn = QPushButton(text)
        btn.setFont(QFont("Arial", 18))
        btn.setFixedSize(80*colspan + (colspan-1)*8, 80*rowspan)
        btn.clicked.connect(lambda _, t=text: parent.keypad_input(t))
        layout.addWidget(btn, row, col, rowspan, colspan)

    # Clear 按钮
    clear_btn = QPushButton("C")
    clear_btn.setFont(QFont("Arial", 18))
    clear_btn.setFixedSize(80, 168)
    clear_btn.clicked.connect(lambda: parent.keypad_input("C"))
    layout.addWidget(clear_btn, 0, 3, 2, 1)

    # OK 按钮
    ok_btn = QPushButton("OK")
    ok_btn.setFont(QFont("Arial", 18))
    ok_btn.setFixedSize(80, 168)
    ok_btn.clicked.connect(lambda: parent.keypad_input("OK"))
    layout.addWidget(ok_btn, 2, 3, 2, 1)

def add_unit_buttons(parent, layout):
    units = ['eV', 'nm', 'cm-1', 'THz', 'ps', 'fs', 'K', 'J', 'kJ', 'kcal/mol', 'kJ/mol']
    positions = [(i, j) for i in range(3) for j in range(3)]
    positions.append((3,0))
    positions.append((3,1))
    parent.unit_buttons = {}

    for pos, unit in zip(positions, units):
        btn = QPushButton(unit)
        btn.setFont(QFont("Arial", 10))
        btn.setCheckable(True)
        btn.setFixedSize(60, 30)
        btn.clicked.connect(lambda _, u=unit: parent.convert_unit(u))
        layout.addWidget(btn, *pos)
        parent.unit_buttons[unit] = btn
