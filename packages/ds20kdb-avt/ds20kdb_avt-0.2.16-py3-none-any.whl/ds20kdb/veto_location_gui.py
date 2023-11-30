#!/usr/bin/env python3
"""
The GUI permits to add entries in the <object>_location tables in order to
update the location of a object. It performs a check of the QR code, which
could by any object.

Input: a QR code, location details (Institute, timestamp, status, comment)
Output: history of the object and post on the DB object>_location table

---

Author: P.Franchini - p.franchini@lancaster.ac.uk
"""

import datetime
import itertools
import re
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

import pandas as pd
from tkcalendar import Calendar

from ds20kdb import interface


##############################################################################
# data structures
##############################################################################


class Object:
    """
    Container for GUI and database interaction.
    """

    dbi = interface.Database()

    def __init__(self):

        ######################################################################
        # build GUI
        ######################################################################

        self.root = tk.Tk()
        self.root.title("Set Veto Location GUI")

        # Set the window size (width x height)
        window_width = 450
        window_height = 750
        self.root.geometry(f"{window_width}x{window_height}")

        # Create a label for error messages
        self.error_label = tk.Label(self.root, text="", fg="red")
        self.error_label.pack()

        # Create a label for output messages
        self.output_label = tk.Label(self.root, text="", fg="green")
        self.output_label.pack()

        # Create labels and text boxes for the QR code
        self.qrcode_label = tk.Label(self.root, text="QR code:")
        self.qrcode_label.pack()
        self.qrcode_var = tk.StringVar(self.root)
        self.qrcode_entry = tk.Entry(self.root, textvariable=self.qrcode_var)
        self.qrcode_entry.pack()

        # Create a Text widget
        self.text_box = scrolledtext.ScrolledText(self.root, height=10, width=55)
        self.text_box.pack(pady=10)

        # Status
        self.status_label = tk.Label(self.root, text="Status:")
        self.status_label.pack()

        options = [
            '', 'received', 'unbagged', 'test', 'bagged', 'shipped',
            'production', 'storage', 'integration', 'scrapped'
        ]
        self.status_var = tk.StringVar(self.root)
        self.status_dropdown = ttk.Combobox(
            self.root, textvariable=self.status_var, values=options
        )
        self.status_dropdown.pack()

        # comment
        self.comment_label = tk.Label(self.root, text="Comment:")
        self.comment_label.pack()
        self.comment_var = tk.StringVar(self.root)
        self.comment_entry = tk.Entry(self.root, textvariable=self.comment_var)
        self.comment_entry.pack()

        # Location: institute
        self.location_label = tk.Label(self.root, text="Institute:")
        self.location_label.pack()

        dfr = self.dbi.get('institute').data
        locations = dfr.name.tolist()
        self.location_var = tk.StringVar(self.root)
        self.location_dropdown = ttk.Combobox(
            self.root, textvariable=self.location_var, values=locations
        )
        self.location_dropdown.pack()

        self.timestamp_label = tk.Label(self.root, text="Timestamp:")
        self.timestamp_label.pack()

        self.timestamp_date_var = tk.StringVar(self.root)
        self.timestamp_date_var.set(datetime.datetime.now().strftime('%Y-%m-%d'))
        self.timestamp_date_entry = tk.Entry(
            self.root, textvariable=self.timestamp_date_var
        )
        self.timestamp_date_entry.pack()
        self.timestamp_date_button = tk.Button(
            self.root, text="Select Date", command=self.open_calendar
        )
        self.timestamp_date_button.pack()

        self.timestamp_time_var = tk.StringVar(self.root)
        self.timestamp_time_var.set(datetime.datetime.now().strftime('%H:%M:%S'))
        self.timestamp_time_entry = tk.Entry(
            self.root, textvariable=self.timestamp_time_var
        )
        self.timestamp_time_entry.pack()
        self.timestamp_time_button = tk.Button(
            self.root, text="Select Time", command=self.open_time_selection
        )
        self.timestamp_time_button.pack()

        # Create the check button
        self.spacer_label = tk.Label(self.root, text="")
        self.spacer_label.pack()
        # Change the font size as needed
        check_font = ("Helvetica", 14)
        self.check_button = tk.Button(
            self.root, text="Check", command=self.check_command, font=check_font
        )
        self.check_button.pack()

        # Create the submit button
        self.spacer_label = tk.Label(self.root, text="")
        self.spacer_label.pack()
        # Change the font size as needed
        submit_font = ("Helvetica", 14)
        self.submit_button = tk.Button(
            self.root, text="Submit", command=self.submit_command, font=submit_font
        )
        self.submit_button.config(state="disabled")
        self.submit_button.pack()

    # Functions to check if a timestamp is not in the specified format
    @staticmethod
    def is_valid_date_format(input_string):
        pattern = r'^\d{4}-\d{2}-\d{2}$'
        return bool(re.match(pattern, input_string))

    @staticmethod
    def is_valid_time_format(input_string):
        pattern = r'^\d{2}:\d{2}:\d{2}$'
        return bool(re.match(pattern, input_string))

    def _get_highest_level_object(self, qrcode):
        """
        """
        tree = [
            # build progression: vpcb -> vpcb_asic -> vtile
            [
                ('vpcb', 'qrcode', 'vpcb_pid'),
                ('vpcb_asic', 'vpcb_id', 'vpcb_asic_pid'),
                ('vtile', 'vpcb_asic_id', 'vtile_pid'),
            ],
            # build progression: vmotherboard -> vpdu
            [
                ('vmotherboard', 'qrcode', 'vmotherboard_pid'),
                ('vpdu', 'vmotherboard_id', 'vpdu_pid'),
            ],
        ]

        obj = parameter = None

        for branch in tree:
            parameter = qrcode

            for test_object, key, select in branch:
                try:
                    tmp_id = self.dbi.get(
                        test_object, **{key: parameter}
                    ).data[select][0]
                except KeyError:
                    break
                else:
                    if not tmp_id:
                        break

                    obj = test_object
                    parameter = tmp_id
            else:
                break

        self.output_label.config(text=obj)

        return obj, parameter

    def _successful_dataframe_merge(self, obj, parameter):
        """
        Merge 2 dataframes to get the acronym for each location entry.

        Return True if the result of the merge contains anything.
        """
        location_dfr = self.dbi.get(f'{obj}_location', **{f'{obj}_id': parameter}).data
        institute_dfr = self.dbi.get('institute').data

        try:
            history = pd.merge(
                location_dfr, institute_dfr,
                left_on='institute_id', right_on='id', how='left'
            )
        except TypeError:
            # location_dfr is probably None
            pass
        else:
            history.rename(columns={'acronym': 'location'}, inplace=True)
            result = history[['timestamp', 'location', 'state', 'comment']]
            if not result.empty:
                self.text_box.delete('1.0', tk.END)
                self.text_box.insert(tk.END, result.to_string(index=False))
                return True

        return False

    # Check button
    def check_command(self):
        """
        Identify the highest-level form of the object represented by the
        user-specified QR code, and display the location information (if any).
        If an object was found in the database, enable the submit button.
        """

        # check QR code: identify the most manufactured form of the object
        obj, parameter = self._get_highest_level_object(self.qrcode_var.get())

        # merge 2 dataframes to get the acronym for each location entry
        if self._successful_dataframe_merge(obj, parameter):
            # One can now submit since the Check was fine
            self.submit_button.config(state='normal')

    def submit_command(self):
        """
        Submit information to database.
        """

        # reset the error message label
        self.error_label.config(text='')
        self.output_label.config(text='')

        selected_location = self.location_var.get()

        selected_date = self.timestamp_date_var.get()
        selected_time = self.timestamp_time_var.get()
        timestamp = f'{selected_date}T{selected_time}'

        # check timestamp
        if not self.is_valid_date_format(selected_date):
            self.error_label.config(text='Date is not in the specified format')
            return

        if not self.is_valid_time_format(selected_time):
            self.error_label.config(text='Time is not in the specified format')
            return

        selected_status = self.status_var.get()
        selected_qrcode = self.qrcode_var.get()

        # check QR code: identify the most manufactured form of the object
        obj, parameter = self._get_highest_level_object(self.qrcode_var.get())

        try:
            institute_id = self.dbi.get('institute', name=selected_location).data.id[0]
        except KeyError:
            self.error_label.config(text='Please select an institute')
            return

        # comment
        comment = self.comment_var.get()

        # Post the table
        table = {
            f'{obj}_id': parameter,
            'institute_id': int(institute_id),
            'timestamp': timestamp,
            'comment': comment,
            'state': selected_status,
        }
        print(table)

        post_successful = self.dbi.post_item(table, f'{obj}_location')
        if post_successful:
            status = 'succeeded'
            self.output_label.config(text=f'POST {status}: {obj} {selected_qrcode}')
            self._successful_dataframe_merge(obj, parameter)
        else:
            status = 'failed'
            self.error_label.config(text=f'POST {status}')

        print(f'POST {status}')

        self.submit_button.config(state="disabled")

    def _set_date(self, top, calendar_widget):
        selected_date = calendar_widget.get_date()
        # Convert the selected date to a datetime object
        selected_date = datetime.datetime.strptime(selected_date, '%d/%m/%Y')
        selected_date_formatted = selected_date.strftime('%Y-%m-%d')  # Format the date
        self.timestamp_date_var.set(selected_date_formatted)
        top.destroy()

    def open_calendar(self):
        top = tk.Toplevel(self.root)
        top.title('Select Date')

        calendar_widget = Calendar(top)
        calendar_widget.pack()

        set_button = tk.Button(
            top,
            text='Set Date',
            command=lambda: self._set_date(top, calendar_widget)
        )
        set_button.pack()

    def _set_time(self, top, time_selection_var):
        selected_time = time_selection_var.get()
        if ':' in selected_time and selected_time.count(':') == 1:
            selected_time += ':00'
        self.timestamp_time_var.set(selected_time)
        top.destroy()

    def open_time_selection(self):
        top = tk.Toplevel(self.root)
        top.title("Select Time")

        hours_minutes = itertools.product(range(24), range(0, 60, 15))
        time_selection_var = tk.StringVar(top)
        time_selection = ttk.Combobox(
            top,
            textvariable=time_selection_var,
            values=[f'{hour:02}:{minute:02}' for (hour, minute) in hours_minutes]
        )
        time_selection.pack()

        set_button = tk.Button(
            top,
            text="Set Time",
            command=lambda: self._set_time(top, time_selection_var)
        )
        set_button.pack()

    def mainloop(self):
        self.root.mainloop()


##############################################################################
def main():
    """
    The GUI permits to add entries in the <object>_location tables in order to
    update the location of a object. It performs a check of the QR code, which
    could by any object.
    """
    gui = Object()
    gui.mainloop()


##############################################################################
if __name__ == "__main__":
    main()
