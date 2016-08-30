#!/usr/bin/env python
"""
Transcriber script using Google speech API: https://cloud.google.com/speech/

Xaratustrah 2016

"""

import speech_recognition as sr
import argparse, os
from pydub import AudioSegment
from pydub.utils import make_chunks
import logging as log

__version_info__ = (0, 0, 1)
__version__ = '.'.join('%d' % d for d in __version_info__)


def cut_and_send(infile, outfile, length):
    # print(infile)
    # print(outfile)
    # print(length)
    # return
    myaudio = AudioSegment.from_file(infile, "wav")
    chunk_length_ms = length  # pydub calculates in millisec
    chunks = make_chunks(myaudio, chunk_length_ms)  # Make chunks of one sec

    for i, chunk in enumerate(chunks):
        chunk_name = "chunk{0}.wav".format(i)
        print("exporting", chunk_name)
        chunk.export(chunk_name, format="wav")
        r = sr.Recognizer()
        with sr.AudioFile(chunk_name) as source:
            audio = r.record(source)
        # recognize speech using Google Speech Recognition
        try:
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            txt = r.recognize_google(audio) + " "
            with open(outfile, 'a') as f:
                f.write(txt)
        except sr.UnknownValueError:
            print("Ehm... sorry not understood this one.")
        except sr.RequestError as e:
            print("Request failed; {0}".format(e))
        os.remove(chunk_name)


def main():
    SCRIPT_NAME = 'transcriber'
    parser = argparse.ArgumentParser(prog=SCRIPT_NAME)
    parser.add_argument('infile', type=str, help="Name of the input wave file.")
    parser.add_argument('outfile', type=str, help="Name of the output text file.")
    parser.add_argument("-l", "--length", nargs='?', type=int, const=1000, default=1000,
                        help="Length of audio chunks in milliseconds.")
    parser.add_argument('--verbose', action='store_true', help='Increase verbosity.')

    print('{} {}'.format(SCRIPT_NAME, __version__))

    args = parser.parse_args()
    # check the first switches

    if args.verbose:
        log.basicConfig(level=log.DEBUG)

    cut_and_send(args.infile, args.outfile, args.length)


# ----------------------------

if __name__ == '__main__':
    main()
