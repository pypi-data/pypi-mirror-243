from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .models import TreeNode, Tree
from .serializers import TreeNodeSerializer, TreeSerializer

class TreeNodeViewSet(viewsets.ModelViewSet):
    serializer_class = TreeNodeSerializer
    queryset = TreeNode.objects.all()

    @action(detail=True, methods=['post'])
    def add_child(self, request, pk=None):
        parent_node = self.get_object()
        child_data = request.data
        child_serializer = self.get_serializer(data=child_data)

        if child_serializer.is_valid():
            child_node = child_serializer.save()
            parent_node.add_child(child_node)
            return Response(child_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(child_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TreeViewSet(viewsets.ModelViewSet):
    serializer_class = TreeSerializer
    queryset = Tree.objects.all()



    @action(detail=True, methods=['post'])
    def add_node(self, request, pk=None):
        tree = self.get_object()
        node_text = request.data.get('node')
        under_id = request.data.get('under')

        try:
            under_node = TreeNode.objects.get(pk=under_id)
        except TreeNode.DoesNotExist:
            return Response({'error': 'TreeNode with the given ID does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        # Create a new TreeNode with the given text and add it under the 'under_node'
        new_node = TreeNode.objects.create(data=node_text)
        under_node.add_child(new_node)

        return Response({'status': 'Node added successfully'}, status=status.HTTP_200_OK)



from rest_framework import viewsets
from django.contrib.contenttypes.models import ContentType
from .models import Tree
from .serializers import TreeSerializer

# class GenericTreeViewSet(viewsets.ModelViewSet):
#
#     def __init__(self, *args, **kwargs):
#         self.serializer_class = kwargs.pop('serializer_class', TreeSerializer)
#         self.model = kwargs.pop('model', Tree)  # Default to Tree if no model is specified
#         super().__init__(*args, **kwargs)
#
#     def get_queryset(self):
#         return self.model.objects.all()
#
#     def perform_create(self, serializer):
#         # Dynamically determine the model class
#         model = self.model
#
#         # Ensure the model is a subclass of Tree
#         if not issubclass(model, Tree):
#             raise ValidationError("Invalid model type")
#
#         # Create an instance of the correct model
#         instance = model(**serializer.validated_data)
#         instance.save()

def customTreeViewSet(serializer_class, model):
    class GenericTreeViewSet(viewsets.ModelViewSet):
        def get_serializer_class(self):
            return serializer_class

        def get_model(self):
            return model

        def get_queryset(self):
            return self.get_model().objects.all()

        def perform_create(self, serializer):
            # Dynamically determine the model class
            model = self.get_model()

            # Ensure the model is a subclass of Tree
            if not issubclass(model, Tree):
                raise ValidationError("Invalid model type")

            # Create an instance of the correct model
            instance = model(**serializer.validated_data)
            instance.save()

        @action(detail=True, methods=['post'])
        def add_node(self, request, pk=None):
            tree = self.get_object()
            node_text = request.data.get('node')
            under_id = request.data.get('under')

            try:
                under_node = TreeNode.objects.get(pk=under_id)
            except TreeNode.DoesNotExist:
                return Response({'error': 'TreeNode with the given ID does not exist.'},
                                status=status.HTTP_404_NOT_FOUND)

            # Create a new TreeNode with the given text and add it under the 'under_node'
            new_node = TreeNode.objects.create(data=node_text)
            under_node.add_child(new_node)

            return Response({'status': 'Node added successfully'}, status=status.HTTP_200_OK)

    return GenericTreeViewSet

