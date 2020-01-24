# SAV Digital Environments
# Julian Kizanis
# generated in part by wxGlade 0.9.4 on Mon Nov 18 07:49:50 2019
#

from datetime import date
from getpass import getuser
from ntpath import basename

import wx
from openpyxl import load_workbook
from openpyxl.styles import Alignment
from openpyxl.formatting.rule import ColorScaleRule

import pandas as pd

# Declare GUI Constants
MENU_FILE_EXIT = wx.ID_ANY
DRAG_SOURCE = wx.ID_ANY

# Global Variables
user = getuser()
pb = False

# Global Constants
ROUGH_PHASE = 1
FINISH_PHASE = 2
CONTINUE = 2
OVERRIDE = -2
CANCEL = -1


def add_row(error_code, username, group, local_date, jobcode_1, jobcode_2, payroll_item, service_item, error_sheet):
    last_row = 1
    for cell in error_sheet['A']:
        if cell.value:
            last_row = cell.row
    error_sheet[f'A{last_row + 1}'].value = error_code
    error_sheet[f'B{last_row + 1}'].value = username
    error_sheet[f'C{last_row + 1}'].value = local_date
    error_sheet[f'D{last_row + 1}'].value = jobcode_1
    error_sheet[f'E{last_row + 1}'].value = jobcode_2
    error_sheet[f'F{last_row + 1}'].value = service_item
    error_sheet[f'G{last_row + 1}'].value = payroll_item
    return error_sheet


