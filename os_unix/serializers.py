from rest_framework import serializers
from os_unix.models import OS_UNIX


class OS_UNIX_Serializer(serializers.ModelSerializer):

    class Meta:
        model = OS_UNIX
        fields = ('computer_id', 'computer_name', 'os_version', 'serial_number', 'build_version', 'hardware_uuid', 'provisioning_udid', 'hostname', 'ip_address', 'mac_address',
                  'softwares_installed', 'software_count', 'authentic_software_count', 'unauthentic_software_count')
