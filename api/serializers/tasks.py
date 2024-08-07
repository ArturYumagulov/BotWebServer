from rest_framework import serializers

from tasks import models as task_models


class AuthorCommentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = task_models.AuthorComments
        fields = "__all__"

    def create(self, validated_data):
        return task_models.AuthorComments.objects.create(**validated_data)


class WorkerCommentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = task_models.WorkerComments
        fields = "__all__"

    def create(self, validated_data):
        return self.Meta.model.objects.create(**validated_data)


class HeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = task_models.Head
        fields = "__all__"


class SupervisorSerializer(serializers.ModelSerializer):

    head = HeadSerializer()

    class Meta:
        model = task_models.Supervisor
        fields = ("code", "name", "chat_id", "phone", "head")

    def create(self, validated_data):
        return task_models.Supervisor.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.code = validated_data.get("code", instance.code)
        instance.name = validated_data.get("name", instance.name)
        instance.chat_id = validated_data.get("chat_id", instance.chat_id)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.save()

        return instance


class AllWorkerSerializer(serializers.ModelSerializer):

    supervisor = SupervisorSerializer()

    class Meta:
        model = task_models.Worker
        fields = (
            "code",
            "name",
            "chat_id",
            "phone",
            "controller",
            "partner",
            "supervisor",
        )


class WorkerSerializer(serializers.ModelSerializer):
    department = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = task_models.Worker
        fields = "__all__"


class PartnerWorkerSerializer(serializers.ModelSerializer):

    class Meta:
        model = task_models.PartnerWorker
        fields = ("name", "positions", "code")


class PartnerSerializer(serializers.ModelSerializer):

    workers = PartnerWorkerSerializer(many=True)

    class Meta:
        model = task_models.Partner
        fields = ("code", "name", "inn", "workers")

    def create(self, validated_data):
        workers_data = validated_data.pop("workers")
        partner = task_models.Partner.objects.create(**validated_data)
        for worker_data in workers_data:
            task_models.PartnerWorker.objects.create(partner=partner, **worker_data)
        return partner

    def update(self, instance, validated_data):
        workers_data = validated_data.pop("workers")
        instance.code = validated_data.get("code", instance.code)
        instance.name = validated_data.get("name", instance.name)
        instance.inn = validated_data.get("inn", instance.name)

        for worker in workers_data:
            task_models.PartnerWorker.objects.update(partner=instance, **worker)
        instance.save()
        return instance


class BasicSerializer(serializers.ModelSerializer):

    class Meta:
        model = task_models.Basics
        fields = "__all__"

    def create(self, validated_data):
        return task_models.Basics.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.number = validated_data.get("number", instance.number)
        instance.name = validated_data.get("name", instance.name)
        instance.date = validated_data.get("date", instance.date)
        instance.save()

        return instance


class ResultGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = task_models.ResultGroup
        fields = "__all__"


class ResultDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = task_models.ResultData
        fields = "__all__"


class ResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = task_models.Result
        fields = "__all__"


class TaskSerializer(serializers.ModelSerializer):

    base_tasks = BasicSerializer(read_only=True)
    partner_tasks = PartnerSerializer(read_only=True)
    task_worker = WorkerSerializer(read_only=True)
    task_author = WorkerSerializer(read_only=True)
    worker_comments = WorkerCommentsSerializer(read_only=True)
    author_comments = AuthorCommentsSerializer(read_only=True)

    class Meta:
        model = task_models.Task
        fields = "__all__"

    def create(self, validated_data):
        task = task_models.Task.objects.create(**validated_data)

        return task

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.number = validated_data.get("number", instance.number)
        instance.date = validated_data.get("date", instance.date)
        instance.status = validated_data.get("status", instance.status)
        instance.deadline = validated_data.get("deadline", instance.deadline)
        instance.base = validated_data.get("base", instance.base)
        instance.partner = validated_data.get("partner", instance.partner)
        instance.author_comment = validated_data.get(
            "author_comment", instance.author_comment
        )
        instance.worker_comment = validated_data.get(
            "worker_comment", instance.worker_comment
        )
        instance.edited = validated_data.get("edited", instance.edited)
        instance.worker = validated_data.get("worker", instance.worker)
        instance.author = validated_data.get("author", instance.author)
        instance.result = validated_data.get("result", instance.result)

        instance.save()

        return instance


class TaskListSerializer(serializers.ModelSerializer):

    base = BasicSerializer()
    partner = PartnerSerializer()
    worker = AllWorkerSerializer()
    author = AllWorkerSerializer()
    worker_comment = WorkerCommentsSerializer()
    author_comment = AuthorCommentsSerializer()
    result = ResultSerializer()

    class Meta:
        model = task_models.Task
        fields = "__all__"


class AllTaskListSerializer(serializers.ModelSerializer):

    author_comment = AuthorCommentsSerializer()
    worker_comment = WorkerCommentsSerializer()
    base = BasicSerializer(read_only=True)
    result = ResultSerializer(read_only=True)

    class Meta:
        model = task_models.Task
        fields = "__all__"

    def update(self, instance, validated_data):

        instance.status = validated_data.get("status", instance.status)
        instance.save()
        return instance


class TaskMessageUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = task_models.Task
        fields = ("number", "message_id")

    def update(self, instance, validated_data):
        instance.message_id = validated_data.get("message_id", instance.message_id)
        instance.save()

        return instance
