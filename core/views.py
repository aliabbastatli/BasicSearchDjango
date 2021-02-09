from django.db.models import Q
from django.shortcuts import render
from .models import Journal, Category

def isValidQueryParam(param):
    return param != '' and param is not None

def BootStrapFilterView(request):

    qs = Journal.objects.all()
    categories = Category.objects.all()
    title_contains_query = request.GET.get('title_contains')
    id_exact_query = request.GET.get('title_exact')
    title_or_author_query = request.GET.get('title_or_author')

    view_count_min = request.GET.get('view_count_min')
    view_count_max = request.GET.get('view_count_max')

    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')

    category = request.GET.get('category')
    reviewed = request.GET.get('reviewed')
    not_reviewed = request.GET.get('notReviewed')

    if isValidQueryParam(title_contains_query):
        qs = qs.filter(title__icontains=title_contains_query)
    
    elif isValidQueryParam(id_exact_query):
        qs = qs.filter(id=id_exact_query )

    elif isValidQueryParam(title_or_author_query):
        qs = qs.filter(Q(title__icontains=title_or_author_query) | Q(author__name__icontains=title_or_author_query)).distinct()

    if isValidQueryParam(view_count_min):
        qs = qs.filter(views__gte=view_count_min)

    if isValidQueryParam(view_count_max):
        qs = qs.filter(views__lt=view_count_max)

    if isValidQueryParam(date_min):
        qs = qs.filter(publishDate__gte = date_min)
    
    if isValidQueryParam(date_max):
        qs = qs.filter(publishDate__lt = date_max)
    
    if isValidQueryParam(category) and category != 'Choose...':
            qs = qs.filter(categories__name=category)

    if reviewed == 'on':
        qs = qs.filter(reviewed=True)

    elif not_reviewed == 'on':
        qs = qs.filter(reviewed=False)

    context = {
        'queryset': qs,
        'categories': categories
    }
    
    return render(request, "bootstrapForm.html", context)

 