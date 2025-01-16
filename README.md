# ActivityWatch Reminder\n\nProject details here.

---

# ActivityWatch Reminder

## 项目简介
**ActivityWatch Reminder** 是一个基于 [ActivityWatch](https://activitywatch.net/) 的桌面小工具，旨在监测用户的应用/网页使用时长，并在达到特定阈值后进行提醒或干预，帮助用户更好地管理注意力和休息时间。

> 如果你经常因为刷网页或看视频导致时间管理失控，这个工具可以帮你在“过度使用”时及时提醒，并让你选择是否强制休息。

---

## 功能概述

1. **ActivityWatch 数据获取**  
   - 利用 ActivityWatch 提供的 API，定期获取用户在各个应用/网站上的使用时长。
2. **阈值提醒**  
   - 用户可设置某一时间阈值（如连续 30 分钟），当超过时自动触发桌面通知弹窗。
3. **可定制配置**  
   - 在 `config.py` 中或其他配置界面里，设置提醒间隔、监控的应用范围等。
4. **（可选）强制阻断**  
   - 当用户多次忽略提醒或达到更高阈值时，进入全屏弹窗/锁屏，帮助用户强制休息。
5. **（可选）AI 个性化提示**  
   - 接入 OpenAI 或其他大语言模型，为用户生成更具人性化的提醒文案。
6. **跨平台可行性**  
   - 目前主要在 **Windows** 上测试和使用，其他平台（macOS、Linux）后续可以适配。

---

## 安装与使用

### 1. 前置环境

- **操作系统**：Windows 10/11（目前只在此环境下测试）
- **Python**：版本 3.7+（建议 3.9 或更高）
- **ActivityWatch**：已在本地安装并运行（确保 ActivityWatch 的服务端口可用）
  - [ActivityWatch 下载与安装指南](https://activitywatch.readthedocs.io/en/latest/getting-started/)

### 2. 克隆仓库

```bash
git clone https://github.com/<YourUsername>/activitywatch-reminder.git
cd activitywatch-reminder
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```
> 如果没有 `pip`，请先安装对应的 Python 环境或使用 `conda` 等包管理工具。

### 4. 配置项目

- 在 `src/config.py` 中修改以下关键参数：
  - `THRESHOLD_MINUTES`：使用阈值（例如 30 分钟）
  - `CHECK_INTERVAL_SECONDS`：监控间隔时间（例如 300 秒）
  - 其他的自定义设置（如监控哪些应用、是否开启AI提醒等）。

### 5. 运行项目

```bash
python src/main.py
```

- 程序将会在后台定期从 ActivityWatch 获取数据，并在达到阈值后弹出提醒或执行阻断操作。
- 若需要停止程序，直接关闭终端窗口或使用 `Ctrl + C` 中断执行。

---

## 目录结构

```text
activitywatch-reminder/
├── README.md              # 项目说明文件
├── .gitignore             # Git忽略文件列表
├── requirements.txt       # Python依赖列表
└── src/
    ├── main.py            # 主入口脚本
    ├── aw_api.py          # ActivityWatch 数据获取相关代码
    ├── config.py          # 全局配置，比如提醒阈值、监控间隔等
    └── notifier.py        # Windows 弹窗或提醒功能
```

- `main.py`：项目启动主脚本，包含主逻辑循环。  
- `aw_api.py`：与 ActivityWatch 交互，获取数据的相关函数。  
- `config.py`：存储并管理应用的各种配置（阈值、间隔、开关等）。  
- `notifier.py`：实现 Windows 通知或弹窗逻辑；后续可扩展到 macOS/Linux。

---

## 主要依赖

- `requests`：用于与 ActivityWatch API 通信  
- `win10toast` 或 `plyer` 等通知库（可根据你的选择更新）  
- `pywin32`（可选，如果需要更深度的 Windows 通知/锁屏功能）
- （可选）`openai`：如果你要使用 AI 提示，需要安装并配置 API Key

详细依赖见 `requirements.txt`。

---

## 常见问题 (FAQ)

1. **Q:** ActivityWatch 运行报错或无法获取数据怎么办？  
   **A:** 请先确保 ActivityWatch 已经启动，默认端口是 `5600`（[文档参考](https://activitywatch.readthedocs.io/)）。如果端口冲突，需在 `aw_api.py` 中修改相应地址。

2. **Q:** 为什么没看到通知/弹窗？  
   **A:** 检查 Windows 通知是否开启；或者确认 `notifier.py` 所用的函数在你的系统上可用。如果弹窗被屏蔽，可以尝试用全屏弹窗（如 `tkinter`）方式进行测试。

3. **Q:** 如果我想让它自动开机启动怎么办？  
   **A:** 目前本项目还没实现自动开机启动。你可以通过把脚本放进系统启动文件夹或注册表的方法来实现（后续可在 README 中补充此操作）。

---

## 待办事项与未来规划

- [ ] **强制阻断**：在超过更长时长或连续多次忽视提醒后，使用全屏/锁屏来让用户休息。  
- [ ] **AI 整合**：使用 OpenAI/ChatGPT 接口生成个性化的提醒文案。  
- [ ] **UI 界面**：提供更友好的图形界面查看统计数据、配置提醒策略。  
- [ ] **跨平台支持**：尝试兼容 macOS 和 Linux（需要做通知与依赖的适配）。  
- [ ] **数据可视化**：展示本日/本周使用时长曲线图或分类统计。

---

## 贡献指南

1. Fork 该项目。  
2. 创建新分支进行开发：`git checkout -b feature/my-feature`。  
3. 提交并推送分支：`git push origin feature/my-feature`。  
4. 发起 Pull Request 并描述具体修改内容。

如果你对 ActivityWatch Reminder 有任何建议或想法，欢迎提 Issue 或直接参与贡献。

---

## 许可证

本项目可能参考了 ActivityWatch 的相关代码/文档。由于 ActivityWatch 自身采用 [Mozilla Public License 2.0](https://github.com/ActivityWatch/activitywatch/blob/master/LICENSE)（或其他开源协议），请在使用本项目前确认是否符合其协议要求。本项目本身可以使用 MIT / Apache / GPL 等你喜欢的开源协议（请自行选择并在此声明）。

---

## 联系方式

- 项目作者：_ziyu-wei_  
- GitHub: [@ziyu-wei](https://github.com/ziyu-wei)  
- 如果你有更多问题或想法，可以在 GitHub Issues 中提出。

---

*感谢你使用 ActivityWatch Reminder，愿它能帮助你更好地把握时间、保持健康专注！*