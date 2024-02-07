from django.utils import timezone

import pytz
from rest_framework import serializers

from django.conf import settings

from census.models import Census, CarsList, OilList, ProviderList, FilterList, AccessoriesCategoryItem, \
    AccessoriesCategory, PointTypes, PointVectors, STOTypeList, PointCategory, CensusFiles, CompanyDatabase, VolumeItem, \
    Volume, EquipmentList, Department, PointVectorsItem
from tasks.models import Task, Basics, Partner, Worker, AuthorComments, WorkerComments, Result, PartnerWorker, \
    ResultGroup, ResultData, Supervisor  # noqa


class AuthorCommentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = AuthorComments
        fields = '__all__'

    def create(self, validated_data):
        return AuthorComments.objects.create(**validated_data)


class WorkerCommentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkerComments
        fields = '__all__'

    def create(self, validated_data):
        return self.Meta.model.objects.create(**validated_data)


class WorkerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Worker
        fields = "__all__"


class SupervisorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Supervisor
        fields = "__all__"

    def create(self, validated_data):
        return Supervisor.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.code = validated_data.get('code', instance.code)
        instance.name = validated_data.get('name', instance.name)
        instance.chat_id = validated_data.get('chat_id', instance.chat_id)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.save()

        return instance


class PartnerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Partner
        fields = ('code', 'name', 'inn')

    def create(self, validated_data):
        return Partner.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.code = validated_data.get('code', instance.code)
        instance.name = validated_data.get('name', instance.name)
        instance.inn = validated_data.get('inn', instance.name)
        instance.save()

        return instance


class PartnerWorkerSerializer(serializers.ModelSerializer):

    class Meta:
        model = PartnerWorker
        fields = "__all__"

    def create(self, validated_data):
        return PartnerWorker.objects.create(**validated_data)


class BasicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Basics
        fields = "__all__"

    def create(self, validated_data):
        return Basics.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.number = validated_data.get('number', instance.number)
        instance.name = validated_data.get('name', instance.name)
        instance.date = validated_data.get('date', instance.date)
        instance.save()

        return instance


class ResultGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = ResultGroup
        fields = "__all__"


class ResultDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = ResultData
        fields = "__all__"


class ResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = Result
        fields = "__all__"


class TaskSerializer(serializers.ModelSerializer):

    base_tasks = BasicSerializer(read_only=True)
    partner_tasks = PartnerSerializer(read_only=True)
    task_worker = WorkerSerializer(read_only=True)
    task_author = WorkerSerializer(read_only=True)
    worker_comments = WorkerCommentsSerializer(read_only=True)
    author_comments = AuthorCommentsSerializer(read_only=True)

    class Meta:
        model = Task
        fields = '__all__'

    def create(self, validated_data):
        task = Task.objects.create(**validated_data)

        return task

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.number = validated_data.get('number', instance.number)
        instance.date = validated_data.get('date', instance.date)
        instance.status = validated_data.get('status', instance.status)
        instance.deadline = validated_data.get('deadline', instance.deadline)
        instance.base = validated_data.get('base', instance.base)
        instance.partner = validated_data.get('partner', instance.partner)
        instance.author_comment = validated_data.get('author_comment', instance.author_comment)
        instance.worker_comment = validated_data.get('worker_comment', instance.worker_comment)
        instance.edited = validated_data.get('edited', instance.edited)
        instance.worker = validated_data.get('worker', instance.worker)
        instance.author = validated_data.get('author', instance.author)
        instance.result = validated_data.get('result', instance.result)

        instance.save()

        return instance


class TaskListSerializer(serializers.ModelSerializer):

    base = BasicSerializer()
    partner = PartnerSerializer()
    worker = WorkerSerializer()
    author = WorkerSerializer()
    worker_comment = WorkerCommentsSerializer()
    author_comment = AuthorCommentsSerializer()
    result = ResultSerializer()

    class Meta:
        model = Task
        fields = '__all__'


class AllTaskListSerializer(serializers.ModelSerializer):

    author_comment = AuthorCommentsSerializer()
    worker_comment = WorkerCommentsSerializer()
    base = BasicSerializer()
    result = ResultSerializer(read_only=True)

    class Meta:
        model = Task
        fields = '__all__'

    def update(self, instance, validated_data):

        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance


class AccessoriesCategoryItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = AccessoriesCategoryItem
        fields = ('name',)


class PointVectorsSerializer(serializers.ModelSerializer):

    class Meta:
        model = PointVectors
        fields = ('name',)


class CensusFilesSerializer(serializers.ModelSerializer):

    class Meta:
        model = CensusFiles
        fields = ('file',)


class DadataSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyDatabase
        fields = '__all__'


class VolumeItemSerializer(serializers.ModelSerializer):

    volume = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = VolumeItem
        fields = ('volume', 'value')


class PointVectorItemsSerializer(serializers.ModelSerializer):

    value = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    vectors = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = PointVectorsItem
        fields = ('vectors', 'value',)


class CensusSerializer(serializers.ModelSerializer):
    department = serializers.SlugRelatedField(slug_field='name', read_only=True)
    cars = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)
    oils = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)
    providers = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)
    filters = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)
    accessories_brands = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    point_type = serializers.SlugRelatedField(slug_field='name', read_only=True)
    vector = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    sto_type = serializers.SlugRelatedField(slug_field='name', read_only=True)
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    accessories_category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    equipment = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)
    files = CensusFilesSerializer(many=True)
    result = ResultSerializer()
    dadata = DadataSerializer()
    volume = VolumeItemSerializer(many=True)
    vectors = PointVectorItemsSerializer(many=True)

    class Meta:
        model = Census
        fields = [
            'department',
            'closing',
            'not_communicate',
            'address_id',
            'point_name',
            'point_type',
            'sto_type',
            'cars',
            'oils',
            'filters',
            'accessories_category',
            'accessories_brands',
            'elevators_count',
            'oil_debit',
            'lukoil_debit',
            'rowe_debit',
            'motul_debit',
            'vitex_debit',
            'decision_firstname',
            'decision_lastname',
            'decision_surname',
            'decision_email',
            'decision_phone',
            'decision_function',
            'other_brand',
            'akb_specify',
            'working',
            'task',
            'id',
            'accessories_brands',
            'accessories_category',
            'category',
            'vector',
            'equipment',
            'filters',
            'point_type',
            'sto_type',
            'files',
            'providers',
            'result',
            'dadata',
            'volume',
            'vectors'
        ]
