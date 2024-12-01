from django.db import models
from django.db.models import Q, F
from django.utils.timezone import now
from datetime import timedelta


class Customer(models.Model):
    username = models.CharField(max_length=100, verbose_name="იუზერნეიმი")
    first_name = models.CharField(max_length=100, verbose_name="სახელი", default="")
    email = models.EmailField("ელ.ფოსტის მისამართი", unique=True)
    is_active = models.BooleanField("აქტიურია", default=False)

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f"{self.first_name} ".strip() or self.email

    @staticmethod
    def username_contains_string_and_is_active(contained_string):
        """
        TODO: Write a query using Q objects to filter customers 
        whose usernames contain a specific string (case-insensitive) 
        AND who are active.
        """
        return Customer.objects.filter(
            Q(username__icontains=contained_string) & Q(is_active=True)
        )

    @staticmethod
    def update_username_to_email():
        """
        TODO: Write a query using F expressions to update all customers' usernames 
        to match their email addresses.
        """
        Customer.objects.update(username=F("email"))

    @staticmethod
    def deactivate_customers_with_short_usernames(min_length):
        """
        TODO: Write a query using F expressions to deactivate customers whose 
        username length is less than a specified minimum length.
        """
        Customer.objects.filter(username__length__lt=min_length).update(is_active=False)

    @staticmethod
    def load_customers_without_email():
        """
        TODO: Write a query using defer() to load customers without retrieving their email field.
        """
        return Customer.objects.defer("email")

    @staticmethod
    def customers_with_active_status_raw(active=True):
        """
        TODO: Write a raw SQL query to return customers based on their active status.
        """
        return Customer.objects.raw(
            "SELECT * FROM customer WHERE is_active = %s", [active]
        )

    @staticmethod
    def get_first_n_customers(n):
        """
        TODO: Write a query to retrieve the first n customers using queryset slicing.
        """
        return Customer.objects.all()[:n]

    @staticmethod
    def sort_customers_by_username():
        """
        TODO: Write a query using order_by() to sort customers by their username in ascending order.
        """
        return Customer.objects.order_by("username")

    get_full_name.verbose_name = "სრული სახელი"

    class Meta:
        ordering = ("-id",)
        verbose_name = "მომხმარებელი"
        verbose_name_plural = "მომხმარებლები"


