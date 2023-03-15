import PySimpleGUI as sg

LABEL_SIZE = (10, 1)


def header_cell(txt):
    t = sg.Text(
        "\n" + txt,
        relief=sg.RELIEF_RAISED,
        expand_x=True,
        size=(15, 3),
        justification="center",
    )
    return t


def content_cell(txt):
    t = sg.Text(txt, relief=sg.RELIEF_SUNKEN, expand_x=True, size=(15, 3))
    return t


def create_timetable_layout(timetable):
    layout = [[header_cell(txt) for txt in ["Time"] + timetable.days]]
    for time in timetable.time_frame:
        layout.append([header_cell(time)] + [ctx for ctx in timetable[time].values()])
    return layout


def create_main_layout(save_files, timetable):
    # save_files = get_profile(with_prefix=False, with_extension=False)
    current_file = save_files[0] if save_files else None
    # top_menu = [["File", ["New Scheme"]], ["Help", ["About"]]]
    layout = [
        # [sg.Menu(top_menu)],
        [
            sg.Combo(
                save_files,
                current_file,
                size=25,
                readonly=True,
                enable_events=True,
                key="-PROFILE-",
            ),
            sg.Push(),
            sg.Button("Add", key="-ADD_BUTTON-", size=10),
            sg.Button("Save", key="-SAVE_BUTTON-", size=10),
            sg.Button("D", key="-DELETE_BUTTON-", button_color="#fe0232", size=3),
            sg.Button("SS", key="-SS_BUTTON-", button_color="#02fe32", size=3),
        ],
    ]
    timetable_layout = create_timetable_layout(timetable)
    layout.append(timetable_layout)
    return layout


def create_input_laytout(
    timetable, d_title="", d_desc="", d_day=0, d_time=0, d_duration=0, edit=False
):
    layout = [
        _text_input("Title", size=LABEL_SIZE, default=d_title),
        _text_input("Description", size=LABEL_SIZE, default=d_desc),
        _element_selector("Day", timetable.days, size=LABEL_SIZE, default=d_day),
        _element_selector(
            "Time", timetable.time_frame, size=LABEL_SIZE, default=d_time
        ),
        _element_selector(
            "Duration",
            tuple(range(1, 10)),
            size=LABEL_SIZE,
            default=d_duration,
            visible=not edit,
        ),
        [
            sg.Push(),
            sg.Button("Cancel", key="-CANCEL-"),
            sg.Button("Confirm", key="-CONFIRM-"),
            sg.Button("Delete", key="-DELETE-", visible=edit),
        ],
    ]
    return layout




def _text_input(
    label, size=(None, None), key=None, default="", input_size=(None, None)
):
    if key is None:
        key = _lkey(label)
    l = sg.Text(label, size=size)
    entry = sg.Input(key=key, default_text=default, size=input_size)
    return l, entry


def _element_selector(
    label, items, size=(None, None), key=None, default=0, visible=True
):
    if key is None:
        key = _lkey(label)
    if isinstance(default, str):
        default = items.index(default)
    l = sg.Text(label, size=size, visible=visible)
    entry = sg.Combo(
        items,
        default_value=items[default],
        key=key,
        size=size[0] + 5,
        readonly=True,
        visible=visible,
    )
    return l, entry

def _lkey(label, *args):
    label = label.strip().strip("-")
    if args:
        label = "-".join([label] + list(args))
    return f'-{label.upper().replace(" ", "_")}-'
