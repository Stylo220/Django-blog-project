
from .permissions import *
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from .serializer import *

# Create your views here.

class PostListView(ListAPIView):
    queryset = Post.man_published.all()
    serializer_class = PostSerializer
    permission_classes = [PostListDetailPermission]

class PostDetailView(RetrieveAPIView):
    queryset = Post.man_published.all()
    serializer_class = PostDetailSerializer
    permission_classes = [PostListDetailPermission]


class UserEditView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [UserEditPermission]
    serializer_class = EditUserSerializer

class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [UserListPermission]

class TicketView(CreateAPIView):
    serializer_class = TicketSerializer
    permission_classes = [TicketPermission]