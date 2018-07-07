from django.urls import path,re_path
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap
from .feeds import LatestPostsFeed

from .views import post_detail, post_list,post_share

app_name = 'blog'

sitemaps = {
    'posts': PostSitemap
}


urlpatterns = [
    path('',post_list, name='post_list'),
    path('tag/<tag_slug>/', post_list, name='post_list_by_tag'),
    path('<int:pk>',post_detail,name='post_detail'),
    path('<int:pk>/share/', post_share, name='post_share'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
     name='django.contrib.sitemaps.views.sitemap'),
    path('feed/',LatestPostsFeed(), name='post_feed')


]