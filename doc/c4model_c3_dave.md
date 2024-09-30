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

    }

    Person(User, "User", "Interacts with the system")

    System_Ext(Camera, "Camera", "Hardware", "Provides live video stream")
    System_Ext(ImageFolder, "Image Folder", "File System", "Provides images for analysis")

    Rel(User, UI, "Interacts via CLI or GUI")
    Rel(Camera, InputHandler, "Provides live video stream")
    Rel(ImageFolder, InputHandler, "Provides images for analysis")
:::
:::mermaid

    flowchart TB
    subgraph opr ["Object Pattern Recognizer Application"]
        UI["User Interface (CLI & GUI with Overlay)"]
        MainController["Main Controller"]
        ConfigManager["Config Manager"]
        InputHandler["Input Handler"]
        Bildverarbeitungsmodul["Image Processing Module"]
        CSVLogger["CSV Logger"]

        UI -->|User interacts via CLI/GUI| MainController
        MainController -->|Loads system configurations| ConfigManager
        MainController -->|Initializes input| InputHandler
        InputHandler -->|Processes images from camera or folder| Bildverarbeitungsmodul
        Bildverarbeitungsmodul -->|Displays detected shapes and colors| UI
        Bildverarbeitungsmodul -->|Logs data| CSVLogger
    end

    User("User") -->|Interacts via CLI or GUI| UI
    Camera("Camera") -.->|Provides live video stream| InputHandler
    ImageFolder("Image Folder") -.->|Provides images for analysis| InputHandler

:::
