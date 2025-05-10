import logging
from src.gui.app_placer import AppPlacerGUI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    """Main entry point for the application."""
    app = AppPlacerGUI()
    app.run()

if __name__ == "__main__":
    main()