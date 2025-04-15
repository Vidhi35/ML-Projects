import json
import os

# Configuration
NOTEBOOK_FILE = "Customer_review_summarizer.ipynb"  # CHANGE THIS TO YOUR ACTUAL FILENAME

def clean_notebook():
    # Verify file exists
    if not os.path.exists(NOTEBOOK_FILE):
        print(f"Error: File '{NOTEBOOK_FILE}' not found!")
        print("Please make sure:")
        print(f"1. The file '{NOTEBOOK_FILE}' exists in this folder")
        print("2. You've replaced 'your_notebook.ipynb' with your actual filename")
        return

    # Load notebook
    try:
        with open(NOTEBOOK_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"Successfully loaded '{NOTEBOOK_FILE}'")
    except Exception as e:
        print(f"Failed to load '{NOTEBOOK_FILE}': {str(e)}")
        return

    # Check and clean metadata
    if "metadata" in data:
        if "widgets" in data["metadata"]:
            print("Found 'widgets' in metadata - removing...")
            del data["metadata"]["widgets"]
            print("Successfully removed widgets metadata")
        else:
            print("No 'widgets' found in metadata (nothing to remove)")
    else:
        print("No 'metadata' section found in notebook")

    # Save changes
    try:
        with open(NOTEBOOK_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Successfully saved cleaned version of '{NOTEBOOK_FILE}'")
    except Exception as e:
        print(f"Failed to save changes: {str(e)}")

if __name__ == "__main__":
    print("\n=== Notebook Cleaning Tool ===")
    clean_notebook()
    print("="*30)