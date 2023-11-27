import inspect
import os


def print_with_filename(message):
    frame_info = inspect.stack()[1]
    filename = os.path.splitext(os.path.basename(frame_info.filename))[0]
    directory = os.path.basename(os.path.dirname(frame_info.filename))
    path = f"/{directory}/{filename}"
    line_number = frame_info.lineno
    function = frame_info.function
    print(f"{path} {function}:{line_number}: {message}")
