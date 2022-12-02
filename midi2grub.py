# Copyright (c) 2019 Lukas Fink
# Released under the MIT license. Read 'LICENSE' for more information.

"""Creates grub play sequences from midi files"""

import abc
import argparse
import struct
import sys
import os

import mido

NAME = os.path.basename(sys.argv[0])


class AbstractSerializer(abc.ABC):
    """A base class for grub play formats"""
    out = None

    @abc.abstractmethod
    def put_event(self, pitch, duration):
        pass

    def put_note(self, midi_note, duration):
        self.put_event(round(440 * 2 ** ((midi_note - 69) / 12)), duration)

    def put_pause(self, duration):
        self.put_event(0, duration)

    def put_end(self):
        if self.out.isatty():
            self.out.write('\n')


class ASCIISerializer(AbstractSerializer):
    """The output of this serializer can be used directly as arguments to the grub play function"""
    def __init__(self, ticks_per_minute, out):
        self.out = out
        out.write('%d' % ticks_per_minute)

    def put_event(self, pitch, duration):
        self.out.write(' %d %d' % (pitch, duration))


class BinarySerializer(AbstractSerializer):
    """Files created with this class can be read by grub play"""
    def __init__(self, ticks_per_minute, out):
        if out.isatty():
            raise ValueError('Cannot write binary to Terminal.')
        self.out = out
        out.buffer.write(struct.pack('<I', ticks_per_minute))

    def put_event(self, pitch, duration):
        self.out.buffer.write(struct.pack('<HH', pitch, duration))


def midi_file_parser(path):
    """Argument type, that reads midi files"""
    with argparse.FileType('rb')(path) as file:
        try:
            return mido.MidiFile(file=file)
        except (EOFError, IOError, ValueError) as e:
            raise argparse.ArgumentTypeError(f'invalid midi file{f": {e}" if str(e) else "."}')


def parse_args():
    """Parses arguments and prepares conversion"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-b', '--binary', action='store_const', const=BinarySerializer,
                        default=ASCIISerializer,
                        help='create a binary file instead of a sequence string')
    parser.add_argument('-t', '--track', type=int,
                        help='the number of the track which should get converted')
    parser.add_argument('-c', '--channel', type=int, choices=range(16), metavar='CHANNEL',
                        help='only events on CHANNEL (0-15) are being processed')
    parser.add_argument('-m', '--tempo', '--bpm', type=float,
                        help='overwrites the tempo of the midi file')
    parser.add_argument('midifile', type=midi_file_parser, help='the midi file as input')
    parser.add_argument('playseq', nargs='?', type=argparse.FileType('w'), default=sys.stdout,
                        help='an output file')
    args = parser.parse_args()

    if args.track is None:
        if args.midifile.type == 2:
            parser.error('no track selected for type 2 midi file')
        track = mido.merge_tracks(args.midifile.tracks)
    else:
        try:
            track = args.midifile.tracks[args.track]
        except IndexError:
            parser.error(f'argument -t/--track: there is no track {args.track} in midifile')

    bpm = args.tempo
    if bpm is None:
        bpm = 120
        for x in (args.midifile if args.midifile.type == 1 else track):
            if x.type == 'set_tempo':
                bpm = mido.tempo2bpm(x.tempo)
                break

    try:
        serializer = args.binary(round(bpm * args.midifile.ticks_per_beat), args.playseq)
    except ValueError as e:
        print(f'{NAME}: {e}', file=sys.stderr)
        exit(1)

    return track, serializer, args.channel


def convert(track, serializer, channel=None):
    """Converts midi tracks"""
    note_on = []
    accu_ticks = 0
    for event in track:
        accu_ticks += event.time
        if channel is not None and getattr(event, 'channel', None) != channel:
            continue
        if event.type == 'note_off' or (event.type == 'note_on' and event.velocity == 0):
            if accu_ticks > 0 and event.note in note_on[-1:]:
                serializer.put_note(note_on[-1], accu_ticks)
                accu_ticks = 0
            try:
                note_on.remove(event.note)
            except ValueError:
                pass
        elif event.type == 'note_on' and event.note not in note_on[-1:]:
            if accu_ticks > 0:
                if note_on:
                    serializer.put_note(note_on[-1], accu_ticks)
                else:
                    serializer.put_pause(accu_ticks)
            try:
                note_on.remove(event.note)
            except ValueError:
                pass
            note_on.append(event.note)
            accu_ticks = 0

    serializer.put_end()


if __name__ == '__main__':
    convert(*parse_args())
