import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'tango_with_django_project.settings')

import django
django.setup()
from rango.models import Category, Page

def populate():
    python_cat = add_cat('Python', views=128, likes=64)
    django_cat = add_cat('Django', views=64, likes=32)
    other_cat = add_cat('Other Frameworks', views=32, likes=16)

    # Sample pages (add more if needed)
    add_page(cat=python_cat, title="Official Python Tutorial", url="http://docs.python.org/3/tutorial/")
    add_page(cat=django_cat, title="Django Official Docs", url="https://docs.djangoproject.com/en/2.2/")
    add_page(cat=other_cat, title="Flask Docs", url="https://flask.palletsprojects.com/")

    print("Database populated successfully!")

    # First, we will create lists of dictionaries containing the pages
    # we want to add into each category.
    # Then we will create a dictionary of dictionaries for our categories.
    # This might seem a little bit confusing, but it allows us to iterate
    # through each data structure, and add the data to our models.
    python_pages = [
        {'title': 'Official Python Tutorial',
         'url':'http://docs.python.org/3/tutorial/'},
        {'title':'How to Think like a Computer Scientist',
         'url':'http://www.greenteapress.com/thinkpython/'},
        {'title':'Learn Python in 10 Minutes',
         'url':'http://www.korokithakis.net/tutorials/python/'} ]

    django_pages = [
        {'title': 'Official Django Tutorial',
         'url':'https://docs.djangoproject.com/en/2.1/intro/tutorial01/'},
        {'title': 'Django Rocks',
         'url': 'http://www.djangorocks.com/'},
        {'title': 'How to Tango with Django',
         'url': 'http://www.tangowithdjango.com/'}]


    other_pages = [
        {'title': 'Bottle',
         'url':'http://bottlepy.org/docs/dev/'},
        {'title': 'Flask',
         'url': 'http://flask.pocoo.org'}]


    cats = {'Python': {'pages': python_pages},
            'Django': {'pages': django_pages},
            'Other Frameworks': {'pages': other_pages}}

    # If you want to add more categories or pages,
    # add them to the dictionaries above.

    # The code below goes through the cats dictionary, then adds each category,
    # and then adds all the associated pages for that category.
    for cat, cat_data in cats.items():
        c = add_cat(cat)
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'])

    # Print out the categories we have added.
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'- {c}: {p}')

def add_page(cat, title, url, views=0):
    page, created = Page.objects.get_or_create(category=cat, title=title, url=url)
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url = url
    p.views = views
    p.save()
    return p

def add_cat(name, views=0, likes=0):
    c = Category.objects.get_or_create(name=name)[0]
    c.save()
    cat, created = Category.objects.get_or_create(name=name)
    cat.views = views
    cat.likes = likes
    cat.save()
    return c


# Start execution here!
if __name__ == '__main__':
     print('Starting Rango population script...')
     populate()