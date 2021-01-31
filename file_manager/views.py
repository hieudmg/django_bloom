import hashlib

from rest_framework.decorators import api_view
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from django.http import JsonResponse, Http404, HttpResponseBadRequest
import fsutil
import re
from django.templatetags.static import static
from django.urls import reverse as original_reverse
from django.utils.http import urlencode
from django.views.decorators.csrf import ensure_csrf_cookie
from django_bloom.settings import BASE_DIR, STATIC_URL, STATICFILES_DIRS
import base64
import time

static_dir = fsutil.join_path(str(BASE_DIR), STATICFILES_DIRS[0])
base_files_dir = fsutil.join_path(static_dir, 'files')
if not fsutil.is_dir(base_files_dir):
    if fsutil.is_file(base_files_dir):
        fsutil.delete_file(base_files_dir)
    fsutil.create_dir(base_files_dir)


class Node:
    def __init__(self, relative, absolute, url):
        self.url = url
        self.absolute = absolute
        self.relative = relative
        self.name = fsutil.get_filename(absolute)
        self.is_exist = fsutil.exists(absolute)
        self.is_file = fsutil.is_file(absolute)
        self.is_dir = fsutil.is_dir(absolute)
        self.__content = None

    @staticmethod
    def parse(relative=None, absolute=None):
        if relative is not None:
            relative = re.split('[/\\\\]', relative)
            absolute = fsutil.join_path(base_files_dir, *relative)
            url = static(fsutil.join_path('files', *relative))
            return Node(fsutil.join_path(*relative), absolute, url)
        elif absolute is not None:
            relative = absolute.replace(base_files_dir, '')
            url = static(fsutil.join_path('files', relative))
            return Node(relative, absolute, url)
        raise FileNotFoundError

    def ls(self):
        if self.__content is not None:
            return self.__content
        self.__content = []
        if self.is_dir:
            folders = fsutil.list_dirs(self.absolute)
            for folder in folders:
                self.__content.append(Node.parse(absolute=folder))

            files = fsutil.list_files(self.absolute)
            for file in files:
                self.__content.append(Node.parse(absolute=file))

        return self.__content

    def to_dict(self):
        return {
            'id': self.relative,
            'cssClass': 'folder' if self.is_dir else 'file ex-' + fsutil.get_file_extension(self.name),
            'text': self.name,
            'url': static('files/' + self.relative),
            'relative': self.relative,
            'isDir': self.is_dir,
            'children': self.is_dir,
        }


class FileManager(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    @staticmethod
    def atob(s):
        return base64.b64decode(s.encode('ascii')).decode('ascii')

    @staticmethod
    def btoa(s):
        return base64.b64encode(s.encode('ascii')).decode('ascii')

    def get(self, request, absolute_path=''):
        absolute_path = self.atob(absolute_path)
        if not absolute_path:
            absolute_path = '/'
        node = Node.parse(relative=absolute_path)
        if not node.is_exist:
            raise NotFound

        return Response(data=[content.to_dict() for content in node.ls()])

    def post(self, request, absolute_path=''):
        absolute_path = self.atob(absolute_path)
        node = Node.parse(relative=absolute_path)
        if node.is_exist:
            raise ParseError('Folder already existed.')

        fsutil.create_dir(node.absolute)
        return Response(data=True)

    def put(self, request, absolute_path=''):
        file_obj = request.FILES.get('file', None)
        if not file_obj:
            raise ParseError
        absolute_path = self.atob(absolute_path)
        node = Node.parse(relative=absolute_path)
        if not node.is_exist:
            fsutil.create_dir(node.absolute)
        file_name = file_obj.name
        base_file_name, extension = fsutil.split_filename(file_name)
        absolute_path = fsutil.join_path(
            absolute_path,
            base_file_name + '-' + str(int(time.time())) + ('.' + extension if extension else '')
        )
        node = Node.parse(relative=absolute_path)

        if node.is_exist:
            raise ParseError('File already existed.')

        with open(node.absolute, 'wb+') as destination:
            for chunk in file_obj.chunks():
                destination.write(chunk)

        return Response(data=True)

    def delete(self, request, absolute_path=''):
        if not absolute_path:
            raise ParseError
        absolute_path = self.atob(absolute_path)
        node = Node.parse(relative=absolute_path)
        if not node.is_exist:
            raise ParseError('Item is not existed.')

        if node.is_dir:
            fsutil.remove_dir(node.absolute)
        else:
            fsutil.remove_file(node.absolute)

        return Response(data=True)

    def patch(self, request, absolute_path=''):
        if not absolute_path:
            raise ParseError
        absolute_path = self.atob(absolute_path)
        node = Node.parse(relative=absolute_path)
        if not node.is_exist:
            raise ParseError('Item is not existed.')
        name = request.data.get('name', False)
        if not name:
            raise ParseError

        try:
            if node.is_file:
                fsutil.rename_file(node.absolute, name)
            else:
                fsutil.rename_dir(node.absolute, name)
        except OSError:
            pass

        return Response(data=True)


def reverse(*args, **kwargs):
    params = kwargs.pop('params', {})
    url = original_reverse(*args, **kwargs)

    if params:
        url += '?' + urlencode(params)

    return url


@ensure_csrf_cookie
def index(request):
    return render(request, 'bloom/file_manager/index.html')


def list_dir(request):
    path = request.GET.get('path', '')
    with_dirs = request.GET.get('dirs', 1)
    with_files = request.GET.get('files', 0)
    node = Node.parse(relative=path)

    result = []

    if not node.is_exist or node.is_file:
        raise Http404

    if with_dirs:
        try:
            folders = fsutil.list_dirs(node.absolute)
        except FileNotFoundError:
            raise Http404
        for i, folder in enumerate(folders):
            relative_path = folder.replace(base_files_dir, '')
            id_path = '/'.join(fsutil.split_path(relative_path))
            folders[i] = {
                'id': hashlib.sha1(folder.encode('utf-8')).hexdigest(),
                'load': reverse('bloom:file_manager:list_dir', params={'path': id_path}),
                'class': 'folder',
                'children': len(fsutil.list_dirs(folder)) > 0,
                'text': fsutil.get_filename(folder),
                'url': static(relative_path),
                'list': reverse('bloom:file_manager:list_dir', params={'path': id_path, 'files': 1}),
            }
        result.extend(folders)

    if with_files:
        try:
            files = fsutil.list_files(node.absolute)
        except FileNotFoundError:
            raise Http404
        for i, file in enumerate(files):
            files[i] = {
                'id': fsutil.get_file_hash(file, 'sha1'),
                'class': 'file ex-' + fsutil.get_file_extension(file),
                'text': fsutil.get_filename(file),
                'url': static(file.replace(static_dir, '')),
            }
        result.extend(files)

    if not path and not with_files:
        result = {
            'id': 'root',
            'text': 'Root Folder',
            'children': result,
            'state': {
                'opened': True,
                'selected': True
            },
            'list': reverse('bloom:file_manager:list_dir', params={'files': 1}),
        }

    return JsonResponse(result, safe=False)


def create_dir(request):
    path = request.POST['path']
    if fsutil.exists(path):
        return HttpResponseBadRequest
    fsutil.create_dir(path)
    return JsonResponse(True, safe=False)
