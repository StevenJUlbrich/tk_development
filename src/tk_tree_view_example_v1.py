import tkinter as tk
from tkinter import ttk
from typing import Any, Union
from pydantic import BaseModel, parse_obj_as
from typing import List
from faker import Faker
import json

class Address(BaseModel):
    street: str
    city: str

class Person(BaseModel):
    name: str
    age: int
    address: Address
    hobbies: List[str]


fake = Faker()

def generate_fake_person() -> Person:
    """Generate a fake Person instance."""
    return Person(
        name=fake.name(),
        age=fake.random_int(min=18, max=80),
        address=Address(
            street=fake.street_address(),
            city=fake.city()
        ),
        hobbies=fake.words(nb=3)
    )

def generate_fake_people(n: int) -> List[Person]:
    """Generate a list of fake Person instances."""
    return [generate_fake_person() for _ in range(n)]

def save_fake_data_to_file(people: List[Person], filename: str):
    """Save a list of Person instances to a JSON file."""
    with open(filename, 'w') as f:
        # Convert the list of Person instances to a list of dictionaries, then save as JSON
        json.dump([person.dict() for person in people], f, indent=4)


# Function to recursively insert items into the treeview
def insert_into_tree(parent, key, value, tree):
    if isinstance(value, BaseModel):
        # For Pydantic models, create a parent node with the model's class name
        node = tree.insert(parent, 'end', text=f"{key}: {value.__class__.__name__}")
        # Recursively insert each field of the model
        for field_key, field_value in value.dict().items():
            insert_into_tree(node, field_key, field_value, tree)
    elif isinstance(value, list):
        # For lists, create a parent node and insert each item
        node = tree.insert(parent, 'end', text=f"{key}: List")
        for i, item in enumerate(value):
            insert_into_tree(node, f"[{i}]", item, tree)
    else:
        # For simple values, insert directly
        tree.insert(parent, 'end', text=f"{key}: {value}")

def load_people_from_json(filename: str) -> List[Person]:
    """Load people data from a JSON file and return a list of Person instances."""
    with open(filename, 'r') as f:
        people_data = json.load(f)
    return parse_obj_as(List[Person], people_data)


def display_people_in_treeview(people: List[Person]):
    """Display a list of Person instances in a treeview configured as a table,
    with hobbies concatenated into a single sub-row."""
    root = tk.Tk()
    root.title("Pydantic Model Viewer")

    # Define columns
    columns = ('name', 'age', 'city', 'hobbies')
    tree = ttk.Treeview(root, columns=columns, show="headings")
    tree.pack(expand=True, fill='both')

    # Define column headings
    tree.heading('name', text='Name')
    tree.heading('age', text='Age')
    tree.heading('city', text='City')
    tree.heading('hobbies', text='Hobbies')

    # Adjust the column widths and alignment
    tree.column('name', anchor='w', width=120)
    tree.column('age', anchor='center', width=50)
    tree.column('city', anchor='w', width=100)
    tree.column('hobbies', anchor='w', width=300)

    # Insert person data
    for person in people:
        # Concatenate hobbies into a single string
        hobbies_str = ", ".join(person.hobbies)
        # Insert the person as a parent item
        person_id = tree.insert('', 'end', values=(person.name, person.age, person.address.city))
        # Insert hobbies as a single child item
        tree.insert(person_id, 'end', values=('', '', 'Hobbies:', hobbies_str))

    root.mainloop()


def main():
    # Generate fake data for 10 people
    fake_people = generate_fake_people(10)

    # Save the fake data to a file
    save_fake_data_to_file(fake_people, 'fake_people_data.json')


    # Load people from the JSON file
    people = load_people_from_json('fake_people_data.json')

    # Display the loaded people in the treeview
    display_people_in_treeview(people)


if __name__ == "__main__":
    main()