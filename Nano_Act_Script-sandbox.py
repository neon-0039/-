# =========================================================
# NANOACTSCRIPT ENGINE
# =========================================================

import re
import sys
import threading
import time
import traceback
import string
import math
import random
import os
import json
import winsound

# =========================================================
# SCRIPT ENGINE MEMORY
# =========================================================

SCRIPT_VARIABLES = {}
SCRIPT_DISPLAYS = {}
SCRIPT_FUNCTIONS = {}
SCRIPT_GAGES = {}

# =========================================================
# COLOR SYSTEM
# =========================================================

class C:

    RESET = "\033[0m"

    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"

    BOLD = "\033[1m"

# =========================================================
# UI WIDTH
# =========================================================

UI_WIDTH = 56

# =========================================================
# CENTER
# =========================================================

def ui_center(text):

    text = str(text)

    return text.center(UI_WIDTH)

# =========================================================
# LINE
# =========================================================

def ui_line(color=C.BRIGHT_MAGENTA):

    print(
        f"{color}"
        + "═" * UI_WIDTH
        + f"{C.RESET}"
    )

# =========================================================
# BOX TITLE
# =========================================================

def ui_title(title):

    print()

    ui_line(C.BRIGHT_MAGENTA)

    print(
        f"{C.BRIGHT_WHITE}"
        f"{ui_center(title)}"
        f"{C.RESET}"
    )

    ui_line(C.BRIGHT_MAGENTA)

# =========================================================
# BOX MESSAGE
# =========================================================

def ui_message(message, color=C.BRIGHT_WHITE):

    print(
        f"{color}"
        f"{ui_center(message)}"
        f"{C.RESET}"
    )

# =========================================================
# STATUS
# =========================================================

def ui_status(label, value, color=C.BRIGHT_CYAN):

    left = f" {label} "

    dots = "." * max(1, UI_WIDTH - len(left) - len(str(value)) - 2)

    print(
        f"{C.BRIGHT_BLACK}"
        f"{left}{dots} "
        f"{color}{value}"
        f"{C.RESET}"
    )

# =========================================================
# MENU ITEM
# =========================================================

def ui_menu(index, text, color=C.BRIGHT_GREEN):

    line = f" [{index}] {text}"

    print(
        f"{color}"
        f"{line}"
        f"{C.RESET}"
    )

# =========================================================
# INPUT BAR
# =========================================================

def ui_input(label="INPUT"):

    return input(
        f"{C.BRIGHT_MAGENTA}"
        f"┌─[{label}]\n"
        f"└──> "
        f"{C.RESET}"
    )

# =========================================================
# SPLASH SCREEN
# =========================================================

def splash_screen():

    print();

    print(
        f"{C.BRIGHT_MAGENTA}"
        "███╗   ██╗ █████╗ ███████╗"
    )

    print(
        "████╗  ██║██╔══██╗██╔════╝"
    )

    print(
        "██╔██╗ ██║███████║███████╗"
    )

    print(
        "██║╚██╗██║██╔══██║╚════██║"
    )

    print(
        "██║ ╚████║██║  ██║███████║"
    )

    print(
        "╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝"
        f"{C.RESET}"
    )

    print()

    ui_message(
        "NANOACTSCRIPT ENGINE",
        C.BRIGHT_CYAN
    )

    ui_message(
        "Simple small-scale programming language",
        C.BRIGHT_YELLOW
    )
    
    ui_message(
        "Simple sandbox environment engine",
        C.BRIGHT_YELLOW
    )

    print()

# =========================================================
# SLOW PRINT
# =========================================================

def slow_print(text, delay=0.01, color=""):

    import time

    text = str(text)

    print(color, end="", flush=True)

    for char in text:

        print(char, end="", flush=True)

        try:
            time.sleep(delay)

        except Exception:
            pass

    print(C.RESET)

# =========================================================
# SAFE CONSTANTS
# =========================================================

SAFE_VAR_PATTERN = re.compile(
    r'^[A-Za-z_][A-Za-z0-9_]*$'
)

SAFE_EXPRESSION_PATTERN = re.compile(
    r'^[0-9A-Za-z_\s+\-*/%()<>!=&|.]+$'
)

# =========================================================
# SCRIPT ENGINE UI
# =========================================================

def script_banner():

    print(f"{C.BRIGHT_MAGENTA}{C.BOLD}")

    print("╔══════════════════════════════════════════════╗")
    print("║         NANOACTSCRIPT ENGINE                 ║")
    print("║             PROTOCOL v1.00                   ║")
    print("╚══════════════════════════════════════════════╝")

    print(C.RESET)

# =========================================================
# SCRIPT ENGINE ERROR
# =========================================================

def script_error(code, message, errno):

    try:

        return (
            f"[{errno}] "
            f"{code}: {message}"
        )

    except Exception:

        return (
            f"[{errno}] "
            f"{code}: {message}"
        )

# =========================================================
# SAFE VALUE PARSER
# =========================================================

def parse_value(value):

    if value is None:
        return ""

    value = str(value).strip()

    if re.fullmatch(r'-?\d+', value):

        try:
            return int(value)

        except ValueError:
            return 0

    if re.fullmatch(r'-?\d+\.\d+', value):

        try:
            return float(value)

        except ValueError:
            return 0.0

    if (
        len(value) >= 2 and
        value.startswith('"') and
        value.endswith('"')
    ):

        return value[1:-1]

    lower = value.lower()

    if lower == "true":
        return True

    if lower == "false":
        return False

    if value == "M.random()":

        return random.random()

    floor_match = re.fullmatch(
        r'M\.floor\((.+)\)',
        value
    )

    if floor_match:

        raw = floor_match.group(1).strip()

        parsed = parse_value(raw)

        try:

            return math.floor(
                float(parsed)
            )

        except:

            return 0

    round_match = re.fullmatch(
        r'M\.round\((.+)\)',
        value
    )

    if round_match:

        raw = round_match.group(1).strip()

        parsed = parse_value(raw)

        try:

            return round(
                float(parsed)
            )

        except:

            return 0

    randint_match = re.fullmatch(
        r'M\.randint\((.+),(.+)\)',
        value
    )

    if randint_match:

        try:

            min_val = int(parse_value(randint_match.group(1).strip()))
            max_val = int(parse_value(randint_match.group(2).strip()))

            return random.randint(min_val, max_val)

        except:

            return 0

    choice_match = re.fullmatch(
        r'M\.choice\((.+)\)',
        value
    )

    if choice_match:

        raw = choice_match.group(1).strip()

        if raw in SCRIPT_VARIABLES and isinstance(SCRIPT_VARIABLES[raw], list):

            arr = SCRIPT_VARIABLES[raw]

            if arr:

                return random.choice(arr)

        return None

    len_match = re.fullmatch(
        r'(.+?)\.len',
        value
    )

    if len_match:

        var_name = len_match.group(1).strip()

        if var_name in SCRIPT_VARIABLES:

            var = SCRIPT_VARIABLES[var_name]

            if isinstance(var, (list, str)):

                return len(var)

        return 0

    if value in SCRIPT_VARIABLES:

        return SCRIPT_VARIABLES[value]

    return value

SCRIPT_BPM = 120

NOTE_FREQUENCIES = {
    "C0": 16.35, "C#0": 17.32, "D0": 18.35, "D#0": 19.45, "E0": 20.60, "F0": 21.83,
    "F#0": 23.12, "G0": 24.50, "G#0": 25.96, "A0": 27.50, "A#0": 29.13, "B0": 30.87,
    
    "C1": 32.70, "C#1": 34.65, "D1": 36.71, "D#1": 38.89, "E1": 41.20, "F1": 43.65,
    "F#1": 46.25, "G1": 49.00, "G#1": 51.91, "A1": 55.00, "A#1": 58.27, "B1": 61.74,
    
    "C2": 65.41, "C#2": 69.30, "D2": 73.42, "D#2": 77.78, "E2": 82.41, "F2": 87.31,
    "F#2": 92.50, "G2": 98.00, "G#2": 103.83, "A2": 110.00, "A#2": 116.54, "B2": 123.47,
    
    "C3": 130.81, "C#3": 138.59, "D3": 146.83, "D#3": 155.56, "E3": 164.81, "F3": 174.61,
    "F#3": 185.00, "G3": 196.00, "G#3": 207.65, "A3": 220.00, "A#3": 233.08, "B3": 246.94,
    
    "C4": 261.63, "C#4": 277.18, "D4": 293.66, "D#4": 311.13, "E4": 329.63, "F4": 349.23,
    "F#4": 369.99, "G4": 392.00, "G#4": 415.30, "A4": 440.00, "A#4": 466.16, "B4": 493.88,
    
    "C5": 523.25, "C#5": 554.37, "D5": 587.33, "D#5": 622.25, "E5": 659.25, "F5": 698.46,
    "F#5": 739.99, "G5": 783.99, "G#5": 830.61, "A5": 880.00, "A#5": 932.33, "B5": 987.77,
    
    "C6": 1046.50, "C#6": 1108.73, "D6": 1174.66, "D#6": 1244.51, "E6": 1318.51, "F6": 1396.91,
    "F#6": 1479.98, "G6": 1567.98, "G#6": 1661.22, "A6": 1760.00, "A#6": 1864.66, "B6": 1975.53,
    
    "C7": 2093.00, "C#7": 2217.46, "D7": 2349.32, "D#7": 2489.02, "E7": 2637.02, "F7": 2793.83,
    "F#7": 2959.96, "G7": 3135.96, "G#7": 3322.44, "A7": 3520.00, "A#7": 3729.31, "B7": 3951.07,
    
    "C8": 4186.01, "C#8": 4434.92, "D8": 4698.63, "D#8": 4978.03, "E8": 5274.04, "F8": 5587.65,
    "F#8": 5919.91, "G8": 6271.93, "G#8": 6644.88, "A8": 7040.00, "A#8": 7458.62, "B8": 7902.13,
}

def cmd_temp(command):

    global SCRIPT_BPM

    match = re.fullmatch(
        r'temp\((.+?)\)',
        command
    )

    if not match:

        print(
            script_error(
                "INVALID_TEMP_SYNTAX",
                "Invalid temp() syntax.",
                "SND01"
            )
        )
        return

    bpm_val = parse_value(match.group(1).strip())

    try:

        bpm_val = int(bpm_val)

    except:

        print(
            script_error(
                "TEMP_VALUE_ERROR",
                "BPM must be numeric.",
                "SND02"
            )
        )
        return

    if bpm_val < 10 or bpm_val > 600:

        print(
            script_error(
                "TEMP_RANGE_ERROR",
                "BPM must be between 10 and 600.",
                "SND03"
            )
        )
        return

    SCRIPT_BPM = bpm_val

    print(
        f"{C.BRIGHT_GREEN}"
        f"[ BPM SET ] {bpm_val}"
        f"{C.RESET}"
    )

