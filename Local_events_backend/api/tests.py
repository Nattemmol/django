from django.test import TestCase
from .models import User, Category, Event, Guest
from django.utils import timezone


class UserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="password123",
            name="Test User"
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, "testuser@example.com")
        self.assertTrue(self.user.check_password("password123"))
        self.assertEqual(self.user.name, "Test User")
        self.assertFalse(self.user.is_staff)

    def test_superuser_creation(self):
        superuser = User.objects.create_superuser(
            email="admin@example.com",
            password="admin123",
            name="Admin User"
        )
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)


class CategoryTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            id="1",
            name="Music",
            icon_name="music_note"
        )

    def test_category_creation(self):
        self.assertEqual(self.category.name, "Music")
        self.assertEqual(self.category.icon_name, "music_note")


class EventTestCase(TestCase):
    def setUp(self):
        # Set up the user and category for the event
        self.user = User.objects.create_user(
            email="eventuser@example.com",
            password="password123",
            name="Event User"
        )
        self.category = Category.objects.create(
            id="1",
            name="Music",
            icon_name="music_note"
        )
        self.event = Event.objects.create(
            id="1",
            image_path="/images/event.jpg",
            title="Test Event",
            description="This is a test event.",
            location="Test Location",
            date=timezone.now(),
            duration="2 hours",
            punch_line1="Fun times!",
            punch_line2="Don't miss it!",
            host=self.user
        )
        self.event.categories.add(self.category)

    def test_event_creation(self):
        self.assertEqual(self.event.title, "Test Event")
        self.assertEqual(self.event.description, "This is a test event.")
        self.assertEqual(self.event.location, "Test Location")
        self.assertEqual(self.event.host, self.user)
        self.assertIn(self.category, self.event.categories.all())


class GuestTestCase(TestCase):
    def setUp(self):
        # Create a user and guest
        self.guest = Guest.objects.create(
            id="1",
            name="John Doe",
            email="johndoe@example.com",
            image_path="/images/john.jpg"
        )

    def test_guest_creation(self):
        self.assertEqual(self.guest.name, "John Doe")
        self.assertEqual(self.guest.email, "johndoe@example.com")
        self.assertEqual(self.guest.image_path, "/images/john.jpg")


class EventGuestRelationTestCase(TestCase):
    def setUp(self):
        # Create user, category, event, and guest
        self.user = User.objects.create_user(
            email="eventuser@example.com",
            password="password123",
            name="Event User"
        )
        self.category = Category.objects.create(
            id="1",
            name="Music",
            icon_name="music_note"
        )
        self.event = Event.objects.create(
            id="1",
            image_path="/images/event.jpg",
            title="Test Event",
            description="This is a test event.",
            location="Test Location",
            date=timezone.now(),
            duration="2 hours",
            punch_line1="Fun times!",
            punch_line2="Don't miss it!",
            host=self.user
        )
        self.event.categories.add(self.category)

        self.guest = Guest.objects.create(
            id="1",
            name="John Doe",
            email="johndoe@example.com",
            image_path="/images/john.jpg"
        )
        self.event.guests.add(self.guest)

    def test_guest_addition_to_event(self):
        self.assertIn(self.guest, self.event.guests.all())


class CategoryEventRelationTestCase(TestCase):
    def setUp(self):
        # Create a category
        self.category = Category.objects.create(
            id="1",
            name="Music",
            icon_name="music_note"
        )
        
        # Create a user to be the host of the event
        self.user = User.objects.create_user(
            email="eventuser@example.com",
            password="password123",
            name="Event User"
        )

        # Create an event and associate it with the category and user (host)
        self.event = Event.objects.create(
            id="1",
            image_path="/images/event.jpg",
            title="Test Event",
            description="This is a test event.",
            location="Test Location",
            date=timezone.now(),
            duration="2 hours",
            punch_line1="Fun times!",
            punch_line2="Don't miss it!",
            host=self.user  # Make sure to assign a host here
        )
        self.event.categories.add(self.category)

    def test_event_category_association(self):
        # Test that the event is correctly associated with the category
        self.assertIn(self.category, self.event.categories.all())
        # Optionally check if the event has the correct host
        self.assertEqual(self.event.host, self.user)
