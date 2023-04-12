import PySimpleGUI as sg
from dash import *
from rsf_functions import CFG_RBR

class Group_mode(Enum):
    Nothing = 0
    Save = 1
    Delete = 2


def reload_dash(dir: str, dash: Dash_Object):
    cfg = CFG_RBR(dir)
    return dash.read_file(cfg.dash_file)

def update_cfg(dash: Dash_Object):
    dash.Output_Dash(dash.filename)


def get_selection(values):
    selection = []
    for obj in values["-Value List-"]:
        selection.append(obj)
    return selection

def reload_controls(window: sg.Window):
    # Update sliders:
    window["-SLIDER-BACKGROUND-"].update(
        window["-SLIDER-BACKGROUND-"].metadata.Alpha)
    window["-SLIDER-LIT-"].update(window["-SLIDER-LIT-"].metadata.Alpha)
    window["-SLIDER-UNLIT-"].update(window["-SLIDER-UNLIT-"].metadata.Alpha)


def disable_offset_controls(window):
    window["-Xoff-"].update(0,disabled=True)
    window["-Yoff-"].update(0,disabled=True)


def enable_offset_controls(window):
    window["-Xoff-"].update(disabled=False)
    window["-Yoff-"].update(disabled=False)

class GUI:
    step_size = 1
    group_mode = Group_mode.Nothing
    window = None
    dash = None

    def __init__(self, dash):
        self.dash = dash
        sg.theme('Default1')   # Add a touch of color
        # All the stuff inside your window.
        layout = self.Build_layout()
        # Create the Window
        window = sg.Window('RBR HUD editor. For RallySimFans launcher', layout,
                           finalize=True, return_keyboard_events=True, use_default_focus=True)
        self.window = window
        window['-SLIDER-BACKGROUND-'].bind('<ButtonRelease-1>', ' Release')
        window['-SLIDER-LIT-'].bind('<ButtonRelease-1>', ' Release')
        window['-SLIDER-UNLIT-'].bind('<ButtonRelease-1>', ' Release')

    def handle_move_event(self, event, values):
        # eh probably could be done better but I guess just put this one last in the event handle loop
        selection = get_selection(values)
        if len(selection) < 1:
            return False
        i = 0
        for sel in selection:
            if event == "UP" or event == "Up:38":
                sel.Up(self.step_size)
            elif event == "DOWN" or event == "Down:40":
                sel.Down(self.step_size)
            elif event == "LEFT" or event == "Left:37":
                sel.Left(self.step_size)
            elif event == "RIGHT" or event == "Right:39":
                sel.Right(self.step_size)
            elif event == "X":
                sel.ScaleX(float(values["-ScaleF-"]))
            elif event == "Y":
                sel.ScaleY(float(values["-ScaleF-"]))
            elif event == "XY":
                sel.ScaleX(float(values["-ScaleF-"]))
                sel.ScaleY(float(values["-ScaleF-"]))
            elif event == "Set":
                sel.Position.x = float(values["-X-"])
                sel.Position.y = float(values["-Y-"])
                sel.Position.x += float(values["-Xoff-"]) * i
                sel.Position.y += float(values["-Yoff-"]) * i
                i += 1
            else:
                # Was not handled
                return False

        update_cfg(self.dash)
        self.reload_coords(values)
        return True

    def Build_list(self):
        values = []
        for obj in self.dash.obj_array_grouped:
            if type(obj) is Simple:
                values.append(obj)
            elif obj.name == ">Alpha Values":
                continue
            else:
                # values.append(obj)
                for child in obj.children:
                    values.append(obj.children[child])
        return values

    def Build_layout(self):
        menu_def = [['File', ['Open (Game dir)', 'Save As', 'Exit', ]]]
        controls_col = [
            [sg.Text('Background :'),
             sg.Slider((0.0, 1.0), key='-SLIDER-BACKGROUND-', orientation='h', resolution=0.01,
                       enable_events=False, disable_number_display=True,
                       metadata=self.dash.Group_alphas.children["Background"], default_value=self.dash.Group_alphas.children["Background"].Alpha)],
            [sg.Text('Lit :'),
             sg.Slider((0.0, 1.0), key='-SLIDER-LIT-', orientation='h', resolution=0.01,
                       enable_events=False, disable_number_display=True,
                       metadata=self.dash.Group_alphas.children["Lit"], default_value=self.dash.Group_alphas.children["Lit"].Alpha)],
            [sg.Text('Unlit :'),
             sg.Slider((0.0, 1.0), key='-SLIDER-UNLIT-', orientation='h', resolution=0.01,
                       enable_events=False, disable_number_display=True,
                       metadata=self.dash.Group_alphas.children["Unlit"], default_value=self.dash.Group_alphas.children["Unlit"].Alpha)],

            [sg.HSeparator()],
            [sg.Text('Position: X:'),
             sg.In(key='-X-', size=(8, 1)),
             sg.Text('Y:'),
             sg.In(key='-Y-', size=(8, 1)),
             sg.Button('Set')],
            [sg.Text('Offset:    X:', tooltip="How to space out objects when using \"Set\""),
             sg.In(key='-Xoff-', size=(8, 1), disabled=True),
             sg.Text('Y:'),
             sg.In(key='-Yoff-', size=(8, 1), disabled=True),
             sg.Text('      '),],
            [sg.HSeparator()],
            [sg.Text('Multiply Coordinates by:', tooltip="Useful for adapting for different resolutions"),
             sg.In(key='-ScaleF-', size=(8, 1)),
             sg.Button('XY'),
             sg.Button('X'),
             sg.Button('Y')],
            [sg.HSeparator()],
            [sg.Text('Step:', tooltip="Coordinate adjustment per input"),
             sg.Button('0.1'),
             sg.Button('0.5'),
             sg.Button('1'),
             sg.Button('10'),
             sg.Button('100')],
            [sg.Button('UP')],
            [sg.Button('LEFT'), sg.Button('RIGHT')],
            [sg.Button('DOWN')],
            [sg.HSeparator()],
            [sg.Text('Selected:', tooltip="These changes become permanent after program exit"),
             sg.Button('Show', key='-ShowSel-'),
             sg.Button('Hide', key='-HideSel-'),
             sg.Text('All:', tooltip="These changes become permanent after program exit"),
             sg.Button('Show', key='-ShowAll-'),
             sg.Button('Hide', key='-HideAll-'),]
        ]

        left_col = [
            [sg.Listbox(values=[], enable_events=True, size=(40, 20), key='-Value List-', select_mode='extended')]]

        group_col = [
            [sg.Text(key='-groupmode-')],
            [sg.Text('Selection:')],
            [sg.Button('ALL')],
            [sg.Button('CLEAR')],
            [sg.Text('Groups:')],
            [sg.Button('Save', key='-Group-Save-'),
             sg.Button('Delete', key='-Group-Delete-')],
            [sg.Button('Group 1')],
            [sg.Button('Group 2')],
            [sg.Button('Group 3')],
            [sg.Button('Group 4')],
            [sg.Button('Group 5')],
            [sg.Button('Group 6')],
            [sg.Button('Group 7')],
        ]

        layout = [
            [sg.Menu(menu_def)],
            [sg.Column(group_col, element_justification='center', vertical_alignment='t'), sg.VSeperator(
            ), sg.Column(left_col, element_justification='left'), sg.VSeperator(
            ), sg.Column(controls_col, element_justification='center', vertical_alignment='t')]]
        return layout
    
    def Save_Dash_Group(self, num, values):
        self.Delete_Dash_Group(num)
        selection = get_selection(values)
        for sel in selection:
            sel.group = num
                
    def Delete_Dash_Group(self, num):
        self.dash.DeleteGroup(num)
            
    def Load_Dash_Group(self, num):
        self.window["-Value List-"].set_value(
                    self.dash.GetGroup(num))
    
    def reload_coords(self, values):
        if values["-Value List-"] and values["-Value List-"][0]:
            if len(values["-Value List-"]) > 1:
                enable_offset_controls(self.window)
                return
            self.window["-X-"].update(values["-Value List-"][0].Position.x)
            self.window["-Y-"].update(values["-Value List-"][0].Position.y)
            disable_offset_controls(self.window)
            
    def Set_Group_mode(self, value):
        if value is Group_mode.Nothing:
            self.group_mode = Group_mode.Nothing
            #Hide control
            return 0
        elif value is Group_mode.Save:
            if self.group_mode == value:
               self.group_mode = Group_mode.Nothing 
            self.group_mode = value
            # Show save
            return 0
        elif value is Group_mode.Delete:
            if self.group_mode == value:
               self.group_mode = Group_mode.Nothing 
            self.group_mode = value
            # show delete
            return 0
        #update visuals
        self.window['-groupmode-'].update(str(self.group_mode)) 
        
    def UpdateGroupDisplay(self):
        if self.group_mode == Group_mode.Nothing:
            self.window["-Group-Save-"].update(button_color=('Black', None))
            self.window["-Group-Delete-"].update(button_color=('Black', None))
        elif self.group_mode is Group_mode.Save:
            self.window["-Group-Save-"].update(button_color=('Red', None))
            self.window["-Group-Delete-"].update(button_color=('Black', None))  
        elif self.group_mode is Group_mode.Delete:
            self.window["-Group-Save-"].update(button_color=('Black', None))
            self.window["-Group-Delete-"].update(button_color=('Red', None))
            
            
    def Run(self):
        # Event Loop to process "events" and get the "values" of the inputs
        while True:
            event, values = self.window.read()
            if event in (sg.WIN_CLOSED, 'Exit'):
                break
            if event == sg.WIN_CLOSED or event == 'Exit':
                break

            if event == '0.1':
                self.step_size = 0.1
            elif event == '0.5':
                self.step_size = 0.5
            elif event == '1':
                self.step_size = 1
            elif event == '10':
                self.step_size = 10
            elif event == '100':
                self.step_size = 100

            elif event == '-Value List-':
                for obj in values["-Value List-"]:
                    print(obj)
                self.reload_coords(values)

            elif event == 'Open (Game dir)':
                folder = sg.popup_get_folder('file to open', no_window=True)
                if not folder:
                    continue
                if reload_dash(folder + "//", self.dash) == False:
                    sg.popup_ok(["Error: something went wrong with reading config file"], title="Error opening file",)
                    continue
                reload_controls(self.window)
                self.window["-Value List-"].Update(self.Build_list())
                print(folder)

            elif event == 'Save As':
                filename = sg.popup_get_file(
                    'file to save', no_window=True, save_as=True)
                if not filename:
                    continue
                self.dash.Output_Dash(filename)

            elif event.startswith('-SLIDER-') and event.endswith(' Release'):
                evt = event.removesuffix(" Release")
                print(values[evt])
                print(self.window[evt].metadata)
                self.window[evt].metadata.Alpha = values[evt]
                update_cfg(self.dash)

            elif event == 'ALL':
                # STUPID BUT ITS LATE
                self.window["-Value List-"].set_value(
                    self.Build_list())

            elif event == 'CLEAR':
                self.window["-Value List-"].set_value([])

            elif event == '-Group-Save-':
                if self.group_mode == Group_mode.Save:
                    self.group_mode = Group_mode.Nothing
                else:
                    self.group_mode = Group_mode.Save
                self.UpdateGroupDisplay()

            elif event == '-Group-Delete-':
                if self.group_mode == Group_mode.Delete:
                    self.group_mode = Group_mode.Nothing
                else:
                    self.group_mode = Group_mode.Delete
                self.UpdateGroupDisplay()
                
            elif event.startswith('Group '):
                num = event.split()
                print(event)
                print(self.group_mode)
                if self.group_mode == Group_mode.Save:
                    self.Save_Dash_Group(int(num[1]), values)
                elif self.group_mode == Group_mode.Delete:
                    self.Delete_Dash_Group(int(num[1]))
                elif self.group_mode == Group_mode.Nothing:
                    self.Load_Dash_Group(int(num[1]))
                self.group_mode = Group_mode.Nothing
                self.UpdateGroupDisplay()
                
            elif event == '-ShowSel-':
                selection = get_selection(values)
                for sel in selection:
                    sel.hide = False   
                update_cfg(self.dash)       
            elif event == '-HideSel-':
                selection = get_selection(values)
                for sel in selection:
                    sel.hide = True
                update_cfg(self.dash)
            elif event == '-ShowAll-':
                self.dash.ShowAll()
                update_cfg(self.dash)
            elif event == '-HideAll-':
                self.dash.HideAll()
                update_cfg(self.dash)
            else:
                self.handle_move_event(event, values)
            print(event)
