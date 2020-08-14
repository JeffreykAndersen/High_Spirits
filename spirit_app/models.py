from django.db import models
import re 
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class LeadManager(models.Manager):
    def basic_validator(self,postData):
        errors={}
        # NAME VALIDATOR
        if len(postData['first_name'])<1:
            errors['first_name'] = "First Name is Required"
        if len(postData['last_name'])<1:
            errors['last_name'] = "Last Name is Required"
        # EMAIL VALIDATIONS
        if len(postData['email'])< 1:
             errors['email'] = "Email is required."
        if not EMAIL_REGEX.match(postData['email']):  
            errors['email'] = "Invalid email address."
        existing_email = self.filter(email=postData['email'])
        if existing_email:
            errors['email'] = "Email already in use."
        # PASSWORD VALIDATOR
        if len(postData['password'])< 8:
            errors['password'] = "Password must be at least 8 characters."
        if postData['password'] != postData['confirm_password']:
            errors['confirm'] = "Passwords do not match."
        return errors

    def register(self, postData):
        hashed_password = bcrypt.hashpw(postData['password'].encode(),bcrypt.gensalt()).decode()
        Lead.objects.create(
            first_name = postData['first_name'],
            last_name = postData['last_name'],
            email = postData['email'],
            password = hashed_password
        )
    
    def authenticate(self, email, password):
        users_with_email = self.filter(email=email)
        if not users_with_email:
            return False
        logged_user = users_with_email[0]
        return bcrypt.checkpw(password.encode(), logged_user.password.encode())

class AlcoholManager(models.Manager):
    def validator(self,postData):
        errors={}
        if len(postData['brand'])<1:
            errors['brand'] = "Please provide the name of the alcohol."
        if postData['alcohol_type'] =="null": 
            errors['alcohol_type'] = "Please select a category."
        if len(postData['cost'])<1: 
            errors['cost'] = "Please enter the bottle price."
        return errors
    
    def add_alcohol(self, postData):
        the_cost = float(postData['cost'])
        if postData['alcohol_type'] == "Fruit Juice":
            per_oz = (the_cost / 25.3605)
            per_oz_round = round(per_oz, 2)
            Alcohol.objects.create(
            brand = postData['brand'],
            alcohol_type = postData['alcohol_type'],
            cost = the_cost,
            ppo = per_oz_round
        )
        if postData['alcohol_type'] == "Simple Syrup":
            per_oz = (the_cost / 25.3605)
            per_oz_round = round(per_oz, 2)
            Alcohol.objects.create(
            brand = postData['brand'],
            alcohol_type = postData['alcohol_type'],
            cost = the_cost,
            ppo = per_oz_round
        )
        else: 
            the_cost = round((the_cost * .205)+2.83+ the_cost, 2)
            per_oz = (the_cost / 25.3605)
            per_oz_round = round(per_oz, 2)
            Alcohol.objects.create(
                brand = postData['brand'],
                alcohol_type = postData['alcohol_type'],
                cost = the_cost,
                ppo = per_oz_round
            )

class CocktailManager(models.Manager):
    def validator(self,postData):
        errors={}
        if len(postData['name']) < 1:
            errors['name'] = "Every drink needs a name"
        if len(postData['desc']) < 15: 
            errors['desc'] = "Please be a little more descriptive"
        # figure outr how to store a fe ingredients and validate
        return errors
    
    def add_cocktail(self, postData):
        Cocktail.objects.create(
            name = postData['name'],
            desc = postData['desc'],
        )
        
class Lead(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    objects = LeadManager()

# class Tender(models.Model):
#     first_name = models.CharField(max_length=255)
#     last_nme = models.CharField(max_length=255)
#     email = models.CharField(max_length=255)
#     password = models.CharField(max_length=255)
#     created_on = models.DateTimeField(auto_now_add=True)
#     updated_on = models.DateTimeField(auto_now=True)

class Cocktail(models.Model):
    name = models.CharField(max_length=255)
    desc = models.TextField()
    # ADD THIS LATER
    # photo = models.FileField(upload_to= "media", null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    objects = CocktailManager()


class Alcohol(models.Model):
    brand = models.CharField(max_length=255)
    alcohol_type = models.CharField(max_length=255)
    cost = models.FloatField()
    ppo = models.FloatField()
    # photo = models.FileField(upload_to= "media", null=True, blank=True)
    owned = models.ManyToManyField(Lead,related_name="bottles_owned")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    objects = AlcoholManager()

class Drink_Ingredient(models.Model):
    liquor = models.ForeignKey(Alcohol, related_name='ingredient', on_delete=models.CASCADE, null = True, blank = True)
    quantity = models.FloatField(null = True, blank = True)
    cocktail = models.ForeignKey(Cocktail, related_name="ingredients", on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


