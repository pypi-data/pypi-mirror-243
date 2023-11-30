import tkinter
import tkinter as tk
from tkinter import ttk

#from matplotlib.backends.backend_tkagg import (
#    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
import copy
from tkinter import ttk
from tkinter.messagebox import showinfo

import py_block_diagram as pybd
pad_options = {'padx': 5, 'pady': 5}
xpad_options = {'padx': 5, 'pady': 0}
ypad_options = {'padx': 0, 'pady': 5}

from pybd_gui.tkinter_utils import my_toplevel_window, window_with_param_widgets_that_appear_and_disappear

def fixed_map(option):
    # Returns the style map for 'option' with any styles starting with
    # ("!disabled", "!selected", ...) filtered out

    # style.map() returns an empty list for missing options, so this should
    # be future-safe
    return [elm for elm in style.map("Treeview", query_opt=option)
            if elm[:2] != ("!disabled", "!selected")]

###############################################################
# To do:
#
# - when adding a new block, I need to be able to specify parameters
#   whose labels adjust, similar to the sensors and actuators
#
#
# - Plan:
#
#    - each block type should be able to create an empty default where
#      any unknown init params are set to None
#
#    - the default block should have a py_param attribute along with a
#      default_params attr
#
#    - the gui will use the py_params as the labels for the parameter
#      boxes and then use the default_params (both from the empty
#      default block) to populate the default values
#
#    - create a base class from actuator_or_sensor_chooser.py that has boxes
#      that appear and disappear and whose labels adapt based on the number
#      of py_params and the labels get set to the py_params and whose default
#      values come from the empty blocks
#
#
###############################################################


class input_viewer(my_toplevel_window, window_with_param_widgets_that_appear_and_disappear):
    def __init__(self, parent, title="Block Placement Viewer"):
        super().__init__(parent, title=title, geometry="700x600")
        self.parent = parent
        self.bd = self.parent.bd
        self.make_widgets()


    def make_widgets(self, startrow=0):
        #def body(self):
        #print("frame: %s" % frame)
        # print(type(frame)) # tkinter.Frame

        #=================================
        #
        # column 0 
        #
        #=================================
        currow = startrow

        self.label1 = ttk.Label(self, text="Unplaced Blocks")

        self.label1.grid(row=currow, column=0, sticky='W', **pad_options)
        currow += 1
        self.tree = ttk.Treeview(self, columns=("Column 1", \
                "Column 2", "Column 3", "Column 4"))

        self.tree.heading("#1", text="Block Name", anchor='w')
        self.tree.heading("#2", text="Input 1")
        self.tree.heading("#3", text="Input 2")
        self.tree.heading("#4", text="Input 3")

        self.tree.column("#0", minwidth=0, width=5, stretch=False)
        for i in range(1,5):
            mystr = '#%i' % i
            self.tree.column(mystr, minwidth=50, width=100, stretch=True)

        
        # Add scrollbar for the Treeview
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # Pack the Treeview and scrollbar
        self.tree.grid(row=currow, column=0, sticky='W', **pad_options)
        self.scrollbar.grid(row=currow, column=1)#, sticky='W', **pad_options)

        currow += 1
        
        # probably need a done button at some point:
        #self.go_button.grid(row=30, columnspan=2, column=0, padx=5, pady=5)

    def list_inputs(self):
        block_list = self.bd.block_name_list
            
        attr_list = ["input_block1_name","input_block2_name", \
                     'bool_input_name']

        for i, block_name in enumerate(block_list):
            block = self.bd.get_block_by_name(block_name)
            myname = block.variable_name
            row = [myname]
            for attr in attr_list:
                if hasattr(block, attr):
                    val = getattr(block, attr)
                    if val:
                        row.append(val)

            if i % 2 == 0:
                mytag = 'evenrow'
            else:
                mytag = 'oddrow'
            self.tree.insert("", "end", values=row, tags = (mytag,))

        self.tree.tag_configure('oddrow', background=fixed_map('#A0A0A0'))
                    
##    def go_pressed(self):
##        # Next step:
##        # - read parameters from the numbered param boxes for kwargs
##        block_name = self.block_name.get()
##        new_block = self._create_new_block()
##        self.parent.append_block_to_dict(block_name, new_block)
##        #self.parent.password = self.my_password
##        self.destroy()
##

    def cancel_pressed(self):
        # print("cancel")
        self.destroy()



