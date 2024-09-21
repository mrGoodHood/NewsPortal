from django.urls import path
from .views import (
    NewsList,
    NewsDetail,
    NewsCreate, NewsUpdate, NewsDelete,
    ArticleCreate, ArticleUpdate, ArticleDelete,
    news_search,
    become_author, user_profile, subscribe_to_category
)

urlpatterns = [
    path('', NewsList.as_view(), name='news'),
    path('search/', news_search, name='news_search'),
    path('<int:pk>/', NewsDetail.as_view()),
    # Новости: Создание, обновление, удаление
    path('create/', NewsCreate.as_view(), name='news_create'),
    path('<int:pk>/edit/', NewsUpdate.as_view(), name='news_edit'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    # Статьи: Создание, обновление, удаление
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', ArticleUpdate.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
    # Аккаунт
    path('profile/', user_profile, name='user_profile'),
    path('become_author/', become_author, name ='become_author'),
    path('category/<int:category_id>/subscribe/', subscribe_to_category, name='subscribe_to_category'),
]
