from django.http import HttpResponse,HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.shortcuts import render,get_object_or_404,redirect,Http404
from urllib import quote_plus
from .models import Post
from .forms import PostForm
from django.utils import timezone
from django.db.models import Q

def post_create(request):
	if not request.user.is_staff or not request.user.is_superuser :
		raise Http404
	form = PostForm(request.POST or None,request.FILES or None)
	if form.is_valid() :
		instance = form.save(commit=False)
		instance.save()
		messages.success(request,"Successfully Created")
		return HttpResponseRedirect(instance.get_absolute_url())

	context = {
			"form" : form
		}

	return  render(request,"post_form.html",context)



def post_detail(request,slug=None):
	
	instance = get_object_or_404(Post , slug=slug)
	if instance.publish > timezone.now() :
		if not request.user.is_staff or not request.user.is_superuser :
			raise Http404
	context = {
		"title" : instance.title,
		"object" : instance
	
	}
	return  render(request,"post_detail.html",context)

def post_list(request):
	query = request.GET.get('q')
	if query :
		queryset_list = Post.objects.active().filter(Q(title__icontains=query)|
			Q(content__icontains=query)|
			Q(user__first_name__icontains=query)|
			Q(user__last_name__icontains=query)
			).distinct()
	else :
		queryset_list = Post.objects.active()

	paginator = Paginator(queryset_list, 3)
	page = request.GET.get('page')

	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)
	context = {
	"title" : "My posts",
	"object_list" : queryset
	}

	return  render(request,"list.html",context)


def post_update(request,slug=None):
	if not request.user.is_staff or not request.user.is_superuser :
		raise Http404
	instance = get_object_or_404(Post , slug=slug)
	form = PostForm(request.POST or None,request.FILES or None, instance=instance)
	if form.is_valid() :
		instance = form.save(commit=False)
		instance.save()
		messages.success(request,"Successfully Updated")
		return HttpResponseRedirect(instance.get_absolute_url())
	# else :
	# 	messages.failure(request,"Successfully Created")

	context = {
		"title" : instance.title,
		"object" : instance,
		"form" : form
	}
	return  render(request,"post_form.html",context)

def post_delete(request,slug=None):
	if not request.user.is_staff or not request.user.is_superuser :
		raise Http404
	instance = get_object_or_404(Post , slug=slug)
	instance.delete()
	messages.success(request,"Successfully Deleted")
	return  redirect("posts:list")

# Create your views here.
