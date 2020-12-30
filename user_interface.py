def prompt_submarine_location(submarine_length: int):
    print(f"Setting location for submarine of size {submarine_length} cells.")
    alignment = input("Choose alignment Vertical/Horizontal: ")
    axis_value = input("Choose axis value (if you chose vertical alignment this represents the column.): ")
    start_point = input("Choose start point: ")
    end_point = input("Choose end point: ")
    return alignment, axis_value, start_point, end_point


def prompt_invalid_location():
    print("Invalid submarine location. Please try again.")


def prompt_is_host():
    is_host = input("Do you want to be the host y/n: ")
    while is_host != "y" or is_host != "n":
        print("Invalid answer. Please try again.")
        is_host = input("Do you want to be the host y/n: ")
    return is_host == "y"


def prompt_opponent_ip():
    opponent_ip = input("Enter opponent's IP address: ")
    return opponent_ip


def prompt_guess():
    x_coordinate = input("Enter X coordinate for guess: ")
    y_coordinate = input("Enter Y coordinate for guess: ")
    return x_coordinate, y_coordinate


def prompt_connection_closed():
    print("Connection with opponent was closed. If you wish to play another game re-run the program.")


def prompt_defeat():
    print("You Lose! :(")


def prompt_victory():
    print("You Win! :)")
