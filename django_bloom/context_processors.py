from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse, resolve
from django.utils.translation import gettext as _

from post.models import Category, Post


def bloom_data(request):
    root_category = None
    try:
        root_category = Category.objects.get(is_root=True)
    except ObjectDoesNotExist:
        pass

    result = {'all_categories': Category.objects.all(), 'site_title': 'Bloom',
              'root_category': root_category}
    if request.user.is_authenticated:
        result['auth'] = {'user': request.user}

    if is_bloom(request):
        result['is_bloom'] = True
        sidebar = [
            {'id': 1, 'text': _('Dashboard'), 'path': reverse('bloom:index'), 'icon_class': 'fa-tachometer-alt'},
            {'id': 2, 'text': _('Post'), 'path': '', 'icon_class': 'fa-file-alt', 'children': [
                {'text': _('All Post'), 'path': reverse('bloom:post:all')},
                {'text': _('New Post'), 'path': reverse('bloom:post:new')},
            ]},
            {'id': 3, 'text': _('Category'), 'path': '', 'icon_class': 'fa-file-alt', 'children': [
                {'text': _('All Category'), 'path': reverse('bloom:category:all')},
                {'text': _('New Category'), 'path': reverse('bloom:category:new')},
            ]},
            {'id': 4, 'text': _('File Manager'), 'path': reverse('bloom:file_manager:index'), 'icon_class': 'fa-folder'},
        ]
        result['bloom_sidebar'] = set_active(request, sidebar)
    else:
        result['latest_posts'] = Post.objects.all().order_by('-created_at')[:5]
        result['most_viewed_posts'] = Post.objects.all().order_by('-views')[:5]

    return result


def is_bloom(request):
    return request.path_info.startswith('/bloom/')


def set_active(request, sidebar):
    current_path = request.path_info
    for i, item in enumerate(sidebar):
        if item['path'] == request.path_info:
            sidebar[i]['active'] = True
            break
        if 'children' in item:
            for ci, child_item in enumerate(item['children']):
                if child_item['path'] == current_path:
                    sidebar[i]['children'][ci]['active'] = True
                    break
            else:
                continue
            item['children_active'] = True
            break
    return sidebar
