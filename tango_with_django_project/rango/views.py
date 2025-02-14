from django.shortcuts import render, redirect, get_object_or_404
from rango.models import Category, Page
from django.http import HttpResponse
from rango.forms import CategoryForm, PageForm
from django.shortcuts import redirect
from rango.forms import PageForm
from django.urls import reverse

def index(request):
    # Query the database for a list of ALL categories currently stored.
    # Order the categories by the number of likes in descending order.
    # Retrieve the top 5 only -- or all if less than 5.
    # Place the list in our context_dict dictionary (with our boldmessage!)
    # that will be passed to the template engine.
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    
    context_dict = {
        'categories': category_list,
        'pages': page_list
    }
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list

    # Render the response and send it back!
    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    return HttpResponse("Rango says here is the about page. <br><a href='/rango/'>Back to Index</a>")
    return render(request, 'rango/about.html')

def show_category(request, category_name_slug):
    context_dict = {}
    category = get_object_or_404(Category, slug=category_name_slug)
    pages = Page.objects.filter(category=category)

    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category'] = category

        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages

    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, 'rango/category.html', {'category': category, 'pages': pages})

def add_category(request):
    form = CategoryForm()

    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            cat = form.save(commit=True)
            # Now that the category is saved, we could confirm this.
            # For now, just redirect the user back to the index view.
            return redirect(reverse('index'))
        else:
            # The supplied form contained errors -
            # just print them to the terminal.
            print(form.errors)
            form = CategoryForm()

    # Will handle the bad form, new form, or no form supplied cases.
    # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):
    category = get_object_or_404(Category, slug=category_name_slug)

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save(commit=False)
            page.category = category
            page.save()
            return redirect('show_category', category_name_slug=category.slug)
    else:
        form = PageForm()

    return render(request, 'rango/add_page.html', {'form': form, 'category': category})

    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

        # Redirect if category does not exist
    if category is None:
        return redirect('/rango/')

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return redirect(reverse('rango:show_category',
                                        kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)



