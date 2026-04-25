import os
import shutil

class HeadLibrarian:
    def __init__(self):
        self.stacks = os.path.expanduser("~/the-library/stacks")
        self.lab = os.path.expanduser("~/the-library/conservation-lab")
        os.makedirs(self.stacks, exist_ok=True)
        os.makedirs(self.lab, exist_ok=True)

    def conserve(self, file_path):
        """The Physician Role: Repairing the file."""
        print(f"🧪 CONSERVATION: Rehydrating parchment at {os.path.basename(file_path)}...")
        prefixes = "@prefix skos: <http://www.w3.org/2004/02/skos/core#> .\n@prefix padi: <https://padi.standard/v2.1/> .\n"
        with open(file_path, 'r') as f:
            content = f.read()
        with open(file_path, 'w') as f:
            f.write(prefixes + content)
        return True

    def catalog(self, file_path):
        """The Cataloguer Role: Determining the shelf."""
        with open(file_path, 'r') as f:
            content = f.read()
        
        if "Vessel" in content: return "vessels"
        if "Bond" in content: return "maritime-finance"
        return "general-collection"

    def manage_collection(self, item_path):
        """The Head Librarian's Mandate."""
        item_path = os.path.abspath(os.path.expanduser(item_path))
        print(f"🏛️  HEAD LIBRARIAN: Auditing {os.path.basename(item_path)}...")

        # 1. Check if the 'book' is damaged (Missing prefixes)
        with open(item_path, 'r') as f:
            if "@prefix" not in f.read():
                print("⚠️  MANDATE: Item damaged. Sending to Conservation Lab.")
                # Move to Lab
                temp_lab_path = os.path.join(self.lab, os.path.basename(item_path))
                shutil.move(item_path, temp_lab_path)
                self.conserve(temp_lab_path)
                item_path = temp_lab_path

        # 2. Determine the correct Stack
        shelf = self.catalog(item_path)
        dest_shelf = os.path.join(self.stacks, shelf)
        os.makedirs(dest_shelf, exist_ok=True)

        # 3. Final Shelving
        shutil.move(item_path, os.path.join(dest_shelf, os.path.basename(item_path)))
        print(f"✅ MANDATE COMPLETE: Item shelved in [{shelf.upper()}].")

if __name__ == "__main__":
    import sys
    librarian = HeadLibrarian()
    if len(sys.argv) > 1:
        librarian.manage_collection(sys.argv[1])
