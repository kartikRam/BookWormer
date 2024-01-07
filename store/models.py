from django.db import models

from django.contrib.auth.models import User

STATE_CHOICES = (
    ('Andaman & Nicobar Islands', 'Andaman & Nicobar Islands'),
    ( 'Andhra Pradesh' , 'Andhra Pradesh'),
    ('Arunachal Pradesh','Arunachal Pradesh'),
    ('Assam','Assam'),
    ('Bihar','Bihar'),
    ('Chandigarh','Chandigarh'),
    ('Chattisgarh','Chattisgarh'),
    ('Dadra & Nagar Haveli','Dadra & Nagar Haveli'),
    ('Daman & Diu','Daman & Diu'),
    ('Delhi','Delhi'),
    ('Goa','Goa'),
    ('Gujarat','Gujarat'),
    ('Haryana','Haryana'),
    ('Himachal Pradesh','Himachal Pradesh'),
    ('Jammu & Kashmir','Jammu & Kashmir'),
    ('Jharkhand', 'Jharkhand'),
    ('Karnataka','Karnataka'),
    ('Kerala','Kerala'),
    ('Lakshadweep','Lakshadweep'),
    ('Madhya Pradesh','Madhya Pradesh'),
    ('Maharashtra','Maharashtra'),
    ('Manipur','Manipur'),
    ('Meghalaya','Meghalaya'),
    ('Mizoram','Mizoram'),
    ('Nagaland','Nagaland'),
    ('Odisha','Odisha'),
    ('Puducherry','Puducherry'),
    ('Punjab','Punjab'),
    ('Rajasthan','Rajasthan'),
    ('Sikkim','Sikkim'),
    ('Tamil Nadu','Tamil Nadu'),
    ('Telangana','Telangana'),
    ('Tripura','Tripura'),
    ('Uttarakhand','Uttarakhand'),
    ('Uttar Pradesh','Uttar Pradesh'),
    ('West Bengal','West Bengal'),
)
GENRES=(
	('Fiction','Fiction'),('Action','Action'),
	('Adventure','Adventure'),('Alternate History','Alternate History'),
	('Anthology','Anthology'),
	('Bildungsroman','Bildungsroman'),('Children','Children'),
	('Comedy','Comedy'),('Commercial Fiction','Commercial Fiction'),('Crime','Crime'),
	('Drama','Drama'),('Dystopian','Dystopian'),('Fairy Tale','Fairy Tale'),('Fantasy','Fantasy'),
	('Gothic','Gothic'),
	('Historical Fiction','Historical Fiction'),('Horror','Horror'),
	('Inspirational','Inspirational'),('Magical Realism','Magical Realism'),
	('Mystery','Mystery'),('Mythology','Mythology'),('Poetry','Poetry'),('Romance','Romance'),)

STATUS=(
    ('0','Out for Delivery'),
    ('1','Delivered'),
    )

# Create your models here.
class Customer(models.Model):
    user=models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    name=models.CharField(max_length=200,null=True)
    email=models.CharField(max_length=200,null=True)
    phone=models.CharField(max_length=200,null=True)
    address=models.CharField(max_length=500,null=True)
    city=models.CharField(max_length=200,null=True)
    state=models.CharField(choices=STATE_CHOICES,max_length=50)
    profile_pic=models.ImageField(blank=True,null=True,default="author1.jpg")
    date_created=models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.name

class author(models.Model):
	name=models.CharField(max_length=200,null=True)
	details=models.CharField(max_length=500,null=True)
    
	def __str__(self):
		return self.name

class books(models.Model):

	name=models.CharField(max_length=200,null=True)
	description=models.CharField(max_length=500,null=True)
	genre=models.CharField(choices=GENRES,max_length=50)
	isbn=models.CharField(max_length=200,null=True)
	image=models.ImageField(blank=True,null=True,default="profile.jpg")
	price=models.IntegerField()
	author=models.ForeignKey(author, on_delete=models.CASCADE)
	
	def __str__(self):
		return self.name

class cart(models.Model):
    book=models.ForeignKey(books,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    price=models.IntegerField()

    def __str__(self):
        return self.book.name

class order(models.Model):
    book=models.ForeignKey(books,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    price=models.IntegerField()
    status=models.CharField(choices=STATUS,max_length=50,default='0')
    date_created=models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.book.name


