from django.urls import path

from . import views

app_name = "site_configuration"

# fmt: off
urlpatterns = [
    path("location/states", views.LocationStateListAPIView.as_view(), name="location-states"),
    path("location/cities", views.LocationCityListAPIView.as_view(), name="location-cities"),
    path("location/zip-codes", views.LocationZipCodeListAPIView.as_view(), name="location-zip-codes"),
    path("testimonials", views.TestimonialListAPIView.as_view(), name="testimonials"),
    path("faqs", views.FAQListAPIView.as_view(), name="faqs")
]
# fmt: on
