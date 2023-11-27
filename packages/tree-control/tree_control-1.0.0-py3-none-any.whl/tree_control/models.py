
from django.db import models

class Tree(models.Model):
    identifier = models.CharField(max_length=255)  # Use StepType Enum for choices


class Node(models.Model):
    text = models.TextField()
    identifier = models.CharField(max_length=255, null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', null=True, blank=True)  # For the hierarchical tree structure
    forward_node_associations = models.ManyToManyField('self', blank=True, related_name='backward_node_associations')  # For associating nodes
    tree = models.ForeignKey(Tree, on_delete=models.CASCADE, related_name='children', null=True, blank=True)
    order = models.IntegerField()
    # Custom method to ensure MAIN cannot have children of ALTERNATE or EXCEPTION
    # def add_child(self, child):
    #     if self.type == StepType.MAIN.value and (child.type == StepType.ALTERNATE.value or child.type == StepType.EXCEPTION.value):
    #         raise ValueError("A MAIN step cannot have children of type ALTERNATE or EXCEPTION")
    #     self.children.add(child)

