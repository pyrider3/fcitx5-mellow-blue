# Mellow Blue for Fcitx5

深色圆角候选窗，搭配 macOS 风格蓝色高亮和轻量动画。基于 [Mellow Youlan dark](https://github.com/sanweiya/fcitx5-mellow-themes) 修改。

![实际候选窗预览](preview/candidates.png)

## 外观与动效

- 蓝色高亮 `#015ad8`，深色背景，柔和边框及候选序号。
- 1× / 2× / 3× / 4× PNG 素材，改善高分屏圆角边缘。
- 可选动画：候选高亮 80 ms 滑动与宽度过渡；打开 90 ms 淡入并上移 2 px，关闭 60 ms 淡出。
- 连续输入不重复播放打开动画；选词立即提交；淡出期间不拦截鼠标点击。
- 支持 Fcitx5 自带拼音、Rime 等引擎，不修改输入方案、词库和快捷键。

## 安装皮肤

需要已安装 Fcitx5、ClassicUI、Python 3。皮肤可以独立使用。

```bash
git clone https://github.com/pyrider3/fcitx5-mellow-blue.git
cd fcitx5-mellow-blue
python3 install.py
```

安装到当前用户目录，自动选择 Mellow Blue。已有配置会备份至 `$XDG_STATE_HOME/fcitx5-mellow-blue`（默认 `~/.local/state/fcitx5-mellow-blue`）。保留用户原有字体和间距；预览使用 Sans 10。

## 可选：启用动画

动画通过修改 Fcitx5 ClassicUI 实现，**不是主题配置自带的功能**。目前固定针对 **Fcitx5 5.1.23**，需要 C++ 编译器、CMake、Git、Fcitx5 的构建依赖及 XCB Shape 开发库。

Arch Linux 构建依赖可参考 Fcitx5 官方 PKGBUILD；`build.py` 自动获取 ECM、nlohmann/json、Fcitx5 5.1.23 与其 Yoga 子模块，在 `.build/` 内编译。

```bash
python3 build.py
python3 install.py --animation
```

会重启 Fcitx5，请先提交正在输入的文字。插件读取原来的 `classicui.conf`，注册名为 `smoothui`。其他 Fcitx5 版本请先只使用皮肤，不建议直接加载本版本动画插件。

已在 Arch Linux / Niri / XWayland 实测；原生 Wayland 路径已编译，尚未完成逐帧验证。原生 Wayland 的关闭过渡可能受合成器弹窗生命周期限制。

## 恢复

```bash
python3 restore.py
```

恢复安装前的 ClassicUI 配置、动画插件注册与同名主题（如果原先存在）。重启 Fcitx5，保留输入方案及词库。建议恢复后再卸载仓库文件。

## 验证与源码

```bash
c++ -std=c++17 tests/motion.cpp -o /tmp/mellow-motion && /tmp/mellow-motion
c++ -std=c++17 tests/popup.cpp -o /tmp/mellow-popup && /tmp/mellow-popup
```

`src/motion.h` 包含动画状态机，`src/fcitx5.patch` 是相对 Fcitx5 5.1.23 的完整接入补丁。实际桌面测试覆盖过候选滑动、立即数字选词、打开/关闭淡化及关闭时清空鼠标输入区域；预览为真实候选窗截图。

## 致谢与许可

- 主题源自 [sanweiya/fcitx5-mellow-themes](https://github.com/sanweiya/fcitx5-mellow-themes)，保留 BSD-2-Clause 许可。
- 动画补丁基于 [fcitx/fcitx5](https://github.com/fcitx/fcitx5) ClassicUI，使用 LGPL-2.1-or-later。
- Yoga 使用 MIT 许可。完整许可文本见 [LICENSES](LICENSES)。

本项目是 Linux Fcitx5 的主题与界面插件，不是 macOS 输入法软件。
