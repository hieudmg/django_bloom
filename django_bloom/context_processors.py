def category_list(request):
    result = {'categories': 'Here we go', 'site_title': 'Bloom'}
    if request.user.is_authenticated:
        result['auth'] = {'user': request.user}
    else:
        result['auth'] = False
    return result
