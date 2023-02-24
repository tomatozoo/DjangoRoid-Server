from rest_framework import pagination


class NoteListPagination(pagination.CursorPagination):
    page_size = 5
    ordering = "-waffle_count"
