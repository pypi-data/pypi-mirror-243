from rest_framework import serializers
from .models import TreeNode, Tree

class TreeNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreeNode
        fields = ['id', 'data', 'parent', 'children']


    children = serializers.SerializerMethodField()

    def get_children(self, obj):
        # This method will be used to serialize the children
        children = obj.children.all()  # Assuming 'children' is the related name in the model
        return TreeNodeSerializer(children, many=True).data

class TreeSerializer(serializers.ModelSerializer):
    root_node = TreeNodeSerializer(read_only=True)

    class Meta:
        model = Tree
        fields = ['id', 'root_node']


