import terka
from textual.screen import Screen
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Label, Tabs, DataTable, TabbedContent, TabPane, Static

EPICS = [
    ("id", "name", "description"),
    (1, "First", None),
    (2, "Second", None),
    (3, "Third", "Sample descr"),
]

TASKS = [
    ("id", "name", "description"),
    (10, "First", None),
    (20, "Second", None),
    (30, "Third", "Sample descr"),
]

STORIES = [
    ("id", "name", "description"),
    (10, "First", None),
    (20, "Second", None),
    (30, "Third", "Sample descr"),
]


class TerkaProject(Screen):
    """Demonstrates the Tabs widget."""

    CSS = """
    Tabs {
        dock: top;
    }
    Screen {
        align: center top;
    }
    .header {
        margin:1 1;
        width: 100%;
        height: 5%;
        background: $panel;
        border: tall $primary;
        content-align: center middle;
    }
    """

    BINDINGS = [("e", "epics", "Epics"), ("t", "tasks", "Tasks"),
                ("s", "stories", "Stories"), ("n", "notes", "Notes"),
                ("o", "overview", "Overview"), ("q", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Project name", classes="header")
        with TabbedContent(initial="tasks"):
            with TabPane("Tasks", id="tasks"):
                table = DataTable(id="tasks")
                table.add_columns(*TASKS[0])
                table.add_rows(TASKS[1:])
                yield table
            with TabPane("Epics", id="epics"):
                table = DataTable(id="epics")
                table.add_columns(*EPICS[0])
                table.add_rows(EPICS[1:])
                yield table
            with TabPane("Stories", id="stories"):
                table = DataTable(id="stories")
                table.add_columns(*STORIES[0])
                table.add_rows(STORIES[1:])
                yield table
            with TabPane("Notes", id="notes"):
                table = DataTable(id="notes")
                table.add_columns(*STORIES[0])
                table.add_rows(STORIES[1:])
                yield table
            with TabPane("Overview", id="overview"):
                table = DataTable(id="overview")
                table.add_columns(*STORIES[0])
                table.add_rows(STORIES[1:])
                yield table
        yield Footer()

    # def on_mount(self) -> None:
    #     """Focus the tabs when the app starts."""
    #     self.query_one(Tabs).focus()

    def action_epics(self) -> None:
        """Add a new tab."""
        self.query_one(TabbedContent).active = "epics"

    def action_tasks(self) -> None:
        """Add a new tab."""
        self.query_one(TabbedContent).active = "tasks"

    def action_stories(self) -> None:
        """Add a new tab."""
        self.query_one(TabbedContent).active = "stories"

    def action_overview(self) -> None:
        """Add a new tab."""
        self.query_one(TabbedContent).active = "overview"

    def action_notes(self) -> None:
        """Add a new tab."""
        self.query_one(TabbedContent).active = "notes"

    # def action_add(self) -> None:
    #     """Add a new tab."""
    #     tabs = self.query_one(Tabs)
    #     # Cycle the names
    #     NAMES[:] = [*NAMES[1:], NAMES[0]]
    #     tabs.add_tab(NAMES[0])

    # def action_remove(self) -> None:
    #     """Remove active tab."""
    #     tabs = self.query_one(Tabs)
    #     active_tab = tabs.active_tab
    #     if active_tab is not None:
    #         tabs.remove_tab(active_tab.id)

    # def action_clear(self) -> None:
    #     """Clear the tabs."""
    #     self.query_one(Tabs).clear()


class TerkaSprint(Screen):
    """Demonstrates the Tabs widget."""

    CSS = """
    Tabs {
        dock: top;
    }
    Screen {
        align: center top;
    }
    .header {
        margin:1 1;
        width: 100%;
        height: 5%;
        background: $panel;
        border: tall $primary;
        content-align: center middle;
    }
    """

    BINDINGS = [("t", "tasks", "Tasks"), ("n", "notes", "Notes"),
                ("o", "overview", "Overview"), ("q", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Sprint name", classes="header")
        with TabbedContent(initial="tasks"):
            with TabPane("Tasks", id="tasks"):
                table = DataTable(id="tasks")
                table.add_columns(*TASKS[0])
                table.add_rows(TASKS[1:])
                yield table
            with TabPane("Overview", id="overview"):
                table = DataTable(id="overview")
                table.add_columns(*STORIES[0])
                table.add_rows(STORIES[1:])
                yield table
        yield Footer()

    # def on_mount(self) -> None:
    #     """Focus the tabs when the app starts."""
    #     self.query_one(Tabs).focus()

    def action_epics(self) -> None:
        """Add a new tab."""
        self.query_one(TabbedContent).active = "epics"

    def action_tasks(self) -> None:
        """Add a new tab."""
        self.query_one(TabbedContent).active = "tasks"

    def action_stories(self) -> None:
        """Add a new tab."""
        self.query_one(TabbedContent).active = "stories"

    def action_overview(self) -> None:
        """Add a new tab."""
        self.query_one(TabbedContent).active = "overview"

    def action_notes(self) -> None:
        """Add a new tab."""
        self.query_one(TabbedContent).active = "notes"

    # def action_add(self) -> None:
    #     """Add a new tab."""
    #     tabs = self.query_one(Tabs)
    #     # Cycle the names
    #     NAMES[:] = [*NAMES[1:], NAMES[0]]
    #     tabs.add_tab(NAMES[0])

    # def action_remove(self) -> None:
    #     """Remove active tab."""
    #     tabs = self.query_one(Tabs)
    #     active_tab = tabs.active_tab
    #     if active_tab is not None:
    #         tabs.remove_tab(active_tab.id)


    # def action_clear(self) -> None:
    #     """Clear the tabs."""
    #     self.query_one(Tabs).clear()
class Terka(App):
    BINDINGS = [
        ("1", "switch_mode('project')", "Dashboard"),
        ("2", "switch_mode('sprint')", "Settings"),
    ]
    MODES = {"project": TerkaProjects, "sprint": TerkaCurrentSprint}

    def on_mount(self) -> None:
        self.switch_mode("project")


if __name__ == "__main__":

    app = Terka()
    app.run()
