from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.utils.translation import gettext as _
from django.views.generic.base import TemplateView
from .models import Post, Comment, Like
from accounts.models import User, Follow
from .forms import SearchForm, CommentForm, AddPostForm, EditPostForm
from django.views.generic.edit import CreateView, UpdateView, FormView


class HomeView(TemplateView):
    template_name = 'home.html'

    def post(self, request):
        post_data = request.POST
        post = Post.objects.get(id=post_data['like_post'])
        user = self.request.user
        try:
            like = Like.objects.get(user=user, post=post)
            like.delete()
            data = {'like_am': len(Like.objects.filter(post=post)), 'id': post.id, 'is_liked': 0}
            return JsonResponse(data, safe=False)
        except Like.DoesNotExist:
            like = Like(post=post, user=user)
            like.save()
            data = {'like_am': len(Like.objects.filter(post=post)), 'id': post.id, 'is_liked': 1}
            return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        follow = None
        if user.is_authenticated:
            follow, created = Follow.objects.get_or_create(user=user)
        posts = Post.objects.all()
        wall = []
        for p in posts:
            if p.user in follow.following.all():
                try:
                    Like.objects.get(post=p, user=user)
                    wall.append([p, 1, len(Like.objects.filter(post=p))])
                except Like.DoesNotExist:
                    wall.append([p, 0, len(Like.objects.filter(post=p))])
        context['posts'] = wall
        context['title'] = _('Home')
        context['user'] = user
        context['follow'] = follow
        return context


class AddPostView(TemplateView):
    model = Post
    template_name = 'add_post.html'
    form_class = AddPostForm

    def post(self, request):
        data = request.FILES['file']
        with open('instagramapp/static/images/upload_image.png', 'wb') as file:
            file.write(data.read())
        return JsonResponse('/static/images/upload_image.png', safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Add Post')
        return context


class EditPostView(UpdateView):
    model = Post
    template_name = 'add_post.html'
    form_class = EditPostForm
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Add Post')
        context['post'] = Post.objects.get(id=self.kwargs['pk'])
        return context


class SearchView(FormView):
    template_name = 'search.html'
    form_class = SearchForm

    def post(self, request, *args, **kwargs):
        data_post = self.request.POST
        users = User.objects.filter(username__contains=data_post['input'])
        result = render_to_string('search_results_template.html', {'results': users})
        return JsonResponse(result, safe=False)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Search')
        context['profile'] = self.request.user
        return context


class PostView(CreateView):
    template_name = 'post.html'
    form_class = CommentForm

    def post(self, request, *args, **kwargs):
        post_data = request.POST
        post = Post.objects.get(id=self.kwargs['pk'])
        user = self.request.user
        if 'add_like' in post_data.keys():
            try:
                like = Like.objects.get(user=user, post=post)
                like.delete()
                data = {'status': 'success', 'like_amount': len(Like.objects.filter(post=post)), 'is_liked': 0}
                return JsonResponse(data, safe=False)
            except Like.DoesNotExist:
                like = Like(post=post, user=user)
                like.save()
                data = {'status': 'success', 'like_amount': len(Like.objects.filter(post=post)), 'is_liked': 1}
                return JsonResponse(data, safe=False)
        if 'body' in post_data.keys():
            comment = Comment(body=post_data['body'], user=user, post=post)
            comment.save()
            comment_info = {'user': user, 'like_am': 0, 'post': post, 'comment': comment}
            block = render_to_string('comment_template.html', comment_info)
            return JsonResponse(block, safe=False)
        if 'delete_comment' in post_data.keys():
            comment = Comment.objects.get(id=int(post_data['delete_comment']))
            comment_id = comment.id
            comment.delete()
            data = {'id': comment_id}
            return JsonResponse(data, safe=False)
        if 'like_comment' in post_data.keys():
            try:
                comment = Comment.objects.get(id=int(post_data['like_comment']))
                like = Like.objects.get(user=user, comment=comment)
                like.delete()
                data = {'like_am': len(Like.objects.filter(comment=comment)), 'id': comment.id, 'is_liked': 0}
                return JsonResponse(data, safe=False)
            except Like.DoesNotExist:
                comment = Comment.objects.get(id=int(post_data['like_comment']))
                like = Like(comment=comment, user=user)
                like.save()
                data = {'like_am': len(Like.objects.filter(comment=comment)), 'id': comment.id, 'is_liked': 1}
                return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        post = Post.objects.get(id=self.kwargs['pk'])
        comments = []
        n = 0
        for c in Comment.objects.filter(post=post):
            comments.append([c])
            try:
                Like.objects.get(comment=c, user=user)
                comments[n].append(1)
            except Like.DoesNotExist:
                comments[n].append(0)
            comments[n].append(len(Like.objects.filter(comment=c)))
            n += 1
        context['comments'] = comments
        likes = []
        for i in Like.objects.filter(post=post):
            likes.append(i.user)
        context['likes'] = likes
        context['like_amount'] = len(Like.objects.filter(post=post))
        try:
            Like.objects.get(post=post, user=user)
            context['post'] = [post, 1]
        except Like.DoesNotExist:
            context['post'] = [post, 0]
        context['title'] = _('Post')
        context['profile'] = user
        return context


__all__ = ['PostView', 'HomeView', 'AddPostView', 'SearchView', 'EditPostView']
