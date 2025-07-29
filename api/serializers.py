from rest_framework import serializers
from .models import User, Assignment, Submission
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class AssignmentSerializer(serializers.ModelSerializer):
    teacher = serializers.ReadOnlyField(source='teacher.id')
    class Meta:
        model = Assignment
        fields = '__all__'

    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters long.")
        return value

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'

    def validate_answer(self, value):
        if not value.strip():
            raise serializers.ValidationError("Answer cannot be empty.")
        return value
