import sys
import os
import tkinter as tk

# Adjust the path to include the src directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

# Import the GUI class
from gui import ObjectPatternRecognizerGUI

if __name__ == "__main__":
    root = tk.Tk()
    app = ObjectPatternRecognizerGUI(root)
    root.mainloop()
