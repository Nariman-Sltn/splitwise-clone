from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import GroupCreateForm, GroupJoinForm
from .models import Group, GroupMembership
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from .forms import ExpenseCreateForm
from .models import Expense, ExpenseSplit
from decimal import Decimal
from .services import calculate_group_balances, simplify_debts


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
            name = form.cleaned_data['name']
            password = form.cleaned_data['password']

            existing_same_name = Group.objects.filter(name=name)
            for g in existing_same_name:
                if g.check_password(password):
                    form.add_error(None, 'لطفاً اسم یا رمز رو عوض کن!!!')
                    return render(request, 'expenses/create_group.html', {'form': form})

            group = Group(name=name, created_by=request.user)
            group.set_password(password)
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

            candidate_groups = Group.objects.filter(name=name)
            matched_group = None
            for g in candidate_groups:
                if g.check_password(password):
                    matched_group = g
                    break

            if matched_group is None:
                messages.error(request, 'اسم یا رمز گروه اشتباهه.')
                return render(request, 'expenses/join_group.html', {'form': form})

            GroupMembership.objects.get_or_create(group=matched_group, user=request.user)
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
    expenses = Expense.objects.filter(group=group).select_related('paid_by').prefetch_related('splits__user')

    balances = calculate_group_balances(group)
    transactions = simplify_debts(balances)

    return render(request, 'expenses/group_detail.html', {
        'group': group,
        'members': members,
        'expenses': expenses,
        'balances': balances,
        'transactions': transactions,
    })

@login_required
def create_expense_view(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    is_member = GroupMembership.objects.filter(group=group, user=request.user).exists()
    if not is_member:
        return HttpResponseForbidden("شما عضو این گروه نیستید.")

    if request.method == 'POST':
        form = ExpenseCreateForm(request.POST, group=group)
        if form.is_valid():
            title = form.cleaned_data['title']
            amount = form.cleaned_data['amount']
            paid_by = form.cleaned_data['paid_by']
            participants = form.cleaned_data['participants']

            expense = Expense.objects.create(
                group=group,
                title=title,
                amount=amount,
                paid_by=paid_by,
            )

            count = participants.count()
            share = (amount / count).quantize(Decimal('0.01'))
            total_assigned = Decimal('0.00')

            participant_list = list(participants)
            for i, user in enumerate(participant_list):
                if i == len(participant_list) - 1:
                    this_share = amount - total_assigned
                else:
                    this_share = share
                    total_assigned += share

                ExpenseSplit.objects.create(
                    expense=expense,
                    user=user,
                    amount=this_share,
                )

            return redirect('group_detail', group_id=group.id)
    else:
        form = ExpenseCreateForm(group=group)

    return render(request, 'expenses/create_expense.html', {'form': form, 'group': group})