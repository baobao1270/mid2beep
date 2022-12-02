# mid2beep

mid2beep is a python to convert a MIDI to a `beep` shell command or [GRUB tune](https://www.gnu.org/software/grub/manual/grub/html_node/play.html).

mid2beep only support single track songs.

The `midi2grub.py` is a open-source script released under MIT license created by Lukas Fink.

To make this program work, you have to install a beeper (not speaker!) to your PC.

**NOTICE: The GRUB plays the tune VERY LOADLY and the VOLUME CAN NOT BE CHANGED.**

Chinese version of this file: [README_CN](https://github.com/baobao1270/mid2beep/blob/master/README_CN.md)

## Usage
### Step 1: Download the source code
Click the _Download ZIP_ button in GitHub or clone the repo with git.

### Step 2: Install dependencies
Make sure you have Python >= 3.7 installed.

First, please create a venv and activicate it:
```shell
python3 -m venv venv
source venv/bin/activate # Linux/macOS
venv\bin\activate.bat    # Windows
```

Then, please install required dependencies with pip:
```shell
pip install -r requirements.txt
```

### Step 3: Obtain or convert a MIDI file
If you don't have the MIDI file, you can obtain MIDI file from MIDI sharing websites like
 - [MidiShow](https://www.midishow.com/)
 - [Musesource](https://musescore.org/)
 - Create a MIDI file with DAW

You can also use Vocaloid projects. To find project, you can use [vsqx.top](https://www.vsqx.top). You can also use [Synthesizer V](https://dreamtonics.com/en/synthesizerv/) to convert or create MIDI files or edit test songs. Make sure you have only one track in Synthizer V. Then, export the project as MIDI file.

### Step 4: Convert the MIDI to GRUB
```shell
python3 midi2grub <filename>.mid
```

The result will be print on standard output. To save it as file, use
```shell
python3 midi2grub.py <filename>.mid > <filename>.grub
```

Then, edit `/etc/default/grub`, add or change `GRUB_INIT_TUNE`.

Example:
```
GRUB_INIT_TUNE="410 668 1 668 1 0 1 668 1 0 1 522 1 668 1 0 1 784 2 0 2 392 2"
```

**NOTICE: The GRUB plays the tune VERY LOADLY and the VOLUME CAN NOT BE CHANGED.**

### Step 5: Test the tune without restart 
Please install the `beep` command.

Then, convert the grub to beep shell script:
```shell
python3 grub2beep.py <filename>.grub
```

The result will be print on standard output. To save it as file, use
```shell
python3 grub2beep.py <filename>.grub > <filename>.sh
```

To play the song with reboot, execucate the shell file.

## Test songs
The test songs are in the `test_songs` folder. Please read the `LICENSE_NOTICE` file before using it.

No|Song           |Original Singer  |Composer/Arranger|MIDI Creator
--|---------------|-----------------|-----------------|------------
01|为了你唱下去     |洛天依            |COP              |澄镜P
02|Feel Your Dream|洛天依            |Trii             |传输控制协议TCP
03|一剪人间客       |星尘/海伊         |papaw泡泡         |皮皮蛋的皮

## License
Code are released under MIT license. 

The test songs are NOT released MIT license. Read the `LICENSE_NOTICE` file for details.