def find_errors(timesheet_directory):
    error_book = open_spreadsheet('timesheet_error_report.xlsx')
    error_sheet = error_book.active

    timesheet = pd.read_csv(timesheet_directory)

    # "username", "group", "local_date", "jobcode_1", "jobcode_2", "payroll item", "service item"
    current_person = ""
    current_phase = ""
    last_job = ""
    current_pay_type = ""
    only_travel = [False, False]
    holidays = ['01/01/2020', '05/25/2020', '07/03/2020', '09/07/2020', '11/26/2020', '11/27/2020', '12/25/2020',
                '2020-01-01', '2020-05-25', '2020-07-03', '2020-09-07', '2020-11-26', '2020-11-27', '2020-12-25']
    for index, (username, group, local_date, jobcode_1, jobcode_2, payroll_item, service_item) in \
            enumerate(zip(timesheet.loc[:, 'username'], timesheet.loc[:, 'group'], timesheet.loc[:, 'local_date'],
                          timesheet.loc[:, 'jobcode_1'], timesheet.loc[:, 'jobcode_2'],
                          timesheet.loc[:, 'payroll item'],
                          timesheet.loc[:, 'service item'])):
        try:
            # Lunch Check
            if 'LUNCH' == jobcode_1:
                continue

            # New person check
            if username != current_person:
                current_person = username
                i = 1
                while 'LUNCH' in timesheet.loc[index + i, 'jobcode_1']:
                    i += 1
                if 'Salary' in timesheet.loc[index + i, 'payroll item']:
                    current_pay_type = 'Salary'
                elif 'Hourly' in timesheet.loc[index + i, 'payroll item']:
                    current_pay_type = 'Hourly'

            # New customer check
            if last_job != (str(jobcode_1) + ':' + str(jobcode_2)):
                # if only_travel == [False, True]:
                #     print(f"Only Travel Error: {last_job}, {(str(jobcode_1) + ':' + str(jobcode_2))}")
                #     error_sheet = add_row("Only Travel Error", timesheet.loc[index - 1, 'username'],
                #                           timesheet.loc[index - 1, 'group'], timesheet.loc[index - 1, 'local_date'],
                #                           timesheet.loc[index - 1, 'jobcode_1'], timesheet.loc[index - 1, 'jobcode_2'],
                #                           timesheet.loc[index - 1, 'payroll item'],
                #                           timesheet.loc[index - 1, 'service item'], error_sheet)

                only_travel = [False, False]
            # Time review combos check
            if ("Production" in jobcode_2 or "Service" in jobcode_2) and "Overhead" in jobcode_2:
                if jobcode_1 == "SAV Digital Environments, Inc WY":
                    print("Wyoming?")
                    print(f"Wyoming?: {username}, {local_date}, {jobcode_1}:{jobcode_2}, "
                          f"{payroll_item}, {service_item}")
                    error_sheet = add_row("Wyoming?", username, group, local_date, jobcode_1, jobcode_2,
                                          payroll_item, service_item, error_sheet)

                elif not jobcode_1 == "SAV Digital Environments, Inc MT":
                    print("Bad customer")
                    print(f"Bad customer: {username}, {local_date}, {jobcode_1}:{jobcode_2}, "
                          f"{payroll_item}, {service_item}")
                    error_sheet = add_row("Bad customer", username, group, local_date, jobcode_1, jobcode_2,
                                          payroll_item, service_item, error_sheet)

                elif not (service_item == "LABOR:Office/Meetings" or service_item == "LABOR:Training"):
                    print("customer != service item")
                    print(f"customer != service item: {username}, {local_date}, {jobcode_1}:{jobcode_2}, "
                          f"{payroll_item}, {service_item}")
                    error_sheet = add_row("customer != service item", username, group, local_date, jobcode_1, jobcode_2,
                                          payroll_item, service_item, error_sheet)

                elif service_item == "LABOR:Office/Meetings":
                    if not (payroll_item == "Salary Other COGS" or payroll_item == "Hourly Other COGS" or
                            payroll_item == "Security Salary Other COGS" or payroll_item == "Security Hourly Other COGS" or
                            payroll_item == "Salary PTO COGS" or payroll_item == "Hourly PTO COGS" or
                            payroll_item == "Security Salary PTO (1)" or payroll_item == "Security Hourly PTO (1)" or
                            payroll_item == "Salary Holiday COGS" or payroll_item == "Hourly Holiday COGS" or
                            payroll_item == "Security Salary Holiday COGS" or payroll_item == "Security Hourly Holiday COGS"):
                        print("customer + service != payroll item")
                        print(f"customer + service != payroll item: {username}, {local_date}, {jobcode_1}:{jobcode_2}, "
                              f"{payroll_item}, {service_item}")
                        error_sheet = add_row("customer + service != payroll item", username, group, local_date,
                                              jobcode_1, jobcode_2, payroll_item, service_item, error_sheet)

                elif service_item == "LABOR:Training":
                    if not (payroll_item == "Salary Other COGS" or payroll_item == "Hourly Other COGS" or
                            payroll_item == "Security Salary Other COGS" or payroll_item == "Security Hourly Other COGS"):
                        print("customer + service != payroll item")
                        print(f"customer + service != payroll item: {username}, {local_date}, {jobcode_1}:{jobcode_2}, "
                              f"{payroll_item}, {service_item}")
                        error_sheet = add_row("customer + service != payroll item", username, group, local_date,
                                              jobcode_1, jobcode_2, payroll_item, service_item, error_sheet)

            elif jobcode_2 == "Global Overhead":
                if jobcode_1 == "SAV Digital Environments, Inc WY":
                    print("Wyoming?")
                    print(f"Wyoming?: {username}, {local_date}, {jobcode_1}:{jobcode_2}, "
                          f"{payroll_item}, {service_item}")
                    error_sheet = add_row("Wyoming?", username, group, local_date, jobcode_1, jobcode_2,
                                          payroll_item, service_item, error_sheet)
                elif not jobcode_1 == "SAV Digital Environments, Inc MT":
                    print("Bad customer")
                    print(f"Bad customer: {username}, {local_date}, {jobcode_1}:{jobcode_2}, "
                          f"{payroll_item}, {service_item}")
                    error_sheet = add_row("Bad customer", username, group, local_date, jobcode_1, jobcode_2,
                                          payroll_item, service_item, error_sheet)

                elif not (service_item == "LABOR:Ops/Admin/Sales" or service_item == "LABOR:Training"):
                    print("customer != service item")
                    print(f"customer != service item: {username}, {local_date}, {jobcode_1}:{jobcode_2}, "
                          f"{payroll_item}, {service_item}")
                    error_sheet = add_row("customer != service item", username, group, local_date, jobcode_1, jobcode_2,
                                          payroll_item, service_item, error_sheet)

                elif service_item == "LABOR:Ops/Admin/Sales":
                    if not (payroll_item == "Salary Expense" or payroll_item == "Hourly Expense" or
                            payroll_item == "Salary PTO Expense" or payroll_item == "Hourly PTO Expense" or
                            payroll_item == "Salary Holiday Expense" or payroll_item == "Hourly Holiday Expense"):
                        print("customer + service != payroll item")
                elif service_item == "LABOR:Training":
                    if not (payroll_item == "Salary Expense" or payroll_item == "Hourly Expense"):
                        print("customer + service != payroll item")
                        print(f"customer + service != payroll item: {username}, {local_date}, {jobcode_1}:{jobcode_2}, "
                              f"{payroll_item}, {service_item}")
                        error_sheet = add_row("customer + service != payroll item", username, group, local_date,
                                              jobcode_1, jobcode_2, payroll_item, service_item, error_sheet)

            elif jobcode_1 != "LUNCH":
                if jobcode_1 == "MISSING CUSTOMER":
                    jobcode_2 = " "
                if not (("LABOR:Finish:" in service_item and ("Base" in service_item or
                                                              "Design" in service_item or
                                                              "Management" in service_item)) or
                        ("LABOR:Rough-in:" in service_item and ("Base" in service_item or
                                                                "Design" in service_item or
                                                                "Management" in service_item)) or
                        ("LABOR:Security Finish:" in service_item and ("Base" in service_item or
                                                                       "Design" in service_item or
                                                                       "Management" in service_item)) or
                        ("LABOR:Security Rough:" in service_item and ("Base" in service_item or
                                                                      "Design" in service_item or
                                                                      "Management" in service_item)) or
                        service_item == "LABOR:Programming:Base" or
                        service_item == "LABOR:Travel Time"):
                    print("customer != service item")
                    print(f"customer != service item: {username}, {local_date}, {jobcode_1}:{jobcode_2}, "
                          f"{payroll_item}, {service_item}")
                    error_sheet = add_row("customer != service item", username, group, local_date, jobcode_1, jobcode_2,
                                          payroll_item, service_item, error_sheet)

                elif "LABOR:Finish:" in service_item and ("Base" in service_item or
                                                          "Design" in service_item or
                                                          "Management" in service_item):
                    if not (payroll_item == "Salary Finish COGS" or payroll_item == "Hourly Finish COGS"):
                        print("customer + service != payroll item")
                elif "LABOR:Rough-in:" in service_item and ("Base" in service_item or
                                                            "Design" in service_item or
                                                            "Management" in service_item):
                    if not (payroll_item == "Salary Rough COGS" or payroll_item == "Hourly Rough COGS"):
                        print("customer + service != payroll item")
                        print(f"customer + service != payroll item: {username}, {local_date}, {jobcode_1}:{jobcode_2}, "
                              f"{payroll_item}, {service_item}")
                        error_sheet = add_row("customer + service != payroll item", username, group, local_date,
                                              jobcode_1, jobcode_2, payroll_item, service_item, error_sheet)

                elif "LABOR:Security Finish:" in service_item and ("Base" in service_item or
                                                                   "Design" in service_item or
                                                                   "Management" in service_item):
                    if not (payroll_item == "Security Salary Finish COGS" or
                            payroll_item == "Security Hourly Finish COGS"):
                        print("customer + service != payroll item")
                elif "LABOR:Security Rough" in service_item and ("Base" in service_item or
                                                                 "Design" in service_item or
                                                                 "Management" in service_item):
                    if not (payroll_item == "Security Salary Rough COGS" or
                            payroll_item == "Security Hourly Rough COGS"):
                        print("customer + service != payroll item")
                        print(f"customer + service != payroll item: {username}, {local_date}, {jobcode_1}:{jobcode_2}, "
                              f"{payroll_item}, {service_item}")
                        error_sheet = add_row("customer + service != payroll item", username, group, local_date,
                                              jobcode_1, jobcode_2, payroll_item, service_item, error_sheet)

                elif service_item == "LABOR:Programming:Base":
                    if not (payroll_item == "Salary Finish COGS" or payroll_item == "Hourly Finish COGS"):
                        print("customer + service != payroll item")
                        print(f"customer + service != payroll item: {username}, {local_date}, {jobcode_1}:{jobcode_2}, "
                              f"{payroll_item}, {service_item}")
                        error_sheet = add_row("customer + service != payroll item", username, group, local_date,
                                              jobcode_1, jobcode_2, payroll_item, service_item, error_sheet)

                if service_item != "LABOR:Travel Time":
                    only_travel[0] = True
                elif service_item == "LABOR:Travel Time":
                    if not (payroll_item == "Salary Finish COGS" or payroll_item == "Hourly Finish COGS" or
                            payroll_item == "Salary Rough COGS" or payroll_item == "Hourly Rough COGS" or
                            payroll_item == "Security Salary Finish COGS" or payroll_item == "Security Hourly Finish COGS" or
                            payroll_item == "Security Salary Rough COGS" or payroll_item == "Security Hourly Rough COGS"):
                        print("customer + service != payroll item")
                        print(f"customer + service != payroll item: {username}, {local_date}, {jobcode_1}:{jobcode_2}, "
                              f"{payroll_item}, {service_item}")
                        error_sheet = add_row("customer + service != payroll item", username, group, local_date,
                                              jobcode_1, jobcode_2, payroll_item, service_item, error_sheet)

                    if last_job == (str(jobcode_1) + ':' + str(jobcode_2)) and current_phase not in payroll_item:
                        print("bad travel phase")
                        print(f"bad travel phase: {username}, {local_date}, {jobcode_1}:{jobcode_2}, "
                              f"{payroll_item}, {service_item}")
                        error_sheet = add_row("bad travel phase", username, group, local_date,
                                              jobcode_1, jobcode_2, payroll_item, service_item, error_sheet)

                    only_travel[1] = True

            if current_pay_type not in payroll_item:
                print("Wrong Pay Type")
                print(f"Wrong Pay Type: {username}, {local_date}, {jobcode_1}:{jobcode_2}, "
                      f"{payroll_item}, {service_item}")
                error_sheet = add_row("Wrong Pay Type", username, group, local_date,
                                      jobcode_1, jobcode_2, payroll_item, service_item, error_sheet)

            if 'Holiday' in payroll_item:
                holiday_check = False
                for day in holidays:
                    if day in local_date:
                        holiday_check = True
                if holiday_check is False:
                    print("Not a Holiday")
                    print(f"Not a Holiday: {username}, {local_date}, {jobcode_1}:{jobcode_2}, "
                          f"{payroll_item}, {service_item}")
                    error_sheet = add_row("Not a Holiday", username, group, local_date,
                                          jobcode_1, jobcode_2, payroll_item, service_item, error_sheet)

            if 'Salary' in payroll_item:
                current_pay_type = 'Salary'
            elif 'Hourly' in payroll_item:
                current_pay_type = 'Hourly'
            last_job = str(jobcode_1) + ':' + str(jobcode_2)

        except TypeError:
            print(f"TypeError: {username}, {local_date}, {jobcode_1}:{jobcode_2}, {payroll_item}, {service_item}")
            # error_sheet = add_row("TypeError", username, group, local_date, jobcode_1, jobcode_2, payroll_item,
            #                       service_item, error_sheet)

    error_book.save('timesheet_error_report.xlsx')


