from django.shortcuts import render, redirect, get_object_or_404
from rango.models import Category, Page
from django.http import HttpResponse
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import datetime
from rango.utils import visitor_cookie_handler

def index(request):
    # Query the database for a list of ALL categories currently stored.
    # Order the categories by the number of likes in descending order.
    # Retrieve the top 5 only -- or all if less than 5.
    # Place the list in our context_dict dictionary (with our boldmessage!)
    # that will be passed to the template engine.
    request.session.set_test_cookie()
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    
    context_dict = {
        'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!',
        'categories': category_list,
        'pages': page_list
    }
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list

    # Call the session-based cookie handler
    visitor_cookie_handler(request)
    return render(request, 'rango/index.html')

    # Retrieve visits count from session and add to context
    context_dict['visits'] = request.session['visits']

    # Obtain the response object
    response = render(request, 'rango/index.html', context=context_dict)

    # Call the helper function to update cookies
    visitor_cookie_handler(request, response)

    # Update the context with the visit count from cookies
    context_dict['visits'] = int(request.COOKIES.get('visits', '1'))

    # Return the response with updated cookies
    return response

    # Render the response and send it back!
    return render(request, 'rango/index.html', context=context_dict)

def about(request):

    visitor_cookie_handler(request)  # Ensure visits are tracked

    visits = request.session.get('visits', 1)  # Get visit count from session
    context_dict = {'visits': visits}

    return HttpResponse("Rango says here is the about page. <br><a href='/rango/'>Back to Index</a>")
    return render(request, 'rango/about.html')

    if request.session.test_cookie_worked():
        print("TEST COOKIE WORKED!")
        request.session.delete_test_cookie()
    
    print("Request Method:", request.method)
    print("User:", request.user)

    return render(request, 'rango/about.html', {})

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

@login_required
def add_category(request):
    form = CategoryForm()

    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        # Have we been provided with a valid form?
        return redirect(reverse('rango:index'))
        if form.is_valid():
            # Save the new category to the database.
            cat = form.save(commit=True)
            # Now that the category is saved, we could confirm this.
            # For now, just redirect the user back to the index view.
            return redirect(reverse('rango:index'))
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
        return redirect(reverse('rango:index'))

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


def register(request):
    registered = False  # Track registration success

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)  # Hash the password
            user.save()

            # Create user profile but don't save yet
            profile = profile_form.save(commit=False)
            profile.user = user  # Link to User instance

            # Save profile picture if uploaded
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()  # Save UserProfile

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'rango/register.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered
    })
def user_login(request):
    if request.method == 'POST':
        # Get username and password from form
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:index'))  # Redirect to homepage
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")

    # Display login form if request is GET
    return render(request, 'rango/login.html')

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')
    return HttpResponse("Since you're logged in, you can see this text!")


@login_required
def add_page(request, category_name_slug):
    category = get_object_or_404(Category, slug=category_name_slug)

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save(commit=False)
            page.category = category
            page.save()
            return redirect(reverse('show_category', kwargs={'category_name_slug': category.slug}))
    else:
        form = PageForm()

    return render(request, 'rango/add_page.html', {'form': form, 'category': category})

@login_required
def user_logout(request):
    """Logs out the user and redirects them to the homepage."""
    logout(request)
    return redirect(reverse('rango:index'))  # Redirect to homepage

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):
    # Retrieve visit count from session
    visits = int(get_server_side_cookie(request, 'visits', '1'))

    # Retrieve last visit timestamp from session
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    # If it's been more than a day since last visit, increment the visit count
    if (datetime.now() - last_visit_time).days > 0:
        visits += 1
        request.session['last_visit'] = str(datetime.now())  # Update last visit
    else:
        request.session['last_visit'] = last_visit_cookie  # Keep previous timestamp

    # Update visits count in session
    request.session['visits'] = visits
