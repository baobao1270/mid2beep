# mid2beep

mid2beep 可以将 MIDI 文件转换为 `beep` 命令脚本和 [GRUB tune](https://www.gnu.org/software/grub/manual/grub/html_node/play.html)。

mid2beep 仅支持单个轨道。

`midi2grub.py` 文件不是由作者编写的，而是由 Lukas Fink 以 MIT 协议开源的。

请在使用本软件前确保您在电脑上安装了蜂鸣器（不是扬声器！扬声器没用！），否则本软件无法正常工作。

**重要提醒：GRUB 会以最大音量播放您设置的 tune，且音量无法调节，请确保您将电脑放在不会干扰到他人的环境中。**

## 使用
### Step 1: 下载源代码
使用 GitHub 下载本仓库的 ZIP 文件或使用 Git 克隆本仓库。

### Step 2: 安装环境和依赖
确保您安装了 Python >= 3.7

首先创建并激活 venv:
```shell
python3 -m venv venv
source venv/bin/activate # Linux/macOS
venv\bin\activate.bat    # Windows
```

然后使用 pip 安装依赖：
```shell
pip install -r requirements.txt
```

### Step 3: 获取或转换 MIDI 文件
如果您没有 MIDI 文件，可以从以下渠道获取
 - [MidiShow](https://www.midishow.com/)
 - [Musesource](https://musescore.org/)
 - Create a MIDI file with DAW

您也可以从 Vocaloid 工程转换 MIDI 文件，或者在 [vsqx.top](https://www.vsqx.top) 上下载。您也可使用 [Synthesizer V](https://dreamtonics.com/en/synthesizerv/) 来转换 MIDI 文件或修改测试歌曲. 请确保您的歌曲文件只有单个音轨，然后在 Synthesizer V 将工程导出为 MIDI 格式。

### Step 4: 将 MIDI 转换为 GRUB 配置
```shell
python3 midi2grub <filename>.mid
```

GRUB 配置将直接通输出。要保存为文件，请
```shell
python3 midi2grub.py <filename>.mid > <filename>.grub
```

然后修改 `/etc/default/grub` 的 `GRUB_INIT_TUNE` 配置项，如果没有改配置项请添加。例如：
```
GRUB_INIT_TUNE="410 668 1 668 1 0 1 668 1 0 1 522 1 668 1 0 1 784 2 0 2 392 2"
```

### Step 5: 在不重启的情况下测试输出
首先请安装 `beep` 命令。

然后，用以下命令从 grub 配置项文件转换：
```shell
python3 grub2beep.py <filename>.grub
```

Shell 命令将直接通输出。要保存为文件，请
```shell
python3 grub2beep.py <filename>.grub > <filename>.sh
```

然后，执行该 shell 文件。

## 测试歌曲
测试歌曲存放在 `test_songs` 文件夹。使用前，请阅读 `LICENSE_NOTICE` 文件。

No|歌曲           |原唱              |作编曲            |扒谱
--|---------------|-----------------|-----------------|------------
01|为了你唱下去     |洛天依            |COP              |澄镜P
02|Feel Your Dream|洛天依            |Trii             |传输控制协议TCP
03|一剪人间客       |星尘/海伊         |papaw泡泡         |皮皮蛋的皮

## 许可
代码以 MIT 许可证公布。测试歌曲和代码并非采用相同的许可证，请阅读 `LICENSE_NOTICE` 以获取详情。
