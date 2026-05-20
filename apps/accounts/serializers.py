from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User

# ── Registration ──────────────────────────────────────────────────────
class RegisterSerializer(serializers.ModelSerializer):
    password  = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, label='Confirm password')

    class Meta:
        model  = User
        fields = ['email','name','role','password','password2']
        extra_kwargs = {'role': {'required': False}}

    def validate(self, data):
        if data['password'] != data.pop('password2'):
            raise serializers.ValidationError({'password2': 'Passwords do not match'})
        return data

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

# ── Login ─────────────────────────────────────────────────────────────
class LoginSerializer(serializers.Serializer):
    email    = serializers.EmailField()
    password = serializers.CharField(write_only=True)

# ── Public profile (read-only, safe to return in responses) ──────────
class UserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = ['id','name','role','created_at']

# ── Full profile (authenticated user viewing/editing their own data) ──
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = ['id','email','name','role','is_verified','created_at']
        read_only_fields = ['id','email','role','is_verified','created_at']

# ── Change password ───────────────────────────────────────────────────
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Old password is incorrect')
        return value

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save(update_fields=['password'])
