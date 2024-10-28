import pyqrcode
from PIL import Image
import io
import boto3

def generate_qr_code(data, filename):
    qr = pyqrcode.create(data)
    buffer = io.BytesIO()
    qr.png(buffer, scale=6)
    buffer.seek(0)
    with open(filename, "wb") as f:
        f.write(buffer.getvalue())
    return buffer

def upload_to_s3(buffer, bucket_name, s3_filename):
    s3 = boto3.client('s3')
    s3.upload_fileobj(buffer, bucket_name, s3_filename, ExtraArgs={'ContentType': 'image/png'})
    print(f"File uploaded to {bucket_name}/{s3_filename}")

def main():
    data = input("Enter the text or link for the QR code: ")
    filename = input("Enter the local filename to save the QR code (e.g., 'input_qr.png'): ")
    bucket_name = "teamcoffeeproject"
    s3_filename = input("Enter the S3 filename for the QR code (e.g., 'input_qr.png'): ")
    
    buffer = generate_qr_code(data, filename)
    upload_to_s3(buffer, bucket_name, s3_filename)

if __name__ == "__main__":
    main()