def cmd_sound(command):

    match = re.fullmatch(
        r'sound\((.+?),(.+?)\)',
        command
    )

    if not match:

        print(
            script_error(
                "INVALID_SOUND_SYNTAX",
                "Invalid sound() syntax.",
                "SND04"
            )
        )
        return

    note_code = match.group(1).strip()
    duration_val = match.group(2).strip()

    if note_code not in NOTE_FREQUENCIES:

        print(
            script_error(
                "INVALID_NOTE",
                f"Note '{note_code}' not found. Use format: C4, D#5, etc.",
                "SND05"
            )
        )
        return

    frequency = NOTE_FREQUENCIES[note_code]

    duration_str = duration_val.lower().strip()

    if duration_str.endswith("ms"):

        try:

            duration_ms = int(duration_str[:-2])

        except:

            print(
                script_error(
                    "INVALID_DURATION",
                    "Duration must be numeric (e.g., '500ms').",
                    "SND06"
                )
            )
            return

    else:

        try:

            note_length = float(parse_value(duration_str))

        except:

            print(
                script_error(
                    "INVALID_NOTE_LENGTH",
                    "Note length must be numeric.",
                    "SND07"
                )
            )
            return

        whole_note_ms = (60000 / SCRIPT_BPM) * 4
        duration_ms = int(whole_note_ms * note_length)

    if duration_ms < 10:

        print(
            script_error(
                "DURATION_TOO_SHORT",
                "Duration must be at least 10ms.",
                "SND08"
            )
        )
        return

    if duration_ms > 60000:

        print(
            script_error(
                "DURATION_TOO_LONG",
                "Duration must not exceed 60000ms.",
                "SND09"
            )
        )
        return

    try:

        winsound.Beep(int(frequency), duration_ms)

    except Exception as e:

        print(
            script_error(
                "SOUND_PLAYBACK_ERROR",
                str(e),
                "SND10"
            )
        )
        
def safe_eval(expression):

    safe_globals = {
        "__builtins__": {}
    }

    safe_locals = {

        **SCRIPT_VARIABLES,

        "M": type(
            "MathModule",
            (),
            {
                "random": random.random,
                "floor": math.floor,
                "round": round,
            }
        )()
    }

    return eval(
        expression,
        safe_globals,
        safe_locals
    )

def render_display(name):

    if name not in SCRIPT_DISPLAYS:

        print(
            script_error(
                "DISPLAY_NOT_FOUND",
                f"Display '{name}' does not exist.",
                "S01"
            )
        )
        return

    state = SCRIPT_DISPLAYS.get(name)

    if state == 1:

        print(
            f"{C.BRIGHT_GREEN}〇{C.RESET}"
        )

    elif state == 0:

        print(
            f"{C.BRIGHT_RED}✕{C.RESET}"
        )

    else:

        print(
            script_error(
                "INVALID_DISPLAY_STATE",
                f"Display '{name}' has invalid state.",
                "S02"
            )
        )

def engine_output(value):

    try:

        value = str(value)

    except Exception:

        value = "[OUTPUT_ERROR]"

    value = value.replace(
        r"\ent",
        "\n"
    )

    print(
        f"{C.BRIGHT_WHITE}"
        f"{value}"
        f"{C.RESET}"
    )

def cmd_inli(command):

    match = re.fullmatch(
        r'inli\((.+?),\[(.*)\]\)',
        command
    )

    if not match:

        print(
            script_error(
                "INVALID_ARRAY_DECLARATION",
                "Invalid inli() syntax.",
                "A01"
            )
        )
        return

    name = match.group(1).strip()

    raw_items = match.group(2).strip()

    if raw_items == "":

        SCRIPT_VARIABLES[name] = []

        print(
            f"{C.BRIGHT_GREEN}"
            f"[ ARRAY REGISTERED ] "
            f"{name}"
            f"{C.RESET}"
        )

        return

    items = []

    split_items = raw_items.split(",")

    for item in split_items:

        parsed = parse_value(
            item.strip()
        )

        items.append(parsed)

    SCRIPT_VARIABLES[name] = items

    print(
        f"{C.BRIGHT_GREEN}"
        f"[ ARRAY REGISTERED ] "
        f"{name}"
        f"{C.RESET}"
    )

def cmd_int(command):

    match = re.fullmatch(
        r'int\((.+?),(.+?)\)',
        command
    )

    if not match:

        print(
            script_error(
                "INVALID_INT_DECLARATION",
                "Invalid int() syntax.",
                "S03"
            )
        )
        return

    name = match.group(1).strip()
    raw_value = match.group(2).strip()

    if not SAFE_VAR_PATTERN.fullmatch(name):

        print(
            script_error(
                "INVALID_VARIABLE_NAME",
                f"'{name}' is not a valid variable name.",
                "S03A"
            )
        )
        return

    if (
        raw_value.startswith('"') and
        raw_value.endswith('"')
    ):

        SCRIPT_VARIABLES[name] = raw_value[1:-1]
        return

    parsed = parse_value(raw_value)

    if isinstance(parsed, str):

        try:

            if SAFE_EXPRESSION_PATTERN.fullmatch(parsed):

                parsed = safe_eval(parsed)

        except Exception:

            print(
                script_error(
                    "EXPRESSION_EVALUATION_FAILED",
                    f"Failed to evaluate '{parsed}'.",
                    "S03B"
                )
            )
            return

    SCRIPT_VARIABLES[name] = parsed

def cmd_on(command):

    match = re.fullmatch(
        r'on\((.+)\)',
        command
    )

    if not match:

        print(
            script_error(
                "INVALID_ON_SYNTAX",
                "Invalid on() syntax.",
                "S04"
            )
        )
        return

    raw = match.group(1).strip()

    if (
        raw.startswith('"') and
        raw.endswith('"')
    ):

        engine_output(raw[1:-1])
        return

    if raw in SCRIPT_VARIABLES:

        engine_output(SCRIPT_VARIABLES[raw])
        return

    value = parse_value(raw)

    if isinstance(value, str) and value == raw:

        print(
            script_error(
                "UNDEFINED_VARIABLE",
                f"Variable '{raw}' does not exist.",
                "S04A"
            )
        )
        return

    engine_output(value)

def cmd_display(command):

    match = re.fullmatch(
        r'display\((.+?)\)',
        command
    )

    if not match:

        print(
            script_error(
                "INVALID_DISPLAY_DECLARATION",
                "Invalid display() syntax.",
                "S05"
            )
        )
        return

    name = match.group(1).strip()

    if not SAFE_VAR_PATTERN.fullmatch(name):

        print(
            script_error(
                "INVALID_DISPLAY_NAME",
                f"'{name}' is not valid.",
                "S05A"
            )
        )
        return

    SCRIPT_DISPLAYS[name] = 0

def cmd_in_dis(command):

    match = re.fullmatch(
        r'in dis \((.+?)\)\s*=\s*(.+)',
        command
    )

    if not match:

        print(
            script_error(
                "INVALID_DISPLAY_INPUT",
                "Invalid display assignment syntax.",
                "S06"
            )
        )
        return

    name = match.group(1).strip()
    value = match.group(2).strip()

    if name not in SCRIPT_DISPLAYS:

        print(
            script_error(
                "DISPLAY_NOT_FOUND",
                f"Display '{name}' does not exist.",
                "S07"
            )
        )
        return

    try:

        value = int(value)

    except ValueError:

        print(
            script_error(
                "INVALID_DISPLAY_VALUE",
                "Display value must be 0 or 1.",
                "S08"
            )
        )
        return

    if value not in (0, 1):

        print(
            script_error(
                "INVALID_DISPLAY_VALUE",
                "Display value must be 0 or 1.",
                "S09"
            )
        )
        return

    SCRIPT_DISPLAYS[name] = value

    render_display(name)

def cmd_multidis(command):

    match = re.fullmatch(
        r'multidis\((.+?),(.+?)\)',
        command
    )

    if not match:

        print(
            script_error(
                "INVALID_MULTIDIS_DECLARATION",
                "Invalid multidis() syntax.",
                "MD01"
            )
        )
        return

    name = match.group(1).strip()
    value = match.group(2).strip()

    if not SAFE_VAR_PATTERN.fullmatch(name):

        print(
            script_error(
                "INVALID_MULTIDIS_NAME",
                f"'{name}' is not a valid display name.",
                "MD02"
            )
        )
        return

    if (
        value.startswith('"') and
        value.endswith('"')
    ):

        value = value[1:-1]

    else:

        value = parse_value(value)
        value = str(value)

    SCRIPT_DISPLAYS[name] = value

    print_multidis(name)

def print_multidis(name):

    if name not in SCRIPT_DISPLAYS:

        print(
            script_error(
                "UNKNOWN_MULTIDIS",
                f"MultiDis '{name}' does not exist.",
                "MD03"
            )
        )
        return

    data = SCRIPT_DISPLAYS[name]

    print(f"[{data}]")

def cmd_in_multidis(command):

    match = re.fullmatch(
        r'in multidis\s*\((.+?)\)\s*=\s*(.+)',
        command
    )

    if not match:

        print(
            script_error(
                "INVALID_MULTIDIS_INPUT",
                "Invalid in multidis() syntax.",
                "MD04"
            )
        )
        return

    name = match.group(1).strip()
    value = match.group(2).strip()

    if name not in SCRIPT_DISPLAYS:

        print(
            script_error(
                "UNKNOWN_MULTIDIS",
                f"MultiDis '{name}' does not exist.",
                "MD05"
            )
        )
        return

    if (
        value.startswith('"') and
        value.endswith('"')
    ):

        value = value[1:-1]

    else:

        value = parse_value(value)
        value = str(value)

    SCRIPT_DISPLAYS[name] = value

    print_multidis(name)

def cmd_func(command):

    match = re.fullmatch(
        r'func\s+([A-Za-z_][A-Za-z0-9_]*)\(\)\{(.+)\}',
        command,
        re.DOTALL
    )

    if not match:

        print(
            script_error(
                "INVALID_FUNCTION",
                "Invalid func syntax.",
                "S10"
            )
        )
        return

    name = match.group(1).strip()
    body = match.group(2).strip()

    if body == "":

        print(
            script_error(
                "EMPTY_FUNCTION",
                "Function body cannot be empty.",
                "S10A"
            )
        )
        return

    SCRIPT_FUNCTIONS[name] = body

    print(
        f"{C.BRIGHT_GREEN}"
        f"[ FUNCTION REGISTERED ] "
        f"{name}"
        f"{C.RESET}"
    )

def cmd_gage(command):

    match = re.fullmatch(
        r'gage\((.+?)\)',
        command
    )

    if not match:

        print(
            script_error(
                "INVALID_GAGE_SYNTAX",
                "Invalid gage() syntax.",
                "G01"
            )
        )
        return

    name = match.group(1).strip()

    SCRIPT_GAGES[name] = [0] * 10

