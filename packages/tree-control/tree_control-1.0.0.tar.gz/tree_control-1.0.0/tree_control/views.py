from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Node, Tree
from .serializers import NodeSerializer, TreeSerializer

from django.db import transaction


# Create your views here.
class NodeViewSet(viewsets.ModelViewSet):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer

    @action(detail=False, methods=['post'])
    def set_order(self, request):
        node_orders = request.data  # Expecting format: { "20": 1, "21": 2, "32": 3 }
        try:
            with transaction.atomic():
                for node_id, order in node_orders.items():
                    Node.objects.filter(id=node_id).update(order=order)
            return Response({"message": "Node orders updated successfully."})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def add_node(self, request, pk=None):
        parent_node = self.get_object()
        node_data = {'text': request.data.get('value'), 'identifier': parent_node.identifier, 'parent': parent_node.id,
                     'forward_step_associations': [], 'order': request.data.get('order')}
        serializer = NodeSerializer(data=node_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def associate_node(self, request, pk=None):
        node = self.get_object()
        try:
            associated_node = Node.objects.get(id=request.data.get('id'))
            node.forward_node_associations.add(associated_node)
            return Response({"message": "Node associated successfully."})
        except Node.DoesNotExist:
            return Response({"error": "Node with given ID does not exist."}, status=status.HTTP_400_BAD_REQUEST)

    # @action(detail=True, methods=['post'])
    # def add_post_condition(self, request, pk=None):
    #     step = self.get_object()
    #     if step.children.exists() or step.forward_step_associations.exists():
    #         return Response({"error": "Step cannot have a post condition as it has children or associated steps."},
    #                         status=status.HTTP_400_BAD_REQUEST)
    #
    #     post_condition_data = {'post_condition': request.data.get('value'), 'step': step.id}
    #     serializer = PostConditionSerializer(data=post_condition_data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # @action(detail=True, methods=['delete'])
    # def clear_post_condition(self, request, pk=None):
    #     step = self.get_object()
    #     if hasattr(step, 'post_condition'):
    #         step.post_condition.delete()
    #         return Response({"message": "Post condition cleared successfully."})
    #     return Response({"error": "No post condition to clear."}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['delete'])
    def clear_associated_nodes(self, request, pk=None):
        node = self.get_object()
        node.forward_node_associations.clear()
        return Response({"message": "Associated nodes cleared successfully."})

    @action(detail=True, methods=['delete'])
    def delete_children(self, request, pk=None):
        node = self.get_object()
        node.children.all().delete()
        return Response({"message": "Children nodes deleted successfully."})


class TreeViewSet(viewsets.ModelViewSet):
    queryset = Tree.objects.all()
    serializer_class = TreeSerializer

    @action(detail=False, methods=['post'])
    def set_order(self, request):
        node_orders = request.data  # Expecting format: { "20": 1, "21": 2, "32": 3 }
        try:
            with transaction.atomic():
                for node_id, order in node_orders.items():
                    Node.objects.filter(id=node_id).update(order=order)
            return Response({"message": "Node orders updated successfully."})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def create_node(self, request, pk=None):
        tree = self.get_object()
        print(tree.identifier)
        node_data = {'text': request.data.get('value'), 'identifier': tree.identifier, 'tree': tree.id,
                     'forward_node_associations': [], 'order': request.data.get('order'), 'parent': None}
        print(node_data)
        serializer = NodeSerializer(data=node_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def create_tree(self, request):
        tree_identifier = request.data.get('identifier')

        tree_data = {'identifier': tree_identifier}
        serializer = self.get_serializer(data=tree_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
