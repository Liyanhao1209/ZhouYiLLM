def hello_world():
    return {'message': 'hello world'}


async def specific_id(username: int):
    return {'message': f'hello world {username}'}
