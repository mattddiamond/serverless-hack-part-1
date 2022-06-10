import boto3
from trp import Document
import json


#function that returns all items in KV pairs
def get_all(doc):
        kvs = {}
        for page in doc.pages:
            
            for field in page.form.fields:
                print("Key: {}, Value: {}".format(field.key, field.value))
                kvs["Value: {}".format(field.key)] = "Value: {}".format(field.value)
        return kvs

#function that retruns single item
def get_item(key, doc):
    get_kv = {}
    for page in doc.pages:
        print("\nSearch Fields:")
        fields = page.form.searchFieldsByKey(key)
        for field in fields:
            print("Key: {}, Value: {}".format(field.key, field.value))
            print("Social Security Number:", str(field.value).replace(" ", ""))
            get_kv = "Key: {}, Value: {}".format(field.key, field.value)
    return get_kv

def lambda_handler(event, context):  
    #Let's set what file and bucket to store image of license
    s3BucketName = "bling-textract-demo"
    documentName = "washington-drivers-license.jpeg"
    fileLocation = '/tmp/' + documentName
    
    # Amazon Textract client setup
    textract = boto3.client('textract')
    
    #Setup the S3 client and retrieve the file
    s3 = boto3.client('s3')
    s3.download_file(s3BucketName, documentName, fileLocation)
    
   
    
    # Call Amazon Textract
    with open(fileLocation, "rb") as document:
        response = textract.analyze_document(
            Document={
                'Bytes': document.read(),
            },
            FeatureTypes=["FORMS"])
    
    #Create a variable for the document
    doc = Document(response)
    
    all_kvs = get_all(doc)
    single_kvs = get_item('4d', doc)
    print("get specfic item: 4d  ",single_kvs)
    
    return {
        'statusCode': 200,
        'body': json.dumps(all_kvs)
    }
