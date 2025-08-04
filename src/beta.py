import os      # To interact with the operating system, e.g., file paths and directory listing
import json    # To create and write JSON formatted files

def build_metadata(root_dir='AI_IMG_GPT'):
    # Define the folder paths inside the root dataset directory
    image_dir = os.path.join(root_dir, 'images')           # Path to images folder
    prompt_dir = os.path.join(root_dir, 'prompts')         # Path to original prompts folder
    recon_prompt_dir = os.path.join(root_dir, 'recon_prompts')  # Path to reconstructed prompts folder

    # Define output file path for the metadata JSON
    output_file = os.path.join(root_dir, 'metadata.json')

    dataset = []  # Initialize an empty list to hold metadata entries

    # Loop over all files in the images folder, sorted alphabetically
    for fname in sorted(os.listdir(image_dir)):
        # Only process files that are image types
        if not fname.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            continue  # Skip non-image files

        base = os.path.splitext(fname)[0]  # Extract the filename without extension (e.g., 'img0001')
        image_path = os.path.join('images', fname)  # Relative path to the image file

        # Construct expected file paths for the matching prompt files
        prompt_path = os.path.join(prompt_dir, f'{base}_prompt.txt')             # Original prompt file
        recon_path = os.path.join(recon_prompt_dir, f'{base}_reconstructed.txt')  # Reconstructed prompt file

        # Check that both prompt files exist before continuing
        if not (os.path.exists(prompt_path) and os.path.exists(recon_path)):
            print(f"Warning: Missing prompt files for {base}, skipping.")  # Warn user
            continue  # Skip this entry if prompt files are missing

        # Open and read the original prompt file (UTF-8 encoded)
        with open(prompt_path, 'r', encoding='utf-8') as f:
            prompt = f.read().strip()  # Read and strip whitespace/newlines

        # Open and read the reconstructed prompt file (UTF-8 encoded)
        with open(recon_path, 'r', encoding='utf-8') as f:
            recon_prompt = f.read().strip()  # Read and strip whitespace/newlines

        # Add a dictionary entry to the dataset list
        dataset.append({
            "id": base,                       # Unique identifier (filename without extension)
            "image_path": image_path,         # Relative path to image file
            "original_prompt": prompt,        # Text of the original prompt
            "reconstructed_prompt": recon_prompt  # Text of the reconstructed prompt
        })

    # After processing all images, write the full dataset list to a JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        # Pretty-print JSON with indent and preserve unicode characters
        json.dump(dataset, f, indent=2, ensure_ascii=False)

    # Inform the user how many entries were saved and where
    print(f"Metadata for {len(dataset)} items saved to {output_file}")

# This ensures that if the script is run directly (not imported), it calls build_metadata()
if __name__ == '__main__':
    build_metadata()
