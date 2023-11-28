# Django REST Framework Exception Handler

The Django REST Framework Exception Handler is a Python package designed to streamline exception handling within Django REST Framework applications. It ensures a consistent format for error responses by structuring them in a predefined JSON format.
Installation

You can install the package via pip:

```bash
pip install your-package-name
```

## Usage

Installation: After installation, include the package in your Django REST Framework settings in `settings.py`.

```python

REST_FRAMEWORK = {
    # Other settings...
    'EXCEPTION_HANDLER': 'django_rest_exception_handler.exception_handlers.exception_handler'
}
```

Response Format: The package handles exceptions and formats the response in the following structure:

```json
{
    "status": false,
    "message": "fail",
    "error": "specific error message here"
}
```

With using this package you could raise an excetion anywhere inside your application. Exceptions other than the APIException class will be raised as 500 Internal server error exception by the exception handler.

Example:
Here the exception handler will raise a 400 exception if the data passed by the request to the serializer is invalid.

```python
# Your Django view code

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from .serializers import YourSerializer

class YourView(APIView):
    def post(self, request: Request) -> Response:
        serializer = YourSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
```

Contributing

We welcome contributions! Feel free to open issues or submit pull requests.
License

This project is licensed under the MIT License - see the LICENSE file for details.