def check_for_duplicates(import_directory, imported_list):
    """This function checks if the file has already been imported"""
    for imp in imported_list:  # cycles through the directories of the previously imported files
        if import_directory == imp:  # if the directory we are trying to import matches a directory in the database
            return True  # we found a match
    return False  # no matches were found


def open_spreadsheet(directory):
    """This function tries to open a spreadsheet and prompts the user if it cannot"""
    while True:  # infinite loop
        try:
            dashboard = load_workbook(filename=directory, read_only=False, data_only=True)  # tries to open spreadsheet
            return dashboard  # returns the spreadsheet if it was opened
        except PermissionError:  # the spreadsheet is already open by something else
            dialog = DatasheetOpenDialog(basename(directory), None, wx.ID_ANY, "")  # asks if the user wants to retry
            retry = dialog.ShowModal()  # captures the users response
            if not retry:  # if the user doesn't want to retry
                return None


class FileDropTarget(wx.FileDropTarget):
    """ This object implements Drop Target functionality for Files """

    def __init__(self, obj, import_files):
        """ Initialize the Drop Target, passing in the Object Reference to
        indicate what should receive the dropped files """
        # Initialize the wxFileDropTarget Object
        wx.FileDropTarget.__init__(self)
        # Store the Object Reference for dropped files
        self.obj = obj
        self.import_files = import_files

    def OnDropFiles(self, x, y, file_names):
        """ Implement File Drop """
        # Move Insertion Point to the end of the widget's text
        self.obj.SetInsertionPointEnd()
        # append a list of the file names dropped
        dup_check = False
        for file in file_names:
            for iFile in self.import_files:
                if file == iFile:
                    dup_check = True
            # if not file.endswith('.xlsx'):
            #     wx.MessageBox("Incorrect file type. Please choose an .xlsx file.", "Error", wx.OK | wx.ICON_INFORMATION)
            #     continue
            if not dup_check:
                self.obj.WriteText(basename(file) + '\n')
                self.import_files.append(file)
            else:
                print("Removed duplicate import file!")
                wx.MessageBox("File already in import list.", "Error", wx.OK | wx.ICON_INFORMATION)
                dup_check = False
        self.obj.WriteText('\n')


