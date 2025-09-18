import google.generativeai as genai
import PIL.Image
import json
import pandas as pd
import os
from google.colab import userdata

# Load your API key from Colab secrets
GOOGLE_API_KEY = userdata.get('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash-latest')

# This is the directory where you uploaded your receipts in Colab
receipts_dir = '/content/receipts'

# The prompt to send to the Gemini API
prompt = """
Analyze this receipt image. Extract the following information and return it as a JSON object:
- **business_name**: The name of the business.
- **date**: The date of the transaction.
- **total**: The grand total of the transaction.
- **items**: An array of objects, where each object has:
  - **name**: The name of the item.
  - **price**: The price of the item.
  - **quantity**: The quantity of the item.

If any information is not found, use a null value. If the list of items is empty, use an empty array `[]`. Do not include any other text, just the JSON.
"""

# A list to store the parsed data for all receipts
all_receipt_data = []

# Loop through all files in the directory
for filename in os.listdir(receipts_dir):
    if filename.endswith(('.jpg', '.jpeg', '.png')): # Process only image files
        image_path = os.path.join(receipts_dir, filename)

        try:
            img = PIL.Image.open(image_path)
            print(f"Processing {filename}...")

            # Send the image and prompt to the Gemini API
            response = model.generate_content([prompt, img])

            # Clean and parse the JSON output
            json_text = response.text.strip().lstrip('`').rstrip('`').lstrip('json').strip()

            try:
                data = json.loads(json_text)
                # Add the filename to the data for tracking
                data['filename'] = filename
                all_receipt_data.append(data)
                print(f"Successfully parsed {filename}.")
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON from {filename}: {e}")
                print(f"Raw response text: {json_text}")

        except Exception as e:
            print(f"An error occurred while processing {filename}: {e}")

# Flatten the nested 'items' data to prepare for a spreadsheet
flattened_data = []
for receipt in all_receipt_data:
    receipt_items = receipt.get('items', [])
    if receipt_items:
        for item in receipt_items:
            flattened_data.append({
                'filename': receipt.get('filename'),
                'business_name': receipt.get('business_name'),
                'date': receipt.get('date'),
                'total': receipt.get('total'),
                'item_name': item.get('name'),
                'item_price': item.get('price'),
                'item_quantity': item.get('quantity'),
            })
    else:
        # Handle receipts with no detected items
        flattened_data.append({
            'filename': receipt.get('filename'),
            'business_name': receipt.get('business_name'),
            'date': receipt.get('date'),
            'total': receipt.get('total'),
            'item_name': None,
            'item_price': None,
            'item_quantity': None,
        })


# Convert the flattened list of dictionaries to a Pandas DataFrame
df = pd.DataFrame(flattened_data)

# Export the DataFrame to a CSV file
output_csv_path = 'receipt_analysis.csv'
df.to_csv(output_csv_path, index=False)

print(f"\nAnalysis complete! Data exported to {output_csv_path}.")
