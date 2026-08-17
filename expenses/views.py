from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import GroupCreateForm, GroupJoinForm
from .models import Group, GroupMembership
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden

def signup_view(request):   
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'expenses/signup.html', {'form': form})

@login_required
def home_view(request):
    memberships = GroupMembership.objects.filter(user=request.user).select_related('group')
    groups = [m.group for m in memberships]
    return render(request, 'expenses/home.html', {'groups': groups})

@login_required
def create_group_view(request):
    if request.method == 'POST':
        form = GroupCreateForm(request.POST)
        if form.is_valid():
            group = Group(
                name=form.cleaned_data['name'],
                created_by=request.user
            )
            group.set_password(form.cleaned_data['password'])
            group.save()
            GroupMembership.objects.create(group=group, user=request.user)
            return redirect('home')
    else:
        form = GroupCreateForm()
    return render(request, 'expenses/create_group.html', {'form': form})


@login_required
def join_group_view(request):
    if request.method == 'POST':
        form = GroupJoinForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            password = form.cleaned_data['password']
            try:
                group = Group.objects.get(name=name)
            except Group.DoesNotExist:
                messages.error(request, 'گروهی با این اسم پیدا نشد.')
                return render(request, 'expenses/join_group.html', {'form': form})

            if not group.check_password(password):
                messages.error(request, 'رمز گروه اشتباهه.')
                return render(request, 'expenses/join_group.html', {'form': form})

            GroupMembership.objects.get_or_create(group=group, user=request.user)
            return redirect('home')
    else:
        form = GroupJoinForm()
    return render(request, 'expenses/join_group.html', {'form': form})

@login_required
def group_detail_view(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    is_member = GroupMembership.objects.filter(group=group, user=request.user).exists()

    if not is_member:
        return HttpResponseForbidden("شما عضو این گروه نیستید.")

    members = GroupMembership.objects.filter(group=group).select_related('user')

    return render(request, 'expenses/group_detail.html', {
        'group': group,
        'members': members,
    })