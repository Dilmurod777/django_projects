from django import template
from blog.models import Post, Tag

register = template.Library()


@register.inclusion_tag('blog/sidebar_tpl.html')
def get_sidebar(count=3):
    posts = Post.objects.order_by('-views')[:count]
    tags = Tag.objects.all()
    return {'posts': posts, 'tags': tags}
