from typing import List, Optional
from pydantic import BaseModel, Field
from faker import Faker

fake = Faker()

class ExclusionType(BaseModel):
    category_exclusion_Type_ID: int = Field(default=0, ge=0)
    category_type_id: int = Field(default=0,ge=0)
    excluded_category_type_id: int = Field(default=0, ge=0)
    excluded_category_type_name: str

class CategoryType(BaseModel):
    category_type_id: int = Field(default=None, ge=0)
    category_type: str
    app_seal_id: int
    skip_days: int = 0
    max_instance_datacenter: int = 0
    monday: int = 0
    tuesday: int = 0
    wednesday: int = 0
    thursday: int = 0
    friday: int = 0
    saturday: int = 0
    sunday: int = 0
    exclusions: Optional[List[ExclusionType]] = []

def create_fake_exclusion(category_type_id: int) -> ExclusionType:
    return ExclusionType(
        category_exclusion_Type_ID=fake.random_int(min=1, max=1000),
        category_type_id=category_type_id,
        excluded_category_type_id=fake.random_int(min=1, max=1000),
        excluded_category_type_name=fake.company()
    )

def create_fake_category_type(category_type_id: int) -> CategoryType:
    exclusions = [create_fake_exclusion(category_type_id) for _ in range(fake.random_int(min=0, max=5))]
    return CategoryType(
        category_type_id=category_type_id,
        category_type=fake.job(),
        app_seal_id=fake.random_int(min=1, max=100),
        skip_days=fake.random_int(min=0, max=7),
        max_instance_datacenter=fake.random_int(min=1, max=10),
        monday=fake.random_int(min=0, max=1),
        tuesday=fake.random_int(min=0, max=1),
        wednesday=fake.random_int(min=0, max=1),
        thursday=fake.random_int(min=0, max=1),
        friday=fake.random_int(min=0, max=1),
        saturday=fake.random_int(min=0, max=1),
        sunday=fake.random_int(min=0, max=1),
        exclusions=exclusions
    )

import tkinter as tk
from tkinter import ttk

def display_data_in_treeview(categories: List[CategoryType]):
    root = tk.Tk()
    root.title("Categories and Exclusions Viewer")

    tree = ttk.Treeview(root, columns=("ID", "Type"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Type", text="Type")
    tree.pack(expand=True, fill='both')

    for category in categories:
        cat_id = tree.insert('', 'end', values=(category.category_type_id, category.category_type), open=True)
        for exclusion in category.exclusions:
            tree.insert(cat_id, 'end', values=(exclusion.excluded_category_type_id, exclusion.excluded_category_type_name))

    root.mainloop()


fake_categories = [create_fake_category_type(i) for i in range(1, 11)]  # Generate 10 fake CategoryTypes
display_data_in_treeview(fake_categories)



