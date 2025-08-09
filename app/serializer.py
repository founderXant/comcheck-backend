from rest_framework import serializers
from app.models import PDFDocument

class ScrapePDFSerializer (serializers.ModelSerializer):
    class Meta:
        model = PDFDocument
        fields = '__all__'

class BuildingAreaSerializer (serializers.Serializer):
    description = serializers.CharField(max_length=200)
    
    class Meta:
        fields = '__all__'


class UserInputsSerializer (serializers.Serializer):
    is_residential = serializers.BooleanField()
    radio_btns = serializers.DictField()
    is_swinging_door = serializers.BooleanField()
    window_area = serializers.ListField(child=serializers.IntegerField())
    r_values = serializers.DictField()
    
    
    class Meta:
        fields = '__all__'
    

