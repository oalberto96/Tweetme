from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from django.views.generic import (DetailView, 
	ListView, 
	CreateView, 
	UpdateView,
	DeleteView
	)

from .models import Tweet
from .forms import TweetModelForm
from .mixins import FormUserNeededMixin, UserOwnerMixin

#Create
#We can use LoginRequiredMixin to present login page if a user is
#not authenticated
#class TweetCreateView(LoginRequiredMixin, FormUserNeededMixin, CreateView):
class TweetCreateView(FormUserNeededMixin, CreateView):
	form_class = TweetModelForm
	template_name = "tweets/create_view.html"
	#success_url = reverse_lazy("tweet:detail")
	#success_url = "/tweet/create/"
	#login_url = "/admin/"

#This has the same functionality as TweetCreateView
def tweet_create_view(request):
	form = TweetModelForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()
	context = {
		"form":form
	}
	return render(request, 'tweets/create_view.html')


class TweetUpdateView(LoginRequiredMixin, UserOwnerMixin, UpdateView):
	queryset = Tweet.objects.all()
	form_class = TweetModelForm
	template_name = "tweets/update_view.html"
	#success_url = "/tweet/"

class TweetDeleteView(LoginRequiredMixin,DeleteView):
	model = Tweet
	template_name = "tweets/delete_confirm.html"
	success_url = reverse_lazy("tweet:list")



# Create your views here.
class TweetDetailView(DetailView):
	#template_name = "tweets/detail_view.html"
	queryset = Tweet.objects.all()


	def get_object(self):
		print(self.kwargs)
		pk = self.kwargs.get("pk")
		obj = get_object_or_404(Tweet, pk=pk)
		return obj

class TweetListView(ListView):
	#template_name = "tweets/list_view.html"
	def get_queryset(self, *args, **kwargs):
		qs = Tweet.objects.all()
		query = self.request.GET.get("q", None)
		if query is not None:
			qs = qs.filter(
				Q(content__icontains=query)|
				Q(user__username__icontains=query)
				)
		return qs

	def get_context_data(self, *args, **kwargs):
		context = super(TweetListView, self).get_context_data(*args, **kwargs)
		return context

def tweet_detail_view(request, pk=None):
	obj = get_object_or_404(Tweet, pk=pk)
	context = {
		"object": obj
	}
	return render(request, "tweets/tweet_detail.html")

