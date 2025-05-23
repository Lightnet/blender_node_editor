# working...

import bpy
from bpy.types import NodeTree, Node, NodeSocketFloat, Operator
from bpy.utils import register_class, unregister_class
from nodeitems_utils import NodeCategory, register_node_categories, unregister_node_categories, NodeItem

# Custom Node Tree
class CustomNodeTree(NodeTree):
    bl_idname = "CustomNodeTree"
    bl_label = "Custom Node Tree"
    bl_icon = "NODETREE"

# Custom Node (Multiplies input by a value)
class CustomNode(Node):
    bl_idname = "CustomNodeType"
    bl_label = "Custom Multiply Node"
    bl_icon = "SOUND"

    my_float_prop: bpy.props.FloatProperty(name="Value", default=1.0, update=lambda self, context: self.update())
    my_title_prop: bpy.props.StringProperty(name="Title", default="Multiply Node")

    def init(self, context):
        self.inputs.new("NodeSocketFloat", "Input")
        self.outputs.new("NodeSocketFloat", "Output")

    def draw_buttons(self, context, layout):
        layout.prop(self, "my_float_prop")
        layout.prop(self, "my_title_prop")

    def update(self):
        if self.inputs[0].is_linked and self.outputs[0].is_linked:
            input_value = self.inputs[0].default_value
            self.outputs[0].default_value = input_value * self.my_float_prop

    def draw_label(self):
        return self.my_title_prop

# Custom Node 2 (Multiplies input by a value, similar to CustomNode)
class CustomNode2(Node):
    bl_idname = "CustomNodeType2"
    bl_label = "Custom Multiply Node 2"
    bl_icon = "PLUS"

    my_float_prop: bpy.props.FloatProperty(name="Value", default=1.0, update=lambda self, context: self.update())
    my_title_prop: bpy.props.StringProperty(name="Title", default="Multiply Node 2")

    def init(self, context):
        self.inputs.new("NodeSocketFloat", "Input")
        self.outputs.new("NodeSocketFloat", "Output")

    def draw_buttons(self, context, layout):
        layout.prop(self, "my_float_prop")
        layout.prop(self, "my_title_prop")

    def update(self):
        if self.inputs[0].is_linked and self.outputs[0].is_linked:
            input_value = self.inputs[0].default_value
            self.outputs[0].default_value = input_value * self.my_float_prop

    def draw_label(self):
        return self.my_title_prop

# Operator to create a new CustomNodeTree
class OBJECT_OT_CreateCustomNodeTree(Operator):
    bl_idname = "object.create_custom_node_tree"
    bl_label = "Create Custom Node Tree"

    def execute(self, context):
        node_tree = bpy.data.node_groups.new("CustomNodeTree", "CustomNodeTree")
        for area in context.screen.areas:
            if area.type == "NODE_EDITOR":
                area.spaces.active.tree_type = "CustomNodeTree"
                area.spaces.active.node_tree = node_tree
                break
        return {'FINISHED'}

# Debug function to print node categories
def print_node_categories():
    from nodeitems_utils import node_categories_iter
    print("Registered Node Categories:")
    for cat in node_categories_iter(context=None):
        print(f"  Category: {cat.identifier}")
        for item in cat.items(context=None):
            print(f"    - Item: {item.label} ({item.nodetype})")
            # print(dir(item))
            # print(f"    - Item: {item.label} ({item.type})")# it has no type for NodeItem

# Node Category for Menu
class CustomNodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == "CustomNodeTree"

node_categories = [
    CustomNodeCategory("CUSTOM_NODES", "Custom Nodes", items=[
        NodeItem("CustomNodeType"),
        NodeItem("CustomNodeType2"),
        # {"label": "Custom Multiply Node", "type": CustomNode.bl_idname},
    ])
]

def cleanup_custom_node_trees():
    """Remove all CustomNodeTree instances to ensure clean unregistration."""
    for tree in bpy.data.node_groups:
        if tree.bl_idname == "CustomNodeTree":
            bpy.data.node_groups.remove(tree)

def is_category_registered(category_id):
    """Check if a node category is already registered."""
    from nodeitems_utils import node_categories_iter
    for cat in node_categories_iter(context=None):
        if cat.identifier == category_id:
            return True
    return False

# List of classes for registration
classes = [
    CustomNodeTree,
    CustomNode,
    CustomNode2,
    OBJECT_OT_CreateCustomNodeTree
]

def register():
    # Register classes
    for cls in classes:
        if not hasattr(bpy.types, cls.bl_idname):
            register_class(cls)

    register_node_categories("CUSTOM_NODES", node_categories)
    # Register node categories
    # if not is_category_registered("CUSTOM_NODES"):
    #     register_node_categories("CUSTOM_NODES", node_categories)
    # else:
    #     print("Node categories 'CUSTOM_NODES' already registered, skipping registration.")

    # Print node categories for debugging
    print_node_categories()

def unregister():
    # testing see log 
    print("======================")
    print("CLEAN UP...")
    print("======================")
    # Unregister node categories first
    if is_category_registered("CUSTOM_NODES"):
        try:
            print("CLEAN UP register_node_categories CUSTOM_NODES")
            unregister_node_categories("CUSTOM_NODES")
        except Exception as e:
            print(f"Failed to unregister node categories: {e}")

    # Remove any lingering CustomNodeTree instances
    cleanup_custom_node_trees()

    # Unregister classes in reverse order
    for cls in reversed(classes):
        if hasattr(bpy.types, cls.bl_idname):
            try:
                unregister_class(cls)
            except Exception as e:
                print(f"Failed to unregister {cls.__name__}: {e}")
    print("CUSTOM_NODES: ", is_category_registered("CUSTOM_NODES"))

if __name__ == "__main__":
    # Clean up before registering to avoid conflicts
    unregister()
    register()