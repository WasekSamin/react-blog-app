from .models import *
from .serializers import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

# Create your views here.
class SubscribeList(APIView):
    def get(self, request, format=None):
        snippets = Subscribe.objects.all().order_by("-id")
        serializer = SubscribeSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        response_msg = {"error": True}

        # print(request.data)
        email = request.data.get("email", None)

        if email is not None:
            email_exist = Subscribe.objects.filter(email=email)

            if email_exist.exists():
                response_msg = {"error": True, "already_subscribed": True}
            else:
                subscribe_obj = Subscribe(
                    email=email
                )
                subscribe_obj.save()

                subject, from_email, to = "Subscribe to Samin's React Blog", settings.EMAIL_HOST_USER, email
                text_content = "Thank you for subscribing to Samin's React Blog! Have a great day, Sir."
                html_content = "<p>Thank you for subscribing to <strong>Samin's React Blog</strong>! Have a great day, Sir.</p>"
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()

                response_msg = {
                    "error": False,
                    "subscribed": True,
                }

        return Response(response_msg)


class SubscribeDetail(APIView):
    def get_object(self, pk):
        try:
            return Subscribe.objects.get(pk=pk)
        except Subscribe.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SubscribeSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SubscribeSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)