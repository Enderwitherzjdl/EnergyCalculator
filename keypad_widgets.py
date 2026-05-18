# keypad_widgets.py
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel, QPushButton


UNIT_LABELS = {
    'eV': 'eV',
    'J': 'J',
    'kJ': 'kJ',
    'kcal/mol': 'kcal/mol',
    'kJ/mol': 'kJ/mol',
    'nm': 'nm',
    'cm-1': 'cm-1',
    'THz': 'THz',
    'ps(period)': 'ps (T)',
    'fs(period)': 'fs (T)',
    'ps(tau)': 'ps (τ)',
    'fs(tau)': 'fs (τ)',
    'K': 'K',
}

BUTTON_STYLE = """
QPushButton {
    border: 1px solid #c8d0dc;
    border-radius: 7px;
    background: #fbfdff;
    color: #18212f;
    padding: 6px 10px;
}
QPushButton:hover {
    background: #eef5ff;
    border-color: #8ab4f8;
}
QPushButton:checked {
    background: #dcecff;
    border: 2px solid #2f6fed;
    color: #143f8f;
    font-weight: 600;
}
"""


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
        btn.setMinimumSize(76 * colspan, 54 * rowspan)
        btn.setStyleSheet(BUTTON_STYLE)
        btn.clicked.connect(lambda _, t=text: parent.keypad_input(t))
        layout.addWidget(btn, row, col, rowspan, colspan)

    clear_btn = QPushButton("清空")
    clear_btn.setFont(QFont("Microsoft YaHei UI", 12))
    clear_btn.setMinimumSize(76, 116)
    clear_btn.setStyleSheet(BUTTON_STYLE)
    clear_btn.clicked.connect(lambda: parent.keypad_input("C"))
    layout.addWidget(clear_btn, 0, 3, 2, 1)

    ok_btn = QPushButton("换算")
    ok_btn.setFont(QFont("Microsoft YaHei UI", 12))
    ok_btn.setMinimumSize(76, 116)
    ok_btn.setStyleSheet(BUTTON_STYLE)
    ok_btn.clicked.connect(lambda: parent.keypad_input("OK"))
    layout.addWidget(ok_btn, 2, 3, 2, 1)


def add_unit_buttons(parent, layout):
    groups = [
        ("能量", ['eV', 'J', 'kJ', 'kcal/mol', 'kJ/mol']),
        ("波长 / 波数", ['nm', 'cm-1']),
        ("频率", ['THz']),
        ("振荡周期", ['ps(period)', 'fs(period)']),
        ("衰减时间常数", ['ps(tau)', 'fs(tau)']),
        ("温度", ['K']),
    ]
    parent.unit_buttons = {}
    parent.unit_labels = UNIT_LABELS
    row = 0

    for title, units in groups:
        label = QLabel(title)
        label.setFont(QFont("Microsoft YaHei UI", 10, QFont.Weight.Bold))
        label.setStyleSheet("color: #526173; padding: 10px 0 2px 0;")
        layout.addWidget(label, row, 0, 1, 2)
        row += 1

        for index, unit in enumerate(units):
            col = index % 2
            if index > 0 and col == 0:
                row += 1
            btn = QPushButton(UNIT_LABELS[unit])
            btn.setFont(QFont("Microsoft YaHei UI", 10))
            btn.setCheckable(True)
            btn.setMinimumSize(156, 38)
            btn.setStyleSheet(BUTTON_STYLE)
            btn.clicked.connect(lambda _, u=unit: parent.convert_unit(u))
            layout.addWidget(btn, row, col)
            parent.unit_buttons[unit] = btn
        row += 1
