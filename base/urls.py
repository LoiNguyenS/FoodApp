from django.urls import path

from .views import FoodList, FoodDetail, FoodCreate, FoodUpdate, FoodDelete, CustomLoginView, RegisterPage, BestFoodDetail
from django.contrib.auth.views import LogoutView
urlpatterns = [
#login page
	path('login/', CustomLoginView.as_view(), name='login'),
	#logout page
	path('logout/', LogoutView.as_view(next_page='login'), name='logout'),	
	path('register/', RegisterPage.as_view(), name='register'),
	path('', FoodList.as_view(), name='foods'),
	#pk is the default, if you want a custom one there is a way
	path('food/<int:pk>/', FoodDetail.as_view(), name='food'),	
	path('best-food/', BestFoodDetail, name='best-food'),
	path('food-create/', FoodCreate.as_view(), name='food-create'),
	path('food-update/<int:pk>/', FoodUpdate.as_view(), name='food-update'),
	path('food-delete/<int:pk>/', FoodDelete.as_view(), name='food-delete'),
]
