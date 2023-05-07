from rest_framework import serializers
from os_windows.models import OS_Windows


class OS_Windows_Serializer(serializers.ModelSerializer):

    class Meta:
        model = OS_Windows
        fields = ('computer_id', 'username', 'computer_name', 'product_key', 'hostname', 'ip_address', 'mac_address', 'softwares_installed', 'software_count', 'authentic_software_count', 'unauthentic_software_count')

