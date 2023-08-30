import djoser
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('', homepage, name='home_page'),
                  path('about', About.as_view(), name='about_site'),
                  path('post/<slug:post_title_slug>/', ShowPost, name='show_post'),
                  path('forums/<slug:cat_slug>/', ShowCategory.as_view(), name='cat_posts'),
                  path('popular/', showpopularposts, name='popular'),
                  path('form/', FormAdd.as_view(), name='add_post'),
                  path('cabinet/', Cabinet.as_view(), name='cabinet'),
                  path('error404/', kek.as_view()),
                  path('auth/', include('djoser.urls')),
                  path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
                  path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
                  path('testapi/', Base.as_view()),
                  path('response200/', Response200.as_view()),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
              + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
