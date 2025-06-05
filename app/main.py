import os
from dataclasses import dataclass
from typing import Optional

# from azure.data.tables import TableServiceClient
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from barcode import Code128
from barcode.writer import ImageWriter

@dataclass
class Product:
    barcode: str
    name: str
    description: str
    price: float

# class AzureTableBackend:
#     def __init__(self):
#         conn_str = os.getenv("AZURE_TABLE_CONNECTION_STRING")
#         if not conn_str:
#             raise EnvironmentError("AZURE_TABLE_CONNECTION_STRING not set")
#         service = TableServiceClient.from_connection_string(conn_str)
#         self.table = service.get_table_client("products")
#         try:
#             self.table.create_table()
#         except Exception:
#             pass  # table may already exist

#     def get_product(self, barcode: str) -> Optional[Product]:
#         try:
#             entity = self.table.get_entity(partition_key="PRODUCT", row_key=barcode)
#             return Product(
#                 barcode=barcode,
#                 name=entity.get("name"),
#                 description=entity.get("description"),
#                 price=float(entity.get("price")),
#             )
#         except Exception:
#             return None

#     def upsert_product(self, product: Product) -> None:
#         entity = {
#             "PartitionKey": "PRODUCT",
#             "RowKey": product.barcode,
#             "name": product.name,
#             "description": product.description,
#             "price": str(product.price),
#         }
#         self.table.upsert_entity(entity)


class FileBackend:
    """Simple backend that stores products in a local text file."""

    def __init__(self, filename: str = "products.txt"):
        self.filename = filename
        if not os.path.exists(self.filename):
            open(self.filename, "w").close()

    def _read_all(self):
        products = []
        with open(self.filename, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                barcode, name, description, price = line.split("|")
                products.append(
                    Product(
                        barcode=barcode,
                        name=name,
                        description=description,
                        price=float(price),
                    )
                )
        return products

    def get_product(self, barcode: str) -> Optional[Product]:
        for product in self._read_all():
            if product.barcode == barcode:
                return product
        return None

    def upsert_product(self, product: Product) -> None:
        products = self._read_all()
        for i, existing in enumerate(products):
            if existing.barcode == product.barcode:
                products[i] = product
                break
        else:
            products.append(product)
        with open(self.filename, "w") as f:
            for p in products:
                f.write(
                    f"{p.barcode}|{p.name}|{p.description}|{p.price}\n"
                )


def prompt_product_info(barcode: str) -> Product:
    name = input("Product name: ")
    description = input("Description: ")
    price = float(input("Price: "))
    return Product(barcode=barcode, name=name, description=description, price=price)


def generate_label_pdf(product: Product, output_path: str) -> None:
    code = Code128(product.barcode, writer=ImageWriter())
    barcode_filename = code.save("barcode")

    c = canvas.Canvas(output_path, pagesize=letter)
    c.setFont("Helvetica", 12)
    c.drawString(100, 700, f"Product: {product.name}")
    c.drawString(100, 680, f"Description: {product.description}")
    c.drawString(100, 660, f"Price: ${product.price:.2f}")
    c.drawImage(barcode_filename + ".png", 100, 500, width=200, height=50)
    c.showPage()
    c.save()

    os.remove(barcode_filename + ".png")


def main():
    # backend = AzureTableBackend()
    backend = FileBackend()
    barcode = input("Scan barcode: ")
    product = backend.get_product(barcode)
    if product is None:
        print("Barcode not found. Please enter product information.")
        product = prompt_product_info(barcode)
        backend.upsert_product(product)
        print("Product saved to text file.")
    else:
        print("Product found. Generating label PDF...")
        output_pdf = f"label_{barcode}.pdf"
        generate_label_pdf(product, output_pdf)
        print(f"Label PDF saved to {output_pdf}.")

if __name__ == "__main__":
    main()
