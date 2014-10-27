from rest_framework import serializers
from models import Circle, Topic, Participant
from django.contrib.auth.models import User

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ('headline', )

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', )

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ('member', )

    member = UserSerializer()


class CircleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Circle
        fields = ('topics', 'participants', 'circle_members', 'board_members')
        depth = 2
    circle_members = serializers.SerializerMethodField('get_circle_members')
    board_members = serializers.SerializerMethodField('get_board_members')

    def get_circle_members(self, obj):
        return obj.participants.circle_members()

    def get_board_members(self, obj):
        return MemberSerializer(Participant.objects.board_members(obj), many=True).data

    #topics = TopicSerializer(many=True)
    #participants = ParticipantSerializer(many=True)

    #aliens = AlienSerializer(many=True)




