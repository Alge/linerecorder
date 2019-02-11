import argparse
import curses
import os

from PyRecorder.soundrecorder import Recorder

parser = argparse.ArgumentParser(description='Handy tool for recording things')

parser.add_argument('-o','--output-file', help='base name for recordings', required=True)

args = vars(parser.parse_args())

def get_output_name(base_name):
    counter = 0
    name = base_name
    while os.path.isfile(name + ".wav"):
        name = base_name + "_take_{}".format(counter)
        counter += 1
    return name + ".wav"

def compare(key, c):
    if key == ord(c) or key == ord(c.lower()) or key == ord(c.upper()):
        return True
    return False

stdscr = curses.initscr()
curses.cbreak()
stdscr.keypad(1)

status = "Ready to start recording"

def print_main_menu(stdscr, refresh = True):
    stdscr.erase()
    stdscr.addstr(1,10,"Linerecorder")
    stdscr.addstr(3,10, status)
    stdscr.addstr(4,10,"press 's' to start recording")
    stdscr.addstr(5,10,"press 'e' to end recording")
    stdscr.addstr(6,10,"press 'd' to end and discard a recording")
    stdscr.addstr(7,10,"press 'n' to enter a new filename")
    stdscr.addstr(10,10,"Hit 'q' to quit")
    stdscr.addstr(12,10,"Storing recording in: " + get_output_name(args["output_file"]))
    stdscr.addstr(16,10,"    ")
    stdscr.addstr(16,10,"")

    if refresh:
        stdscr.refresh()


print_main_menu(stdscr)

r = Recorder()

key = ''
recording = False
while True:
    key = stdscr.getch()

    if compare(key, 'q'):
        if recording:
            r.stop_recording()
        break

    if compare(key, 's'):
        if not recording:
            status = "Recording"
            recording = True

            # Update the filename so we can record multiple takes
            filename = get_output_name(args["output_file"])
            r.record(filename)

    if compare(key, 'e'):
        if recording:
            status = "Ready to record"
            recording = False
            r.stop_recording()
            r = Recorder()

    if compare(key, 'd'):
        if recording:
            r.stop_recording()
            r = Recorder()
            os.remove(filename)
            recording = False
            status = "Discarded recording, ready to start recording again"

    if compare(key, 'n'):
        if not recording:
            args["output_file"] = stdscr.getstr(0,0, 32).decode("utf-8")
    print_main_menu(stdscr)

curses.endwin()