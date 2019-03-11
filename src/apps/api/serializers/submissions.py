from os.path import basename
from rest_framework import serializers, fields

from competitions.models import Submission
from datasets.models import Data
from leaderboards.models import SubmissionScore


class SubmissionScoreSerializer(serializers.ModelSerializer):
    index = fields.IntegerField(source='column.index', read_only=True)

    class Meta:
        model = SubmissionScore
        fields = (
            'index',
            'score',
        )


class SubmissionSerializer(serializers.ModelSerializer):
    scores = SubmissionScoreSerializer(many=True)
    filename = fields.SerializerMethodField(read_only=True)

    class Meta:
        model = Submission
        fields = (
            'phase',
            'name',
            'filename',
            'description',
            'pk',
            'id',
            'created_when',
            'is_public',
            'status',
            'status_details',
            'scores',
            'leaderboard',
        )
        extra_kwargs = {
            "phase": {"read_only": True},
            "scores": {"read_only": True},
            "leaderboard": {"read_only": True},
        }

    def get_filename(self, instance):
        return basename(instance.data.data_file.name)


class SubmissionCreationSerializer(serializers.ModelSerializer):
    data = serializers.SlugRelatedField(queryset=Data.objects.all(), required=False, allow_null=True, slug_field='key')
    filename = fields.SerializerMethodField(read_only=True)

    class Meta:
        model = Submission
        fields = (
            'id',
            'data',
            'phase',
            'status',
            'status_details',
            'filename',
            'description',
            'secret',
        )
        extra_kwargs = {
            'secret': {"write_only": True},
            'description': {"read_only": True},
            # 'status': {"read_only": True},
        }

    def get_filename(self, instance):
        return basename(instance.data.data_file.name)

    # TODO: Validate the user is a participant in this competition.phase

    def create(self, validated_data):
        validated_data["owner"] = self.context['owner']
        sub = super().create(validated_data)
        sub.start()
        return sub

    def update(self, instance, validated_data):
        if instance.secret != validated_data.get('secret'):
            raise PermissionError("Submission secret invalid")

        print("Updated to...")
        print(validated_data)

        if validated_data["status"] == Submission.SCORING:
            # Start scoring because we're "SCORING" status now from compute worker
            from competitions.tasks import run_submission
            run_submission(instance.pk, is_scoring=True)
        return super().update(instance, validated_data)