from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from decimal import InvalidOperation

from . import forms
from .models import Drink, Account, Purchase, Ingredient


def main(request):
    return render(request, "pages/main.html")


def about(request):
    return render(request, "pages/about.html")


class LoginUser(LoginView):
    form_class = forms.LoginUserForm
    template_name = 'authorization/login.html'
    success_url = reverse_lazy('main')
    context_object_name = 'Вход'


class RegisterUser(CreateView):
    form_class = forms.RegisterUserForm
    template_name = 'authorization/register.html'
    success_url = reverse_lazy('login')
    context_object_data = 'Регистрация'


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('main'))


def menu(request):
    posts = Drink.objects.all()
    return render(request, 'pages/menu.html', {'posts': posts, 'title': "Меню"})


from decimal import Decimal

@login_required
def deposit(request):
    account = Account.objects.get(user=request.user)

    if request.method == "POST":
        amount = request.POST.get('amount')
        if amount:
            try:
                # Преобразуем строку в Decimal
                amount = Decimal(amount)
                if amount > 0:
                    account.deposit(amount)
                    return redirect('profile')  # Перенаправляем обратно на меню после пополнения
                else:
                    # Обработать ошибку, если сумма отрицательная
                    pass
            except InvalidOperation:
                # Если строку нельзя преобразовать в число, обработать ошибку
                pass

    return render(request, 'pages/deposit.html', {'account': account})

@login_required
def profile(request):
    info = Account.objects.get(user=request.user)
    purchases = Purchase.objects.filter(user=request.user)

    # Рассчитываем общую сумму
    total_price = sum(purchase.total_price for purchase in purchases)

    return render(request, 'pages/profile.html', {'info': info, 'purchases': purchases,
        'total_price': total_price})


@login_required
def add_to_cart(request):
    if request.method == "POST":
        drink_id = request.POST.get('drink_id')
        quantity = int(request.POST.get('quantity'))
        ingredients_ids = request.POST.getlist('ingredients')

        # Получаем напиток
        drink = Drink.objects.get(id=drink_id)

        if drink.available_portions < quantity:
            messages.error(request, "Недостаточно порций напитка. Пожалуйста, подождите пополнения.")
            return redirect('menu')

        # Получаем выбранные ингредиенты
        ingredients = Ingredient.objects.filter(id__in=ingredients_ids)

        # Рассчитываем общую цену
        total_price = drink.price * quantity

        if ingredients_ids:
            ingredients = Ingredient.objects.filter(id__in=ingredients_ids)
            for ingredient in ingredients:
                if ingredient.quantity == 0:
                    messages.error(request, f"Ингредиент {ingredient.name} отсутствует на складе.")
                    return redirect('menu')

        # Создаем покупку и добавляем в корзину
        purchase = Purchase.objects.create(
            user=request.user,
            drink=drink,
            quantity=quantity,
            total_price=total_price
        )

        if ingredients_ids:
            for ingredient in ingredients:
                purchase.ingredients.add(ingredient)
                ingredient.quantity -= 1  # Уменьшаем количество ингредиента
                ingredient.save()

        # Добавляем выбранные ингредиенты в покупку
        purchase.ingredients.set(ingredients)

        # Перенаправляем на страницу с корзиной
        return redirect('menu')  # Страница с корзиной или профилем

    return redirect('menu')  # Если метод не POST, то перенаправляем назад

@login_required
def cart(request):
    # Получаем все покупки для текущего пользователя
    purchases = Purchase.objects.filter(user=request.user)

    # Рассчитываем общую сумму
    total_price = sum(purchase.total_price for purchase in purchases)

    return render(request, 'cart.html', {
        'purchases': purchases,
        'total_price': total_price
    })

@login_required
def checkout(request):
    # Получаем все покупки для текущего пользователя
    purchases = Purchase.objects.filter(user=request.user)

    # Рассчитываем общую сумму
    total_price = sum(purchase.total_price for purchase in purchases)

    # Получаем аккаунт пользователя
    account = Account.objects.get(user=request.user)

    # Проверяем, достаточно ли средств на балансе
    if account.balance < total_price:
        messages.error(request, "Недостаточно средств на счете для оплаты!")
        return redirect('profile')  # Возвращаем на страницу корзины

    # Обрабатываем оплату
    account.withdraw(total_price)  # Списываем деньги с баланса

    # Обновляем количество напитков и ингредиентов
    for purchase in purchases:
        drink = purchase.drink
        # Уменьшаем количество напитков, если оно достаточно
        if drink.available_portions >= purchase.quantity:
            drink.reduce_portion(purchase.quantity)
        else:
            messages.error(request, f"Недостаточно порций для напитка {drink.name}.")
            return redirect('profile')

        # Уменьшаем количество только выбранных ингредиентов
        for ingredient in purchase.ingredients.all():
            if ingredient.quantity >= purchase.quantity:
                ingredient.quantity -= purchase.quantity
                ingredient.save()
            else:
                messages.error(request, f"Недостаточно ингредиента {ingredient.name}.")
                return redirect('profile')

    # Очищаем корзину (удаляем все покупки пользователя)
    purchases.delete()

    # Отправляем сообщение об успешной оплате
    messages.success(request, "Оплата прошла успешно!")

    # Перенаправляем на страницу профиля или меню
    return redirect('profile')


def clear_cart(request):
    if request.method == "POST":
        # Получаем все покупки текущего пользователя
        purchases = Purchase.objects.filter(user=request.user)

        for purchase in purchases:
            if purchase.quantity <= 0:  # Проверка на отрицательное или нулевое количество
                messages.error(request, "Неверное количество товара в корзине.")
                return redirect('profile')  # Перенаправляем обратно в корзину
        # Удаляем все товары из корзины
        purchases.delete()

        # Отправляем уведомление пользователю
        messages.success(request, "Корзина очищена.")
        return redirect('profile')