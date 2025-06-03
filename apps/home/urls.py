from django.urls import path

from apps.home.views.blog import BlogListView, BlogCategoryListView, BlogDetailView
from apps.home.views.contactus import ContactUsView
from apps.home.views.faq import FAQList, FAQDetail
from apps.home.views.info import PedagogInfoListView
from apps.home.views.news import NewsListView, NewsCategoryListView, NewsDetailView
from apps.home.views.price import PriceView
from apps.home.views.privacy import PrivacyPolicyView
from apps.home.views.seo import SeoView

urlpatterns = [
    path("news/", NewsListView.as_view(), name="news-list"),
    path("news/category/", NewsCategoryListView.as_view(), name="news-category"),
    path("news/<int:pk>/", NewsDetailView.as_view(), name="news-detail"),
    path("blog/", BlogListView.as_view(), name="blog-list"),
    path("blog/category/", BlogCategoryListView.as_view(), name="blog-category"),
    path("blog/<int:pk>/", BlogDetailView.as_view(), name="blog-detail"),
    path("privacy/", PrivacyPolicyView.as_view(), name="privacy-policy"),
    path("price/", PriceView.as_view(), name="price-list"),
    path("info/", PedagogInfoListView.as_view(), name="info-list"),
    path("contact-us/", ContactUsView.as_view(), name="contact-us"),
    path("seo/", SeoView.as_view(), name="seo"),
    path("faq/", FAQList.as_view(), name="faq"),
    path("faq/<int:pk>/", FAQDetail.as_view(), name="faq"),
]