def print_gage(name):

    if name not in SCRIPT_GAGES:

        print(
            script_error(
                "UNKNOWN_GAGE",
                f"Gage '{name}' does not exist.",
                "G02"
            )
        )
        return

    data = SCRIPT_GAGES[name]

    visual = "".join(
        "■" if x else "□"
        for x in data
    )

    print(f"[{visual}]")

def cmd_gagecn(command):

    match = re.fullmatch(
        r'(.+?)\.gagecn\((.+?)\)',
        command
    )

    if not match:

        print(
            script_error(
                "INVALID_GAGECN_SYNTAX",
                "Invalid .gagecn() syntax.",
                "G03"
            )
        )
        return

    name = match.group(1).strip()

    value = int(
        parse_value(
            match.group(2).strip()
        )
    )

    if name not in SCRIPT_GAGES:

        print(
            script_error(
                "UNKNOWN_GAGE",
                f"Gage '{name}' does not exist.",
                "G04"
            )
        )
        return

    value = max(0, min(10, value))

    SCRIPT_GAGES[name] = [
        1 if i < value else 0
        for i in range(10)
    ]

    print_gage(name)

def cmd_gagepin(command):

    match = re.fullmatch(
        r'(.+?)\.gagepin\((.+?),(.+?)\)',
        command
    )

    if not match:

        print(
            script_error(
                "INVALID_GAGEPIN_SYNTAX",
                "Invalid .gagepin() syntax.",
                "G05"
            )
        )
        return

    name = match.group(1).strip()

    index = int(
        parse_value(
            match.group(2).strip()
        )
    )

    value = int(
        parse_value(
            match.group(3).strip()
        )
    )

    if name not in SCRIPT_GAGES:

        print(
            script_error(
                "UNKNOWN_GAGE",
                f"Gage '{name}' does not exist.",
                "G06"
            )
        )
        return

    if not (1 <= index <= 10):

        print(
            script_error(
                "INVALID_GAGE_INDEX",
                "Gage index must be 1-10.",
                "G07"
            )
        )
        return

    SCRIPT_GAGES[name][index - 1] = 1 if value else 0

    print_gage(name)

def cmd_array_on(command):

    match = re.fullmatch(
        r'(.+?)\.on\((.+?)\)',
        command
    )

    if not match:
        return False

    name = match.group(1).strip()

    value = parse_value(
        match.group(2).strip()
    )

    if name not in SCRIPT_VARIABLES:

        print(
            script_error(
                "UNKNOWN_ARRAY",
                f"Array '{name}' does not exist.",
                "A20"
            )
        )
        return True

    if not isinstance(SCRIPT_VARIABLES[name], list):

        print(
            script_error(
                "NOT_ARRAY",
                f"'{name}' is not an array.",
                "A21"
            )
        )
        return True

    SCRIPT_VARIABLES[name].append(value)

    return True

def cmd_array_unon(command):

    match = re.fullmatch(
        r'(.+?)\.unon\((.+?)\)',
        command
    )

    if not match:
        return False

    name = match.group(1).strip()

    value = parse_value(
        match.group(2).strip()
    )

    if name not in SCRIPT_VARIABLES:
        return True

    if not isinstance(SCRIPT_VARIABLES[name], list):
        return True

    SCRIPT_VARIABLES[name].insert(0, value)

    return True

def cmd_array_off(command):

    match = re.fullmatch(
        r'(.+?)\.off\(\)',
        command
    )

    if not match:
        return False

    name = match.group(1).strip()

    if name not in SCRIPT_VARIABLES:
        return True

    if not isinstance(SCRIPT_VARIABLES[name], list):
        return True

    if SCRIPT_VARIABLES[name]:

        SCRIPT_VARIABLES[name].pop()

    return True

def cmd_array_unoff(command):

    match = re.fullmatch(
        r'(.+?)\.unoff\(\)',
        command
    )

    if not match:
        return False

    name = match.group(1).strip()

    if name not in SCRIPT_VARIABLES:
        return True

    if not isinstance(SCRIPT_VARIABLES[name], list):
        return True

    if SCRIPT_VARIABLES[name]:

        SCRIPT_VARIABLES[name].pop(0)

    return True

def cmd_array_pointer(command):

    match = re.fullmatch(
        r'(.+?)\.pointer\((.+?),(.+?)\)',
        command
    )

    if not match:
        return False

    name = match.group(1).strip()

    index = int(
        parse_value(
            match.group(2).strip()
        )
    )

    value = parse_value(
        match.group(3).strip()
    )

    if name not in SCRIPT_VARIABLES:
        return True

    if not isinstance(SCRIPT_VARIABLES[name], list):
        return True

    if not (
        0 <= index < len(SCRIPT_VARIABLES[name])
    ):

        print(
            script_error(
                "ARRAY_INDEX_ERROR",
                "Index out of range.",
                "A22"
            )
        )

        return True

    SCRIPT_VARIABLES[name][index] = value

    return True

class LoopBreak(Exception):
    pass

class LoopContinue(Exception):
    pass

LAST_IF_RESULT = False

def cmd_if(command):

    global LAST_IF_RESULT

    match = re.fullmatch(
        r'if\((.*?)\)\{(.*)\}',
        command,
        re.DOTALL
    )

    if not match:

        print(
            script_error(
                "INVALID_IF_SYNTAX",
                "Invalid if() syntax.",
                "S19"
            )
        )
        return

    condition = match.group(1).strip()
    body = match.group(2).strip()

    if body == "":

        print(
            script_error(
                "EMPTY_IF_BODY",
                "if() body cannot be empty.",
                "S19A"
            )
        )
        return

    try:

        result = safe_eval(condition)

    except NameError as e:

        print(
            script_error(
                "IF_VARIABLE_NOT_FOUND",
                str(e),
                "S20A"
            )
        )
        return

    except SyntaxError as e:

        print(
            script_error(
                "IF_SYNTAX_ERROR",
                str(e),
                "S20B"
            )
        )
        return

    except Exception as e:

        print(
            script_error(
                "IF_EVALUATION_FAILED",
                str(e),
                "S20"
            )
        )
        return

    if bool(result):

        LAST_IF_RESULT = True

        try:

            execute_script(body)

        except Exception as e:

            print(
                script_error(
                    "IF_RUNTIME_ERROR",
                    str(e),
                    "S20C"
                )
            )

    else:

        LAST_IF_RESULT = False

def cmd_ifel(command):

    global LAST_IF_RESULT

    match = re.fullmatch(
        r'ifel\((.+?)\)\{(.*)\}',
        command,
        re.DOTALL
    )

    if not match:

        print(
            script_error(
                "INVALID_IFEL_SYNTAX",
                "Invalid ifel() syntax.",
                "S20D"
            )
        )
        return

    if LAST_IF_RESULT:
        return

    condition = match.group(1).strip()
    body = match.group(2).strip()

    if body == "":

        print(
            script_error(
                "EMPTY_IFEL_BODY",
                "ifel() body cannot be empty.",
                "S20E"
            )
        )
        return

    try:

        result = safe_eval(condition)

    except Exception as e:

        print(
            script_error(
                "IFEL_EVALUATION_FAILED",
                str(e),
                "S20F"
            )
        )
        return

    if bool(result):

        LAST_IF_RESULT = True

        try:

            execute_script(body)

        except Exception as e:

            print(
                script_error(
                    "IFEL_RUNTIME_ERROR",
                    str(e),
                    "S20G"
                )
            )

    else:

        LAST_IF_RESULT = False

def cmd_else(command):

    global LAST_IF_RESULT

    match = re.fullmatch(
        r'else\{(.*)\}',
        command,
        re.DOTALL
    )

    if not match:

        print(
            script_error(
                "INVALID_ELSE_SYNTAX",
                "Invalid else syntax.",
                "S20H"
            )
        )
        return

    body = match.group(1).strip()

    if body == "":

        print(
            script_error(
                "EMPTY_ELSE_BODY",
                "else body cannot be empty.",
                "S20I"
            )
        )
        return

    if not LAST_IF_RESULT:

        try:

            execute_script(body)

        except Exception as e:

            print(
                script_error(
                    "ELSE_RUNTIME_ERROR",
                    str(e),
                    "S20J"
                )
            )

    LAST_IF_RESULT = False

def cmd_while(command):

    match = re.fullmatch(
        r'while\s*\((.*?)\)\s*\{(.*)\}',
        command,
        re.DOTALL
    )

    if not match:

        print(
            script_error(
                "INVALID_WHILE_SYNTAX",
                "Invalid while() syntax.",
                "S21"
            )
        )

        return

    condition = match.group(1).strip()
    body = match.group(2).strip()

    if body == "":

        print(
            script_error(
                "EMPTY_WHILE_BODY",
                "while() body cannot be empty.",
                "S21A"
            )
        )
        return

    loop_count = 0
    max_loops = 10000

    while True:

        loop_count += 1

        if loop_count > max_loops:

            print(
                script_error(
                    "WHILE_LIMIT_EXCEEDED",
                    "Loop exceeded safety limit.",
                    "S22"
                )
            )

            return

        try:

            result = safe_eval(condition)

        except NameError as e:

            print(
                script_error(
                    "WHILE_VARIABLE_NOT_FOUND",
                    str(e),
                    "S23A"
                )
            )

            return

        except SyntaxError as e:

            print(
                script_error(
                    "WHILE_CONDITION_SYNTAX_ERROR",
                    str(e),
                    "S23B"
                )
            )

            return

        except Exception as e:

            print(
                script_error(
                    "WHILE_CONDITION_FAILURE",
                    str(e),
                    "S23"
                )
            )

            return

        if not result:
            break

        try:

            execute_script(body)

        except LoopBreak:

            break

        except LoopContinue:

            continue

        except Exception as e:

            print(
                script_error(
                    "WHILE_RUNTIME_FAILURE",
                    str(e),
                    "S24"
                )
            )

            return

def cmd_for(command):

    match = re.fullmatch(
        r'for\s*\(\s*(.+?)\s*,\s*(.+?)\s*,\s*(.+?)\s*\)\s*\{(.*)\}',
        command,
        re.DOTALL
    )

    if not match:

        print(
            script_error(
                "INVALID_FOR_SYNTAX",
                "Invalid for() syntax.",
                "F01"
            )
        )
        return

    var_name = match.group(1).strip()
    start_val = parse_value(match.group(2).strip())
    end_val = parse_value(match.group(3).strip())
    body = match.group(4).strip()

    if not SAFE_VAR_PATTERN.fullmatch(var_name):

        print(
            script_error(
                "INVALID_FOR_VARIABLE",
                f"'{var_name}' is not a valid variable name.",
                "F02"
            )
        )
        return

    if body == "":

        print(
            script_error(
                "EMPTY_FOR_BODY",
                "for() body cannot be empty.",
                "F03"
            )
        )
        return

    try:

        start_val = int(start_val)
        end_val = int(end_val)

    except:

        print(
            script_error(
                "FOR_VALUE_ERROR",
                "for() values must be numeric.",
                "F04"
            )
        )
        return

    loop_count = 0
    max_loops = 10000

    if start_val <= end_val:

        current = start_val

        while current < end_val:

            loop_count += 1

            if loop_count > max_loops:

                print(
                    script_error(
                        "FOR_LIMIT_EXCEEDED",
                        "Loop exceeded safety limit.",
                        "F05"
                    )
                )

                return

            SCRIPT_VARIABLES[var_name] = current

            try:

                execute_script(body)

            except LoopBreak:

                break

            except LoopContinue:

                current += 1
                continue

            except Exception as e:

                print(
                    script_error(
                        "FOR_RUNTIME_ERROR",
                        str(e),
                        "F06"
                    )
                )

                return

            current += 1

    else:

        current = start_val

        while current > end_val:

            loop_count += 1

            if loop_count > max_loops:

                print(
                    script_error(
                        "FOR_LIMIT_EXCEEDED",
                        "Loop exceeded safety limit.",
                        "F05"
                    )
                )

                return

            SCRIPT_VARIABLES[var_name] = current

            try:

                execute_script(body)

            except LoopBreak:

                break

            except LoopContinue:

                current -= 1
                continue

            except Exception as e:

                print(
                    script_error(
                        "FOR_RUNTIME_ERROR",
                        str(e),
                        "F06"
                    )
                )

                return

            current -= 1

