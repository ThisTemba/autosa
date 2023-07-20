import PySimpleGUI as sg

INST_FOUND_KEY = "-INST FOUND-"
INST_NOT_FOUND_KEY = "-INST NOT FOUND-"
SETTINGS_VALIDITY_KEY = "-SETTINGS VALIDITY-"
INST_FOUND_INFO_KEY = "-INST INFO-"

BUTTON_DETAILS = [
    {"band": "B0", "freqs": "10 kHz - 160 kHz"},
    {"band": "B1", "freqs": "150 kHz - 650 kHz"},
    {"band": "B2", "freqs": "500 kHz - 3 MHz"},
    {"band": "B3", "freqs": "2.5 MHz - 7.5 MHz"},
    {"band": "B4", "freqs": "5 MHz - 30 MHz"},
    {"band": "B5", "freqs": "25 MHz - 325 MHz"},
    {"band": "B6", "freqs": "300 MHz - 1.3 GHz"},
    {"band": "B7", "freqs": "1 GHz - 6 GHz"},
]


def get_single_band_section():
    font = "Any 15"
    button_color = ("white", "dark blue")

    buttons = [
        sg.Button(
            b["band"],
            key=f"-BUTTON {b['band']}-",
            font=font,
            button_color=button_color,
            size=(15, 2),
        )
        for b in BUTTON_DETAILS
    ]

    # arrange section 4 such that there are two rows for 4 buttons
    sectoion4 = [[sg.Text("Run a Band:")], buttons[0:4], buttons[4:8]]
    return sectoion4


def set_band_button_disabled(window, disabled):
    disabled_color = ("white", "grey")
    enabled_color = ("white", "dark blue")
    button_color = disabled_color if disabled else enabled_color
    for b in BUTTON_DETAILS:
        window[f"-BUTTON {b['band']}-"].update(disabled=disabled)
        window[f"-BUTTON {b['band']}-"].update(button_color=button_color)


def get_defuault_layout():
    section1 = [
        [
            sg.Text(
                "Make sure to check the settings before running sweeps!", expand_x=True
            )
        ],
        [sg.Text("", text_color="green", key=INST_FOUND_INFO_KEY, expand_x=True)],
        [sg.Text("", text_color="green", key=SETTINGS_VALIDITY_KEY, expand_x=True)],
    ]

    section2 = [
        [
            sg.Text("Band Range:"),
            sg.OptionMenu(
                key="-BAND RANGE-",
                values=["B0 - B4 (monopole)", "B5 - B7 (bilogical)"],
                background_color="white",
            ),
        ],
        [sg.Text("Last Run Index:"), sg.Input(key="-LAST INDEX-", default_text="0")],
        [sg.Button("Run Sweeps", disabled=True, key="-RUN-")],
        [
            sg.ProgressBar(
                1, orientation="h", size=(60, 20), key="-PROGRESS-", expand_x=True
            )
        ],
    ]

    sectoion3 = get_single_band_section()

    layout = [
        [
            sg.Text("Setup", font=("", 15)),
            sg.Text("", expand_x=True),  # This will push the button to the right
            sg.B("Settings", button_color=("black", "light gray"), size=(10, 2)),
        ],
        *section1,
        [sg.HorizontalSeparator()],
        [sg.Text("Multiple Bands", font=("", 15))],
        *section2,
        [sg.HorizontalSeparator()],
        [sg.Text("Individual Bands", font=("", 15))],
        *sectoion3,
    ]

    return layout


def get_inst_not_found_layout():
    steps = [
        "1. Make sure the instrument is plugged in to power and turned on",
        "2. Make sure the instrument is connected to this computer via USB-B (back of instrument) to USB-A (computer) cable",
        '3. Make sure the signal analyzer program is running on the device (may be called "LaunchXSA" on the desktop)',
        "4. Ask for help",
    ]

    layout = [
        [
            sg.Text(
                "Instrument Not Detected",
                size=(40, 1),
                text_color="red",
                font=("Helvetica", 16, "bold"),
            )
        ],
        [sg.Text("Steps to fix:", size=(40, 1))],
        *[[sg.Text(step, size=(80, 1))] for step in steps],
    ]

    return layout


def get_main_layout(inst_found):
    # only one of these will be visible at a time
    default_col = sg.Column(
        get_defuault_layout(),
        visible=inst_found,
        key=INST_FOUND_KEY,
    )

    inst_not_fount_col = sg.Column(
        get_inst_not_found_layout(),
        visible=not inst_found,
        key=INST_NOT_FOUND_KEY,
    )

    return [[sg.pin(default_col)], [sg.pin(inst_not_fount_col)]]


def update_main_window(window, inst_found, inst_info, settings_error):
    settings_validity_text = (
        "✅ Settings Valid"
        if not settings_error
        else f'❎ Settings Invalid. Please open settings and click "Save" to see error.'
    )
    settings_validity_color = "red" if settings_error else "green"
    inst_found_info_text = "✅ Instrument Detected - " + inst_info

    window[INST_FOUND_KEY].update(visible=inst_found)
    window[INST_NOT_FOUND_KEY].update(visible=not inst_found)
    window[SETTINGS_VALIDITY_KEY].update(settings_validity_text)
    window[SETTINGS_VALIDITY_KEY].update(text_color=settings_validity_color)
    window[INST_FOUND_INFO_KEY].update(inst_found_info_text)
    return


def get_main_mindow(inst_found, inst_info, settings_error):
    layout = get_main_layout(inst_found)

    # Create the window
    window = sg.Window(
        "Autosa by Tenco",
        layout,
        margins=(20, 20),
        default_element_size=(20, 1),
        auto_size_text=False,
        finalize=True,
    )
    update_main_window(window, inst_found, inst_info, settings_error)

    return window
