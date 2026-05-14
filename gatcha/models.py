from django.db import models


class User(models.Model):
    user_id = models.BigAutoField(primary_key=True)
    email = models.CharField(max_length=100)
    nickname = models.CharField(max_length=50)
    currency_balance = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "users"


class GatchaType(models.Model):
    gatcha_id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    class Meta:
        db_table = "gatcha_type"


class GatchaItemList(models.Model):
    item_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    grade = models.CharField(max_length=10)
    description = models.TextField()

    class Meta:
        db_table = "gatcha_item_list"


class GatchaPoolItem(models.Model):
    pool_item_id = models.BigAutoField(primary_key=True)
    gatcha = models.ForeignKey(GatchaType, on_delete=models.CASCADE, db_column="gatcha_id")
    item = models.ForeignKey(GatchaItemList, on_delete=models.CASCADE, db_column="item_id")
    drop_rate = models.DecimalField(max_digits=5, decimal_places=4)

    class Meta:
        db_table = "gatcha_pool_item"


class UserGatchaRecord(models.Model):
    record_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id")
    gatcha = models.ForeignKey(GatchaType, on_delete=models.CASCADE, db_column="gatcha_id")
    item = models.ForeignKey(GatchaItemList, on_delete=models.CASCADE, db_column="item_id")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user_gatcha_record"


class UserItemList(models.Model):
    inventory_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id")
    item = models.ForeignKey(GatchaItemList, on_delete=models.CASCADE, db_column="item_id")
    quantity = models.IntegerField(default=1)
    acquired_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user_item_list"