def cmd_for_of(command):

    match = re.fullmatch(
        r'for\s*of\s*\(\s*(.+?)\s*,\s*(.+?)\s*\)\s*\{(.*)\}',
        command,
        re.DOTALL
    )

    if not match:

        print(
            script_error(
                "INVALID_FOR_OF_SYNTAX",
                "Invalid for of() syntax.",
                "FO01"
            )
        )
        return

    var_name = match.group(1).strip()
    array_name = match.group(2).strip()
    body = match.group(3).strip()

    if not SAFE_VAR_PATTERN.fullmatch(var_name):

        print(
            script_error(
                "INVALID_FOR_OF_VARIABLE",
                f"'{var_name}' is not a valid variable name.",
                "FO02"
            )
        )
        return

    if array_name not in SCRIPT_VARIABLES:

        print(
            script_error(
                "ARRAY_NOT_FOUND",
                f"Array '{array_name}' does not exist.",
                "FO03"
            )
        )
        return

    if not isinstance(SCRIPT_VARIABLES[array_name], list):

        print(
            script_error(
                "NOT_ARRAY",
                f"'{array_name}' is not an array.",
                "FO04"
            )
        )
        return

    if body == "":

        print(
            script_error(
                "EMPTY_FOR_OF_BODY",
                "for of() body cannot be empty.",
                "FO05"
            )
        )
        return

    array = SCRIPT_VARIABLES[array_name]

    loop_count = 0
    max_loops = 10000

    for element in array:

        loop_count += 1

        if loop_count > max_loops:

            print(
                script_error(
                    "FOR_OF_LIMIT_EXCEEDED",
                    "Loop exceeded safety limit.",
                    "FO06"
                )
            )

            return

        SCRIPT_VARIABLES[var_name] = element

        try:

            execute_script(body)

        except LoopBreak:

            break

        except LoopContinue:

            continue

        except Exception as e:

            print(
                script_error(
                    "FOR_OF_RUNTIME_ERROR",
                    str(e),
                    "FO07"
                )
            )

            return

def cmd_swi(command):

    match = re.fullmatch(
        r'swi\((.+?)\)\{(.*)\}',
        command,
        re.DOTALL
    )

    if not match:

        print(
            script_error(
                "INVALID_SWITCH_SYNTAX",
                "Invalid swi() syntax.",
                "SW01"
            )
        )
        return

    switch_value = parse_value(match.group(1).strip())
    body = match.group(2).strip()

    if body == "":

        print(
            script_error(
                "EMPTY_SWITCH_BODY",
                "swi() body cannot be empty.",
                "SW02"
            )
        )
        return

    case_pattern = re.findall(
        r'case\((.+?)\)\{(.+?)\}(?=case|default|\Z)',
        body,
        re.DOTALL
    )

    default_pattern = re.search(
        r'default\{(.+?)\}',
        body,
        re.DOTALL
    )

    matched = False

    for case_val, case_body in case_pattern:

        case_val = parse_value(case_val.strip())

        if switch_value == case_val:

            try:

                execute_script(case_body.strip())

            except Exception as e:

                print(
                    script_error(
                        "SWITCH_RUNTIME_ERROR",
                        str(e),
                        "SW03"
                    )
                )

            matched = True
            break

    if not matched and default_pattern:

        default_body = default_pattern.group(1).strip()

        try:

            execute_script(default_body)

        except Exception as e:

            print(
                script_error(
                    "SWITCH_DEFAULT_ERROR",
                    str(e),
                    "SW04"
                )
            )

def cmd_break(command):

    if command != "break":

        print(
            script_error(
                "INVALID_BREAK_SYNTAX",
                "Invalid break syntax.",
                "LB01"
            )
        )
        return

    raise LoopBreak()

def cmd_continue(command):

    if command != "continue":

        print(
            script_error(
                "INVALID_CONTINUE_SYNTAX",
                "Invalid continue syntax.",
                "LB02"
            )
        )
        return

    raise LoopContinue()

def split_cipher_commands(script):

    commands = []
    current = []
    brace_depth = 0
    paren_depth = 0
    bracket_depth = 0
    in_string = False
    escape = False

    for i, char in enumerate(script):
        if escape:
            current.append(char)
            escape = False
            continue

        if char == "\\":
            current.append(char)
            escape = True
            continue

        if char == '"':
            in_string = not in_string
            current.append(char)
            continue

        if in_string:
            current.append(char)
            continue

        if char == "{":
            brace_depth += 1
            current.append(char)
            continue

        if char == "}":
            brace_depth -= 1
            current.append(char)
            continue

        if char == "(":
            paren_depth += 1
            current.append(char)
            continue

        if char == ")":
            paren_depth -= 1
            current.append(char)
            continue

        if char == "[":
            bracket_depth += 1
            current.append(char)
            continue

        if char == "]":
            bracket_depth -= 1
            current.append(char)
            continue

        if char == "\n":
            if brace_depth == 0 and paren_depth == 0 and bracket_depth == 0 and not in_string:
                continue
            else:
                current.append(" ")
                continue

        if (
            char == ";"
            and brace_depth == 0
            and paren_depth == 0
            and bracket_depth == 0
            and not in_string
        ):
            command = "".join(current).strip()
            if command:
                commands.append(command)
            current = []
            continue

        current.append(char)

    final_command = "".join(current).strip()
    if final_command:

        if final_command and not final_command.endswith("}"):
            print(
                script_error(
                    "MISSING_COMMAND_SEPARATOR",
                    f"Command must end with ';' or '}}': {final_command}",
                    "PARSE01"
                )
            )
            return []

        commands.append(final_command)

    return commands

FUNC_RETURN_VALUE = None

class FunctionReturn(Exception):
    def __init__(self, value):
        self.value = value
        super().__init__()

def cmd_func_run(command):

    global FUNC_RETURN_VALUE

    match = re.fullmatch(
        r'([A-Za-z_][A-Za-z0-9_]*)\.run\((.*?)\)',
        command
    )

    if not match:

        print(
            script_error(
                "INVALID_FUNCTION_RUN",
                "Invalid function execution syntax.",
                "S11"
            )
        )
        return

    name = match.group(1).strip()

    if name not in SCRIPT_FUNCTIONS:

        print(
            script_error(
                "FUNCTION_NOT_FOUND",
                f"Function '{name}' does not exist.",
                "S12"
            )
        )
        return

    body = SCRIPT_FUNCTIONS.get(name)

    if not body:

        print(
            script_error(
                "EMPTY_FUNCTION_BODY",
                f"Function '{name}' is empty.",
                "S12A"
            )
        )
        return

    FUNC_RETURN_VALUE = None

    try:

        execute_script(body)

    except Exception as e:

        print(
            script_error(
                "FUNCTION_RUNTIME_ERROR",
                str(e),
                "S12B"
            )
        )

def cmd_func_return(command):

    match = re.fullmatch(
        r'>>\s*(.+)',
        command
    )

    if not match:

        print(
            script_error(
                "INVALID_RETURN_SYNTAX",
                "Invalid >> syntax.",
                "S12C"
            )
        )
        return

    raw = match.group(1).strip()

    value = parse_value(raw)

    raise FunctionReturn(value)

TOUCH_BINDINGS = {
    "w": None,
    "a": None,
    "s": None,
    "d": None,
}

def cmd_touch_bind(command):

    match = re.fullmatch(
        r'touch\.([wasd])=\{(.*)\}',
        command,
        re.DOTALL
    )

    if not match:

        print(
            script_error(
                "INVALID_TOUCH_BIND",
                "Invalid touch binding syntax.",
                "S13"
            )
        )
        return

    key = match.group(1).strip().lower()
    body = match.group(2).strip()

    if body == "":

        print(
            script_error(
                "EMPTY_TOUCH_BIND",
                "Touch bind body cannot be empty.",
                "S13A"
            )
        )
        return

    TOUCH_BINDINGS[key] = body

    print(
        f"{C.BRIGHT_CYAN}"
        f"[ TOUCH BIND SET ] "
        f"{key.upper()}"
        f"{C.RESET}"
    )

def touch_session():

    print()

    slow_print(
        "[ TOUCH SESSION STARTED ]",
        0.005,
        C.BRIGHT_MAGENTA
    )

    print(
        f"{C.BRIGHT_BLACK}"
        "PRESS W/A/S/D"
        f"{C.RESET}"
    )

    print(
        f"{C.BRIGHT_BLACK}"
        "TYPE 'exit' TO LEAVE"
        f"{C.RESET}"
    )

    while True:

        print()

        try:

            key = input(
                f"{C.BRIGHT_YELLOW}touch >> {C.RESET}"
            ).strip().lower()

        except KeyboardInterrupt:

            print()

            slow_print(
                "[ TOUCH SESSION INTERRUPTED ]",
                0.005,
                C.BRIGHT_RED
            )

            break

        except EOFError:

            print(
                script_error(
                    "TOUCH_INPUT_ERROR",
                    "Input stream closed.",
                    "S14A"
                )
            )
            break

        if key == "exit":

            print()

            slow_print(
                "[ TOUCH SESSION CLOSED ]",
                0.005,
                C.BRIGHT_RED
            )

            break

        if key not in TOUCH_BINDINGS:

            print(
                script_error(
                    "INVALID_TOUCH_KEY",
                    f"'{key}' is not supported.",
                    "S14"
                )
            )
            continue

        body = TOUCH_BINDINGS.get(key)

        if body is None:

            print(
                script_error(
                    "UNBOUND_TOUCH_KEY",
                    f"'{key}' has no binding.",
                    "S15"
                )
            )
            continue

        try:

            execute_script(body)

        except Exception as e:

            print(
                script_error(
                    "TOUCH_RUNTIME_ERROR",
                    str(e),
                    "S15A"
                )
            )

