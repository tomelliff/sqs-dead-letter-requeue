import requeue

def handler(event, context):
    requeue.requeue_all_messages()

    response = {
        "statusCode": 200
    }

    return response
