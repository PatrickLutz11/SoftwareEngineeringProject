# main.py

import os
import sys
import tkinter as tk


def resource_path(relative_path: str) -> str:
    """Gets the absolute path to a resource, works for development and PyInstaller.

    Args:
        relative_path (str): The relative path to the resource.

    Returns:
        str: The absolute path to the resource.
    """
    try:
        # PyInstaller creates a temporary folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def main() -> None:
    """Main function to start the Object Pattern Recognizer GUI."""
    # Adjust the path to include the src directory
    src_path = os.path.join(os.path.dirname(__file__), "src")
    sys.path.insert(0, os.path.abspath(src_path))

    # Import the GUI class
    from gui import ObjectPatternRecognizerGUI  # noqa: E402

    root = tk.Tk()
    app = ObjectPatternRecognizerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
