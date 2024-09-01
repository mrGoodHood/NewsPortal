from django.urls import path
from .views import (
    NewsList,
    NewsDetail,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    add_comment,
)

urlpatterns = [
    path('', NewsList.as_view()),
    path('<int:id>/', NewsDetail.as_view()),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post-edit'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/comment/', add_comment, name='add-comment'),
]
