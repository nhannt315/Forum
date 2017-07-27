from braces.views._access import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, CreateView
from django.core.urlresolvers import reverse
from .models import Thread, ThreadImages
from . import forms


class ThreadDetailView(DetailView):
    model = Thread
    context_object_name = 'thread'
    template_name = 'threads/thread-detail.html'


def thread_detail_view(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    thread.increase_view()
    comment_list = thread.comments.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(comment_list, 7)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.num_pages(paginator.num_pages)
    context_dict = {
        'thread': thread,
        'comment_list': comments,
    }
    return render(request, 'threads/thread-detail.html', context_dict)


class ThreadCreateView(LoginRequiredMixin, CreateView):
    login_url = '/accounts/login-site/'
    redirect_field_name = 'next'
    form_class = forms.ThreadForm
    model = Thread
    template_name = 'threads/thread-form.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('threads:detail', kwargs={'pk': self.object.pk})


@login_required(login_url='/accounts/login-site/')
def post_thread(request):
    thread_form = forms.ThreadForm()
    if request.method == 'POST':
        thread_form = forms.ThreadForm(request.POST)
        if thread_form.is_valid():
            thread = thread_form.save(commit=False)
            thread.author = request.user
            thread_form.save()

            if 'images' in request.FILES:
                images = request.FILES.getlist('images')
                ThreadImages.objects.bulk_create([
                    ThreadImages(thread=thread, image=image) for image in
                    images
                ])
            return HttpResponseRedirect('/')
    return render(request, 'threads/thread-form.html',
                  {'thread_form': thread_form, })
