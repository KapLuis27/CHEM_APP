from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import SignUpForm, MemberForm
from .models import Member
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model, authenticate, login

User = get_user_model()

# Set a strong password for accessing admin creation
PASSWORD = 'DLSU1234!'  # You can change this to a more secure password
def create_admin(request):
    show_form = False

    if request.method == 'POST':
        entered_password = request.POST.get('password')

        if entered_password != PASSWORD:
            return HttpResponseForbidden("Incorrect password.")

        # Once password is correct, show the admin creation form
        if 'new_password' in request.POST:
            # Create the admin user
            username = request.POST.get('username')
            password = request.POST.get('new_password')
            email = request.POST.get('email')

            if User.objects.filter(username=username).exists():
                return render(request, 'create_admin.html', {'error': 'Username already exists', 'show_form': True})

            # Create the admin user
            user = User.objects.create(username=username, password=password, email=email)
            user.is_staff = True  # Set user as admin
            user.save()

            # Authenticate and log the user in
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('admin_dashboard')  # Redirect to your custom admin dashboard

        show_form = True  # Show the form after the password is validated

    return render(request, 'create_admin.html', {'show_form': show_form})

def welcome(request):
    show_form = False
    error = None

    if request.GET.get('show_admin_form') == 'true':
        request.session['show_admin_form'] = True
        request.session['password_verified'] = False

    if request.method == 'POST':
        entered_password = request.POST.get('password')

        if entered_password != PASSWORD:
            error = "Incorrect password."
        else:
            request.session['password_verified'] = True
            show_form = True

        if 'new_password' in request.POST:
            username = request.POST.get('username')
            password = request.POST.get('new_password')
            email = request.POST.get('email')

            if User.objects.filter(username=username).exists():
                error = 'Username already exists.'
            else:
                user = User.objects.create(username=username, password=password, email=email)
                user.set_password(password)  # Hash the password
                user.is_staff = True
                user.save()

                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('admin_dashboard')

            show_form = True  

    return render(request, 'welcome.html', {
        'show_form': show_form,
        'error': error,
        'show_admin_form': request.session.get('show_admin_form', False),
        'password_verified': request.session.get('password_verified', False),
    })

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Redirect based on user type
            if user.is_staff:
                # If user is an admin, redirect to admin dashboard
                return redirect('admin_dashboard')
            else:
                # If user is a regular member, redirect to regular dashboard
                return redirect('dashboard')
        else:
            # If authentication fails, you can show a message or handle the error
            return render(request, 'login.html', {'error': 'Invalid username or password'})

    return render(request, 'login.html')
@login_required
def dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'dashboard.html', {'member': request.user})
    return redirect('login')

@login_required
def admin_dashboard(request):
    # Fetch only non-admin members
    members = Member.objects.filter(is_staff=False)
    return render(request, 'admin_dashboard.html', {'members': members})


# Edit Member View
@login_required
def edit_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    
    if request.method == 'POST':
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = MemberForm(instance=member)

    return render(request, 'edit_member.html', {'form': form})

# Delete Member View
@login_required
def delete_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    member.delete()
    return redirect('admin_dashboard')


def logout_view(request):
    logout(request)
    return redirect('welcome')
