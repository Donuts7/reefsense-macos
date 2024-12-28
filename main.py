"""Main entry point for the Coral Analysis Tool."""
import sys
import os

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from PyQt6.QtWidgets import QApplication
from src.gui.main_window import MainWindow

def main():
    """Initialize and run the application."""
    print("Starting application...")
    
    # Create the application
    app = QApplication(sys.argv)
    #print("Application created.")
    
    # Create the main window
    window = MainWindow()
    print("Main window created.")
    
    # Show the window
    window.show()
    #print("Main window shown.")
    
    # Run the event loop
    exit_code = app.exec()
    print(f"Application exited with code {exit_code}.")
    
    sys.exit(exit_code)

if __name__ == "__main__":
    main()