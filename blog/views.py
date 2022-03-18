from .models import *
from .serializers import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import timedelta
from django.conf import settings


class CategoryList(APIView):
    def get(self, request, format=None):
        snippets = Category.objects.all().order_by("-id")
        serializer = CategorySerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetail(APIView):
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = CategorySerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = CategorySerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagList(APIView):
    def get(self, request, format=None):
        snippets = Tag.objects.all().order_by("-id")
        serializer = TagSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TagDetail(APIView):
    def get_object(self, pk):
        try:
            return Tag.objects.get(pk=pk)
        except Tag.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = TagSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = TagSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BlogList(APIView):
    def get(self, request, format=None):
        snippets = Blog.objects.all().order_by("-id")
        serializer = BlogSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        response_msg = {"error": True}

        # print(request.data)
        email = request.data.get("email", None)
        title = request.data.get("title", None)
        main_image = request.data.get("mainImage", None)
        post_text = request.data.get("postText", None)
        category = request.data.get("category", None)
        tags = request.data.get("tag", None)

        if email is not None or title is not None or post_text is not None or category is not None:
            try:
                account_obj = Account.objects.get(email=email)
                category_obj = Category.objects.get(id=int(category))
            except:
                response_msg = {"error": True, "invalid_request": True}
            else:
                # Getting all the tags
                tagList = None
                if len(tags) > 0:
                    tagList = tags.split(",")

                # Creating blog object
                blog_obj = Blog(
                    user=account_obj,
                    title=title,
                    main_image=main_image,
                    category=category_obj,
                    post_text=post_text
                )

                blog_obj.save()

                # print(settings.NUDE_DETECTED)

                # If nude is detected in the main image, then delete the blog object
                if settings.NUDE_DETECTED:
                    blog_obj.delete()

                    response_msg = {
                        "error": True,
                        "nude_detected": True,
                    }

                    # Resetting NUDE_DETECTED value
                    settings.NUDE_DETECTED = False
                else:   # --> If the main image is clean, no nude detected
                    # Appending tags to the blog object
                    if tagList is not None:
                        for item in tagList:
                            blog_obj.tag.add(int(item))

                    response_msg = {
                        "error": False,
                        "blog_created": True,
                        "blog_id": blog_obj.id,
                        "blog_created_at": blog_obj.created_at - timedelta(hours=8),
                    }

        return Response(response_msg)


class BlogDetail(APIView):
    def get_object(self, pk):
        try:
            return Blog.objects.get(pk=pk)
        except Blog.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = BlogSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        response_msg = {"error": True}

        # print(request.data)
        email = request.data.get("email", None)
        title = request.data.get("title", None)
        category = request.data.get("category", None)
        tags = request.data.get("tag", None)
        post_text = request.data.get("postText", None)
        main_image = request.data.get("mainImage", None)

        # print(main_image)
        # print(type(main_image))

        try:
            blog_obj = Blog.objects.get(id=pk)
            account_obj = Account.objects.get(email=email)
            category_obj = Category.objects.get(id=int(category))
        except:
            response_msg = {"error": True, "invalid_request": True}
        else:
            prev_img = blog_obj.main_image
            # Getting all the tags
            tagList = None
            if len(tags) > 0:
                tagList = tags.split(",")

            blog_obj.title = title
            blog_obj.category = category_obj
            blog_obj.post_text = post_text

            if  main_image == "null":
                blog_obj.main_image = None
            elif main_image is not None:
                blog_obj.main_image = main_image

            # Appending tags to the blog object
            if tagList is not None:
                blog_obj.tag.set([])
                for item in tagList:
                    blog_obj.tag.add(int(item))
            else:
                blog_obj.tag.set([])

            blog_obj.save()

            if settings.NUDE_DETECTED:
                blog_obj.main_image = prev_img
                blog_obj.save()

                settings.NUDE_DETECTED = False

                response_msg = {
                    "error": True,
                    "blog_id": blog_obj.id,
                    "nude_detected": True,
                }
            else:
                response_msg = {
                    "error": False,
                    "blog_updated": True,
                    "blog_id": blog_obj.id,
                    "blog_created_at": blog_obj.created_at - timedelta(hours=8)
                }

        return Response(response_msg)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
