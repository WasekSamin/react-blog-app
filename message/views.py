import email
from .models import *
from .serializers import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import timedelta


class CommentList(APIView):
    def get(self, request, format=None):
        snippets = Comment.objects.all().order_by("-id")
        serializer = CommentSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        response_msg = {"error": True}

        # print(request.data)
        email = request.data.get("email", None)
        blog_id = request.data.get("blogId", None)
        message = request.data.get("commentText", None)

        if email is not None or blog_id is not None or message is not None:
            try:
                account_obj = Account.objects.get(email=email)
                blog_obj = Blog.objects.get(id=blog_id)
            except:
                response_msg = {"error": True}
            else:
                comment_obj = Comment(
                    user=account_obj,
                    blog=blog_obj,
                    message=message
                )
                comment_obj.save()

                response_msg = {
                    "error": False,
                    "comment_created": True,
                    "comment_obj_id": comment_obj.id,
                    "comment_created_at": comment_obj.created_at - timedelta(hours=8)
                }

        return Response(response_msg)


class CommentDetail(APIView):
    def get_object(self, pk):
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = CommentSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = CommentSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReplyList(APIView):
    def get(self, request, format=None):
        snippets = Reply.objects.all()
        serializer = ReplySerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        response_msg = {"error": True}

        # print(request.data)
        sender = request.data.get("sender", None)
        receiver = request.data.get("receiver", None)
        message = request.data.get("repliedText", None)
        comment_id = request.data.get("commentId", None)

        if sender is not None or receiver is not None or message is not None or comment_id is not None:
            try:
                sender_obj = Account.objects.get(email=sender)
                receiver_obj = Account.objects.get(email=receiver)
                comment_obj = Comment.objects.get(id=comment_id)
            except:
                response_msg = {"error": True}
            else:
                reply_obj = Reply(
                    sender=sender_obj,
                    receiver=receiver_obj,
                    comment=comment_obj,
                    message=message
                )
                reply_obj.save()

                response_msg = {
                    "error": False,
                    "reply_success": True,
                    "reply_obj_id": reply_obj.id,
                    "reply_created_at": reply_obj.created_at - timedelta(hours=8)
                }

        return Response(response_msg)


