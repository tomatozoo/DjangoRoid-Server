from rest_framework import pagination


class TagListPagination(pagination.CursorPagination):
    page_size = 10
