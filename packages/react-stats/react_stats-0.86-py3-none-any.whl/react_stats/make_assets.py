

import os
import json
import sys
import pkg_resources
import logging



def setup_logging():
    logging.basicConfig(level=logging.INFO, 
                        format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    setup_logging()
    
    current_dir = os.getcwd()
    logging.info(f"Current directory: {current_dir}")
    
    print("\n\nEnsure that you are in the root directory.")
    print(f"\ncurrently in: {current_dir}.")
    proceed = input(f"Do you want to proceed? (yes/no): ")
    
    if proceed.lower() != "yes":
        logging.info("User chose not to proceed.")
        sys.exit("")
    else:
        logging.info("User chose to proceed. Making structure.")
        make_structure(current_dir)
    
def make_structure(path):
    try: 
        os.makedirs(os.path.join(path, "assets"))
        logging.info("Created assets directory.")

        resource_package = __name__
        resource_path = 'assets.json'
        assets_path = pkg_resources.resource_filename(resource_package, resource_path)
        
        with open(assets_path, "r") as file:
            file_types = json.load(file)["extension_to_folder"]
            dir_set = set(file_types.values())

            for dir in dir_set:
                os.makedirs(os.path.join(path, "assets", dir))
                logging.info(f"Created {dir} in assets.")
            
    except FileExistsError:
        logging.error("Creation not possible. Assets dir already exists.")
        sys.exit("Creation not possible. Assets dir already exists.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        sys.exit(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