class ReplyDetail(APIView):
    def get_object(self, pk):
        try:
            return Reply.objects.get(pk=pk)
        except Reply.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = ReplySerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = ReplySerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReactBlogList(APIView):
    def get(self, request, format=None):
        snippets = ReactBlog.objects.all()
        serializer = ReactBlogSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        response_msg = {"error": True}

        # print(request.data)
        email = request.data.get("email", None)
        blog_id = request.data.get("blogId", None)
        like = request.data.get("like", None)
        dislike = request.data.get("dislike", None)

        if email is not None or blog_id is not None or like is not None or dislike is not None:
            try:
                account_obj = Account.objects.get(email=email)
                blog_obj = Blog.objects.get(id=blog_id)
            except:
                response_msg = {"error": True}
            else:
                react_blog_exist = ReactBlog.objects.filter(
                    user=account_obj, blog=blog_obj)
                react_number_on_blog_exist = ReactNumberOnBlog.objects.filter(
                    blog=blog_obj)

                if react_number_on_blog_exist.exists():
                    react_number_on_blog_obj = react_number_on_blog_exist.last()
                else:
                    # Creating ReactNumberOnBlog object
                    react_number_on_blog_obj = ReactNumberOnBlog(
                        blog=blog_obj
                    )
                    react_number_on_blog_obj.save()

                # If user has already reacted on the blog
                if react_blog_exist.exists():
                    react_blog_obj = react_blog_exist.last()
                    # For like
                    if like and not dislike:
                        # If user has already disliked the video, then dislike to like
                        if react_blog_obj.dislike == True and react_blog_obj.like == False:
                            react_blog_obj.like = True
                            react_blog_obj.dislike = False
                            react_blog_obj.save()

                            # Updating like and dislike react number of the blog
                            react_number_on_blog_obj.number_of_likes += 1
                            react_number_on_blog_obj.number_of_dislikes -= 1
                            react_number_on_blog_obj.save()

                            response_msg = {
                                "error": False,
                                "like_success": True,
                                "react_blog_id": react_blog_obj.id,
                                "react_blog_exist": True,
                                "like": True,
                                "dislike": False,
                                "react_number_on_blog_id": react_number_on_blog_obj.id,
                                "total_likes": react_number_on_blog_obj.number_of_likes,
                                "total_dislikes": react_number_on_blog_obj.number_of_dislikes
                            }
                        # If user has already liked the video, then delete the object
                        elif react_blog_obj.like == True and react_blog_obj.dislike == False:
                            react_blog_obj_id = react_blog_obj.id
                            react_blog_obj.delete()

                            # Updating like and dislike react number of the blog
                            react_number_on_blog_obj.number_of_likes -= 1
                            react_number_on_blog_obj.save()

                            response_msg = {
                                "error": False,
                                "delete_like_success": True,
                                "react_blog_id": react_blog_obj_id,
                                "react_blog_exist": True,
                                "dislike": False,
                                "like_delete": True,
                                "react_number_on_blog_id": react_number_on_blog_obj.id,
                                "total_likes": react_number_on_blog_obj.number_of_likes,
                                "total_dislikes": react_number_on_blog_obj.number_of_dislikes
                            }
                    # For dislike
                    elif not like and dislike:
                        # If user has already liked the video, then change like to dislike
                        if react_blog_obj.like == True and react_blog_obj.dislike == False:
                            react_blog_obj.like = False
                            react_blog_obj.dislike = True
                            react_blog_obj.save()

                            # Updating like and dislike react number of the blog
                            react_number_on_blog_obj.number_of_likes -= 1
                            react_number_on_blog_obj.number_of_dislikes += 1
                            react_number_on_blog_obj.save()

                            response_msg = {
                                "error": False,
                                "dislike_success": True,
                                "react_blog_id": react_blog_obj.id,
                                "react_blog_exist": True,
                                "like": False,
                                "dislike": True,
                                "react_number_on_blog_id": react_number_on_blog_obj.id,
                                "total_likes": react_number_on_blog_obj.number_of_likes,
                                "total_dislikes": react_number_on_blog_obj.number_of_dislikes
                            }
                        # If user has already disliked the video, then delete the object
                        elif react_blog_obj.like == False and react_blog_obj.dislike == True:
                            react_blog_obj_id = react_blog_obj.id
                            react_blog_obj.delete()

                            # Updating like and dislike react number of the blog
                            react_number_on_blog_obj.number_of_dislikes -= 1
                            react_number_on_blog_obj.save()

                            response_msg = {
                                "error": False,
                                "delete_dislike_success": True,
                                "react_blog_id": react_blog_obj_id,
                                "react_blog_exist": True,
                                "like": False,
                                "dislike_delete": False,
                                "react_number_on_blog_id": react_number_on_blog_obj.id,
                                "total_likes": react_number_on_blog_obj.number_of_likes,
                                "total_dislikes": react_number_on_blog_obj.number_of_dislikes
                            }
                # If the user has not reacted on the blog yet
                else:
                    # For like
                    if like and not dislike:
                        react_blog_obj = ReactBlog(
                            user=account_obj,
                            blog=blog_obj,
                            like=True,
                            dislike=False
                        )
                        react_blog_obj.save()

                        # Updating like and dislike react number of the blog
                        react_number_on_blog_obj.number_of_likes += 1
                        react_number_on_blog_obj.save()

                        response_msg = {
                            "error": False,
                            "like_success": True,
                            "react_blog_id": react_blog_obj.id,
                            "react_blog_exist": False,
                            "like": True,
                            "dislike": False,
                            "react_number_on_blog_id": react_number_on_blog_obj.id,
                            "total_likes": react_number_on_blog_obj.number_of_likes,
                            "total_dislikes": react_number_on_blog_obj.number_of_dislikes
                        }
                    # For dislike
                    elif not like and dislike:
                        react_blog_obj = ReactBlog(
                            user=account_obj,
                            blog=blog_obj,
                            like=False,
                            dislike=True
                        )
                        react_blog_obj.save()

                        # Updating like and dislike react number of the blog
                        react_number_on_blog_obj.number_of_dislikes += 1
                        react_number_on_blog_obj.save()

                        response_msg = {
                            "error": False,
                            "dislike_success": True,
                            "react_blog_id": react_blog_obj.id,
                            "react_blog_exist": False,
                            "like": False,
                            "dislike": True,
                            "react_number_on_blog_id": react_number_on_blog_obj.id,
                            "total_likes": react_number_on_blog_obj.number_of_likes,
                            "total_dislikes": react_number_on_blog_obj.number_of_dislikes
                        }

        return Response(response_msg)


class ReactBlogDetail(APIView):
    def get_object(self, pk):
        try:
            return ReactBlog.objects.get(pk=pk)
        except ReactBlog.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = ReactBlogSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = ReactBlogSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReactNumberOnBlogList(APIView):
    def get(self, request, format=None):
        snippets = ReactNumberOnBlog.objects.all().order_by("-number_of_likes")
        serializer = ReactNumberOnBlogSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ReactNumberOnBlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReactNumberOnBlogDetail(APIView):
    def get_object(self, pk):
        try:
            return ReactNumberOnBlog.objects.get(pk=pk)
        except ReactNumberOnBlog.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = ReactNumberOnBlogSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = ReactNumberOnBlogSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
