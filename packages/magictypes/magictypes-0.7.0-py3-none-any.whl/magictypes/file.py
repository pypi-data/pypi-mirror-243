import ast
import astunparse
# from rich import print

class TypeAnnotator(ast.NodeTransformer):
    def __init__(self):
        super().__init__()
        self.mode = "discover"
        self.discovered = {"global": { }}
        self.classes = {}
        self.state = []
        self.current = "global"

    def visit_ClassDef(self, node):
        self.current = node.name
        if self.mode == "discover":
            self.discovered[node.name] = {}
            for f in node.body:
                self.discovered[node.name][f.name] = {}
                self.state.append(f.name)

            self.classes[node.name] = {}
        return self.generic_visit(node)

    def visit_FunctionDef(self, node):
        # Annotate function arguments
        if self.mode == "discover":
            # print(node.name)
            if node.name not in self.discovered:
                self.discovered[self.current][node.name] = {}

            # if node.args.vararg:
            #     print('antes')
            #     print(self.discovered[node.name])
            #     self.discovered[node.name].append({"arg_name": node.args.vararg.arg,"type":{'Any'}})
            #     print('depois')
            #     print(self.discovered[node.name])

            for arg in node.args.args:
                if arg.arg == "self":
                    continue
                # create a new key named by argument name
                self.discovered[self.current][node.name][arg.arg] = {}

                # Try to undercover already existence of annotations into arguments
                try:
                    self.discovered[self.current][node.name][arg.arg]["type"] = {arg.annotation.id}
                except AttributeError:
                    pass

            defaults = node.args.defaults
            for a, d in zip(
                defaults, node.args.args[len(node.args.args) - len(defaults) :]
            ):
                self.discovered[self.current][node.name][d.arg].update(
                    {"type": {type(a.value).__name__}}
                )

            # exist return in this function?
            if isinstance(node.body[-1], ast.Return):
                v = node.body[-1].value
                if isinstance(v, ast.Constant):
                    self.discovered[self.current][node.name]["return"] = type(v.value).__name__
                else:
                    self.discovered[self.current][node.name]["meta"] = type(v).__name__
                    self.discovered[self.current][node.name]["return"] = {
                        type(vx.value).__name__ for vx in v.elts
                    }

        else:
            # print(f'Based on: {self.discovered[node.name]}')
            for arg in node.args.args:
                if arg.arg == "self":
                    continue
                # print(node.name)
                scope = self.current
                if node.name not in self.discovered[scope]:
                    scope = "global"

                d = self.discovered[scope][node.name][arg.arg]
                if isinstance(d["type"], set):
                    typ = (
                        f'Union[ {", ".join(d["type"])} ]'
                        if len(d["type"]) > 1
                        else tuple(d["type"])[0]
                    )
                    arg.annotation = ast.Name(id=typ, ctx=ast.Load())
                else:
                    arg.annotation = ast.Name(id=d["type"], ctx=ast.Load())

            ret = self.discovered[scope][node.name]["return"]
            if ret:
                if isinstance(ret, set):
                    d = self.discovered[self.current][node.name]
                    if "meta" in d:
                        typ = (
                            f'{d["meta"]}[ {", ".join(ret)} ]'
                            if len(ret) > 1
                            else tuple(ret)[0]
                        )
                    else:
                        typ = (
                            f'Union[ {", ".join(ret)} ]' if len(ret) > 1 else tuple(ret)[0]
                        )
                    node.returns = ast.Name(id=typ, ctx=ast.Load())
                else:
                    node.returns = ast.Name(id=ret, ctx=ast.Load())
        
        # clean up state current in class
        if len(self.state):
            # print(self.state)
            self.state.remove(node.name)
            if len(self.state) == 0:
                # print('seting global')
                self.current = "global"

        return self.generic_visit(node)

    def visit_Assign(self, node):
        # armazena nome de objeto associado a classe
        if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name):
            if node.value.func.id in self.classes:
                self.classes[node.value.func.id]["instance"] = node.targets[0].id
                # self.discovered[node.value.func.id]["instance"] = node.targets[0].id

        if isinstance(node.value, ast.Constant):
            typ = type(node.value.value).__name__
        elif (
            isinstance(node.value, ast.List)
            or isinstance(node.value, ast.Set)
            or isinstance(node.value, ast.Dict)
            or isinstance(node.value, ast.Tuple)
        ):
            typ = type(node.value).__name__
        else:
            return self.generic_visit(node)
        
        # Replace the Assign node with the AnnAssign node
        ann_assign_node = ast.AnnAssign(
            target=node.targets[0],
            annotation=ast.Name(id=typ, ctx=ast.Load()),
            value=node.value,
            simple=1,
        )
        return ann_assign_node

    def visit_Call(self, node):
        # Annotate function calls
        if isinstance(node.func, ast.Name):
            ref = node.func.id
            # construtor geralmente não é chamado pelo __init__
            if ref in self.discovered and ref in self.classes:
                # del self.classes[ref]
                ref = '__init__'
            
            scope = node.func.id
            if node.func.id not in self.discovered:
                scope = "global"

            for arg, pos in zip(node.args, self.discovered[scope][ref]):
                pos = self.discovered[scope][ref][pos]
                if isinstance(arg, ast.Constant):
                    pos["type"] = type(arg.value).__name__
                else:
                    pos["meta"] = type(arg).__name__
                    pos["type"] = { type(vx.value).__name__ for vx in arg.elts }

        elif isinstance(node.func, ast.Attribute):
            ref = [key for key, value in self.classes.items() if value['instance'] == node.func.value.id][0]
            for arg, pos in zip(node.args, self.discovered[ref][node.func.attr]):
                pos = self.discovered[ref][node.func.attr][pos]
                if isinstance(arg, ast.Constant):
                    pos["type"] = type(arg.value).__name__
                else:
                    pos["meta"] = type(arg).__name__
                    pos["type"] = { type(vx.value).__name__ for vx in arg.elts }

        return self.generic_visit(node)


def annotate_types(script):
    tree = ast.parse(script)
    t = TypeAnnotator()
    tree = t.visit(tree)
    t.mode = ""
    tree = t.visit(tree)
    return astunparse.unparse(tree)

