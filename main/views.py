from django.shortcuts import render, redirect,reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404


from main import models, forms, tasks


class PubList(generic.ListView):
    """
    List of publications

    get only publications with 'is_pub=True'(ready to publicate)
    """
    model = models.Pub
    template_name = 'main/pub_list.html'
    context_object_name = 'pubs'

    def get_queryset(self):
        return self.model.objects.filter(is_pub=True)


class PubDetail(generic.DetailView):
    """
    Publication detail

    besides publication data get also comments
    """
    model = models.Pub
    comment_form = forms.CommentForm
    template_name = 'main/pub_detail.html'
    context_object_name = 'pub'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not context.get('pub').is_pub:
            raise Http404
        context['comment_form'] = self.comment_form
        return context

    def post(self, request, *args, **kwargs):
        """
        save comment
        """
        form = self.comment_form(request.POST)
        if form.is_valid():
            obj = self.get_object()
            form.instance.pub = obj
            form.instance.author = request.user
            form.save()

            post_url = request.build_absolute_uri()
            tasks.send_email_about_comment.delay(obj.author.email, post_url)
            return redirect(reverse('pub_detail', args=[obj.slug]))


@method_decorator(login_required, name='dispatch')
class PubCreation(generic.CreateView):
    model = models.Pub
    form_class = forms.PubCreationForm
    template_name = 'main/create_pub.html'

    def form_valid(self, form):
        """
        get author which auth
        check perms to pub
        """
        user = self.request.user
        form.instance.author = user
        pub = form.save()
        if user.has_perm('pub.can_publish'):
            pub.is_pub = True
            pub.save()
        return redirect('pub_list')


