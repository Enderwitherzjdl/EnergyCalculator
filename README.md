# Energy Converter

一个使用 PyQt6 编写的桌面能量转换器，用于在常见物理、光谱、化学能量单位之间快速转换。

## 支持单位

- 能量：`eV`, `J`, `kJ`, `kcal/mol`, `kJ/mol`
- 波长：`nm`
- 频率/波数：`THz`, `cm-1`
- 振荡周期：`ps (T)`, `fs (T)`，对应 `ν = 1/T`
- 衰减时间常数：`ps (τ)`, `fs (τ)`，对应 `Δν̃ = 1/(2πτc)`
- 温度：`K`

注意：`T` 是振荡周期，`τ` 是指数衰减时间常数。相同数值下二者对应的波数相差 `2*pi`。

## 项目结构

```text
EnergyCalculator/
├── run.py             # 程序入口
├── main_gui.py        # PyQt 主窗口
├── keypad_widgets.py  # 数字键盘和单位按钮
├── energy_core.py     # 单位换算核心逻辑
└── full_code.py       # 兼容入口，转发到模块化界面
```

## 运行

```bash
python run.py
```

打包：

```bash
./CompilePackage.bat
```
