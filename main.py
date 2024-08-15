from game import *
from menu import *

if __name__ == "__main__":
    while True:
        action = main_menu()
        if action == "start_game":
            run_game()
        elif action == "choose_map":
            # Implement map choice logic
            pass
        elif action == "tutorial":
            # Implement tutorial logic
            pass