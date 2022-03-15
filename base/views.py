from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Food

# Create your views here.
class CustomLoginView(LoginView):
	template_name = 'base/login.html'
	fields = '__all__'
	redirect_authenticated_user = True

	def get_success_url(self):
		return reverse_lazy('foods')

class RegisterPage(FormView):
	template_name = 'base/register.html'
	form_class = UserCreationForm
	redirect_authenticated_user = True	
	success_url = reverse_lazy('foods')

	def form_valid(self, form):
		user = form.save()
		if user is not None:
			#this is from the following: from django.contrib.auth.login import login
			#so if the user is not NONE it will auto login the suer
			login(self.request, user)
		return super(RegisterPage, self).form_valid(form)	

	def get(self, *args, **kwargs):
		if self.request.user.is_authenticated:
			return redirect('foods')
		return super(RegisterPage, self).get(*args, **kwargs)



#foodlist inherits from list views
#when you add the mixin: LoginRequiredMixin, you have to put it before the view class
#now all classes are restricted if they are not logged in
class FoodList(LoginRequiredMixin, ListView):
	model = Food
	#this would be the object_name in the object list, u can rename it
	context_object_name = 'foods'

	#ensure user can only get their own data
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['foods'] = context['foods'].filter(user=self.request.user)
		#context['count'] = context['foods'].filter(complete=False).count()

		search_input = self.request.GET.get('search-area') or ''
		if search_input: 
			context['foods'] = context['foods'].filter(
					title__startswith=search_input) # can also do title_icontains

		context['search_input'] = search_input		
		return context 


class FoodDetail(LoginRequiredMixin, DetailView):
	model = Food
	context_object_name = 'food'
	#custom name for the html page
	template_name = 'base/food.html'

class FoodCreate(LoginRequiredMixin, CreateView):
	model = Food
	fields = ['title', 'description']
	success_url = reverse_lazy('foods')

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super(FoodCreate, self).form_valid(form)

class FoodUpdate(LoginRequiredMixin, UpdateView):
	model = Food
	fields = ['title', 'description']
	success_url = reverse_lazy('foods')

class FoodDelete(LoginRequiredMixin, DeleteView):
	model = Food
	context_object_name = 'food'
	success_url = reverse_lazy('foods')

def BestFoodDetail(request):
	try:
		temp = set(Food.objects.filter(user=request.user).order_by('date'))		
		queryset = temp.pop()
		context = {
		"object_list": queryset
		}
	except Food.DoesNotExist:
		raise Http404("Food does not exist")

	return render(request, 'base/best_food.html', context)