def cmd_run_file(command):
    match = re.fullmatch(r'run_file\s*\(\s*["\']?(.+?)["\']?\s*\)', command)
    if not match:
        print(script_error("SYNTAX_ERROR", "Invalid run_file syntax. Use: run_file(\"filename\")", "P01"))
        return

    raw_filename = match.group(1).strip()
    
    safe_filename = os.path.basename(raw_filename)
    
    if not safe_filename.lower().endswith(".nas"):
        safe_filename += ".nas"

    file_path = os.path.join(os.getcwd(), safe_filename)

    if not os.path.exists(file_path):
        print(script_error("FILE_NOT_FOUND", f"The script file '{safe_filename}' was not found.", "F08"))
        return

    if not os.path.isfile(file_path):
        print(script_error("IO_ERROR", f"'{safe_filename}' is not a valid file.", "F09"))
        return

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            script_content = f.read()
            print(f"{C.BRIGHT_CYAN}[ EXECUTING: {safe_filename} ]{C.RESET}")
            execute_script(script_content)
            
            print(f"{C.BRIGHT_CYAN}[ EXECUTION COMPLETED ]{C.RESET}")

    except UnicodeDecodeError:
        print(script_error("ENCODING_ERROR", "Failed to decode the file. Please use UTF-8 encoding.", "F10"))
    except Exception as e:
        print(script_error("FILE_READ_ERROR", f"An unexpected error occurred: {str(e)}", "F11"))


ACTIVE_INTERVALS = {}
INTERVAL_COUNTER = 0

MIN_INTERVAL_MS = 10
MAX_INTERVAL_MS = 3600000

def validate_timer_value(value):

    try:

        value = int(value)

    except:

        return None

    if value < MIN_INTERVAL_MS:
        return None

    if value > MAX_INTERVAL_MS:
        return None

    return value

def cmd_settime(command):

    match = re.fullmatch(
        r'settime\((\d+)\)\{(.*)\}',
        command,
        re.DOTALL
    )

    if not match:

        print(
            script_error(
                "INVALID_SETTIME",
                "Invalid settime syntax.",
                "T01"
            )
        )
        return

    delay = validate_timer_value(
        match.group(1)
    )

    if delay is None:

        print(
            script_error(
                "INVALID_SETTIME_VALUE",
                (
                    f"Timer must be between "
                    f"{MIN_INTERVAL_MS}ms and "
                    f"{MAX_INTERVAL_MS}ms."
                ),
                "T02"
            )
        )
        return

    body = match.group(2).strip()

    if body == "":

        print(
            script_error(
                "EMPTY_SETTIME_BODY",
                "settime body cannot be empty.",
                "T03"
            )
        )
        return

    def runner():

        try:

            time.sleep(delay / 1000)

            execute_script(body)

        except Exception as e:

            print(
                script_error(
                    "SETTIME_RUNTIME",
                    str(e),
                    "T04"
                )
            )

    thread = threading.Thread(
        target=runner,
        daemon=True
    )

    thread.start()

    print(
        f"{C.BRIGHT_CYAN}"
        f"[ SETTIME REGISTERED ] "
        f"{delay}ms"
        f"{C.RESET}"
    )

def cmd_setinter(command):

    global INTERVAL_COUNTER

    match = re.fullmatch(
        r'setInter\((\d+)\)\{(.*)\}',
        command,
        re.DOTALL
    )

    if not match:

        print(
            script_error(
                "INVALID_SETINTER",
                "Invalid setInter syntax.",
                "T05"
            )
        )
        return

    interval = validate_timer_value(
        match.group(1)
    )

    if interval is None:

        print(
            script_error(
                "INVALID_SETINTER_VALUE",
                (
                    f"Interval must be between "
                    f"{MIN_INTERVAL_MS}ms and "
                    f"{MAX_INTERVAL_MS}ms."
                ),
                "T06"
            )
        )
        return

    body = match.group(2).strip()

    if body == "":

        print(
            script_error(
                "EMPTY_SETINTER_BODY",
                "setInter body cannot be empty.",
                "T07"
            )
        )
        return

    INTERVAL_COUNTER += 1

    interval_id = INTERVAL_COUNTER

    ACTIVE_INTERVALS[interval_id] = True

    def runner():

        while ACTIVE_INTERVALS.get(interval_id):

            try:

                execute_script(body)

            except Exception as e:

                print(
                    script_error(
                        "SETINTER_RUNTIME",
                        str(e),
                        "T08"
                    )
                )

            time.sleep(interval / 1000)

    thread = threading.Thread(
        target=runner,
        daemon=True
    )

    thread.start()

    print(
        f"{C.BRIGHT_GREEN}"
        f"[ SETINTER STARTED ] "
        f"ID={interval_id} "
        f"{interval}ms"
        f"{C.RESET}"
    )

def cmd_clearinter(command):

    match = re.fullmatch(
        r'clearInter\((\d+)\)',
        command
    )

    if not match:

        print(
            script_error(
                "INVALID_CLEARINTER",
                "Invalid clearInter syntax.",
                "T09"
            )
        )
        return

    interval_id = int(
        match.group(1)
    )

    if interval_id not in ACTIVE_INTERVALS:

        print(
            script_error(
                "INTERVAL_NOT_FOUND",
                f"Interval ID '{interval_id}' does not exist.",
                "T10"
            )
        )
        return

    ACTIVE_INTERVALS[interval_id] = False

    print(
        f"{C.BRIGHT_RED}"
        f"[ SETINTER STOPPED ] "
        f"ID={interval_id}"
        f"{C.RESET}"
    )

def cmd_input(command):

    match = re.fullmatch(
        r'input\((.+?)\)',
        command
    )

    if not match:

        print(
            script_error(
                "INVALID_INPUT_SYNTAX",
                "Invalid input() syntax.",
                "I01"
            )
        )

        return

    variable_name = match.group(1).strip()

    if not SAFE_VAR_PATTERN.fullmatch(variable_name):

        print(
            script_error(
                "INVALID_INPUT_VARIABLE",
                f"'{variable_name}' is not valid.",
                "I02"
            )
        )

        return

    try:

        value = input(
            f"{C.BRIGHT_CYAN}"
            f"{variable_name} >> "
            f"{C.RESET}"
        )

    except KeyboardInterrupt:

        print()

        print(
            script_error(
                "INPUT_INTERRUPTED",
                "Input interrupted.",
                "I03"
            )
        )

        return

    except EOFError:

        print(
            script_error(
                "INPUT_STREAM_CLOSED",
                "Input stream closed.",
                "I04"
            )
        )

        return

    SCRIPT_VARIABLES[variable_name] = value

def cmd_clear(command):

    if command != "clear()":

        print(
            script_error(
                "INVALID_CLEAR_SYNTAX",
                "Invalid clear() syntax.",
                "C01"
            )
        )

        return

    try:

        if os.name == "nt":
            os.system("cls")

        else:
            os.system("clear")

    except Exception as e:

        print(
            script_error(
                "CLEAR_FAILED",
                str(e),
                "C02"
            )
        )

def cmd_wait(command):

    match = re.fullmatch(
        r'wait\((.+?)\)',
        command
    )

    if not match:

        print(
            script_error(
                "INVALID_WAIT_SYNTAX",
                "Invalid wait() syntax.",
                "W01"
            )
        )

        return

    raw = match.group(1).strip()

    value = parse_value(raw)

    try:

        value = float(value)

    except:

        print(
            script_error(
                "WAIT_NOT_NUMBER",
                "wait() value must be numeric.",
                "W02"
            )
        )

        return

    if value < 0:

        print(
            script_error(
                "NEGATIVE_WAIT",
                "wait() cannot be negative.",
                "W03"
            )
        )

        return

    if value > 3600:

        print(
            script_error(
                "WAIT_TOO_LARGE",
                "wait() exceeded safety limit.",
                "W04"
            )
        )

        return

    try:

        time.sleep(value)

    except Exception as e:

        print(
            script_error(
                "WAIT_RUNTIME_ERROR",
                str(e),
                "W05"
            )
        )

def cmd_exit(command):

    if command != "exit()":

        print(
            script_error(
                "INVALID_EXIT_SYNTAX",
                "Invalid exit() syntax.",
                "E01"
            )
        )

        return

    slow_print(
        "[ ENGINE TERMINATED ]",
        0.005,
        C.BRIGHT_RED
    )

    sys.exit(0)

SAVE_DIRECTORY = "nanoactscript_saves"

def init_save_directory():

    try:

        if not os.path.exists(SAVE_DIRECTORY):

            os.makedirs(SAVE_DIRECTORY)

    except Exception as e:

        print(
            script_error(
                "SAVE_DIRECTORY_ERROR",
                str(e),
                "F01"
            )
        )

def cmd_save(command):

    match = re.fullmatch(
        r'save\((.+?)\)',
        command
    )

    if not match:

        print(
            script_error(
                "INVALID_SAVE_SYNTAX",
                "Invalid save() syntax.",
                "F02"
            )
        )

        return

    filename = match.group(1).strip()

    if (
        filename.startswith('"')
        and filename.endswith('"')
    ):

        filename = filename[1:-1]

    filename = filename.strip()

    if filename == "":

        print(
            script_error(
                "EMPTY_SAVE_FILENAME",
                "Filename cannot be empty.",
                "F03"
            )
        )

        return

    invalid_chars = r'<>:"/\|?*'

    for char in invalid_chars:

        if char in filename:

            print(
                script_error(
                    "INVALID_SAVE_FILENAME",
                    f"Illegal filename character '{char}'.",
                    "F04"
                )
            )

            return

    if not filename.endswith(".json"):

        filename += ".json"

    init_save_directory()

    path = os.path.join(
        SAVE_DIRECTORY,
        filename
    )

    data = {

        "variables": SCRIPT_VARIABLES,
        "displays": SCRIPT_DISPLAYS,
        "functions": SCRIPT_FUNCTIONS,
        "gages": SCRIPT_GAGES,
    }

    try:

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=4
            )

    except Exception as e:

        print(
            script_error(
                "SAVE_WRITE_ERROR",
                str(e),
                "F05"
            )
        )

        return

    print(
        f"{C.BRIGHT_GREEN}"
        f"[ SAVE COMPLETE ] "
        f"{filename}"
        f"{C.RESET}"
    )

