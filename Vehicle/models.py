from django.db import models

# Create your models here.
from django.urls import reverse
from Company import models as company_models
from setting import models as setting_models
from Employee import models as employee_models


class GeneralVehicle(models.Model):
    name = models.CharField(max_length=40, null=True, blank=True, unique=True)
    image = models.ImageField(upload_to='images/allvehicles', null=True, blank=True)
    company = models.ForeignKey(company_models.CompanyProfileModel, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.name


class Vehicle(models.Model):
    all_vehicle_name = models.ForeignKey(GeneralVehicle, on_delete=models.SET_NULL, null=True, blank=True,
                                         verbose_name='Vehicle Name')
    # all_vehicle_name = models.CharField(max_length=50, null=False, blank=False)
    image = models.ImageField(upload_to='images', null=True, blank=True)
    make = models.CharField(max_length=50, null=False, blank=False)
    # vehicle_type=models.CharField(max_length=10,null=False,blank=False,choices=vehicle_types,default='SEDAN')
    vehicle_type = models.ForeignKey(setting_models.VehicleType, on_delete=models.CASCADE, null=True, blank=True,
                                     verbose_name="Vehicle Type")
    is_on_ride = models.BooleanField(default=False, null=False)
    model_name = models.CharField(max_length=50, null=False, blank=False, verbose_name="Model")
    year = models.CharField(max_length=15, null=False, blank=False)
    license = models.CharField(max_length=40, null=False, blank=False)
    plate_number = models.CharField(max_length=50, null=False, blank=False,unique=True)
    vehicle_number = models.CharField(max_length=30, null=False, blank=False,unique=True)
    color = models.CharField(max_length=50, null=False, blank=False)
    vin = models.CharField(max_length=17, null=False, blank=False, verbose_name="VIN",unique=True)
    insurance_company = models.CharField(max_length=50, null=False, blank=False)
    tabs_expiration_date = models.CharField(max_length=30, null=False, blank=False,
                                            verbose_name="Registration expiration date")
    inspection_expiration_date = models.CharField(max_length=30, null=False, blank=False)
    company = models.ForeignKey(company_models.CompanyProfileModel, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)
    milage = models.IntegerField(null=True, blank=True, verbose_name="Mileage")
    last_ride_started_milage = models.IntegerField(null=True, blank=True)
    last_ride_ending_milage = models.IntegerField(null=True, blank=True)

    driver = models.ForeignKey(employee_models.EmployeeProfileModel, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        try:
            return str(self.all_vehicle_name.name)
        except:
            return "-"

    @property
    def name(self):
        return self.all_vehicle_name.name


def get_checklist_options():
    Satisfactory = "Satisfactory"
    Unsatisfactory = "Unsatisfactory"
    Good = "Good"
    Refilled = "Refilled"
    Replaced = "Replaced"
    options = [
        (Satisfactory, Satisfactory),
        (Unsatisfactory, Unsatisfactory),
        (Good, Good),
        (Refilled, Refilled),
        (Replaced, Replaced)
    ]
    return options


class Fluid(models.Model):
    options = get_checklist_options()
    anti_freeze = models.CharField(max_length=20, choices=options, null=True, blank=True,
                                   default=options[0][0])
    brake_fluid = models.CharField(max_length=20, choices=options, null=True, blank=True, default=options[0][0])
    oil_level = models.CharField(max_length=20, choices=options, null=True, blank=True, default=options[0][0])
    ps_fluid = models.CharField(max_length=20, choices=options, null=True, blank=True, default=options[0][0])
    washer_fluid = models.CharField(max_length=20, choices=options, null=True, blank=True, default=options[0][0])
    fluid_comments = models.TextField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.oil_level


class Light(models.Model):
    options = get_checklist_options()
    headlights_Lo = models.CharField(max_length=20, choices=options, null=True, blank=True, default=options[0][0])
    headlights_Hi = models.CharField(max_length=20, choices=options, null=True, blank=True, default=options[0][0])
    turn_signal_Lt = models.CharField(max_length=20, choices=options, null=True, blank=True, default=options[0][0])
    turn_signal_Rt = models.CharField(max_length=20, choices=options, null=True, blank=True, default=options[0][0])
    hazard_lights = models.CharField(max_length=20, choices=options, null=True, blank=True, default=options[0][0])
    Interior_lights = models.CharField(max_length=20, choices=options, null=True, blank=True, default=options[0][0])
    brake_lights = models.CharField(max_length=20, choices=options, null=True, blank=True, default=options[0][0])
    light_comments = models.TextField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.brake_lights


class BrakeTyre(models.Model):
    options = get_checklist_options()
    brakes = models.CharField(max_length=20, choices=options, null=True, blank=True, default=options[0][0])
    rims = models.CharField(max_length=20, choices=options, null=True, blank=True, default=options[0][0])
    tyres = models.CharField(max_length=20, choices=options, null=True, blank=True, default=options[0][0])
    wear = models.CharField(max_length=20, choices=options, null=True, blank=True, default=options[0][0])
    break_comments = models.TextField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.brakes


class Misc(models.Model):
    options = get_checklist_options()
    doors = models.CharField(max_length=20, choices=options, null=True, blank=True, default=options[0][0])
    heater = models.CharField(max_length=20, choices=options, null=True, blank=True, default=options[0][0])
    horn = models.CharField(max_length=20, choices=options, null=True, blank=True, default=options[0][0])
    mirrors = models.CharField(max_length=20, choices=options, null=True, blank=True, default=options[0][0])
    seats = models.CharField(max_length=20, choices=options, null=True, blank=True, default=options[0][0])
    seat_belts = models.CharField(max_length=20, choices=options, null=True, blank=True, default=options[0][0])
    steering = models.CharField(max_length=20, choices=options, null=True, blank=True, default=options[0][0])
    windows = models.CharField(max_length=20, choices=options, null=True, blank=True, default=options[0][0])
    windshield = models.CharField(max_length=20, choices=options, null=True, blank=True, default=options[0][0])
    wiperblades = models.CharField(max_length=20, choices=options, null=True, blank=True, default=options[0][0])
    misc_comments = models.TextField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.steering


class Checklist(models.Model):
    options = get_checklist_options()
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True)
    driver = models.ForeignKey(employee_models.EmployeeProfileModel, on_delete=models.SET_NULL, null=True, blank=True)
    fluids = models.ForeignKey(Fluid, null=True, on_delete=models.SET_NULL, blank=True)
    lights = models.ForeignKey(Light, null=True, on_delete=models.SET_NULL, blank=True)
    brake_and_tyres = models.ForeignKey(BrakeTyre, null=True, on_delete=models.SET_NULL, blank=True)
    misc = models.ForeignKey(Misc, null=True, on_delete=models.SET_NULL, blank=True)
    other = models.TextField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def check_list_title(self):
        return "Checklist #{}".format(self.id)
