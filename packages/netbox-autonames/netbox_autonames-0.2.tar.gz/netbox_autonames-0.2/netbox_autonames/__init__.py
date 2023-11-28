from extras.plugins import PluginConfig


class NetboxAutoNamesConfig(PluginConfig):
    name = 'netbox_autonames'
    verbose_name = 'NetBoxAutoNames'
    version = '0.1'
    description = 'Auto-generate names for devices in NetBox based on their role.'
    base_url = ''
    required_settings = ['DEVICE_NAME_MAP']
    min_version = '2.10.0'

    def ready(self):
        import netbox_autonames.signals


config = NetboxAutoNamesConfig
