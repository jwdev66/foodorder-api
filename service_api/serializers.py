from django.contrib.auth.models import User
from rest_framework import serializers

from service_api.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('birth_date', 'gender', 'phone_number', 'city', 'is_manager')


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'profile',)
        extra_kwargs = {'first_name': {'allow_null': False, 'required': True, 'allow_blank': False},
                        'last_name': {'allow_null': False, 'required': True, 'allow_blank': False},
                        'profile': {'allow_null': False, 'required': True, 'allow_blank': False},
                        'password': {'allow_null': False, 'required': True, 'allow_blank': False, 'write_only': True},
                        'id': {'read_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        Profile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        profile = instance.profile

        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.set_password(validated_data.get('password'))

        profile.gender = profile_data.get('birth_date', profile.birth_date)
        profile.gender = profile_data.get('gender', profile.gender)
        profile.gender = profile_data.get('phone_number', profile.phone_number)
        profile.gender = profile_data.get('city', profile.city)
        profile.gender = profile_data.get('manager', profile.manager)

        instance.save()

        profile.save()

        return instance