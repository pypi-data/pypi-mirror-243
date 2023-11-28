from django.db.models.signals import pre_save
from django.dispatch import receiver
from dcim.models import Device
from django.conf import settings
import re

@receiver(pre_save, sender=Device)
def auto_generate_device_name(sender, instance, **kwargs):
    try:
        if not instance.name:
            role = instance.role.slug
            device_name_map = settings.PLUGINS_CONFIG['netbox_autonames'].get('DEVICE_NAME_MAP', {})
            prefix = device_name_map.get(role)
            if prefix:
                pattern = re.compile(f'^{prefix}(\d+)$')
                existing_devices = Device.objects.filter(role__slug=role)
                max_num = 0
                for device in existing_devices:
                    if device.name is None:
                        continue
                    match = pattern.match(device.name)
                    if match:
                        num = int(match.group(1))
                        if num > max_num:
                            max_num = num
                next_num = max_num + 1
                instance.name = f"{prefix}{next_num:04d}"
    except Exception as e:
        pass
