from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Organization, Role,CustomUser
from .forms import SubOrganizationForm   
from django.contrib import messages


# for usercreaton 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model, logout


# user auth for logout

def user_logout(request):
    logout(request)
    return redirect('admin:login')   


# org list for specific user
# @login_required
def organization_list(request):
    
    # if request.user.is_superuser:
        organizations = Organization.objects.filter(created_by=request.user)
        
        main_organizations = organizations.filter(is_main=True)
        sub_organizations = organizations.filter(is_main=False)

        return render(request, 'org_list.html', {
            'main_organizations': main_organizations,
            'sub_organizations': sub_organizations,
        })
    # else:
        # return HttpResponseForbidden("You are not authorized to view this page.")


# crud for sub-org 
def create_sub_organization(request):
    user = request.user
    if not user.is_authenticated or not user.is_superuser:
        # messages.error(request, "You are not authorized to create sub-organizations!")
        return redirect('organization_list')

    if request.method == 'POST':
        form = SubOrganizationForm(request.POST, user=user)
        if form.is_valid():
            sub_org = form.save(commit=False)
            sub_org.created_by = user  # Automatically set the creator
            sub_org.is_main = False   # Ensure it's always a sub-organization
            sub_org.save()
            # messages.success(request, "Sub-organization created successfully!")
            return redirect('organization_list')
    else:
        form = SubOrganizationForm(user=user)

    return render(request, 'create_sub_organization.html', {'form': form})

def update_sub_organization(request, org_id):
    user = request.user
    # Fetch the sub-organization object by ID
    sub_organization = get_object_or_404(Organization, id=org_id, is_main=False)  # Ensures it's a sub-org

    # Check if the current user is authorized to update this sub-organization
    if sub_organization.created_by != request.user and not request.user.is_superuser:
        # messages.error(request, "You are not authorized to update this sub-organization.")
        return redirect('organization_list')  # Redirect if not authorized

    if request.method == 'POST':
        form = SubOrganizationForm(request.POST, instance=sub_organization)
        if form.is_valid():
            form.save()
            # messages.success(request, "Sub-organization updated successfully!")
            return redirect('organization_list')  # Redirect after successful update
    else:
        form = SubOrganizationForm(instance=sub_organization,user=user)

    return render(request, 'update_sub_organization.html', {'form': form, 'sub_organization': sub_organization})

def delete_sub_org(request, org_id):
    # Fetch the sub-organization object by ID and ensure it is a sub-organization
    sub_organization = get_object_or_404(Organization, id=org_id, is_main=False)

    # Check if the current user is authorized to delete this sub-organization
    if sub_organization.created_by != request.user and not request.user.is_superuser:
        # messages.error(request, "You are not authorized to delete this sub-organization.")
        return redirect('organization_list')  # Redirect if not authorized

    # Delete the sub-organization
    sub_organization.delete()

    # messages.success(request, "Sub-organization deleted successfully!")
    return redirect('organization_list')  # Redirect to the organization list page after deletion





# user creation with crud and role tagging 

def create_user(request):
    if not request.user.is_superuser:
        raise Http404("You do not have permission to create users.")
    
    if request.method == 'POST':
        # Getting the data from the form
        username = request.POST.get('username')
        password = request.POST.get('password')
        organization_id = request.POST.get('organization')
        role_id = request.POST.get('role', None)

        # Fetch the organization and role
        try:
            organization = Organization.objects.get(id=organization_id)
        except Organization.DoesNotExist:
            messages.error(request, "Invalid organization.")
            return redirect('create_user')

        # Ensure the superuser is assigning users to sub-organizations they created
        if organization.parent is None or organization.parent.created_by != request.user:
            # messages.error(request, "You can only assign users to sub-organizations you created.")
            return redirect('create_user')

        # Default role is Viewer if none is specified
        role = None
        if role_id:
            try:
                role = Role.objects.get(id=role_id)
            except Role.DoesNotExist:
                messages.error(request, "Invalid role.")
                return redirect('user_list')
        if not role:
            role = Role.objects.get(name='Viewer')  # Default role

        # Create the user
        user = get_user_model().objects.create_user(username=username, password=password)
        user.organization = organization
        user.role = role  # Assign the role to the user
        user.save()

        # Provide a success message
        # messages.success(request, f"User '{username}' created successfully and assigned to {organization.name} as {role.name}.")
        return redirect('user_list')

    else:
        # Fetch available sub-organizations created by the current superuser
        sub_organizations = Organization.objects.filter(created_by=request.user, parent__isnull=False)
        roles = Role.objects.all()
        return render(request, 'create_user.html', {'sub_organizations': sub_organizations, 'roles': roles})


def list_users(request):
    if not request.user.is_superuser:
        raise Http404("You do not have permission to view this page.")

    # Fetch sub-organizations created by the superuser
    sub_organizations = Organization.objects.filter(created_by=request.user, parent__isnull=False)

    # Fetch users belonging to those sub-organizations
    users = get_user_model().objects.filter(organization__in=sub_organizations)

    return render(request, 'user_list.html', {'users': users})


def update_user(request, user_id):
    # Check if the user is a superuser or the creator of the sub-organization
    user = get_object_or_404(get_user_model(), id=user_id)
    if not request.user.is_superuser and request.user != user.organization.created_by:
        raise Http404("You do not have permission to update this user.")

    if request.method == 'POST':
        # Getting the data from the form
        username = request.POST.get('username')
        password = request.POST.get('password')
        organization_id = request.POST.get('organization')
        role_id = request.POST.get('role')

        # Fetch the organization and role
        try:
            organization = Organization.objects.get(id=organization_id)
            role = Role.objects.get(id=role_id)
        except Organization.DoesNotExist or Role.DoesNotExist:
            # messages.error(request, "Invalid organization or role.")
            return redirect('update_user', user_id=user.id)

        # Check if the organization is a sub-organization created by the current superuser
        if organization.parent is None or organization.parent.created_by != request.user:
            # messages.error(request, "You can only assign users to sub-organizations you created.")
            return redirect('update_user', user_id=user.id)

        # Update the user fields
        user.username = username
        if password:
            user.set_password(password)
        user.organization = organization
        user.role = role  # Assign the new role to the user
        user.save()

        # messages.success(request, f"User '{username}' updated successfully and assigned to {organization.name} as {role.name}.")
        return redirect('user_list')

    else:
        # Fetch available sub-organizations created by the current superuser
        sub_organizations = Organization.objects.filter(created_by=request.user, parent__isnull=False)
        roles = Role.objects.all()

        # Pass the current user data to pre-populate the form
        return render(request, 'update_user.html', {
            'sub_organizations': sub_organizations,
            'roles': roles,
            'user': user,
        })

def delete_user(request, user_id):
    # Fetch the user object
    user = get_object_or_404(get_user_model(), id=user_id)
    
    # Check if the user is a superuser or the creator of the sub-organization
    if not request.user.is_superuser and request.user != user.organization.created_by:
        raise Http404("You do not have permission to delete this user.")

    # Deleting the user
    if request.method == 'POST':
        user.delete()  # Delete the user from the database
        # messages.success(request, f"User '{user.username}' deleted successfully.")
        return redirect('user_list')  # Redirect to the organization list page

    # Display confirmation page before deletion
    return render(request, 'delete_user.html', {'user': user})