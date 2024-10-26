import asyncio

from rich.style import Style
from textual import work
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Tree
from textual.widgets.tree import TreeNode

from gitlabrador.api import GitLabClient
from gitlabrador.config import settings, save_recent_project
from gitlabrador.models import Group


class ProjectsTree(Tree[Group]):
    def __init__(self):
        root_group = settings.gitlab.default_group
        super().__init__(root_group.name, data=root_group)
        self.gitlab = GitLabClient()

    def render_label(self, node: TreeNode, base_style: Style, style: Style):
        new_style = style.copy()
        if not node.allow_expand:
            new_style = Style.chain(Style(bold=True), new_style)
        return super().render_label(node, base_style, new_style)

    async def on_mount(self):
        self.loading = True
        self.load_projects()

    @work(exclusive=True)
    async def load_projects(self):
        async with self.gitlab.connect():
            await self.load_descendants(self.root)
        self.root.expand()
        self.loading = False

    async def load_descendants(self, parent_node: TreeNode):
        parent_group: Group = parent_node.data

        child_loaders = []
        async for group in self.gitlab.get_descendant_groups(parent_group.full_path):
            node = parent_node.add(group.name, data=group)
            child_loaders.append(self.load_descendants(node))

        async for project in self.gitlab.get_projects(parent_node.data.full_path):
            parent_node.add_leaf("🌀 " + project.name, data=project)

        await asyncio.gather(*child_loaders)

    def on_tree_node_selected(self, node_selected: Tree.NodeSelected):
        node = node_selected.node
        if not node.allow_expand:
            save_recent_project(node.data)
            self.app.pop_screen()


class ProjectSelectionScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Return to previous screen")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield ProjectsTree()
        yield Footer()
