from rest_framework import serializers
from .models import Job, CustomUser
from .models import Employer, Candidate




class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'
        extra_kwargs = {
            'employer': {'required': False}   # ✅ FIX
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'phone', 'role']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)
    


# class CandidateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Candidate
#         fields = '__all__'
#         read_only_fields = ['user']

#     def validate_expected_salary(self, value):
#         if value and value < 0:
#             raise serializers.ValidationError("Salary must be positive")
#         return value

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = '__all__'
        read_only_fields = ['user']

    def validate_resume(self, value):
        # file size limit (2MB)
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError("File too large (max 2MB)")

        # file type check
        if not value.name.endswith(('.pdf', '.doc', '.docx')):
            raise serializers.ValidationError("Only PDF/DOC/DOCX allowed")

        return value
    
    


class EmployerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = '__all__'
        read_only_fields = ['user']