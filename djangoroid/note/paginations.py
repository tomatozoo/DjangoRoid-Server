from rest_framework import pagination


class NoteListPagination(pagination.CursorPagination):
    page_size = 10
    ordering = "-created_at"
    