def cmd_load(command):

    match = re.fullmatch(
        r'load\((.+?)\)',
        command
    )

    if not match:

        print(
            script_error(
                "INVALID_LOAD_SYNTAX",
                "Invalid load() syntax.",
                "F06"
            )
        )

        return

    filename = match.group(1).strip()

    if (
        filename.startswith('"')
        and filename.endswith('"')
    ):

        filename = filename[1:-1]

    filename = filename.strip()

    if filename == "":

        print(
            script_error(
                "EMPTY_LOAD_FILENAME",
                "Filename cannot be empty.",
                "F07"
            )
        )

        return

    if not filename.endswith(".json"):

        filename += ".json"

    path = os.path.join(
        SAVE_DIRECTORY,
        filename
    )

    if not os.path.exists(path):

        print(
            script_error(
                "SAVE_FILE_NOT_FOUND",
                f"'{filename}' does not exist.",
                "F08"
            )
        )

        return

    try:

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

    except json.JSONDecodeError as e:

        print(
            script_error(
                "SAVE_FILE_CORRUPTED",
                str(e),
                "F09"
            )
        )

        return

    except Exception as e:

        print(
            script_error(
                "SAVE_FILE_READ_ERROR",
                str(e),
                "F10"
            )
        )

        return

    if not isinstance(data, dict):

        print(
            script_error(
                "INVALID_SAVE_STRUCTURE",
                "Save data must be object.",
                "F11"
            )
        )

        return

    try:

        SCRIPT_VARIABLES.clear()
        SCRIPT_DISPLAYS.clear()
        SCRIPT_FUNCTIONS.clear()
        SCRIPT_GAGES.clear()

        SCRIPT_VARIABLES.update(
            data.get("variables", {})
        )

        SCRIPT_DISPLAYS.update(
            data.get("displays", {})
        )

        SCRIPT_FUNCTIONS.update(
            data.get("functions", {})
        )

        SCRIPT_GAGES.update(
            data.get("gages", {})
        )

    except Exception as e:

        print(
            script_error(
                "SAVE_APPLY_ERROR",
                str(e),
                "F12"
            )
        )

        return

    print(
        f"{C.BRIGHT_GREEN}"
        f"[ LOAD COMPLETE ] "
        f"{filename}"
        f"{C.RESET}"
    )

def cmd_reset(command):

    if command != "reset()":

        print(
            script_error(
                "INVALID_RESET_SYNTAX",
                "Invalid reset() syntax.",
                "R01"
            )
        )

        return

    SCRIPT_VARIABLES.clear()
    SCRIPT_DISPLAYS.clear()
    SCRIPT_FUNCTIONS.clear()
    SCRIPT_GAGES.clear()

    ACTIVE_INTERVALS.clear()

    print(
        f"{C.BRIGHT_RED}"
        f"[ MEMORY RESET COMPLETE ]"
        f"{C.RESET}"
    )

def cmd_del(command):

    match = re.fullmatch(
        r'del\((.+?)\)',
        command
    )

    if not match:

        print(
            script_error(
                "INVALID_DEL_SYNTAX",
                "Invalid del() syntax.",
                "D01"
            )
        )

        return

    name = match.group(1).strip()

    if name not in SCRIPT_VARIABLES:

        print(
            script_error(
                "VARIABLE_NOT_FOUND",
                f"Variable '{name}' does not exist.",
                "D02"
            )
        )

        return

    del SCRIPT_VARIABLES[name]

    print(
        f"{C.BRIGHT_RED}"
        f"[ VARIABLE DELETED ] "
        f"{name}"
        f"{C.RESET}"
    )

def cmd_memory(command):

    if command != "memory()":

        print(
            script_error(
                "INVALID_MEMORY_SYNTAX",
                "Invalid memory() syntax.",
                "M01"
            )
        )

        return

    print()

    print(
        f"{C.BRIGHT_MAGENTA}"
        f"{C.BOLD}"
        "========== VARIABLES =========="
        f"{C.RESET}"
    )

    if len(SCRIPT_VARIABLES) == 0:

        print(
            f"{C.BRIGHT_BLACK}"
            "[ EMPTY ]"
            f"{C.RESET}"
        )

    else:

        for key, value in SCRIPT_VARIABLES.items():

            print(
                f"{C.BRIGHT_CYAN}"
                f"{key}"
                f"{C.RESET}"
                f" = "
                f"{C.BRIGHT_WHITE}"
                f"{repr(value)}"
                f"{C.RESET}"
            )

    print()

    print(
        f"{C.BRIGHT_MAGENTA}"
        f"{C.BOLD}"
        "========== DISPLAYS =========="
        f"{C.RESET}"
    )

    if len(SCRIPT_DISPLAYS) == 0:

        print(
            f"{C.BRIGHT_BLACK}"
            "[ EMPTY ]"
            f"{C.RESET}"
        )

    else:

        for key, value in SCRIPT_DISPLAYS.items():

            print(
                f"{C.BRIGHT_YELLOW}"
                f"{key}"
                f"{C.RESET}"
                f" = "
                f"{C.BRIGHT_WHITE}"
                f"[{value}]"
                f"{C.RESET}"
            )

    print()

    print(
        f"{C.BRIGHT_MAGENTA}"
        f"{C.BOLD}"
        "========== FUNCTIONS =========="
        f"{C.RESET}"
    )

    if len(SCRIPT_FUNCTIONS) == 0:

        print(
            f"{C.BRIGHT_BLACK}"
            "[ EMPTY ]"
            f"{C.RESET}"
        )

    else:

        for key in SCRIPT_FUNCTIONS.keys():

            print(
                f"{C.BRIGHT_GREEN}"
                f"{key}"
                f"{C.RESET}"
            )

    print()

    print(
        f"{C.BRIGHT_MAGENTA}"
        f"{C.BOLD}"
        "========== GAGES =========="
        f"{C.RESET}"
    )

    if len(SCRIPT_GAGES) == 0:

        print(
            f"{C.BRIGHT_BLACK}"
            "[ EMPTY ]"
            f"{C.RESET}"
        )

    else:

        for key in SCRIPT_GAGES.keys():

            print(
                f"{C.BRIGHT_MAGENTA}"
                f"{key}"
                f"{C.RESET}"
            )

