from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username} - Balance: {self.balance}"

    def deposit(self, amount):
        self.balance += amount
        self.save()

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            self.save()
            return True
        return False



class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=0)  # количество порций

    def __str__(self):
        return f"{self.name} ({self.quantity} порций)"

    def add_quantity(self, amount):
        self.quantity += amount
        self.save()

    def reduce_quantity(self, amount):
        if self.quantity >= amount:
            self.quantity -= amount
            self.save()
            return True
        return False



class Drink(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    available_portions = models.PositiveIntegerField(default=0)
    ingredients = models.ManyToManyField(Ingredient, related_name='drinks')
    photo = models.ImageField(upload_to='images/%Y/%m/%d/', default=True, verbose_name='Фото')

    def __str__(self):
        return f"{self.name} - Price: {self.price} - Available: {self.available_portions} порций"

    def reduce_portion(self, amount):
        if self.available_portions >= amount:
            self.available_portions -= amount
            self.save()
            return True
        return False



class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    drink = models.ForeignKey(Drink, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    ingredients = models.ManyToManyField(Ingredient, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.drink.name} - {self.quantity} шт"