class Stadium(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    address = models.CharField(max_length=100, null=False, blank=False)
    capacity = models.IntegerField(null=False)

    def __str__(self):
        return self.name

    @staticmethod
    def stadiums_with_name_and_capacity(name, min_capacity):
        """
        TODO: Write a query using Q objects to return stadiums whose name contains 
        a specific string (case-insensitive) AND whose capacity is greater than a specified amount.
        """
        return Stadium.objects.filter(
            Q(name__icontains=name) & Q(capacity__gt=min_capacity)
        )

    @staticmethod
    def double_capacity_for_large_stadiums(min_capacity):
        """
        TODO: Write a query using F expressions to double the capacity of stadiums 
        whose current capacity is greater than a specified minimum value.
        """
        Stadium.objects.filter(capacity__gt=min_capacity).update(
            capacity=F("capacity") * 2
        )

    @staticmethod
    def increase_capacity_by_sold_tickets(event_id):
        """
        TODO: Write a query using F expressions to increase the capacity of the stadium 
        for a specific event by the number of tickets sold for that event.
        """
        pass

    @staticmethod
    def load_stadiums_without_address():
        """
        TODO: Write a query using defer() to load stadiums without retrieving their address field.
        """
        return Stadium.objects.defer("address")

    @staticmethod
    def stadiums_filtered_by_capacity_raw(min_capacity):
        """
        TODO: Write a raw SQL query to return stadiums with a capacity greater than a specified value.
        """
        return Stadium.objects.raw(
            "SELECT * FROM stadium WHERE capacity > %s", [min_capacity]
        )

    @staticmethod
    def get_top_n_stadiums_by_capacity(n):
        """
        TODO: Write a query to retrieve the top n stadiums sorted by capacity in descending order.
        """
        return Stadium.objects.order_by("-capacity")[:n]


    @staticmethod
    def sort_stadiums_by_name():
        """
        TODO: Write a query using order_by() to sort stadiums by their name in ascending order.
        """
        return Stadium.objects.order_by("name")


class Event(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    date = models.DateTimeField(null=False, blank=False)
    stadium = models.ForeignKey(Stadium, null=False, blank=False, on_delete=models.DO_NOTHING)
    is_active = models.BooleanField("აქტიურია", null=False, default=True)

    def __str__(self):
        return self.name

    @staticmethod
    def extend_event_dates_by_days(days):
        """
        TODO: Write a query using F expressions to extend the dates of all events 
        by a specified number of days.
        """
        Event.objects.update(date=F("date") + timedelta(days=days))


    @staticmethod
    def deactivate_past_events():
        """
        TODO: Write a query using F expressions to mark events as inactive if their 
        date is in the past.
        """
        Event.objects.filter(date__lt=now()).update(is_active=False)


    @staticmethod
    def adjust_event_name_with_stadium_name():
        """
        TODO: Write a query using F expressions to append the stadium name 
        to the event name for all events.
        """
        pass

    @staticmethod
    def load_events_without_stadium():
        """
        TODO: Write a query using defer() to load events without retrieving the stadium field.
        """
        return Event.objects.defer("stadium")


    @staticmethod
    def events_with_date_in_future_raw():
        """
        TODO: Write a raw SQL query to return events whose date is in the future.
        """
        return Event.objects.raw("SELECT * FROM event WHERE date > NOW()")


    @staticmethod
    def get_upcoming_events(limit):
        """
        TODO: Write a query to retrieve a limited number of upcoming events sorted by date.
        """
        return Event.objects.filter(date__gte=now()).order_by("date")[:limit]


    @staticmethod
    def sort_events_by_name():
        """
        TODO: Write a query using order_by() to sort events by their name in ascending order.
        """
        return Event.objects.order_by("name")



class Ticket(models.Model):
    customer = models.ForeignKey(Customer, null=False, blank=False, on_delete=models.DO_NOTHING)
    event = models.ForeignKey(Event, null=False, blank=False, on_delete=models.CASCADE)
    bought_at = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.customer} -- {self.event}"

    @staticmethod
    def tickets_by_customer_or_event(customer_id, event_id):
        """
        TODO: Write a query using Q objects to return tickets bought by a 
        specific customer OR for a specific event.
        """
        return Ticket.objects.filter(Q(customer_id=customer_id) | Q(event_id=event_id))


    @staticmethod
    def recent_tickets_excluding_event(event_id, days=30):
        """
        TODO: Write a query using Q objects to return tickets purchased 
        in the last specified number of days, but exclude those for a specified event.
        """
        return Ticket.objects.filter(
            Q(bought_at__gte=now() - timedelta(days=days)) & ~Q(event_id=event_id)
        )

    @staticmethod
    def apply_bulk_discount_to_recent_tickets(days=30, discount_percent=10):
        """
        TODO: Write a query using F expressions to reduce the price of tickets 
        purchased in the last specified number of days by a given percentage.
        """
        Ticket.objects.filter(bought_at__gte=now() - timedelta(days=days)).update(
            price=F("price") * (1 - discount_percent / 100)
        )

    @staticmethod
    def transfer_tickets_to_another_customer(old_customer_id, new_customer_id):
        """
        TODO: Write a query using F expressions to update the customer field 
        of tickets from one customer to another.
        """
        Ticket.objects.filter(customer_id=old_customer_id).update(customer_id=new_customer_id)


    @staticmethod
    def load_tickets_without_event():
        """
        TODO: Write a query using defer() to load tickets without retrieving the event field.
        """
        return Ticket.objects.defer("event")


    @staticmethod
    def tickets_for_event_raw(event_id):
        """
        TODO: Write a raw SQL query to return tickets for a specific event.
        """
        return Ticket.objects.raw(
            "SELECT * FROM ticket WHERE event_id = %s", [event_id]
        )

    @staticmethod
    def get_recent_tickets(limit):
        """
        TODO: Write a query to retrieve a limited number of recent tickets sorted by purchase date.
        """
        return Ticket.objects.order_by("-bought_at")[:limit]


    @staticmethod
    def sort_tickets_by_customer_name():
        """
        TODO: Write a query using order_by() to sort tickets by the customer name in ascending order.
        """
        return Ticket.objects.order_by("customer__username")