HELP_CATEGORIES = {

    "1": {
        "title": "VARIABLES / OUTPUT",
        "content": """
============================================================
VARIABLES / OUTPUT
============================================================

int(name,value)
------------------------------------------------------------
Create a variable.

Example:
int(hp,100)

You can also use expressions.

Example:
int(power,8+9)

------------------------------------------------------------

on(value)
------------------------------------------------------------
Display text, variable values, or expressions.

Examples:
on("HELLO")
on(hp)
on(8+9)

------------------------------------------------------------

input(name)
------------------------------------------------------------
Store keyboard input into a variable.

Example:
input(username)

============================================================
"""
    },

    "2": {
        "title": "DISPLAY SYSTEM",
        "content": """
============================================================
DISPLAY SYSTEM
============================================================

display(name)
------------------------------------------------------------
Create a display object (0 or 1).

Example:
display(power)

------------------------------------------------------------

in dis (name)=0/1
------------------------------------------------------------
Change display visibility.

0 = OFF
1 = ON

Example:
in dis (power)=1

------------------------------------------------------------

multidis(name,value)
------------------------------------------------------------
Create a multi-display (any text/value).

Example:
multidis(message,"Hello")
multidis(counter,0)

------------------------------------------------------------

in multidis(name)=value
------------------------------------------------------------
Change multi-display content.

Example:
in multidis(message)="World"
in multidis(counter,10)

============================================================
"""
    },

    "3": {
        "title": "FUNCTION SYSTEM",
        "content": """
============================================================
FUNCTION SYSTEM
============================================================

func name(){...}
------------------------------------------------------------
Create a reusable function.

Example:
func heal(){
    on("HEAL")
}

------------------------------------------------------------

name.run()
------------------------------------------------------------
Execute a function.

Example:
heal.run()

------------------------------------------------------------

>> value
------------------------------------------------------------
Return value from function.

The return value is stored in FUNC_RETURN_VALUE.

Example:
func getValue(){
    int(x,100)
    >> x
}

getValue.run()
on(FUNC_RETURN_VALUE)

============================================================
"""
    },

    "4": {
        "title": "CONTROL FLOW",
        "content": """
============================================================
CONTROL FLOW
============================================================

if(condition){...}
------------------------------------------------------------
Execute code if condition is true.

Example:
if(hp>0){
    on("ALIVE")
}

------------------------------------------------------------

ifel(condition){...}
------------------------------------------------------------
Execute code if previous if failed.

Example:
ifel(hp<=0){
    on("DEAD")
}

------------------------------------------------------------

else{...}
------------------------------------------------------------
Execute code if previous if/ifel failed.

Example:
else{
    on("UNKNOWN")
}

------------------------------------------------------------

while(condition){...}
------------------------------------------------------------
Loop while condition is true.

Example:
while(x>0){
    on(x)
    int(x,x-1)
}

------------------------------------------------------------

for(var,start,end){...}
------------------------------------------------------------
Loop from start to end.

Increments if start < end.
Decrements if start > end.

Example:
for(i,0,5){
    on(i)
}

Result: 0 1 2 3 4

------------------------------------------------------------

for of(var,array){...}
------------------------------------------------------------
Loop through array elements.

Example:
inli(colors,["red","blue","green"])
for of(color,colors){
    on(color)
}

------------------------------------------------------------

swi(value){
    case(1){on("ONE")}
    case(2){on("TWO")}
    default{on("OTHER")}
}
------------------------------------------------------------
Switch statement for multiple conditions.

Example:
int(status,2)
swi(status){
    case(1){on("Active")}
    case(2){on("Inactive")}
    default{on("Unknown")}
}

------------------------------------------------------------

break
------------------------------------------------------------
Exit from loop immediately.

Example:
for(i,0,10){
    if(i==5){
        break
    }
    on(i)
}

------------------------------------------------------------

continue
------------------------------------------------------------
Skip to next iteration of loop.

Example:
for(i,0,10){
    if(i==5){
        continue
    }
    on(i)
}

============================================================
"""
    },

    "5": {
        "title": "ARRAY SYSTEM",
        "content": """
============================================================
ARRAY SYSTEM
============================================================

inli(name,[...])
------------------------------------------------------------
Create an array.

Example:
inli(nums,[1,2,3])

------------------------------------------------------------

array.on(value)
------------------------------------------------------------
Add element to end of array.

Example:
nums.on(4)

------------------------------------------------------------

array.unon(value)
------------------------------------------------------------
Add element to start of array.

Example:
nums.unon(0)

------------------------------------------------------------

array.off()
------------------------------------------------------------
Remove element from end.

Example:
nums.off()

------------------------------------------------------------

array.unoff()
------------------------------------------------------------
Remove element from start.

Example:
nums.unoff()

------------------------------------------------------------

array.pointer(index,value)
------------------------------------------------------------
Set element at index.

Example:
nums.pointer(0,99)

------------------------------------------------------------

array.len
------------------------------------------------------------
Get array length.

Example:
inli(arr,[1,2,3,4,5])
int(size,arr.len)
on(size)

Result: 5

============================================================
"""
    },

    "6": {
        "title": "GAGE SYSTEM",
        "content": """
============================================================
GAGE SYSTEM
============================================================

gage(name)
------------------------------------------------------------
Create a gage (10-slot bar).

Example:
gage(health)

------------------------------------------------------------

name.gagecn(value)
------------------------------------------------------------
Set gage fill (0-10).

Example:
health.gagecn(7)

------------------------------------------------------------

name.gagepin(index,value)
------------------------------------------------------------
Set specific gage slot (1-10).

0 = empty, 1 = filled

Example:
health.gagepin(5,1)

============================================================
"""
    },

    "7": {
        "title": "MATH SYSTEM",
        "content": """
============================================================
MATH SYSTEM
============================================================

M.random()
------------------------------------------------------------
Generate random float (0.0-1.0).

Example:
int(x,M.random())

------------------------------------------------------------

M.floor(value)
------------------------------------------------------------
Round number down.

Example:
int(x,M.floor(3.9))

Result: 3

------------------------------------------------------------

M.round(value)
------------------------------------------------------------
Round number normally.

Example:
int(x,M.round(3.5))

Result: 4

------------------------------------------------------------

M.randint(min,max)
------------------------------------------------------------
Generate random integer between min and max.

Example:
int(dice,M.randint(1,6))

Result: 1~6

------------------------------------------------------------

M.choice(array)
------------------------------------------------------------
Select random element from array.

Example:
inli(colors,["red","blue","green"])
int(pick,M.choice(colors))

============================================================
"""
    },

    "8": {
        "title": "TIMER SYSTEM",
        "content": """
============================================================
TIMER SYSTEM
============================================================

settime(ms){...}
------------------------------------------------------------
Execute code once after delay.

Example:
settime(1000){
    on("READY")
}

------------------------------------------------------------

setInter(ms){...}
------------------------------------------------------------
Execute code repeatedly.

Example:
setInter(500){
    on("tick")
}

------------------------------------------------------------

clearInter(id)
------------------------------------------------------------
Stop interval execution.

Example:
clearInter(1)

============================================================
"""
    },

    "9": {
        "title": "TOUCH SYSTEM",
        "content": """
============================================================
TOUCH SYSTEM
============================================================

touch.w={...}
touch.a={...}
touch.s={...}
touch.d={...}

------------------------------------------------------------
Bind actions to keyboard controls.

Example:
touch.w={
    on("UP")
}

------------------------------------------------------------

touch()
------------------------------------------------------------
Start touch input session.

============================================================
"""
    },

    "10": {
        "title": "FILE SYSTEM",
        "content": """
============================================================
FILE SYSTEM
============================================================

save(filename)
------------------------------------------------------------
Save all memory to file.

Example:
save("game1")

------------------------------------------------------------

load(filename)
------------------------------------------------------------
Load memory from file.

Example:
load("game1")

------------------------------------------------------------

reset()
------------------------------------------------------------
Clear all memory.

============================================================
"""
    },

    "11": {
        "title": "SYSTEM COMMANDS",
        "content": """
============================================================
SYSTEM COMMANDS
============================================================

clear()
------------------------------------------------------------
Clear terminal screen.

------------------------------------------------------------

del(name)
------------------------------------------------------------
Delete a variable.

Example:
del(hp)

------------------------------------------------------------

memory()
------------------------------------------------------------
Show current memory state.

------------------------------------------------------------

wait(sec)
------------------------------------------------------------
Pause execution.

Example:
wait(1)

------------------------------------------------------------

run_file(name)
------------------------------------------------------------
Execute a .nas script file.
The extension '.nas' is added automatically.

Example:
run_file("myscript")

------------------------------------------------------------

exit()
------------------------------------------------------------
Shutdown system.

============================================================
"""
    },
    
    "12": {
        "title": "SOUND SYSTEM",
        "content": """
============================================================
SOUND SYSTEM
============================================================

temp(bpm)
------------------------------------------------------------
Set BPM (Beats Per Minute) for sound playback.

Range: 10-600

Example:
temp(120)

------------------------------------------------------------

sound(note,duration)
------------------------------------------------------------
Play a note with specified duration.

Note format: C4, D#5, etc. (C0-B8)

Duration can be:
- Milliseconds: "500ms"
- BPM-based: 1=whole note, 0.5=half note,
  0.25=quarter note, 0.125=eighth note

Example:
temp(120)
sound(C4,500ms)
sound(D4,0.25)
sound(E4,0.125)

============================================================
"""
    },
    "13": {
        "title": "CREDIT",
        "content": """

============================================================
MAIN PROGRAMMERS / AI ASSISTANCE
============================================================

GitHub Copilot

OpenAI ChatGPT
- GPT-4o
- GPT-4.1
- GPT-5.3-mini

Google Gemini
- 1.5 Flash
- 3 Flash

Someone who wrote a little bit of「print」
(However, everything I wrote was revised)

- neon_0039 (@Sakuran@misskey.day)

============================================================
INSTRUCTOR & ARCHITECT
============================================================

neon_0039 (@Sakuran@misskey.day)

============================================================
TESTERS
============================================================

My Friends

============================================================
SPECIAL THANKS
============================================================

Thank you for all support and inspiration.
============================================================
"""
    }
}
def script_help():

    while True:

        print()

        print(
            f"{C.BRIGHT_MAGENTA}"
            "╔════════════════════════════════════════════════╗"
        )

        print(
            f"{C.BRIGHT_MAGENTA}"
            "║             HELP MENU                         ║"
            f"{C.RESET}"
        )

        print(
            f"{C.BRIGHT_MAGENTA}"
            "╚════════════════════════════════════════════════╝"
            f"{C.RESET}"
        )

        print()

        for key, value in HELP_CATEGORIES.items():

            print(
                f"{C.BRIGHT_GREEN}"
                f"  [{key:>2}] "
                f"{value['title']}"
                f"{C.RESET}"
            )

        print()

        print(
            f"{C.BRIGHT_RED}"
            "  [ 0] EXIT HELP"
            f"{C.RESET}"
        )

        print()

        choice = input(
            f"{C.BRIGHT_CYAN}HELP >> {C.RESET}"
        ).strip()

        if choice == "0":

            break

        if choice in HELP_CATEGORIES:

            print()

            print(
                f"{C.BRIGHT_WHITE}"
                f"{HELP_CATEGORIES[choice]['content']}"
                f"{C.RESET}"
            )

            input(
                f"{C.BRIGHT_BLACK}"
                "Press Enter to continue..."
                f"{C.RESET}"
            )

            continue

        print(
            script_error(
                "INVALID_HELP_MENU",
                "Unknown help category selected.",
                "H01"
            )
        )

def cmd_help(command):

    if command != "help()":

        print(
            script_error(
                "INVALID_HELP_SYNTAX",
                "Invalid help() syntax.",
                "H02"
            )
        )

        return

    script_help()

def cmd_exec_file(command):

    match = re.fullmatch(
        r'exec\((.+?)\)',
        command
    )

    if not match:

        print(
            script_error(
                "INVALID_EXEC_SYNTAX",
                "Invalid exec() syntax.",
                "F13"
            )
        )
        return

    filename = match.group(1).strip()

    if (
        filename.startswith('"')
        and filename.endswith('"')
    ):

        filename = filename[1:-1]

    filename = filename.strip()

    if not filename.endswith(".nas"):

        filename += ".nas"

    if not os.path.exists(filename):

        print(
            script_error(
                "SCRIPT_FILE_NOT_FOUND",
                f"'{filename}' does not exist.",
                "F14"
            )
        )
        return

    try:

        with open(
            filename,
            "r",
            encoding="utf-8"
        ) as file:

            script_content = file.read()

    except Exception as e:

        print(
            script_error(
                "SCRIPT_FILE_READ_ERROR",
                str(e),
                "F15"
            )
        )
        return

    try:

        execute_script(script_content)

    except Exception as e:

        print(
            script_error(
                "SCRIPT_EXEC_ERROR",
                str(e),
                "F16"
            )
        )

def script_editor():

    print()

    print(
        f"{C.BRIGHT_MAGENTA}"
        "╔════════════════════════════════════════════════╗"
    )

    print(
        f"{C.BRIGHT_MAGENTA}"
        "║          NANOACTSCRIPT EDITOR                ║"
        f"{C.RESET}"
    )

    print(
        f"{C.BRIGHT_MAGENTA}"
        "╚════════════════════════════════════════════════╝"
        f"{C.RESET}"
    )

    print(
        f"{C.BRIGHT_BLACK}"
        "  Type lines of script code"
        f"{C.RESET}"
    )

    print(
        f"{C.BRIGHT_BLACK}"
        "  Type 'END' on new line to finish"
        f"{C.RESET}"
    )

    print()

    lines = []

    try:

        while True:

            line = input(
                f"{C.BRIGHT_YELLOW}{len(lines)+1:3d} > {C.RESET}"
            )

            if line == "END":
                break

            lines.append(line)

    except KeyboardInterrupt:

        print()

        slow_print(
            "[ EDITOR INTERRUPTED ]",
            0.005,
            C.BRIGHT_RED
        )

        return

    script_content = "\n".join(lines)

    print()

    print(
        f"{C.BRIGHT_GREEN}"
        f"[ {len(lines)} LINES ENTERED ]"
        f"{C.RESET}"
    )

    print()

    try:

        filename = input(
            f"{C.BRIGHT_CYAN}Filename (.nas): {C.RESET}"
        )

        if not filename.endswith(".nas"):

            filename += ".nas"

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(script_content)

        print()

        print(
            f"{C.BRIGHT_GREEN}"
            f"[ SAVED ] {filename}"
            f"{C.RESET}"
        )

    except Exception as e:

        print(
            script_error(
                "SAVE_ERROR",
                str(e),
                "F17"
            )
        )

def execute_command(command):

    command = str(command).strip()

    if command == "":
        return

    if command == "break":

        cmd_break(command)
        return

    if command == "continue":

        cmd_continue(command)
        return

    if command.startswith(">>"):

        cmd_func_return(command)
        return

    if command.startswith("for of"):

        cmd_for_of(command)
        return

    if command.startswith("for("):

        cmd_for(command)
        return

    if command.startswith("swi("):

        cmd_swi(command)
        return

    if command.startswith("inli("):

        cmd_inli(command)
        return

    if command.startswith("int("):

        cmd_int(command)
        return

    if command.startswith("on("):

        cmd_on(command)
        return

    if command.startswith("display("):

        cmd_display(command)
        return

    if command.startswith("in dis"):

        cmd_in_dis(command)
        return

    if command.startswith("multidis("):

        cmd_multidis(command)
        return

    if command.startswith("in multidis"):

        cmd_in_multidis(command)
        return

    if command.startswith("func "):

        cmd_func(command)
        return

    if re.fullmatch(
        r'[A-Za-z_][A-Za-z0-9_]*\.run\((.*?)\)',
        command
    ):

        cmd_func_run(command)
        return

    if command.startswith("if("):

        cmd_if(command)
        return

    if command.startswith("ifel("):

        cmd_ifel(command)
        return

    if command.startswith("else{"):

        cmd_else(command)
        return

    if command.startswith("while("):

        cmd_while(command)
        return

    if command.startswith("touch."):

        cmd_touch_bind(command)
        return

    if command.startswith("settime("):

        cmd_settime(command)
        return

    if command.startswith("setInter("):

        cmd_setinter(command)
        return

    if command.startswith("clearInter("):

        cmd_clearinter(command)
        return

    if command == "touch()":

        touch_session()
        return

    if command.startswith("gage("):

        cmd_gage(command)
        return

    if ".gagecn(" in command:

        cmd_gagecn(command)
        return

    if ".gagepin(" in command:

        cmd_gagepin(command)
        return

    if ".on(" in command:
        if cmd_array_on(command):
            return

    if ".unon(" in command:
        if cmd_array_unon(command):
            return

    if ".off()" in command:
        if cmd_array_off(command):
            return

    if ".unoff()" in command:
        if cmd_array_unoff(command):
            return

    if ".pointer(" in command:
        if cmd_array_pointer(command):
            return

    if command.startswith("input("):

        cmd_input(command)
        return

    if command == "clear()":

        cmd_clear(command)
        return

    if command.startswith("wait("):

        cmd_wait(command)
        return

    if command == "exit()":

        cmd_exit(command)
        return

    if command.startswith("save("):

        cmd_save(command)
        return

    if command.startswith("load("):

        cmd_load(command)
        return
        
    if command.startswith("run_file("):

        cmd_run_file(command)
        return
        
    if command.startswith("exec("):

        cmd_exec_file(command)
        return

    if command == "reset()":

        cmd_reset(command)
        return

    if command.startswith("del("):

        cmd_del(command)
        return

    if command == "memory()":

        cmd_memory(command)
        return

    if command == "help()":

        cmd_help(command)
        return

    print(
        script_error(
            "UNKNOWN_COMMAND",
            f"Unknown command '{command}'",
            "S16"
        )
    )