class FirstFrame(wx.Frame):
    """This object is the main window"""

    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)

        self.import_files = []

        self.SetSize((640, 428))
        self.button_browse = wx.FilePickerCtrl(self)
        # self.button_4.Bind(wx.EVT_FILEPICKER_CHANGED, self.on_choose_file)
        self.text_ctrl_drag_drop = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_MULTILINE | wx.TE_READONLY)
        drop_target = FileDropTarget(self.text_ctrl_drag_drop, self.import_files)
        # Link the Drop Target Object to the Text Control
        self.text_ctrl_drag_drop.SetDropTarget(drop_target)

        # initializes the buttons
        # self.choice_phase = wx.Choice(self, wx.ID_ANY, choices=["Choose Phase", "Rough In", "Finish"])
        # self.checkbox_general_dashboard = wx.CheckBox(self, wx.ID_ANY, "General Master Dashboard")
        # self.checkbox_kacey_dashboard = wx.CheckBox(self, wx.ID_ANY, "Kaceys's Master Dashboard")
        # self.checkbox_jake_dashboard = wx.CheckBox(self, wx.ID_ANY, "Jake's Master Dashboard")
        self.panel_1 = wx.Panel(self, wx.ID_ANY)
        self.button_continue = wx.Button(self, wx.ID_ANY, "Continue")
        self.button_cancel = wx.Button(self, wx.ID_ANY, "Cancel")
        self.button_clear = wx.Button(self, wx.ID_ANY, "Clear")

        self.__set_properties()
        self.__do_layout()
        self.SetMinSize((345, 345))

        # initializes the events
        self.Bind(wx.EVT_FILEPICKER_CHANGED, self.on_choose_file, self.button_browse)
        # self.Bind(wx.EVT_CHOICE, self.on_phase_selection, self.choice_phase)
        # self.Bind(wx.EVT_CHECKBOX, self.on_general_master_dashboard_checkbox, self.checkbox_general_dashboard)
        # self.Bind(wx.EVT_CHECKBOX, self.on_kaceys_master_dashboard_checkbox, self.checkbox_kacey_dashboard)
        # self.Bind(wx.EVT_CHECKBOX, self.on_jakes_master_dashboard_checkbox, self.checkbox_jake_dashboard)
        self.Bind(wx.EVT_BUTTON, self.on_continue_from_main_window, self.button_continue)
        self.Bind(wx.EVT_BUTTON, self.on_cancel_program, self.button_cancel)
        self.Bind(wx.EVT_BUTTON, self.on_clear, self.button_clear)
        self.Bind(wx.EVT_ICONIZE, self.on_minimize)

    def __set_properties(self):
        self.SetTitle("Import Project Datasheet")
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(wx.Bitmap("SAV-Social-Profile.jpg", wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)

        self.SetBackgroundColour(wx.Colour(255, 255, 255))
        # self.choice_phase.SetMinSize((102, 23))
        # self.choice_phase.SetSelection(0)
        # self.checkbox_general_dashboard.SetValue(1)
        # self.checkbox_kacey_dashboard.SetValue(1)
        # self.checkbox_jake_dashboard.SetValue(0)

    def __do_layout(self):
        sizer_5 = wx.BoxSizer(wx.VERTICAL)
        sizer_9 = wx.GridBagSizer(0, 0)
        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_8 = wx.BoxSizer(wx.VERTICAL)
        sizer_11 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_15 = wx.BoxSizer(wx.VERTICAL)
        sizer_12 = wx.BoxSizer(wx.VERTICAL)
        sizer_13 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_7 = wx.BoxSizer(wx.VERTICAL)
        sizer_14 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_16 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_10 = wx.BoxSizer(wx.VERTICAL)
        global user
        label_1 = wx.StaticText(self, wx.ID_ANY, f"Hello {user}! This program imports job costing spreadsheets "
                                                 f"to a master dashboard.")
        sizer_10.Add(label_1, 0, wx.ALL, 5)
        static_line_1 = wx.StaticLine(self, wx.ID_ANY)
        sizer_10.Add(static_line_1, 0, wx.EXPAND, 0)
        sizer_5.Add(sizer_10, 0, wx.EXPAND, 0)
        sizer_16.Add(self.button_browse, 0, wx.ALL, 12)
        label_6 = wx.StaticText(self, wx.ID_ANY, "Or drag and drop files below")
        sizer_16.Add(label_6, 0, wx.ALIGN_CENTER, 0)
        sizer_7.Add(sizer_16, 0, wx.EXPAND, 0)
        sizer_14.Add(self.text_ctrl_drag_drop, 1, wx.EXPAND, 0)
        sizer_7.Add(sizer_14, 1, wx.EXPAND, 0)
        sizer_6.Add(sizer_7, 2, wx.EXPAND, 0)
        bitmap_2 = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap("SAV-Company-Logo.png", wx.BITMAP_TYPE_ANY))
        sizer_12.Add(bitmap_2, 0, wx.BOTTOM | wx.RIGHT | wx.TOP, 12)
        # sizer_13.Add(self.choice_phase, 0, wx.BOTTOM | wx.LEFT, 6)
        sizer_12.Add(sizer_13, 1, wx.EXPAND, 0)
        sizer_8.Add(sizer_12, 0, wx.EXPAND, 0)
        # sizer_15.Add(self.checkbox_general_dashboard, 0, wx.LEFT | wx.RIGHT | wx.TOP, 6)
        # sizer_15.Add(self.checkbox_kacey_dashboard, 0, wx.LEFT | wx.RIGHT | wx.TOP, 6)
        # sizer_15.Add(self.checkbox_jake_dashboard, 0, wx.LEFT | wx.RIGHT | wx.TOP, 6)
        sizer_11.Add(sizer_15, 1, wx.EXPAND, 0)
        sizer_8.Add(sizer_11, 1, wx.EXPAND, 0)
        sizer_6.Add(sizer_8, 0, wx.EXPAND | wx.LEFT, 6)
        sizer_5.Add(sizer_6, 1, wx.EXPAND, 0)
        sizer_9.Add(self.panel_1, (0, 0), (1, 1), wx.EXPAND, 0)
        sizer_9.Add(self.button_continue, (0, 1), (1, 1), wx.ALIGN_BOTTOM | wx.ALIGN_RIGHT | wx.ALL, 6)
        sizer_9.Add(self.button_cancel, (0, 3), (1, 1), wx.ALIGN_BOTTOM | wx.ALIGN_RIGHT | wx.ALL, 6)
        sizer_9.Add(self.button_clear, (0, 2), (1, 1), wx.ALIGN_BOTTOM | wx.ALIGN_RIGHT | wx.ALL, 6)
        sizer_5.Add(sizer_9, 0, wx.ALIGN_BOTTOM | wx.ALIGN_RIGHT | wx.ALL | wx.EXPAND, 12)
        self.SetSizer(sizer_5)
        self.Layout()

    def on_choose_file(self, event):  # button_browse
        dup_check = False
        file = self.button_browse.GetPath()  # catches what file the user chose
        for iFile in self.import_files:  # checks if file is already in the to-be imported list
            if file == iFile:
                dup_check = True
        if not file.endswith('.xlsx'):
            wx.MessageBox("Incorrect file type. Please choose an .xlsx file.", "Error", wx.OK | wx.ICON_INFORMATION)
            event.skip()
        if not dup_check:
            self.import_files.append(file)
            self.text_ctrl_drag_drop.WriteText(basename(file) + '\n')  # shows the user they chose this
        else:
            print("Removed duplicate import file!")
            wx.MessageBox("File already in import list.", "Error", wx.OK | wx.ICON_INFORMATION)
        event.Skip()

    # def on_phase_selection(self, event):  # event handler
    #     print(self.choice_phase.GetSelection())
    #     event.Skip()
    #
    # def on_general_master_dashboard_checkbox(self, event):  # event handler
    #     print(self.checkbox_general_dashboard.GetValue())
    #     event.Skip()
    #
    # def on_kaceys_master_dashboard_checkbox(self, event):  # event handler
    #     print(self.checkbox_kacey_dashboard.GetValue())
    #     event.Skip()

    # def on_jakes_master_dashboard_checkbox(self, event):  # event handler
    #     print(self.checkbox_jake_dashboard.GetValue())
    #     wx.MessageBox("Jake's dashboard not yet implemented.", "Error", wx.OK | wx.ICON_INFORMATION)
    #     self.checkbox_jake_dashboard.SetValue(0)
    #     event.Skip()

    def on_continue_from_main_window(self, event):  # event handler
        if not self.import_files:
            wx.MessageBox("Please choose a file to import.", "Error", wx.OK | wx.ICON_INFORMATION)
        else:
            for file in self.import_files:
                print(file)
                find_errors(file)
            wx.MessageBox("Done!", "Done!", wx.OK | wx.ICON_INFORMATION)

            self.text_ctrl_drag_drop.SetValue("")  # resets the program
            self.import_files.clear()  # resets the program
        event.Skip()

    def on_cancel_program(self, event):  # event handler
        print(getuser())
        self.Destroy()
        event.Skip()

    def on_clear(self, event):  # resets the program
        self.text_ctrl_drag_drop.SetValue("")
        global pb
        self.import_files.clear()
        pb = not pb
        event.Skip()

    @staticmethod
    def on_minimize(event):  # easter egg
        global pb
        if pb:
            wx.MessageBox("Or is it Peanutbutter?", "Peanutbutter!", wx.OK | wx.ICON_INFORMATION)
        pb = False
        event.Skip()


