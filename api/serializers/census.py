from rest_framework import serializers

from census import models as census_models
from .tasks import ResultSerializer


class PointVectorsSerializer(serializers.ModelSerializer):

    class Meta:
        model = census_models.PointVectors
        fields = ('name',)


class CensusFilesSerializer(serializers.ModelSerializer):

    class Meta:
        model = census_models.CensusFiles
        fields = ('file',)


class DadataSerializer(serializers.ModelSerializer):

    class Meta:
        model = census_models.CompanyDatabase
        fields = '__all__'


class VolumeItemSerializer(serializers.ModelSerializer):

    volume = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = census_models.VolumeItem
        fields = ('volume', 'value')


class PointVectorItemsSerializer(serializers.ModelSerializer):

    value = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    vectors = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = census_models.PointVectorsItem
        fields = ('vectors', 'value',)


class OtherSerializer(serializers.ModelSerializer):
    class Meta:
        model = census_models.Others
        fields = ("equipment_name", "volume_name", "volume_value", 'vector', 'access_brand', 'providers')


class DecisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = census_models.Decision
        fields = ('firstname', 'lastname', 'surname', 'email', 'phone', 'function')


class EquipmentSerializer(serializers.ModelSerializer):

    equipment = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = census_models.EquipmentItem
        fields = ('equipment', 'value',)


class PartnerShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = census_models.Partner
        fields = ('code', 'name', 'inn')


class CensusSerializer(serializers.ModelSerializer):
    department = serializers.SlugRelatedField(slug_field='name', read_only=True)
    working = PartnerShortSerializer(read_only=True)
    cars = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)
    providers = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)
    point_type = serializers.SlugRelatedField(slug_field='name', read_only=True)
    sto_type = serializers.SlugRelatedField(slug_field='name', read_only=True)
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    equipment = EquipmentSerializer(many=True)
    files = CensusFilesSerializer(many=True)
    result = ResultSerializer()
    dadata = DadataSerializer()
    volume = VolumeItemSerializer(many=True)
    vectors = PointVectorItemsSerializer(many=True)
    others = OtherSerializer()
    decision = DecisionSerializer()

    class Meta:
        model = census_models.Census
        fields = [
            'id',
            'address_id',
            'department',
            'closing',
            'not_communicate',
            'edited',
            'loaded',
            'inn',
            'point_name',
            'address',
            'edit_date',
            'created_date',
            'organizations_name',
            'name',
            'position',
            'point_type',
            'nets',
            'sto_type',
            'elevators_count',
            'akb_specify',
            'tender',
            'working',
            'task',
            'basics',
            'category',
            'decision',
            'cars',
            'equipment',
            'point_type',
            'sto_type',
            'files',
            'providers',
            'result',
            'volume',
            'vectors',
            'others',
            'dadata',
        ]


class CensusUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = census_models.Census
        fields = ('loaded',)

    def update(self, instance, validated_data):
        instance.loaded = validated_data.get('loaded', instance.loaded)
        instance.save()

        return instance


class AddressesCountSerializer(serializers.ModelSerializer):

    class Meta:
        model = census_models.AddressesCount
        fields = '__all__'