def script_console():

    # Windows / CMD 安定版コンソール（EOF非依存・シンプル操作版）

    while True:

        print()
        print(
            f"{C.BRIGHT_MAGENTA}"
            "╔════════════════════════════════════════════════╗"
        )
        print(
            f"{C.BRIGHT_MAGENTA}"
            "║          NANOACTSCRIPT CONSOLE                ║"
            f"{C.RESET}"
        )
        print(
            f"{C.BRIGHT_MAGENTA}"
            "╚════════════════════════════════════════════════╝"
            f"{C.RESET}"
        )

        print(
            f"{C.BRIGHT_BLACK}"
            "  Type script lines below (press ENTER after each line)"
            f"{C.RESET}"
        )
        print(
            f"{C.BRIGHT_BLACK}"
            "  END   = execute script"
            f"{C.RESET}"
        )
        print(
            f"{C.BRIGHT_BLACK}"
            "  EXIT  = return to home menu"
            f"{C.RESET}"
        )
        print(
            f"{C.BRIGHT_BLACK}"
            "  BACK  = remove last line"
            f"{C.RESET}"
        )
        print(
            f"{C.BRIGHT_BLACK}"
            "  HIST  = show current input history"
            f"{C.RESET}"
        )
        print()

        lines = []

        while True:
            try:
                raw_line = input(f"{C.BRIGHT_YELLOW}>>> {C.RESET}")
                line = raw_line.strip()

                # EXIT → ホームへ戻る
                if line.lower() == "exit":
                    print()
                    slow_print("[ RETURNING TO HOME ]", 0.005, C.BRIGHT_RED)
                    return
                # END → スクリプト実行（Enterは不要、ENDと入力するだけ）
                if line.lower() == "end":
                    script = "\n".join(lines).strip()
                    
                    if script:
                        print()
                        slow_print("[ EXECUTING SCRIPT ]", 0.003, C.BRIGHT_MAGENTA)

                        try:
                            execute_script(script)
                        except KeyboardInterrupt:
                            print()
                            slow_print("[ SCRIPT INTERRUPTED ]", 0.005, C.BRIGHT_RED)
                        except Exception as e:
                            print(
                                script_error(
                                    "SCRIPT_RUNTIME_FAILURE",
                                    str(e),
                                    "P13"
                                )
                            )
                    else:
                        slow_print("[ EMPTY SCRIPT ]", 0.005, C.BRIGHT_BLACK)
                        
                    lines = []
                    print(f"\n{C.BRIGHT_BLACK}  Ready for next script{C.RESET}\n")
                    continue

                # BACK → 最後の1行削除
                if line.lower() == "back":
                    if lines:
                        removed = lines.pop()
                        print(f"{C.BRIGHT_BLACK}[ REMOVED ] {removed}{C.RESET}")
                    continue

                # HIST → 現在入力中の内容表示
                if line.lower() == "hist":
                    print()
                    print(f"{C.BRIGHT_CYAN}[ CURRENT BUFFER ]{C.RESET}")
                    if lines:
                        for i, l in enumerate(lines, 1):
                            print(f"  {i}: {l}")
                    else:
                        print("  [ EMPTY ]")
                    print()
                    continue

                # 空行無視
                if not line:
                    continue

                lines.append(raw_line)

                print(
                    f"{C.BRIGHT_BLACK}[{len(lines)}] Added{C.RESET}"
                )

            except EOFError:
                # Windows: Ctrl+Z + Enter
                print()
                slow_print("[ EOF RECEIVED -> RETURNING TO HOME ]", 0.005, C.BRIGHT_RED)
                return

            except KeyboardInterrupt:
                if lines:
                    print(f"\n{C.BRIGHT_YELLOW}[ INPUT CLEARED ]{C.RESET}")
                    lines = []
                    continue
                else:
                    print()
                    slow_print("[ RETURNING TO HOME ]", 0.005, C.BRIGHT_RED)
                    return

def script_menu():

    while True:

        print()

        print(
            f"{C.BRIGHT_MAGENTA}"
            "╔════════════════════════════════════════════════╗"
        )

        print(
            f"{C.BRIGHT_MAGENTA}"
            "║          NANOACTSCRIPT MENU                  ║"
            f"{C.RESET}"
        )

        print(
            f"{C.BRIGHT_MAGENTA}"
            "╚════════════════════════════════════════════════╝"
            f"{C.RESET}"
        )

        print()

        print(
            f"{C.BRIGHT_GREEN}  [1]{C.WHITE} Run Script (Console)"
        )

        print(
            f"{C.BRIGHT_GREEN}  [2]{C.WHITE} Script Editor"
        )

        print(
            f"{C.BRIGHT_CYAN}  [3]{C.WHITE} Help"
        )

        print(
            f"{C.BRIGHT_YELLOW}  [4]{C.WHITE} Clear Memory"
        )

        print(
            f"{C.BRIGHT_BLUE}  [5]{C.WHITE} Debug Memory"
        )

        print(
            f"{C.BRIGHT_RED}  [6]{C.WHITE} Exit NANOACTSCRIPT"
        )

        print()

        try:

            choice = input(
                f"{C.BRIGHT_MAGENTA}MENU >> {C.RESET}"
            )

        except KeyboardInterrupt:

            print()

            slow_print(
                "[ MENU INTERRUPTED ]",
                0.005,
                C.BRIGHT_RED
            )

            break

        except EOFError:

            print(
                script_error(
                    "MENU_INPUT_ERROR",
                    "Input stream closed.",
                    "P14"
                )
            )

            break

        choice = choice.strip()

        if choice == "1":

            clear_screen()
            script_console()

        elif choice == "2":

            clear_screen()
            script_editor()

        elif choice == "3":

            clear_screen()
            script_help()

        elif choice == "4":

            SCRIPT_VARIABLES.clear()
            SCRIPT_DISPLAYS.clear()
            SCRIPT_FUNCTIONS.clear()
            SCRIPT_GAGES.clear()
            ACTIVE_INTERVALS.clear()

            print()

            slow_print(
                "[ MEMORY CLEARED ]",
                0.005,
                C.BRIGHT_YELLOW
            )

        elif choice == "5":

            clear_screen()

            print()

            print(
                f"{C.BRIGHT_MAGENTA}"
                "╔════════════════════════════════════════════════╗"
            )

            print(
                f"{C.BRIGHT_MAGENTA}"
                "║           MEMORY STATE                       ║"
                f"{C.RESET}"
            )

            print(
                f"{C.BRIGHT_MAGENTA}"
                "╚════════════════════════════════════════════════╝"
                f"{C.RESET}"
            )

            print()

            print(
                f"{C.BRIGHT_GREEN}[ VARIABLES ]{C.RESET}"
            )

            if SCRIPT_VARIABLES:

                for key, value in SCRIPT_VARIABLES.items():

                    print(
                        f"{C.BRIGHT_CYAN}"
                        f"  {key}"
                        f"{C.BRIGHT_BLACK} = "
                        f"{C.BRIGHT_YELLOW}{repr(value)}"
                        f"{C.RESET}"
                    )

            else:

                print(
                    f"{C.BRIGHT_BLACK}  [ EMPTY ]{C.RESET}"
                )

            print()

            print(
                f"{C.BRIGHT_CYAN}[ FUNCTIONS ]{C.RESET}"
            )

            if SCRIPT_FUNCTIONS:

                for key in SCRIPT_FUNCTIONS.keys():

                    print(
                        f"{C.BRIGHT_WHITE}"
                        f"  {key}()"
                        f"{C.RESET}"
                    )

            else:

                print(
                    f"{C.BRIGHT_BLACK}  [ EMPTY ]{C.RESET}"
                )

            print()

            input(
                f"{C.BRIGHT_BLACK}"
                "Press Enter to continue..."
                f"{C.RESET}"
            )

            clear_screen()

        elif choice == "6":

            print()

            slow_print(
                "[ NANOACTSCRIPT SHUTDOWN ]",
                0.005,
                C.BRIGHT_RED
            )

            break

        elif choice == "":

            continue

        else:

            print(
                script_error(
                    "INVALID_MENU",
                    "Unknown menu index.",
                    "P15"
                )
            )

def clear_screen():

    os.system('cls' if os.name == 'nt' else 'clear')

def main():

    clear_screen()

    splash_screen()

    try:

        script_banner()

    except Exception:

        print(
            f"{C.BRIGHT_MAGENTA}"
            "[ NANOACTSCRIPT ]"
            f"{C.RESET}"
        )

    try:

        slow_print(
            "[ NANOACTSCRIPT ONLINE ]",
            0.005,
            C.BRIGHT_MAGENTA
        )

    except Exception:

        print("[ NANOACTSCRIPT ONLINE ]")

    print()

    try:

        script_menu()

    except KeyboardInterrupt:

        print()

        slow_print(
            "[ SYSTEM INTERRUPTED ]",
            0.005,
            C.BRIGHT_RED
        )

    except Exception as e:

        print(
            script_error(
                "SYSTEM_ERROR",
                str(e),
                "P16"
            )
        )

if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        print()

        try:

            slow_print(
                "[ SYSTEM INTERRUPTED ]",
                0.005,
                C.BRIGHT_RED
            )

        except:

            print("[ SYSTEM INTERRUPTED ]")

    except Exception as e:

        print(
            script_error(
                "FATAL_ERROR",
                str(e),
                "P17"
            )
        )
