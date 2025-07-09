import boto3

# Create S3 client
s3 = boto3.client("s3")

# Upload file
s3.upload_file("news.json", "newsapi-raw-data", "news.json")

print("✅ Upload successful!")
