from rest_framework.pagination import PageNumberPagination

class DiaryPagination(PageNumberPagination):
    page_size = 10          # записей на страницу
    page_size_query_param = 'page_size'
    max_page_size = 50