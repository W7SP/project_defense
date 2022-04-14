from django.urls import path

from final_project.main.views.generic_views import HomeView, AboutUsView, contact_us_view
from final_project.main.views.books_views import CreateBookView, BookShopView, BuyBookView, EditBookView, DeleteBookView
from final_project.main.views.courses_views import CreateCourseView, CoursesShopView, BuyCourseView, EditCourseView, \
    DeleteCourseView
from final_project.main.views.equipment_views import CreateEquipmentView, EquipmentShopView, BuyEquipmentView, \
    EditEquipmentView, DeleteEquipmentView
from final_project.main.views.post_views import CreatePostView, EditPostView, DeletePostView, ShowPostsView, like_post, \
    ShowPostsByLikesView

urlpatterns = (
    # GENERIC URLS
    path('', HomeView.as_view(), name='index'),
    path('about/', AboutUsView.as_view(), name='about us'),
    path('contact_us/', contact_us_view, name='contact us'),
    # path('restricted/', RestrictedView.as_view(), name='restricted'),

    # COURSE URLS
    path('create/course/', CreateCourseView.as_view(), name='create course'),
    path('edit/course/<int:pk>', EditCourseView.as_view(), name='edit course'),
    path('delete/course/<int:pk>', DeleteCourseView.as_view(), name='delete course'),
    path('course/shop/', CoursesShopView.as_view(), name='courses shop'),
    path('course/buy/<int:pk>', BuyCourseView.as_view(), name='buy course'),

    # BOOK URLS
    path('create/book/', CreateBookView.as_view(), name='create book'),
    path('edit/book/<int:pk>', EditBookView.as_view(), name='edit book'),
    path('delete/book/<int:pk>', DeleteBookView.as_view(), name='delete book'),
    path('books/shop/', BookShopView.as_view(), name='book shop'),
    path('books/buy/<int:pk>', BuyBookView.as_view(), name='buy book'),

    # EQUIPMENT URLS
    path('create/equipment/', CreateEquipmentView.as_view(), name='create equipment'),
    path('edit/equipment/<int:pk>', EditEquipmentView.as_view(), name='edit equipment'),
    path('delete/equipment/<int:pk>', DeleteEquipmentView.as_view(), name='delete equipment'),
    path('equipment/shop/', EquipmentShopView.as_view(), name='equipment shop'),
    path('equipment/buy/<int:pk>', BuyEquipmentView.as_view(), name='buy equipment'),

    # POST URLS
    path('create/post/', CreatePostView.as_view(), name='create post'),
    path('edit/post/<int:pk>', EditPostView.as_view(), name='edit post'),
    path('delete/post/<int:pk>', DeletePostView.as_view(), name='delete post'),
    path('show/posts/', ShowPostsView.as_view(), name='show all posts'),
    path('show/posts/by_likes/', ShowPostsByLikesView.as_view(), name='show all posts by likes'),
    path('post/like/<int:pk>/', like_post, name='like post'),
    # path('post/dislike/<int:pk>/', dislike_post, name='dislike post'),

)
