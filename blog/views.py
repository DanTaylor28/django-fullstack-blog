from django.shortcuts import render, get_object_or_404, reverse  # reverse can look up url from name given in urls.py
from django.views import generic, View
from django.http import HttpResponseRedirect
from .models import Post
from .forms import CommentForm


# A class based view to display a list of blog posts.
# Paginate_by tells the browser to display a total of 6 posts per page.
class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 6


# Another view to render the post_details html.
class PostDetail(View):
    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by('created_on')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            'post_detail.html',
            {
                'post': post,
                'comments': comments,
                'commented': False,
                'liked': liked,
                'comment_form': CommentForm()
            },
        )

    # had to define post method so comments can be posted.
    # nearly identical to get above.
    def post(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by('created_on')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
        # this will get all the data posted from the form(comment)
        comment_form = CommentForm(data=request.POST)

        # is_valid is python built in method
        # ( ie have all required fields been completed)
        if comment_form.is_valid():
            # setting name & email automatically from logged in user
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            # saving the form but not yet commiting it to database
            comment = comment_form.save(commit=False)
            # because we want to assign post to it first
            comment.post = post
            comment.save()
        else:
            # return empty comment form if not valid
            comment_form = CommentForm()

        return render(
            request,
            'post_detail.html',
            {
                'post': post,
                'comments': comments,
                # to tell user comment is awaiting approval(false on get method)
                'commented': True,
                'liked': liked,
                'comment_form': CommentForm()
            },
        )


class PostLike(View):
    def post(self, request, slug):
        # first, get the post or show error
        post = get_object_or_404(Post, slug=slug)

        # if statement to check if post is already liked.
        # if it is, then unlike it, and vice versa.
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        # when a post is liked/unliked it will reload the post_detail page
        # using http method and reverse with the argument [slug]
        return HttpResponseRedirect(reverse('post_detail', args=[slug]))
