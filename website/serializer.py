from rest_framework import serializers

class BackgroundTasksSerializer(serializers.Serializer):
    task_name = serializers.CharField(max_length=200)
    class Meta:
        fields = ['task_name']


class SearchDestinationOutputSerializer(serializers.ListSerializer):
    def to_representation(self, instance):
        response = []
        for place in instance:
            if "destination_name" in dir(place):
                data = {"destination": place.destination_name,
                        "id": place.destination_id,
                        "type": place.destination_type}
            elif "country_name" in dir(place):
                data = {"destination":place.country_name,
                        "id":place.country_code,
                        "type":"country"}
            elif "city_name" in dir(place):
                data = {"destination": place.city_name,
                        "id": place.city_code,
                        "type":"city"}

            response.append(data)

        return response



class SearchDestinationSerializer(serializers.Serializer):
    data = serializers.JSONField()
    class Meta:
        fields = ['data']
        list_serializer_class = SearchDestinationOutputSerializer