from rest_framework import serializers

from tree_control.models import Tree, Node


class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = '__all__'

    forward_node_associations = serializers.PrimaryKeyRelatedField(many=True, queryset=Node.objects.all())
    parent = serializers.PrimaryKeyRelatedField(queryset=Node.objects.all(), allow_null=True)

    children = serializers.SerializerMethodField()

    def get_children(self, obj):
        # This method will be used to serialize the children
        children = obj.children.all()  # Assuming 'children' is the related name in the model
        return NodeSerializer(children, many=True).data

    def validate(self, data):
        """
        Ensure that the type of the step matches the type of its parent.
        """
        if data.get('parent') and data.get('identifier') != data['parent'].identifier:
            raise serializers.ValidationError("The type of the node should match the type of its parent.")
        return data

class TreeSerializer(serializers.ModelSerializer):
    children = NodeSerializer(many=True, read_only=True)

    class Meta:
        model = Tree
        fields = ['id', 'identifier', 'children']
