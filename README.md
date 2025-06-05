# Barcode Product Labeler

This Python application stores product information in a local text file. It accepts a barcode, looks up the product, and if it exists generates a PDF suitable for printing on a Dymo shipping label. If the barcode is not yet in the file, the application prompts for product details which are then stored locally.

## Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   python -m app.main
   ```
3. Scan or enter a barcode when prompted.

A PDF file (`label_<barcode>.pdf`) will be created if the product exists. You can print this PDF using your Dymo printer.
