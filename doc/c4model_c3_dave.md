:::mermaid
C4Component
    title Component Diagram for Object Pattern Recognizer System

    Container_Boundary(opr, "Object Pattern Recognizer Application") {
        Component(UI, "User Interface (CLI & GUI with Overlay)", "Python", "Allows user interaction via CLI or GUI, and displays results with overlays")
        Component(MainController, "Main Controller", "Python", "Coordinates the entire system workflow")
        Component(ConfigManager, "Config Manager", "Python", "Loads and manages system configurations from a separate file")
        Component(InputHandler, "Input Handler", "Python", "Handles input from the camera or images in a folder")
        Component(Bildverarbeitungsmodul, "Image Processing Module", "Python", "Processes images to detect shapes and colors")
        Component(CSVLogger, "CSV Logger", "Python", "Logs detected patterns, colors, and timestamps into a CSV file")

        Rel(UI, MainController, "User interacts via CLI/GUI")
        Rel(MainController, ConfigManager, "Loads system configurations")
        Rel(MainController, InputHandler, "Initializes input")
        Rel(InputHandler, Bildverarbeitungsmodul, "Processes images from camera or folder")
        Rel(Bildverarbeitungsmodul, UI, "Displays detected shapes and colors")
        Rel(Bildverarbeitungsmodul, CSVLogger, "Logs data")

        UpdateRelStyle(UI, MainController, $offsetY="-10", $offsetX="-60")
        UpdateRelStyle(MainController, ConfigManager, $offsetY="-35", $offsetX="-80")
        UpdateRelStyle(MainController, InputHandler, $offsetY="0", $offsetX="10")
        UpdateRelStyle(InputHandler, Bildverarbeitungsmodul, $offsetY="0", $offsetX="-200")
        UpdateRelStyle(Bildverarbeitungsmodul, UI, $offsetY="110", $offsetX="-240")
        UpdateRelStyle(Bildverarbeitungsmodul, CSVLogger, $offsetY="-25", $offsetX="-35")

    }

    Person(User, "User", "Interacts with the system")

    System_Ext(Camera, "Camera", "Hardware", "Provides live video stream")
    System_Ext(ImageFolder, "Image Folder", "File System", "Provides images for analysis")
    ContainerDb_Ext(CSV, "CSV", "File", "Logging Data")

    Rel(User, UI, "Interacts via CLI or GUI")
    Rel(Camera, InputHandler, "Provides live video stream")
    Rel(ImageFolder, InputHandler, "Provides images for analysis")
    Rel(CSVLogger, CSV, "loggs detectet objects")

    UpdateRelStyle(User, UI, $offsetY="-150", $offsetX="-50")
    UpdateRelStyle(Camera, InputHandler, $offsetY="-150", $offsetX="-70")
    UpdateRelStyle(ImageFolder, InputHandler, $offsetY="-150", $offsetX="20")
    UpdateRelStyle(CSVLogger, CSV, $offsetY="-270", $offsetX="-340")
:::
