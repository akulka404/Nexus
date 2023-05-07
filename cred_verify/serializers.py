from rest_framework import serializers
from cred_verify.models import CRED_VERIFY


class CRED_VERIFY_Serializer(serializers.ModelSerializer):

    class Meta:
        model = CRED_VERIFY
        fields = ('name', 'email', 'username', 'password', 'type_login')
