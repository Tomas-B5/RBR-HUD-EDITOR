import PySimpleGUI as sg
from dash import *
from rsf_functions import CFG_RBR


def reload_dash(dir, dash):
    cfg = CFG_RBR(dir)
    dash.read_file(cfg.dash_file)


def update_cfg(dash):
    dash.Output_Dash(dash.filename)


def reload_controls(window, values):
    # Update sliders:
    window["-SLIDER-BACKGROUND-"].update(
        window["-SLIDER-BACKGROUND-"].metadata.Alpha)
    window["-SLIDER-LIT-"].update(window["-SLIDER-LIT-"].metadata.Alpha)
    window["-SLIDER-UNLIT-"].update(window["-SLIDER-UNLIT-"].metadata.Alpha)


def reload_coords(window, values):
    if values["-Value List-"] and values["-Value List-"][0]:
        if type(values["-Value List-"][0]) is not Simple:
            window["-X-"].update(disabled=True)
            window["-Y-"].update(disabled=True)
            window["Set"].update(disabled=True)
            return
        window["-X-"].update(values["-Value List-"][0].Position.x)
        window["-Y-"].update(values["-Value List-"][0].Position.y)
        window["-X-"].update(disabled=False)
        window["-Y-"].update(disabled=False)
        window["Set"].update(disabled=False)


def Init_GUI(dash):
    step_size = 1
    sg.theme('Default1')   # Add a touch of color
    # All the stuff inside your window.
    layout = Build_layout(dash)
    # Create the Window
    window = sg.Window('RBR HUD editor. For RallySimFans launcher', layout,
                       finalize=True, return_keyboard_events=True, use_default_focus=True)
    window['-SLIDER-BACKGROUND-'].bind('<ButtonRelease-1>', ' Release')
    window['-SLIDER-LIT-'].bind('<ButtonRelease-1>', ' Release')
    window['-SLIDER-UNLIT-'].bind('<ButtonRelease-1>', ' Release')

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        if event == sg.WIN_CLOSED or event == 'Exit':
            break

        if event == '0.1':
            step_size = 0.1
        if event == '0.5':
            step_size = 0.5
        if event == '1':
            step_size = 1
        if event == '10':
            step_size = 10
        if event == '100':
            step_size = 100

        if event == "UP" or event == "Up:38":
            if values["-Value List-"] and values["-Value List-"][0]:
                values["-Value List-"][0].Up(step_size)
                update_cfg(dash)
                reload_coords(window, values)
            continue

        if event == "DOWN" or event == "Down:40":
            if values["-Value List-"] and values["-Value List-"][0]:
                values["-Value List-"][0].Down(step_size)
                update_cfg(dash)
                reload_coords(window, values)
            continue

        if event == "LEFT" or event == "Left:37":
            if values["-Value List-"] and values["-Value List-"][0]:
                values["-Value List-"][0].Left(step_size)
                update_cfg(dash)
                reload_coords(window, values)
            continue

        if event == "RIGHT" or event == "Right:39":
            if values["-Value List-"] and values["-Value List-"][0]:
                values["-Value List-"][0].Right(step_size)
                update_cfg(dash)
                reload_coords(window, values)
            continue

        if event == "X":
            dash.ScaleX(float(values["-ScaleF-"]))
            update_cfg(dash)
            reload_coords(window, values)
            continue

        if event == "Y":
            dash.ScaleY(float(values["-ScaleF-"]))
            update_cfg(dash)
            reload_coords(window, values)
            continue

        if event == "XY":
            dash.ScaleXY(float(values["-ScaleF-"]))
            update_cfg(dash)
            reload_coords(window, values)
            continue

        if event == "Set":
            if values["-Value List-"] and values["-Value List-"][0]:
                if type(values["-Value List-"][0]) is not Simple:
                    continue
                values["-Value List-"][0].Position.x = float(values["-X-"])
                values["-Value List-"][0].Position.y = float(values["-Y-"])
                update_cfg(dash)
                reload_coords(window, values)
            continue

        if event == '-Value List-':
            reload_coords(window, values)

        if event == 'Open':
            folder = sg.popup_get_folder('file to open', no_window=True)
            if not folder:
                continue
            reload_dash(folder + "//", dash)
            reload_controls(window, values)
            window["-Value List-"].Update(Build_list(dash))
            print(folder)

        if event == 'Save':
            filename = sg.popup_get_file(
                'file to save', no_window=True, save_as=True)
            if not filename:
                continue
            dash.Output_Dash(filename)

        if event == '-FOLDER-':
            folder = values['-FOLDER-']
            reload_dash(folder + "//", dash)
            reload_controls(window, values)
            window["-Value List-"].Update(Build_list(dash))
            print(folder)

        if event.startswith('-SLIDER-') and event.endswith(' Release'):
            evt = event.removesuffix(" Release")
            print(values[evt])
            print(window[evt].metadata)
            window[evt].metadata.Alpha = values[evt]
            update_cfg(dash)

        print(event)
    # --------------------------------- Close & Exit ---------------------------------


def Build_list(dash):
    values = []
    for obj in dash.obj_array_grouped:
        if type(obj) is Simple:
            values.append(obj)
        elif obj.name == ">Alpha Values":
            continue
        else:
            values.append(obj)
            for child in obj.children:
                values.append(obj.children[child])
    return values


def Build_layout(dash):
    menu_def = [['File', ['Open', 'Save', 'Exit', ]], ['Help', 'About...'], ]
    controls_col = [[sg.Text('Background :'),
                     sg.Slider((0.0, 1.0), key='-SLIDER-BACKGROUND-', orientation='h', resolution=0.01,
                               enable_events=False,
                               metadata=dash.Group_alphas.children["Background"], default_value=dash.Group_alphas.children["Background"].Alpha)],
                    [sg.Text('Lit :'),
                     sg.Slider((0.0, 1.0), key='-SLIDER-LIT-', orientation='h', resolution=0.01,
                               enable_events=False,
                               metadata=dash.Group_alphas.children["Lit"], default_value=dash.Group_alphas.children["Lit"].Alpha)],
                    [sg.Text('Unlit :'),
                     sg.Slider((0.0, 1.0), key='-SLIDER-UNLIT-', orientation='h', resolution=0.01,
                               enable_events=False,
                               metadata=dash.Group_alphas.children["Unlit"], default_value=dash.Group_alphas.children["Unlit"].Alpha)],


                    [sg.Text('Position:'), sg.In(key='-X-', size=(8, 1)),
                     sg.In(key='-Y-', size=(8, 1)), sg.Button('Set')],
                    [sg.Text('Multiply Coordinates:'), sg.In(
                        key='-ScaleF-', size=(8, 1)), sg.Button('XY'), sg.Button('X'), sg.Button('Y')],
                    [sg.Text('Step:'), sg.Button('0.1'), sg.Button(
                        '0.5'), sg.Button('1'), sg.Button('10'), sg.Button('100')],
                    [sg.Button('UP')],
                    [sg.Button('LEFT'), sg.Button('RIGHT')],
                    [sg.Button('DOWN')],
                    ]
    left_col = [
        [sg.Listbox(values=[], enable_events=True, size=(40, 20), key='-Value List-', select_mode='LISTBOX_SELECT_MODE_EXTENDED')]]
    layout = [[sg.Menu(menu_def)],
              [sg.Column(left_col, element_justification='left'), sg.VSeperator(
              ), sg.Column(controls_col, element_justification='center')]]
    return layout
