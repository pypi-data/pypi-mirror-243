from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError

# Create your models here.
class TreeNode(models.Model):
    data = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def add_child(self, child_node):
        # Ensure the child_node is a TreeNode instance
        if not isinstance(child_node, TreeNode):
            raise ValueError("child_node must be an instance of TreeNode")

        # Disassociate the child_node from any existing parent or tree
        if child_node.parent:
            child_node.parent = None
        child_node.save()

        # Set the child_node's parent to self and save
        child_node.parent = self
        child_node.save()

    def __str__(self):
        return self.data


class Tree(models.Model):
    root_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    root_object_id = models.PositiveIntegerField(null=True, blank=True)
    root_node = GenericForeignKey('root_content_type', 'root_object_id')


    def __init__(self, *args, root_node=None, **kwargs):
        super().__init__(*args, **kwargs)
        if root_node is not None:
            if not isinstance(root_node, TreeNode) or type(root_node) is TreeNode:
                raise ValueError("root_node must be an instance of TreeNode or its subclass")
            self.set_root_node(root_node)

    def save(self, *args, **kwargs):
        if not self.root_node:
            # Automatically create a new TreeNode as the root if not already set
            root_node = TreeNode.objects.create(data="Root Node")
            self.root_content_type = ContentType.objects.get_for_model(root_node)
            self.root_object_id = root_node.id
        super().save(*args, **kwargs)


    def set_root_node(self, node):
        if not isinstance(node, TreeNode) or type(node) is TreeNode:
            raise ValueError("node must be an instance of a TreeNode subclass")

        # Check if a Tree already exists with this node as root
        if Tree.objects.filter(root_content_type=ContentType.objects.get_for_model(type(node)), root_object_id=node.id).exists():
            raise ValidationError("This node is already set as a root for another tree")

        self.root_content_type = ContentType.objects.get_for_model(type(node))
        self.root_object_id = node.id
        self.save()


    def add_node(self, node, under):
        if not isinstance(node, TreeNode) or type(node) is TreeNode:
            raise ValueError("node must be an instance of a TreeNode subclass")

        if not isinstance(under, TreeNode) or type(under) is TreeNode:
            raise ValueError("node must be an instance of a TreeNode subclass")

        under.add_child(node)

    def __str__(self):
        return f'Tree with root: {self.root_node}'
