import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QGridLayout, QTextEdit
)
from PyQt6.QtGui import QFont, QTextCursor, QTextBlockFormat
from PyQt6.QtCore import Qt

# --- 格式化函数 ---
def format_number(value: float) -> str:
    superscripts = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")
    if value == 0:
        return "0"
    abs_val = abs(value)
    if 1e-3 <= abs_val <= 1e5:
        return f"{value:.5g}"
    else:
        formatted = f"{value:.4e}"
        base, exp = formatted.split("e")
        exp = int(exp)
        return f"{base} × 10{str(exp).translate(superscripts)}"

# --- 转换函数 ---
def energy_converter(value, unit):
    unit_conversions = {
        'eV': lambda x: x,
        'nm': lambda x: 1239.8420 / x,
        'cm-1': lambda x: x * 1239.8420e-7,
        'THz': lambda x: x / 241.7989,
        'ps': lambda x: 4.135668e-3/x,
        'fs': lambda x: 4.135668/x,
        'K': lambda x: 8.61733e-5*x,
        'J': lambda x: x/1.60218e-19,
        'kJ': lambda x: x/1.60218e-22,
    }
    ir_unit_conversions = {
        'eV': lambda x: x,
        'nm': lambda x: 1239.8420 / x,
        'cm-1': lambda x: x / 1239.8420e-7,
        'THz': lambda x: x * 241.7989,
        'ps': lambda x: 4.135668e-3/x,
        'fs': lambda x: 4.135668/x,
        'K': lambda x: x/8.61733e-5,
        'J': lambda x: x*1.60218e-19,
        'kJ': lambda x: x*1.60218e-22,
    }
    symbol = {
        'eV': 'E',
        'nm': 'λ',
        'cm-1': 'ν',
        'THz': 'f',
        'ps': 'T',
        'fs': 'T',
        'K': 'Temp',
        'J': 'E',
        'kJ': 'E',
    }

    if unit not in unit_conversions:
        return []

    results = []
    E = unit_conversions[unit](value)
    for u in ir_unit_conversions:
        val = ir_unit_conversions[u](E)
        results.append((symbol[u], format_number(val), u))
    return results

# --- 主界面 ---
class EnergyConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("能量转换器")
        self.resize(850, 550)

        # 数字输入框
        self.input_edit = QLineEdit()
        self.input_edit.setFont(QFont("Arial", 24))
        self.input_edit.setPlaceholderText("输入数值")
        self.input_edit.setFixedWidth(150)

        # 单位小键盘
        self.unit_grid_layout = QGridLayout()
        self.unit_grid_layout.setHorizontalSpacing(4)
        self.unit_grid_layout.setVerticalSpacing(4)
        self.add_unit_buttons(self.unit_grid_layout)

        # 输入框 + 单位
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.input_edit)
        top_layout.addLayout(self.unit_grid_layout)

        # 数字键盘
        self.digit_keypad_layout = QGridLayout()
        self.digit_keypad_layout.setHorizontalSpacing(8)
        self.digit_keypad_layout.setVerticalSpacing(8)
        self.digit_keypad_layout.setContentsMargins(12, 12, 12, 12)
        self.add_digit_buttons(self.digit_keypad_layout)

        left_layout = QVBoxLayout()
        left_layout.addLayout(top_layout)
        left_layout.addLayout(self.digit_keypad_layout)

        # 输出文本区
        self.output_display = QTextEdit()
        self.output_display.setFont(QFont("Consolas", 14))
        self.output_display.setReadOnly(True)

        # 主布局
        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout)
        main_layout.addWidget(self.output_display)
        self.setLayout(main_layout)

    # --- 数字小键盘 ---
    def add_digit_buttons(self, layout):
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
            btn.clicked.connect(lambda _, t=text: self.keypad_input(t))
            layout.addWidget(btn, row, col, rowspan, colspan)

        clear_btn = QPushButton("C")
        clear_btn.setFont(QFont("Arial", 18))
        clear_btn.setFixedSize(80, 168)
        clear_btn.clicked.connect(lambda: self.keypad_input("C"))
        layout.addWidget(clear_btn, 0, 3, 2, 1)

        ok_btn = QPushButton("OK")
        ok_btn.setFont(QFont("Arial", 18))
        ok_btn.setFixedSize(80, 168)
        ok_btn.clicked.connect(lambda: self.keypad_input("OK"))
        layout.addWidget(ok_btn, 2, 3, 2, 1)

    # --- 单位按钮 ---
    def add_unit_buttons(self, layout):
        units = ['eV', 'nm', 'cm-1', 'THz', 'ps', 'fs', 'K', 'J', 'kJ']
        positions = [(i, j) for i in range(3) for j in range(3)]
        self.unit_buttons = {}

        for pos, unit in zip(positions, units):
            btn = QPushButton(unit)
            btn.setFont(QFont("Arial", 10))
            btn.setCheckable(True)
            btn.setFixedSize(50, 30)
            btn.clicked.connect(lambda _, u=unit: self.convert_unit(u))
            layout.addWidget(btn, *pos)
            self.unit_buttons[unit] = btn

    # --- 键盘输入 ---
    def keypad_input(self, key):
        if key == 'C':
            self.input_edit.clear()
            self.output_display.clear()
            for btn in self.unit_buttons.values():
                btn.setChecked(False)
                btn.setStyleSheet("")
        elif key == 'OK':
            pass
        else:
            self.input_edit.insert(key)

    # --- 单位转换 ---
    def convert_unit(self, unit):
        try:
            value = float(self.input_edit.text())
            results = energy_converter(value, unit)

            # 设置选中样式
            for u, btn in self.unit_buttons.items():
                btn.setChecked(u == unit)
                btn.setStyleSheet("border: 2px solid blue;" if u == unit else "")

            self.output_display.clear()
            lines = []
            sym_width = max(len(s) for s, _, _ in results)
            val_width = max(len(v) for _, v, _ in results)
            for sym, val, u in results:
                lines.append(f"{sym.ljust(sym_width)} = {val.rjust(val_width)} {u}")
            all_text = "\n".join(lines)
            cursor = self.output_display.textCursor()
            cursor.movePosition(QTextCursor.MoveOperation.Start)
            block_format = QTextBlockFormat()
            block_format.setAlignment(Qt.AlignmentFlag.AlignHCenter)  # 整体居中
            block_format.setLineHeight(200, 1)  # 可调行距
            cursor.setBlockFormat(block_format)
            cursor.insertText(all_text)

        except ValueError:
            self.output_display.setPlainText("错误：请输入数字！")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EnergyConverterApp()
    window.show()
    sys.exit(app.exec())
