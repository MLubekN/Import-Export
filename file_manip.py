import os
import csv
import sqlite3
from typing import List


class Car:
    def __init__(self, brand:str, type: str, year: int):
        self.brand = brand
        self.type = type
        self.year = int(year)

    def to_dict(self):
        return {"brand": self.brand, "type": self.type, "year": self.year}
    
    def __repr__(self):
        return f"Car(brand={self.brand}, type={self.type}, year={self.year})"
    
    def __str__(self):
        return f"{self.brand}, {self.type}, {self.year}"

    def __eq__(self, other):
        return self.brand == other.brand and self.type == other.type and self.year == other.year



def export_to_txt(objects: List[Car], filename: str) -> None:
    """Export a list of objects to a text file."""
    with open(filename, 'w') as file:
        for obj in objects:
            file.write(f"{obj.brand},{obj.type},{obj.year}\n")


def export_to_csv(objects: List[Car], filename: str) -> None:
    """Export a list of objects to a csv file."""
    with open(filename, 'w', newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["brand", "type", "year"])
        writer.writeheader()
        for obj in objects:
            writer.writerow(obj.to_dict())


def list_files_in_directory(extension: str = None) -> List[str]:
    """List files in the current directory."""
    files = [f for f in os.listdir() if os.path.isfile(f)]
    if extension:
        files = [f for f in files if f.endswith(extension)]
    return files


def import_from_txt(filename: str) -> List[Car]:
    """Import a list of objects from a text file."""
    with open(filename, "r") as file:
        return [Car(*line.strip().split(",")) for line in file.readlines()]


def import_from_csv(filename: str) -> List[Car]:
    """Import a list of objects from a csv file."""
    with open(filename, "r") as file:
        reader = csv.DictReader(file)
        return [Car(row["brand"], row["type"], int(row["year"])) for row in reader]


def show_obj(objects):
    """Show a list of objects."""
    if objects:
        for n, obj in enumerate(objects, 1):
            print(f"{n}. {obj}")
    else:
        print("No objects in the list. First populate the list.")


def create_database(filename: str):
    """Create a database file."""
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()

    cursor.execute('''
CREATE TABLE IF NOT EXISTS cars (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    brand TEXT NOT NULL,
    type TEXT NOT NULL,
    year INTEGER NOT NULL
)
''')
    connection.commit()
    connection.close()


def add_to_database(filename:str, objects: List[Car]):
    """Add objects to a database."""
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.executemany('''INSERT INTO cars (brand, type, year) VALUES (?, ?, ?)''', [list(obj.to_dict().values()) for obj in objects])
    connection.commit()
    connection.close()


def open_database(filename: str) -> List[Car]:
    """Open a database file."""
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM cars')
    cars_sql = cursor.fetchall()
    connection.close()
    cars = [Car(brand, type, year) for _, brand, type, year in cars_sql]
    return cars


def check_duplicates(objects: List[Car], filename: str) -> List[Car]:
    """Check for duplicates in the given file."""
    existing_cars = []
    if filename.endswith('.txt'):
        existing_cars = import_from_txt(filename)
    elif filename.endswith('.csv'):
        existing_cars = import_from_csv(filename)

    duplicates = []
    for obj in objects:
        if obj in existing_cars:
            duplicates.append(obj)
    return duplicates


def export_menu(objects: List[Car]):
    """Show export interface and make choices"""
    filename = input("Give file name without extension:\n")
    print("\nWhich format to export:")
    print("1. txt")
    print("2. csv")
    print("3. db")
    print("e. Exit")
    choice = input("Choose extension: ").strip().lower()
    extension = ''
    
    if choice == "1":
        extension = '.txt'
        filename += extension
    elif choice == "2":
        extension = '.csv'
        filename += extension
    elif choice == "3":
        extension = '.db'
        filename += extension
    elif choice == "e":
        print("Exiting...")
        return

    #Check for duplicates
    try:
        duplicates = check_duplicates(objects, filename)
        if duplicates:
            print("The following cars already exist in the file:")
            for car in duplicates:
                print(car)
            overwrite_choice = input("Do you want to overwrite existing entries? (y/n): ").strip().lower()
            if overwrite_choice == 'y':
                objects = [obj for obj in objects if obj not in duplicates]
    except FileNotFoundError:
        pass

    if extension == '.txt':
        export_to_txt(objects, filename)
    elif extension == '.csv':
        export_to_csv(objects, filename)
    elif extension == '.db':
        create_database(filename)
        add_to_database(filename, objects)

    print(f"Cars exported to {filename}")


def import_menu(objects: List[Car]):
    """Show import interface and make choices"""
    print("Choose a file to import:")
    for idx, file in enumerate(list_files_in_directory()):
        print(f"{idx + 1}. {file}")

    choice = (int(input("Number of the file: "))) - 1
    chosen_file = list_files_in_directory()[choice]

    if chosen_file.endswith(".txt"):
        imported_cars = import_from_txt(chosen_file)
    elif chosen_file.endswith(".csv"):
        imported_cars = import_from_csv(chosen_file)
    elif chosen_file.endswith(".db"):
        imported_cars = open_database(chosen_file)
    else:
        print("Unsupported file format.")
        imported_cars = []
    
    print("Imported objects: ")
    for object in imported_cars:
        print(f"{object}")
    for object in imported_cars:
        objects.append(object)
    

def add_car(objects: List[Car]):
    """Add a class object"""
    brand = input("Enter car brand: ")
    type = input("Enter car type (diesel, gas, electric): ")
    year = int(input("Enter car year: "))
    object = Car(brand, type, year)
    objects.append(object)
    return objects


def delete_car(objects: List[Car]):
    """Delete a class object"""
    print("List of cars:")
    show_obj(objects)
    if objects:
        index = int(input("Enter the number of the car to delete: ")) - 1
        del objects[index]
        print("Car deleted.")
    return objects


if __name__ == "__main__":
    print("Application to manipulate files")
    objects = []
    while True:
        print("---------------")
        print("Choose what to do:")
        print("1. Export")
        print("2. Import")
        print("3. Add a car")
        print("4. Show list of cars")
        print("5. Delete a car")
        print("e. Exit")
        choice = input("Enter a number: ").strip().lower()

        if choice == "1":
            export_menu(objects)
        elif choice == "2":
            import_menu(objects)
        elif choice == "3":
            objects = add_car(objects)
        elif choice == "4":
            show_obj(objects)
        elif choice == "5":
            objects = delete_car(objects)
        elif choice == "e":
            break
        else:
            print("Wrong input. You can only type in a number or \"e\" for exit.")