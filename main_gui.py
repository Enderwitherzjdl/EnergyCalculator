# main_gui.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QGridLayout, QTextEdit
from PyQt6.QtGui import QFont, QTextCursor, QTextBlockFormat
from PyQt6.QtCore import Qt
from energy_core import energy_converter
from keypad_widgets import add_digit_buttons, add_unit_buttons

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
        add_unit_buttons(self, self.unit_grid_layout)

        # 输入 + 单位布局
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.input_edit)
        top_layout.addLayout(self.unit_grid_layout)

        # 数字键盘
        self.digit_keypad_layout = QGridLayout()
        self.digit_keypad_layout.setHorizontalSpacing(8)
        self.digit_keypad_layout.setVerticalSpacing(8)
        self.digit_keypad_layout.setContentsMargins(12,12,12,12)
        add_digit_buttons(self, self.digit_keypad_layout)

        left_layout = QVBoxLayout()
        left_layout.addLayout(top_layout)
        left_layout.addLayout(self.digit_keypad_layout)

        # 输出文本区
        self.output_display = QTextEdit()
        self.output_display.setFont(QFont("Consolas", 14))
        self.output_display.setReadOnly(True)

        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout)
        main_layout.addWidget(self.output_display)
        self.setLayout(main_layout)

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

    def convert_unit(self, unit):
        try:
            value = float(self.input_edit.text())
            results = energy_converter(value, unit)

            # 设置选中样式
            for u, btn in self.unit_buttons.items():
                btn.setChecked(u==unit)
                btn.setStyleSheet("border:2px solid blue;" if u==unit else "")

            # 输出
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
            block_format.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            block_format.setLineHeight(200,1)
            cursor.setBlockFormat(block_format)
            cursor.insertText(all_text)

        except ValueError:
            self.output_display.setPlainText("错误：请输入数字！")
