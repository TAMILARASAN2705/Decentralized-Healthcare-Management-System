"""
Main Entry Point for Healthcare Management System (Python Backend)
"""

from ui import UserInterface


def main():
    """Main function to start the healthcare management system"""
    print("=== Decentralized Healthcare Management System ===")
    print("Python Backend - Version 2.0.0")
    print("Initializing system...")
    
    # Start the user interface
    ui = UserInterface()
    ui.start()


if __name__ == "__main__":
    main()
