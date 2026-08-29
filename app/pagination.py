from rest_framework import pagination
from rest_framework.response import Response


def sort_dict_recursive(d):
    return {
        k: sort_dict_recursive(v) if isinstance(v, dict) else v
        for k, v in sorted(d.items())
    }


# Tutorial creator didn't use a custom paginator.
# He went with LimitOffsetPagination but I prefer
# PageNumberPagination for my projects.
# Docs:
# https://www.django-rest-framework.org/api-guide/pagination
class CustomPagination(pagination.PageNumberPagination):
    # Disabled if not explicitly set here.
    page_size_query_param = 'page_size'
    # Only relevant if page_size_query_param is set.
    max_page_size = 30
    
    def get_paginated_response(self, data):
        result = {
            "meta": {
                "links": {
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                },
                "total_items": self.page.paginator.count,
                "current_page": self.page.number,
                "pages": self.page.paginator.num_pages,
                "page_size": self.get_page_size(self.request),
            },
            "results": data,
        }
        return Response(sort_dict_recursive(result))