class DatasheetOpenDialog(wx.Dialog):
    def __init__(self, open_data_sheet, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.open_data_sheet = open_data_sheet
        self.text_ctrl_open_datasheet = wx.TextCtrl(self, wx.ID_ANY,
                                                    f"{open_data_sheet} is open by a user. Please close "
                                                    f"{open_data_sheet} and click \"Retry\".",
                                                    style=wx.BORDER_NONE | wx.TE_MULTILINE | wx.TE_READONLY)
        self.panel_2 = wx.Panel(self, wx.ID_ANY)
        self.button_1 = wx.Button(self, wx.ID_ANY, "Retry")
        self.button_5 = wx.Button(self, wx.ID_ANY, "Back")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_TEXT, self.text_ctrl_open_data_sheet, self.text_ctrl_open_datasheet)
        self.Bind(wx.EVT_BUTTON, self.on_retry, self.button_1)
        self.Bind(wx.EVT_BUTTON, self.on_back, self.button_5)

    def __set_properties(self):
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(wx.Bitmap("SAV-Social-Profile.jpg", wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)

        self.SetTitle("dialog_3")
        self.text_ctrl_open_datasheet.SetBackgroundColour(wx.Colour(255, 255, 255))

    def __do_layout(self):
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(self.text_ctrl_open_datasheet, 0, wx.ALL | wx.EXPAND, 12)
        sizer_2.Add(self.panel_2, 1, 0, 0)
        sizer_2.Add(self.button_1, 0, wx.ALIGN_BOTTOM | wx.ALL | wx.FIXED_MINSIZE, 12)
        sizer_2.Add(self.button_5, 0, wx.ALIGN_BOTTOM | wx.ALL | wx.FIXED_MINSIZE, 12)
        sizer_1.Add(sizer_2, 1, wx.ALIGN_BOTTOM | wx.ALIGN_RIGHT | wx.ALL | wx.EXPAND | wx.FIXED_MINSIZE, 1)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()

    def text_ctrl_open_data_sheet(self, event):  # event handler
        print(f"{self.open_data_sheet} is currently open by a user!")
        event.Skip()

    def on_retry(self, event):  # event handler
        self.EndModal(True)
        self.Destroy()
        event.Skip()

    def on_back(self, event):  # event handler
        self.EndModal(False)
        self.Destroy()
        event.Skip()


class DatasheetAlreadyImportedDialog(wx.Dialog):
    def __init__(self, open_sheet, imported_by, imported_date, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.open_data_sheet = open_sheet
        self.text_ctrl_already_imported = wx.TextCtrl(self, wx.ID_ANY,
                                                      f"{open_sheet}\nHas already been imported by {imported_by} on "
                                                      f"{imported_date}. If you would  like to import the project as a "
                                                      f"new project, select \"Duplicate\". If you want to refresh the "
                                                      f"existing data, select \"Replace\".",
                                                      style=wx.BORDER_NONE | wx.TE_MULTILINE | wx.TE_READONLY)
        self.panel_2 = wx.Panel(self, wx.ID_ANY)
        self.button_6 = wx.Button(self, wx.ID_ANY, "Duplicate")
        self.button_1 = wx.Button(self, wx.ID_ANY, "Replace")
        self.button_5 = wx.Button(self, wx.ID_ANY, "Back")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_TEXT, self.text_ctrl_open_data_sheet, self.text_ctrl_already_imported)
        self.Bind(wx.EVT_BUTTON, self.on_duplicate, self.button_6)
        self.Bind(wx.EVT_BUTTON, self.on_replace, self.button_1)
        self.Bind(wx.EVT_BUTTON, self.on_back, self.button_5)

    def __set_properties(self):
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(wx.Bitmap("SAV-Social-Profile.jpg", wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)

        self.SetTitle("dialog_2")
        self.text_ctrl_already_imported.SetBackgroundColour(wx.Colour(255, 255, 255))

    def __do_layout(self):
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(self.text_ctrl_already_imported, 0, wx.ALL | wx.EXPAND, 12)
        sizer_2.Add(self.panel_2, 1, 0, 0)
        sizer_2.Add(self.button_6, 0, wx.ALIGN_BOTTOM | wx.ALL | wx.FIXED_MINSIZE, 12)
        sizer_2.Add(self.button_1, 0, wx.ALIGN_BOTTOM | wx.ALL | wx.FIXED_MINSIZE, 12)
        sizer_2.Add(self.button_5, 0, wx.ALIGN_BOTTOM | wx.ALL | wx.FIXED_MINSIZE, 12)
        sizer_1.Add(sizer_2, 1, wx.ALIGN_BOTTOM | wx.ALIGN_RIGHT | wx.ALL | wx.EXPAND | wx.FIXED_MINSIZE, 1)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()

    def text_ctrl_open_data_sheet(self, event):  # event handler
        print(f"{self.open_data_sheet} has already been imported")
        event.Skip()

    def on_duplicate(self, event):  # event handler
        if user == "Julian.Kizanis":
            dialog = AreYouSureDuplicateDialog(None, wx.ID_ANY, "")
            answer = dialog.ShowModal()
            if answer:
                self.EndModal(0)
            else:
                self.EndModal(CANCEL)
            self.Destroy()
        else:
            wx.MessageBox("This functionality has been disabled, please contact "
                          "Julian.Kizanis if you wish to duplicate project entries.",
                          "Duplicate", wx.OK | wx.ICON_INFORMATION)
        event.Skip()

    def on_replace(self, event):  # event handler
        dialog = AreYouSureReplaceDialog(None, wx.ID_ANY, "")
        answer = dialog.ShowModal()
        if answer:
            self.EndModal(OVERRIDE)
        else:
            self.EndModal(CANCEL)
        self.Destroy()
        event.Skip()

    def on_back(self, event):  # event handler
        self.EndModal(CANCEL)
        self.Destroy()
        event.Skip()


class AreYouSureReplaceDialog(wx.Dialog):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.panel_2 = wx.Panel(self, wx.ID_ANY)
        self.button_1 = wx.Button(self, wx.ID_ANY, "Replace")
        self.button_5 = wx.Button(self, wx.ID_ANY, "Back")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.on_replace, self.button_1)
        self.Bind(wx.EVT_BUTTON, self.on_back, self.button_5)

    def __set_properties(self):
        self.SetTitle("dialog")
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(wx.Bitmap("SAV-Social-Profile.jpg", wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)

    def __do_layout(self):
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        label_2 = wx.StaticText(self, wx.ID_ANY,
                                "Are you Sure you want to replace/overwrite the project? "
                                "The old data will not be saved.")
        label_2.Wrap(300)
        sizer_1.Add(label_2, 0, wx.ALL, 12)
        sizer_2.Add(self.panel_2, 1, 0, 0)
        sizer_2.Add(self.button_1, 0, wx.ALIGN_BOTTOM | wx.ALL | wx.FIXED_MINSIZE, 12)
        sizer_2.Add(self.button_5, 0, wx.ALIGN_BOTTOM | wx.ALL | wx.FIXED_MINSIZE, 12)
        sizer_1.Add(sizer_2, 1, wx.ALIGN_BOTTOM | wx.ALIGN_RIGHT | wx.ALL | wx.EXPAND | wx.FIXED_MINSIZE, 1)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()

    def on_replace(self, event):  # event handler
        self.EndModal(True)
        self.Destroy()
        event.Skip()

    def on_back(self, event):  # event handler
        self.EndModal(False)
        self.Destroy()
        event.Skip()


class AreYouSureDuplicateDialog(wx.Dialog):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.panel_2 = wx.Panel(self, wx.ID_ANY)
        self.button_1 = wx.Button(self, wx.ID_ANY, "Duplicate")
        self.button_5 = wx.Button(self, wx.ID_ANY, "Back")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.on_duplicate, self.button_1)
        self.Bind(wx.EVT_BUTTON, self.on_back, self.button_5)

    def __set_properties(self):
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(wx.Bitmap("SAV-Social-Profile.jpg", wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)
        self.SetTitle("dialog_1")

    def __do_layout(self):
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        label_2 = wx.StaticText(self, wx.ID_ANY, "Are you Sure you want to add the project as a duplicate?")
        label_2.Wrap(300)
        sizer_1.Add(label_2, 0, wx.ALL, 12)
        sizer_2.Add(self.panel_2, 1, 0, 0)
        sizer_2.Add(self.button_1, 0, wx.ALIGN_BOTTOM | wx.ALL | wx.FIXED_MINSIZE, 12)
        sizer_2.Add(self.button_5, 0, wx.ALIGN_BOTTOM | wx.ALL | wx.FIXED_MINSIZE, 12)
        sizer_1.Add(sizer_2, 1, wx.ALIGN_BOTTOM | wx.ALIGN_RIGHT | wx.ALL | wx.EXPAND | wx.FIXED_MINSIZE, 1)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()

    def on_duplicate(self, event):  # event handler
        self.EndModal(True)
        self.Destroy()
        event.Skip()

    def on_back(self, event):  # event handler
        self.EndModal(False)
        self.Destroy()
        event.Skip()


class SuccessFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((350, 150))
        self.panel_2 = wx.Panel(self, wx.ID_ANY)
        self.button_5 = wx.Button(self, wx.ID_ANY, "Okay")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.on_okay, self.button_5)

    def __set_properties(self):
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(wx.Bitmap("SAV-Social-Profile.jpg", wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)

        self.SetTitle("frame_2")
        self.SetBackgroundColour(wx.Colour(255, 255, 255))

    def __do_layout(self):
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        label_2 = wx.StaticText(self, wx.ID_ANY, "The project was successfully imported!")
        label_2.Wrap(300)
        sizer_1.Add(label_2, 0, wx.ALL, 12)
        sizer_2.Add(self.panel_2, 1, 0, 0)
        sizer_2.Add(self.button_5, 0, wx.ALIGN_BOTTOM | wx.ALL | wx.FIXED_MINSIZE, 12)
        sizer_1.Add(sizer_2, 1, wx.ALIGN_BOTTOM | wx.ALIGN_RIGHT | wx.ALL | wx.EXPAND | wx.FIXED_MINSIZE, 1)
        self.SetSizer(sizer_1)
        self.Layout()

    def on_okay(self, event):  # event handler
        print("Event handler 'on_okay' not implemented!")
        self.Destroy()
        event.Skip()


class ErrorFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((350, 150))
        self.panel_2 = wx.Panel(self, wx.ID_ANY)
        self.button_5 = wx.Button(self, wx.ID_ANY, "Okay")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.on_okay, self.button_5)

    def __set_properties(self):
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(wx.Bitmap("SAV-Social-Profile.jpg", wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)
        self.SetTitle("frame_2")
        self.SetBackgroundColour(wx.Colour(255, 255, 255))

    def __do_layout(self):
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        label_2 = wx.StaticText(self, wx.ID_ANY, "An unexpected error has occurred!")
        label_2.Wrap(300)
        sizer_1.Add(label_2, 0, wx.ALL, 12)
        sizer_2.Add(self.panel_2, 1, 0, 0)
        sizer_2.Add(self.button_5, 0, wx.ALIGN_BOTTOM | wx.ALL | wx.FIXED_MINSIZE, 12)
        sizer_1.Add(sizer_2, 1, wx.ALIGN_BOTTOM | wx.ALIGN_RIGHT | wx.ALL | wx.EXPAND | wx.FIXED_MINSIZE, 1)
        self.SetSizer(sizer_1)
        self.Layout()

    @staticmethod
    def on_okay(event):  # event handler
        print("Event handler 'on_okay' not implemented!")
        event.Skip()


class MyApp(wx.App):
    def OnInit(self):
        self.frame = FirstFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True


if __name__ == "__main__":
    ImportProjectDatasheets = MyApp(0)
    ImportProjectDatasheets.MainLoop()
