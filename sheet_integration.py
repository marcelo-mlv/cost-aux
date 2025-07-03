import pandas as pd
from anytree import Node, RenderTree

def load_BOM_df(filename):
    path = './' + filename
    df = pd.read_excel(path, sheet_name='BOM', header=5, dtype=str)
    return df

def preprocess(df):
    # Remove white rows (sum of a subsystem)
    df = df[df['Asm/Prt #'].notna()]
    return df

def create_hierarchy(df):
    # Root: Parent of all subsystems
    BOM_root = Node("BOM", parent=None)
    subsystem_nodes = {}
    assembly_nodes = {}

    for _, row in df.iterrows():
        subsystem = row['Area of Commodity']
        asm_prt = row['Asm/Prt #']
        component = row['Component']

        # Create subsystem node if it doesn't exist already
        if subsystem not in subsystem_nodes:
            subsystem_nodes[subsystem] = Node(subsystem, parent=BOM_root)

        # Create assembly node as child of subsystem node
        if asm_prt[0] == 'A': # Assembly
            assembly_nodes[component] = Node(component, parent=subsystem_nodes[subsystem])
        # Part (under an assembly)
        elif assembly_nodes:
            Node(component, parent=list(assembly_nodes.values())[-1])
        # If no assembly node exists, raise an error
        else:
            raise ValueError(f"Component {component} does not have a parent assembly. The first BOM row is probably a Part.")
    return BOM_root

def get_BOM_df(filename):
    BOM_raw = load_BOM_df(filename)
    BOM_data = preprocess(BOM_raw)
    return BOM_data

def get_BOM_tree(filename):
    BOM_data = get_BOM_df(filename)
    BOM_root = create_hierarchy(BOM_data)
    return BOM_root

def save_tree_to_txt(filename):
    BOM_root = get_BOM_tree(filename)
    with open("bom_tree.txt", "w", encoding="utf-8") as f:
        for pre, _, node in RenderTree(BOM_root):
            f.write(f"{pre}{node.name}\n")
    