from django.db import models



class Register(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    company_name = models.CharField(max_length=100)
    address = models.TextField()
    role = models.CharField(max_length=3)
    password = models.CharField(max_length=128)  # Store hashed password
    created_at = models.DateTimeField(auto_now_add=True)

    def set_password(self, raw_password):
        self.password = raw_password


    def save(self, *args, **kwargs):
        # Hash the password before saving
        # if not self.password.startswith('pbkdf2_sha256$'):
        #     self.password = make_password(self.password)
        super(Register, self).save(*args, **kwargs)

    def __str__(self):
        return self.full_name
    