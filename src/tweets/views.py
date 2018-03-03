
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView, CreateView

from .models import Tweet
from .forms import TweetModelForm

#Create

class TweetCreateView(CreateView):
	form_class = TweetModelForm
	template_name = 'tweets/create_view.html'
	success_url = "/tweet/create/"
	def form_valid(self, form):
		form.instance.user = self.request.user
		return super(TweetCreateView, self).form_valid(form)
		
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
	queryset = Tweet.objects.all()

	def get_context_data(self, *args, **kwargs):
		context = super(TweetListView, self).get_context_data(*args, **kwargs)
		return context

def tweet_detail_view(request, pk=None):
	obj = get_object_or_404(Tweet, pk=pk)
	context = {
		"object": obj
	}
	return render(request, "tweets/tweet_detail.html")

