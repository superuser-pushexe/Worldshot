import csv

def read_settings():
    with open('settings.csv', mode='r') as file:
        reader = csv.reader(file)
        first_line = next(reader)
        number = int(first_line[0].strip())
    return number

# Example usage
if __name__ == "__main__":
    number = read_settings()
    if (number) == (""):
        exit()
    else:
        FPS = (number)

