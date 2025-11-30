from django.shortcuts import render
from django.db.models import Q 
from .models import Category, Post, Author, AboutPage

def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None

def homepage (request):
    categories = Category.objects.all()[0:3]
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]
    context= {
        'object_list': featured,
        'latest': latest,
        'categories':categories,
    }
    return render(request, 'homepage.html',context)

def post (request,slug):
    post = Post.objects.get(slug = slug)
    latest = Post.objects.order_by('-timestamp')[:3]
    context = {
        'post': post,
        'latest': latest,
    }
    return render(request, 'post.html', context)


###################################

def about (request):
    about_content = AboutPage.objects.first()
    context = {
        'about': about_content
    }
    return render(request, 'about_page.html', context)

def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    about_match = None
    
    if query:
        # Post-ları axtar
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query) |
            Q(content__icontains=query) |
            Q(author__user__username__icontains=query) |
            Q(author__user__first_name__icontains=query) |
            Q(author__user__last_name__icontains=query) |
            Q(categories__title__icontains=query) |
            Q(categories__subtitle__icontains=query)
        ).distinct()
        
        # About səhifəsində axtar (database)
        about_pages = AboutPage.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author_name__icontains=query) |
            Q(author_role__icontains=query)
        )
        if about_pages.exists():
            about_match = {
                'title': 'About Me',
                'content': about_pages.first().content,
                'type': 'page'
            }
        else:
            # Statik about məzmununda axtar
            static_about_content = "A little bit about me. I am a 23 year old from South Africa. I am new to software development and this is my first tutorial to hopefully help some of you guys wanting to learn too. I hope you enjoy my teaching style and learn a lot from this. I know it's very basic but we have to start somewhere, hopefully sometime soon in the future you'll be learning some pretty cool stuff from me."
            static_author = "SAVANNAH - New Django Developer"
            
            if (query.lower() in static_about_content.lower() or 
                query.lower() in static_author.lower()):
                about_match = {
                    'title': 'About Me',
                    'content': static_about_content,
                    'author': static_author,
                    'type': 'page'
                }
    
    context = {
        'object_list': queryset,
        'query': query,
        'about_match': about_match
    }
    return render(request, 'search_bar.html', context)


##############################


def postlist (request,slug):
    category = Category.objects.get(slug = slug)
    posts = Post.objects.filter(categories__in=[category])

    context = {
        'posts': posts,
        'category': category,
    }
    return render(request, 'post_list.html', context)

def allposts(request):
    posts = Post.objects.order_by('-timestamp')

    context = {
        'posts': posts,
    }
    return render(request, 'all_posts.html',context)
