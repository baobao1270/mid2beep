import sys
import os.path

if len(sys.argv) < 2:
    print("Usage: grub2beep.py <grub-txt-filename>")

file = sys.argv[1]
if not os.path.exists(file):
    print("File not found: " + file)
    sys.exit(1)

with open(file) as f:
    notes = f.read().strip().split(" ")

tempo = int(notes[0])
notes = notes[1:]
output = []

for note in range(0, len(notes), 2):
    frequency = int(notes[note])
    duration = int(int(notes[note + 1]) / tempo * 1000 * 60)
    if frequency == 0:
        output.append(f"-D {duration}")
        continue
    output.append(f"-n -f {frequency} -l {duration}")

output = " ".join(output).strip()
if output[:2] == "-n":
    output = output[2:]
print("beep", output)
