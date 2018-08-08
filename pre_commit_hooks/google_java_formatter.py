from __future__ import print_function

import argparse
import subprocess
import os
import errno
import urllib

FORMATTER_VERSION = "1.6"


def get_google_java_formatter():
    bin_dir = os.path.join(os.path.expanduser("~"), ".google-java-formatter")
    if not os.path.exists(bin_dir):
        try:
            os.makedirs(bin_dir)
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    gjf_jar = os.path.join(
        bin_dir, "google-java-format-" + FORMATTER_VERSION + ".jar")

    if not os.path.isfile(gjf_jar):
        print("Downloading " + gjf_jar + "...")
        url = "https://github.com/google/google-java-format/releases/" \
            + "download/google-java-format-" + FORMATTER_VERSION \
            + "/google-java-format-" \
            + FORMATTER_VERSION + "-all-deps.jar"
        urllib.urlretrieve(url, gjf_jar)

    return os.path.abspath(gjf_jar)


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*',
                        help='Java filenames to check.')
    args = parser.parse_args(argv)

    formatter = get_google_java_formatter()
    return subprocess.call([
        'java', '-jar', formatter, '--replace'] + args.filenames)


if __name__ == "__main__":
    exit(main())
