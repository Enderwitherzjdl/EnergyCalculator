# main_gui.py
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QSizePolicy,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from energy_core import energy_converter
from keypad_widgets import UNIT_LABELS, add_digit_buttons, add_unit_buttons


class EnergyConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.current_unit = None
        self.unit_labels = UNIT_LABELS
        self.setWindowTitle("能量转换器")
        self.resize(1280, 760)
        self.setMinimumSize(1180, 700)
        self.setStyleSheet("""
            QWidget {
                background: #f4f7fb;
                color: #18212f;
                font-family: "Microsoft YaHei UI";
                font-size: 13px;
            }
            QLineEdit {
                background: white;
                border: 1px solid #c8d0dc;
                border-radius: 8px;
                padding: 10px 12px;
                selection-background-color: #2f6fed;
            }
            QFrame#panel {
                background: white;
                border: 1px solid #d9e1ec;
                border-radius: 8px;
            }
            QLabel#sectionTitle {
                color: #1d2b3a;
                font-size: 15px;
                font-weight: 700;
            }
            QLabel#subtle {
                color: #657386;
                font-size: 12px;
            }
            QLabel#formula {
                background: #f0f5fb;
                border-radius: 6px;
                color: #31506f;
                padding: 8px 10px;
                font-family: "Cambria Math";
                font-size: 16px;
            }
            QTableWidget {
                background: white;
                border: 1px solid #d9e1ec;
                border-radius: 8px;
                gridline-color: #e6ecf3;
                selection-background-color: #dcecff;
                selection-color: #18212f;
                alternate-background-color: #f8fafc;
            }
            QHeaderView::section {
                background: #edf3fa;
                border: 0;
                border-bottom: 1px solid #d9e1ec;
                padding: 8px;
                font-weight: 700;
            }
        """)

        self.input_edit = QLineEdit()
        self.input_edit.setFont(QFont("Arial", 25))
        self.input_edit.setPlaceholderText("输入数值")
        self.input_edit.returnPressed.connect(self.convert_current_unit)

        self.selected_unit_label = QLabel("请选择输入单位")
        self.selected_unit_label.setObjectName("subtle")

        input_panel = self.make_panel()
        input_layout = QHBoxLayout(input_panel)
        input_layout.setContentsMargins(18, 14, 18, 14)
        input_layout.setSpacing(14)
        input_title = QLabel("输入")
        input_title.setObjectName("sectionTitle")
        input_title.setFixedWidth(64)
        self.selected_unit_label.setMinimumWidth(260)
        input_layout.addWidget(input_title)
        input_layout.addWidget(self.input_edit, 1)
        input_layout.addWidget(self.selected_unit_label)

        unit_panel = self.make_panel()
        unit_panel.setMinimumWidth(380)
        unit_layout = QVBoxLayout(unit_panel)
        unit_layout.setContentsMargins(18, 14, 18, 18)
        unit_layout.setSpacing(8)
        unit_title = QLabel("单位选择")
        unit_title.setObjectName("sectionTitle")
        self.unit_grid_layout = QGridLayout()
        self.unit_grid_layout.setHorizontalSpacing(10)
        self.unit_grid_layout.setVerticalSpacing(8)
        add_unit_buttons(self, self.unit_grid_layout)
        unit_layout.addWidget(unit_title)
        unit_layout.addLayout(self.unit_grid_layout)
        unit_layout.addStretch(1)

        keypad_panel = self.make_panel()
        keypad_panel.setMinimumWidth(370)
        keypad_layout = QVBoxLayout(keypad_panel)
        keypad_layout.setContentsMargins(18, 14, 18, 18)
        keypad_layout.setSpacing(10)
        keypad_title = QLabel("数字键盘")
        keypad_title.setObjectName("sectionTitle")
        self.digit_keypad_layout = QGridLayout()
        self.digit_keypad_layout.setHorizontalSpacing(10)
        self.digit_keypad_layout.setVerticalSpacing(10)
        add_digit_buttons(self, self.digit_keypad_layout)
        keypad_layout.addWidget(keypad_title)
        keypad_layout.addLayout(self.digit_keypad_layout)
        keypad_layout.addStretch(1)

        self.output_table = QTableWidget(0, 3)
        self.output_table.setHorizontalHeaderLabels(["物理量", "数值", "单位"])
        self.output_table.verticalHeader().setVisible(False)
        self.output_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.output_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.output_table.setAlternatingRowColors(True)
        self.output_table.setFont(QFont("Microsoft YaHei UI", 12))
        self.output_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.output_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.output_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.output_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        output_panel = self.make_panel()
        output_layout = QVBoxLayout(output_panel)
        output_layout.setContentsMargins(18, 14, 18, 18)
        output_layout.setSpacing(12)
        output_title = QLabel("换算结果")
        output_title.setObjectName("sectionTitle")
        self.output_hint = QLabel("周期：ν = 1/T，ν̃ = 1/(cT)    衰减：Δν̃ = 1/(2πτc)")
        self.output_hint.setObjectName("formula")
        output_layout.addWidget(output_title)
        output_layout.addWidget(self.output_hint)
        output_layout.addWidget(self.output_table)

        content_layout = QHBoxLayout()
        content_layout.setSpacing(14)
        content_layout.addWidget(unit_panel, 0)
        content_layout.addWidget(keypad_panel, 0)
        content_layout.addWidget(output_panel, 1)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(18, 18, 18, 18)
        main_layout.setSpacing(14)
        main_layout.addWidget(input_panel, 0)
        main_layout.addLayout(content_layout, 1)
        self.setLayout(main_layout)

    def make_panel(self):
        panel = QFrame()
        panel.setObjectName("panel")
        return panel

    def display_unit(self, unit):
        return self.unit_labels.get(unit, unit)

    def keypad_input(self, key):
        if key == 'C':
            self.input_edit.clear()
            self.output_table.setRowCount(0)
            self.current_unit = None
            self.selected_unit_label.setText("请选择输入单位")
            for btn in self.unit_buttons.values():
                btn.setChecked(False)
            return

        if key == 'OK':
            self.convert_current_unit()
            return

        self.input_edit.insert(key)

    def convert_current_unit(self):
        if self.current_unit is not None:
            self.convert_unit(self.current_unit)

    def convert_unit(self, unit):
        try:
            value = float(self.input_edit.text())
        except ValueError:
            self.output_table.setRowCount(0)
            self.selected_unit_label.setText("请先输入数字")
            return

        results = energy_converter(value, unit)
        if not results:
            return

        self.current_unit = unit
        self.selected_unit_label.setText(f"当前单位：{self.display_unit(unit)}")
        for u, btn in self.unit_buttons.items():
            btn.setChecked(u == unit)

        self.output_table.setRowCount(len(results))
        math_font = QFont("Cambria Math", 15)
        value_font = QFont("Consolas", 12)
        unit_font = QFont("Microsoft YaHei UI", 11)
        for row, (symbol, val, result_unit) in enumerate(results):
            quantity_item = QTableWidgetItem(symbol)
            value_item = QTableWidgetItem(val)
            unit_item = QTableWidgetItem(self.display_unit(result_unit))
            quantity_item.setFont(math_font)
            value_item.setFont(value_font)
            unit_item.setFont(unit_font)
            quantity_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            value_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            unit_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.output_table.setItem(row, 0, quantity_item)
            self.output_table.setItem(row, 1, value_item)
            self.output_table.setItem(row, 2, unit_item)
            self.output_table.setRowHeight(row, 38)
