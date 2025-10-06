from django.db import models
from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.

class Record(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    creation_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.first_name + " " + self.last_name
    

class TicketType(models.Model):
    """Defines the different types of tickets and their base prices."""
    name = models.CharField(max_length=50, unique=True) # e.g., 'Adult', 'Child', 'Senior'
    base_price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0.01)])

    def __str__(self):
        return f"{self.name} (${self.base_price})"

class Booking(models.Model):
    """Stores the details of a single ticket booking."""
    booking_date = models.DateField()
    adult_tickets = models.PositiveIntegerField(default=1)
    child_tickets = models.PositiveIntegerField(default=0)
    senior_tickets = models.PositiveIntegerField(default=0)
    customer_name = models.CharField(max_length=100)
    email = models.EmailField()
    # total_price is calculated and stored automatically
    total_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True) 

    def calculate_total_price(self):
        """Calculates and returns the total price for the booking based on current TicketType prices."""
        try:
            # Fetch prices dynamically
            prices = {t.name: t.base_price for t in TicketType.objects.all()}
            
            # Use .get() with a default of 0 to handle cases where a type might be missing
            adult_price = prices.get('Adult', 0)
            child_price = prices.get('Child', 0)
            senior_price = prices.get('Senior', 0)

            # Calculation
            adult_cost = self.adult_tickets * adult_price
            child_cost = self.child_tickets * child_price
            senior_cost = self.senior_tickets * senior_price
            
            return adult_cost + child_cost + senior_cost
            
        except Exception:
            # Fallback in case of database error or no prices defined
            return 0.00

    def save(self, *args, **kwargs):
        """Overrides save to automatically calculate total price before saving."""
        self.total_price = self.calculate_total_price()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking for {self.customer_name} on {self.booking_date}"

