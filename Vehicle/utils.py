import os
from Vehicle.models import GeneralVehicle
from PIL import Image
from io import BytesIO
from django.core.files import File
from django.core.files.base import ContentFile



def populate_images():
    path = '/home/lc/PycharmProjects/limoucloud-backend/Vehicle/Fleets'
    image_path = "Vehicle/Fleets/"
    files = os.listdir(image_path)
    all_vehicles = GeneralVehicle.objects.all()
    for vehicle in all_vehicles:
        path = str(vehicle.name) + '.png'
        if path in files:
            final_path = "{}{}".format(image_path, path)
            image = Image.open(final_path)
            blob = BytesIO()
            image.save(blob, 'PNG')
            vehicle.image.save(path, ContentFile(blob.getvalue()))
            # vehicle.save()
        else:
            pass
