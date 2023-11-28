# NetBox AutoNames Plugin

## Overview

The `netbox_autonames` plugin for NetBox automatically generates device names based on their Device Role. If the device name field is left empty during creation, the plugin will populate it using a pre-configured naming scheme and an incremental integer.

## Installation via pip

### Activate your virtual environment and install via pip:

```bash
$ source /opt/netbox/venv/bin/activate
(venv) $ pip install netbox_autonames
```

### To ensure the NetBox AutoNames plugin is automatically re-installed during future upgrades, add the package to your `local_requirements.txt`:

```bash
# echo netbox_autonames >> local_requirements.txt
```



## Manual Installation

1. Clone this repository.
    ```bash
    git clone https://github.com/yourusername/netbox_autonames.git
    ```

2. Install the plugin using pip.
    ```bash
    pip install .
    ```



## Configuration

1. Add the plugin to your `configuration.py`.
    ```python
    PLUGINS = [
        'netbox_autonames',
    ]
    ```

2. configure the map.
You can configure the naming scheme in your `configuration.py` under `PLUGINS_CONFIG`.

Here's an example configuration:

```python
PLUGINS_CONFIG = {
    'netbox_autonames': {
        'DEVICE_NAME_MAP': {
            'access-router': 'corou',
            'firewalls': 'cofwi',
            'l2-switch': 'coswi',
            'mpls-routers': 'compls',
            'isp-router': 'corou',
        }
    }
}
```

In this example, devices with Device Role `access-router` will be named starting with `corou`, followed by an incremental integer (e.g., `corou01`, `corou02`, etc.).

## Usage

Once configured, the plugin will automatically populate the device name field when creating a new device if it's left empty. The naming scheme is based on the Device Role and the `DEVICE_NAME_MAP` configuration.

## Contributing

Pull requests are welcome. For major changes, please open an issue first.

## License

This project is licensed under the AGPLv3 License.