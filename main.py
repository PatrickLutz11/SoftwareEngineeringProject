import os
import sys
import tkinter as tk


def main() -> None:
    """Main function to start the Object Pattern Recognizer GUI."""
    # Adjust the path to include the src directory
    src_path = os.path.join(os.path.dirname(__file__), "src")
    sys.path.insert(0, os.path.abspath(src_path))
    
    from gui import ObjectPatternRecognizerGUI  # noqa: E402
    root = tk.Tk()
    app = ObjectPatternRecognizerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
