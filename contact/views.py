from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from .serializers import ContactSerializer
from .services import create_contact_message


class ContactCreateAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = ContactSerializer(data=request.data)

        if not serializer.is_valid():

            return Response(
                {
                    "success": False,
                    "message": "Please correct the errors.",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:

            contact = create_contact_message(
                serializer.validated_data
            )

            return Response(
                {
                    "success": True,
                    "message": "Your message has been sent successfully.",
                    "data": contact,
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception:
            return Response(
                {
                    "success": False,
                    "message": "Something went wrong while sending your message.",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )