# 🌙 MoonTask

> 极致丝滑的侧边栏交互，专注于当下的任务管理。
> A minimal desktop To-Do app with silky smooth sidebar animations and weekly focus view.

![Python](https://img.shields.io/badge/python-3.10%2B-green)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-purple)

## ✨ 核心亮点

### 1. 丝滑侧边栏动画 (Silky Smooth Animation)
MoonTask v5.0 引入了**帧级动画引擎**。当你点击菜单键时，侧边栏不再是生硬的跳变，而是以丝滑的缓动效果收缩或展开。
![A](https://github.com/MoonPointer-Byte/MoonTask/blob/main/A.png)
### 2. 智能周视图 (Adaptive Week View)
- **展开时**：显示完整的**月历**，方便规划长远任务。
- **收缩时**：自动切换为**周视图**，只显示当前日期所在的一周（Mo-Su），垂直排列，让你专注于本周日程。
![B](https://github.com/MoonPointer-Byte/MoonTask/blob/main/C.png)
### 3. 全局搜索 (Search)
侧边栏底部集成搜索入口，随时查找历史任务。

### 4. 诗意奖励 (Poetic Reward)
任务清空时，系统会全屏展示一句精选古诗词，给你片刻的宁静。
![C](https://github.com/MoonPointer-Byte/MoonTask/blob/main/B.png)
## 🛠️ 安装与运行

```bash
# 1. 克隆项目
git clone https://github.com/MoonPointer-Byte/MoonTask.git

# 2. 安装依赖
pip install customtkinter requests

# 3. 运行
python main.py
```
##📦 打包教程

```
pip install pyinstaller
pyinstaller --noconsole --onefile --name="MoonTask" main.py
