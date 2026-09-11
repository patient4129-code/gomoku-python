# Python 五子棋

一个使用 Python 标准库 `tkinter` 编写的双人五子棋小游戏，不需要安装第三方依赖。

## 功能

- 15 × 15 标准棋盘
- 黑棋、白棋双人轮流落子
- 自动判断横向、纵向和两种斜向的五连胜
- 已落子位置保护、边界检查和平局判断
- 一键重新开始

## 运行环境

- Python 3.10 或更高版本
- Windows 和 macOS 的官方 Python 通常自带 `tkinter`
- Ubuntu/Debian 若缺少 `tkinter`，可安装 `python3-tk`

## 启动游戏

```bash
python gomoku.py
```

在棋盘交叉点单击即可落子，黑棋先行。

## 运行测试

```bash
python -m unittest -v
```

## 项目结构

```text
gomoku-python/
├── gomoku.py          # 游戏规则和图形界面
├── test_gomoku.py     # 单元测试
├── README.md          # 使用说明
└── .gitignore
```

## 规则说明

任意一方先在横向、纵向或斜向连成至少五颗棋子即获胜。本项目采用适合入门演示的自由规则，不包含禁手。
