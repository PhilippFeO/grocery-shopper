import os
import sys
import random
import main
import defaults

# Specify the number of files to choose via command line
# N = int(sys.argv[1])
num_req_recipes = 1

# Check if the directory exists
if os.path.isdir(defaults.recipe_dir):
    # Check if there are files in the directory
    num_files = len(os.listdir(defaults.recipe_dir))
    if num_files == 0:
        print(f"Error: No files found in the directory '{defaults.recipe_dir}'.")
        sys.exit(1)

    # Get a list of files in the directory
    files = [os.path.join(defaults.recipe_dir, f) for f in os.listdir(defaults.recipe_dir)]

    # Check the command-line argument
    # if len(sys.argv) != 2 or 0 > num_req_recipes > num_files:
    #     print(f"Usage: {sys.argv[0]} N")
    #     print(f"\twhere 0 < N <= {num_files} (Number of Recipes)")
    #     sys.exit(1)

    # Check if N is greater than the number of files
    if num_req_recipes > num_files:
        print(f"Error: {num_req_recipes} is greater than the number of files in the directory ({num_files}).")
        sys.exit(1)

    # Generate an array of random indices within the range of the number of files
    indices = random.sample(range(num_files), num_req_recipes)

    # Loop through the randomly chosen indices and get the corresponding files
    selected_recipes = [files[index] for index in indices]

    # Go on
    main.main(selected_recipes)
else:
    print(f"Error: Directory '{defaults.recipe_dir}' not found.")
    sys.exit(1)
