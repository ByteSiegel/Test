# Barcode Product Labeler

This Python application uses an Azure Table backend to store product information. It accepts a barcode, looks up the product, and if it exists generates a PDF suitable for printing on a Dymo shipping label. If the barcode is not yet in the database, the application prompts for product details which are then stored in Azure.

## Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set the environment variable `AZURE_TABLE_CONNECTION_STRING` to your Azure Table Storage connection string.
3. Run the application:
   ```bash
   python -m app.main
   ```
4. Scan or enter a barcode when prompted.

A PDF file (`label_<barcode>.pdf`) will be created if the product exists. You can print this PDF using your Dymo printer.
