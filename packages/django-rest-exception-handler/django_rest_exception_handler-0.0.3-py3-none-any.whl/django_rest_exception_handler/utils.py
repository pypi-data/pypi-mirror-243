from typing import Any


def fail(error: Any) -> dict:
    return {'status': False, 'message': 'fail', 'errror': error}
