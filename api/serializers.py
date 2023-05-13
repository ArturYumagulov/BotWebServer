from rest_framework import serializers
from tasks.models import Task, Basics, Partner, Worker, AuthorComments, WorkerComments  # noqa


class AuthorCommentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = AuthorComments
        fields = '__all__'

    def create(self, validated_data):
        return AuthorComments.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('comment', instance.name)
        instance.number = validated_data.get('author', instance.author)
        instance.save()
        return instance


class WorkerCommentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkerComments
        fields = '__all__'

    def create(self, validated_data):
        return self.Meta.model.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('comment', instance.name)
        instance.number = validated_data.get('worker', instance.worker)
        instance.save()
        return instance


class WorkerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Worker
        fields = "__all__"

    def create(self, validated_data):
        return Worker.objects.create(**validated_data)

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
        fields = "__all__"

    def create(self, validated_data):
        return Partner.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.number = validated_data.get('number', instance.number)
        instance.name = validated_data.get('name', instance.name)
        instance.date = validated_data.get('date', instance.date)
        instance.save()

        return instance


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

        task = Task.objects.create(
            number=validated_data.get('number'),
            name=validated_data.get('name'),
            date=validated_data.get('date'),
            status=validated_data.get('status'),
            deadline=validated_data.get('deadline'),
            base=validated_data.get('base'),
            partner=validated_data.get('partner'),
            author_comment=validated_data.get('author_comment'),
            author=validated_data.get('author'),
            worker=validated_data.get('worker'),
            worker_comment=validated_data.get('worker_comment')
            )

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

        instance.save()

        return instance
