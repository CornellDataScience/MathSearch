import pandas as pd
import os

images_directory = 'formula_images'
formulas_file_path = 'im2latex_formulas.lst'

# Step 3: Function to create a DataFrame from .lst file
def create_dataframe(lst_file_path, formulas_list, images_directory):
    data = []
    with open(lst_file_path, 'r') as file:
        for line in file:
            formula_idx, image_name, _ = line.strip().split()
            formula_idx = int(formula_idx)  # Convert index to integer
            latex = formulas_list[formula_idx]
            image_path = os.path.join(images_directory, image_name + '.png')
            data.append({'latex': latex, 'image_path': image_path})
    return pd.DataFrame(data)

# Load formulas
with open(formulas_file_path, 'r') as file:
    formulas = file.readlines()
formulas_list = [formula.strip() for formula in formulas]  # Remove newline characters

# Create DataFrame
df = create_dataframe(formulas_file_path, formulas_list, images_directory)
print(df.head())

