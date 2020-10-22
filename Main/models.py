from django.db import models


class User(models.Model):
  first_name = models.CharField(max_length=20)
  second_name = models.CharField(max_length=20)
  patronymic = models.CharField(max_length=20)
  birth_date = models.DateField()
  email = models.EmailField(unique=True)
  password = models.CharField(max_length=30)
  company = models.CharField(max_length=20)
  position = models.CharField(max_length=20)
  SEX = (
    (1, 'м'),
    (2, 'ж'),
  )
  sex = models.IntegerField(choices=SEX)
  is_su = models.BooleanField()
  created_date = models.DateField(auto_now=True)
  
  def __str___(self):
    return self.first_name


class Photo(models.Model):
  user = models.ForeignKey(User, on_delete = models.CASCADE)
  photo_path = models.ImageField(upload_to='media/') # may be bugs bc of MEDIA_ROOT or MEDIA_URL
  well= models.CharField(max_length=20) 
  depth = models.IntegerField()
  KINDS = (
    (1, 'daylight'),
    (2, 'ultraviolet'),
  )
  kind = models.IntegerField(choices=KINDS)


class Model(models.Model):
  user = models.ForeignKey(User, on_delete = models.CASCADE)
  is_default = models.BooleanField()
  name = models.CharField(max_length=20)


class Mask(models.Model):
  user = models.ForeignKey(User, on_delete = models.CASCADE)
  photo = models.ForeignKey(Photo, on_delete = models.CASCADE)
  classification_path = models.FilePathField() # ??? it's json 
  path = models.FilePathField()  # ??? it's numpy array
  likes = models.PositiveSmallIntegerField()
  model = models.ManyToManyField(Model, db_table='Model_to_mask')
