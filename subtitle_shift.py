import sys

"""
open a sbv text file and shift the time stamps of everything by a constant amount
"""


def shift_timestamps(input_file, output_file, shift_seconds):
    def shift_time(timestamp, shift_seconds):
        hours, minutes, seconds = map(float, timestamp.split(":"))
        total_seconds = hours * 3600 + minutes * 60 + seconds + shift_seconds
        if total_seconds < 0:
            total_seconds = 0
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = total_seconds % 60
        return f"{hours:01}:{minutes:02}:{seconds:06.3f}"

    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        for line in infile:
            if "," in line and len(line.split(",")) == 2 and line.startswith("0:"):
                t1, t2 = line.strip().split(",", 1)
                t1 = shift_time(t1, shift_seconds)
                t2 = shift_time(t2, shift_seconds)
                outfile.write(f"{t1},{t2}\n")
            else:
                outfile.write(line)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(
            "Usage: python subtitle_shift.py <input_file> <output_file> <shift_seconds>"
        )
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    shift_seconds = float(sys.argv[3])

    shift_timestamps(input_file, output_file, shift_seconds)
