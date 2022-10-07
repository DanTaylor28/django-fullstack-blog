from . import views
from django.urls import path

# This links up my templates so they can be rendered. im using
# as_view because we are using class based views. You will need
# to add these paths for every page that you want to be rendered.
# You also need to import these views to main codestar urls file.
urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    # <slug:slug> tells the url what layout my url will have so it can find
    # the page to render
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
]
