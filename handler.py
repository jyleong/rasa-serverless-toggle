import json
import boto3

lambda_client = boto3.client('lambda', region_name="us-west-2")

def isPostRequest(event):
    return str(event['requestContext']['httpMethod']) == "POST"

def isGetRequest(event):
    return str(event['requestContext']['httpMethod']) == "GET"


def unwrapEvent(event):
    wrappedPayload = json.loads(event['body'])
    return wrappedPayload['toggle'].lower()

def postInstance(toggle):
    event = {'toggle': toggle}
    if toggle == "on" or toggle == "off":
        try:
            response = lambda_client.invoke(
                FunctionName='ec2-rasa-start',
                InvocationType="RequestResponse",
                Payload=json.dumps(event)
            )

            string_response = response["Payload"].read().decode('utf-8')
            parsed_response = json.loads(string_response)
            print('postInstance() parsed_response:', parsed_response)
            return { "statusCode": 200, "body": json.dumps(parsed_response) }
        except Exception as e:
            print("invokeLamba error: ", e)
            parsed_response = {
                "statusCode": 400,
                "InvokeLambaError": json.dumps(e)
            }
        return parsed_response
    else:
        return {"statusCode": 422, "Error": "toggle should be ON or OFF"}

def getStatus():
    try:
        response = lambda_client.invoke(
            FunctionName='ec2-rasa-status',
            InvocationType="RequestResponse"
        )
        string_response = response["Payload"].read().decode('utf-8')
        parsed_response = json.loads(string_response)
        print('getStatus() parsed_response:', parsed_response)
        return {"statusCode": 200, "body": json.dumps(parsed_response)}
    except Exception as e:
        print("invokeLamba error: ", e)
        parsed_response = {
            "statusCode": 400,
            "InvokeLambaError": json.dumps(e)
        }
    return parsed_response

def endpoint(event, context):
    if not isPostRequest(event):
        return { "statusCode": 422, "body": "Request should be POST"}

    toggle = unwrapEvent(event) # "ON"/"OFF"
    response = postInstance(toggle)
    return response

def status(event, context):
    if not isGetRequest(event):
        return {"statusCode": 422, "body": "Request should be GET"}
    response = getStatus()
    return response