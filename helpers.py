import os
import re
import sys


class PIDWriter:
    def __init__(self):
        self._base_dir = get_base_dir()
        self._pid_fname = None

    def __enter__(self):
        self.write_pid()
        return self

    def __exit__(self, *args):
        try:
            os.remove(self._pid_fname)
        except FileNotFoundError as e:
            print(str(e))

    def write_pid(self):
        prefix = os.path.splitext(os.path.basename(sys.argv[0]))[0]
        previous_pid = self.find_previous_pid(prefix)
        if previous_pid:
            print(f"\nRemoving {previous_pid}...")
            os.remove(previous_pid)
        pid_fname = get_abs_path(f'{prefix}_{os.getpid()}.pid', base_dir=self._base_dir)
        print(f"Writing {pid_fname}\n")
        with open(pid_fname, 'w') as handler:
            handler.write(str())
        self._pid_fname = pid_fname

    def find_previous_pid(self, prefix):
        for fname in os.listdir(self._base_dir):
            if re.fullmatch(rf'{prefix}_\d+\.pid', fname):
                return get_abs_path(fname, base_dir=self._base_dir)


def get_base_dir():
    return os.path.dirname(os.path.abspath(__file__))


def get_abs_path(fname, base_dir=None):
    if base_dir is None:
        base_dir = get_base_dir()
    return os.path.join(base_dir, fname)


def get_chat_id(update):
    return update.message.chat_id
