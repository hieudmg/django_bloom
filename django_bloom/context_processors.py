from django.urls import reverse, resolve
from django.utils.translation import gettext as _


def bloom_data(request):
    result = {'categories': _('Here we go'), 'site_title': 'Bloom'}
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
        ]
        result['bloom_sidebar'] = set_active(request, sidebar)

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
