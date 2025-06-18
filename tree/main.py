from __future__ import annotations

from localizations import translate, find_key

from collections import deque
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from _typeshed import SupportsAllComparisons


class TreeNode[T: SupportsAllComparisons]:

    def __init__(self, value: T, parent: TreeNode[T] | None = None) -> None:
        self.__value: T = value
        self.__parent: TreeNode[T] | None = parent
        self.__children: list[TreeNode[T]] = list()

    @property
    def value(self) -> T:
        return self.__value

    @value.setter
    def value(self, new: T) -> None:
        self.__value = new

    @property
    def parent(self) -> TreeNode[T]:
        return self.__parent

    @parent.setter
    def parent(self, parent: TreeNode[T]):
        self.__parent = parent

    @property
    def children(self) -> list[TreeNode[T]]:
        return self.__children

    @children.setter
    def children(self, children: list[TreeNode[T]]):
        self.__children = children

    def add_child(self, child: TreeNode[T]):
        self.__children.append(child)

    def __str__(self):
        return str(self.__value)


class Tree[T: SupportsAllComparisons]:

    def __init__(self, value: T | None = None):
        self.__root: TreeNode[T] = TreeNode(value)

    @property
    def root(self):
        return self.__root

    def multi_insert(self, values: list[T], parent: TreeNode[T] | None = None) -> list[TreeNode[T]]:
        res: list[TreeNode[T]] = list()
        for item in values:
            res.append(self.insert(item, parent))
        return res

    def insert(self, value: T, parent: TreeNode[T] | None = None) -> TreeNode[T]:
        child = TreeNode(value, parent if parent is not None else self.root)
        if parent is None:
            self.root.add_child(child)
            return child
        parent.add_child(child)
        return child

    def __print_levels(self) -> str:
        queue = deque([(self.__root, 0)])
        current_level = 0
        level_nodes: list[TreeNode[T]] = []
        lines = list()
        while queue:
            node, level = queue.popleft()
            if level != current_level:
                lines.append("Level" + str(current_level) + ":" + " ".join(str(n) for n in level_nodes))
                level_nodes = []
                current_level = level
            level_nodes.append(node)
            for child in node.children:
                queue.append((child, level + 1))
        if level_nodes:
            lines.append("Level" + str(current_level) + ":" + " ".join(str(n) for n in level_nodes))
        return "\n".join(lines)

    def traverse_preorder(self, node: TreeNode[T] | None = None):
        if node is None:
            node = self.__root
        return self.__traverse_preorder(node)

    def __traverse_preorder(self, node: TreeNode[T], result: list | None = None):
        if result is None:
            result = list()
        result.append(node)
        for child in node.children:
            self.__traverse_preorder(child, result)
        return result

    # busca em profundidade
    def depth_first_search(self, value: T, node: TreeNode[T] | None = None) -> TreeNode[T] | None:
        if node is None:
            node = self.__root
        if node.value == value:
            return node
        for child in node.children:
            found = self.depth_first_search(value, child)
            if found is not None:
                return found
        return None

    # busca em largura
    def breadth_first_search_value(self, value):
        return self.breadth_first_search(lambda n: n.value == value)

    def breadth_first_search_multi(self, compare_fn: Callable[[TreeNode[T]], bool]) -> list[TreeNode[T]]:
        queue: deque[TreeNode[T]] = deque([self.__root])
        res: list[TreeNode[T]] = list()
        while queue:
            node: TreeNode[T] = queue.popleft()
            if compare_fn(node):
                res.append(node)
            queue.extend(node.children)
        return res

    def breadth_first_search(self, compare_fn: Callable[[TreeNode[T]], bool]) -> TreeNode[T] | None:
        queue: deque[TreeNode[T]] = deque([self.__root])
        while queue:
            node: TreeNode[T] = queue.popleft()
            if compare_fn(node):
                return node
            queue.extend(node.children)
        return None

    def __str__(self) -> str:
        return self.__print_levels()


class MenuTree[T: tuple[str, str | None]  # (localization_key, shortcut)
               ](Tree[T]):

    def __init__(self, menu_name: str, menu_key: str | None = None, lang: str = "en") -> None:
        super().__init__((menu_name, menu_key))
        self.__lang: str = lang

    @property
    def lang(self) -> str:
        return self.__lang

    @lang.setter
    def lang(self, new: str) -> None:
        self.__lang = new

    def __str__(self) -> str:
        return self.__print_translated_levels()

    def __print_translated_levels(self) -> str:
        queue = deque([(self.root, 0)])
        current_level = 0
        level_nodes: list[TreeNode[T]] = []
        lines = list()
        while queue:
            node, level = queue.popleft()
            if level != current_level:
                lines.append("Level" + str(current_level) + ":" + " ".join(
                    f"({translate(n.value[0], self.lang)}, {n.value[1]})" for n in level_nodes))
                level_nodes = []
                current_level = level
            level_nodes.append(node)
            for child in node.children:
                queue.append((child, level + 1))
        if level_nodes:
            lines.append("Level" + str(current_level) + ":" + " ".join(
                f"({translate(n.value[0], self.lang)}, {n.value[1]})" for n in level_nodes))
        return "\n".join(lines)

    def find_shortcut(self, name: str) -> str | None:
        l = lambda n: name.lower() == translate(n.value[0], self.lang).lower()
        res: TreeNode[T] | None = self.breadth_first_search(l) or None
        return res.value[1] if res is not None else "None"

    def find_all_nodes(self, name: str) -> list[str]:
        l = lambda n: name.lower() in translate(n.value[0], self.lang).lower()
        res: list[TreeNode[T]] = self.breadth_first_search_multi(l)
        return [f"({translate(n.value[0])}, {n.value[1]})" for n in res]

    def find_menu_item(self, shortcut: str) -> str | None:
        l = lambda n: shortcut.lower() == (n.value[1] or "").lower()
        res: TreeNode[T] | None = self.breadth_first_search(l) or None
        return translate(res.value[0], self.lang) if res is not None else "None"


if __name__ == "__main__":
    tree = MenuTree(menu_name="menu.app", lang="en")
    _, edit, *_ = tree.multi_insert([
        ("menu.pain", None),
        ("menu.edit", "<C-S-e>"),
        ("menu.open", "<C-o>"),
        ("menu.save", "<C-s>"),
        ("menu.save_as", "<C-S-s>")
    ])
    tree.multi_insert([
        ("menu.undo", "<C-z>"),
        ("menu.redo", "<C-y>"),
        ("menu.format", "<C-A-l>")
    ], parent=edit)
    print(tree)
    print(tree.find_shortcut("Redo"))
    print(tree.find_menu_item("<C-z>"))
    print(tree.find_all_nodes("a"))
