from rest_framework import serializers
from models import Circle, Topic, Participant
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', )

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ('uuid', 'headline', 'applicant', 'summary', 'created', 'sponsor', 'opened', 'closed')

    applicant = UserSerializer()
    sponsor = UserSerializer()

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ('member', )

    member = UserSerializer()

class CircleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Circle
        #fields = ('topics', 'circle_members', 'board_members', 'members', 'aliens')
        depth = 2

    topics = TopicSerializer()
    circle_members = serializers.SerializerMethodField('get_circle_members')
    board_members = serializers.SerializerMethodField('get_board_members')
    members = serializers.SerializerMethodField('get_members')
    aliens = serializers.SerializerMethodField('get_aliens')

    def get_circle_members(self, obj):
        return obj.participants.circle_members()

    def get_board_members(self, obj):
        return obj.participants.board_members()

    def get_members(self, obj):
        return obj.participants.all()

    def get_aliens(self, obj):
        return []

    #topics = TopicSerializer(many=True)
    #participants = ParticipantSerializer(many=True)

    #aliens = AlienSerializer(many=True)




