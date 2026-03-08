import flet as ft
import json
import time

class Task(ft.Column):
    def __init__(self, name, completed, on_status_change, on_delete):
        super().__init__()
        self.completed = completed
        self.task_name = name
        self.on_status_change = on_status_change
        self.on_delete = on_delete

        self.display_task = ft.Checkbox(
            value=self.completed, label=self.task_name, on_change=self.status_changed
        )
        self.controls = [
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    self.display_task,
                    ft.IconButton(ft.Icons.DELETE_OUTLINE, icon_color="red", on_click=self.delete_clicked),
                ],
            )
        ]

    def status_changed(self, e):
        self.completed = self.display_task.value
        self.on_status_change()

    def delete_clicked(self, e):
        self.on_delete(self)

def main(page: ft.Page):
    page.title = "Ultimate To-Do"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.theme_mode = ft.ThemeMode.LIGHT # Set a default immediately
    
    tasks_view = ft.Column()
    new_task_input = ft.TextField(hint_text="What needs to be done?", expand=True)
    items_left = ft.Text("0 active tasks")

    def save_data():
        try:
            task_data = [{"name": t.task_name, "completed": t.completed} for t in tasks_view.controls]
            page.client_storage.set("tasks", json.dumps(task_data))
            page.client_storage.set("theme", page.theme_mode.value)
        except:
            pass

    def load_data():
        # Small delay to prevent black screen crash on Android startup
        time.sleep(0.5) 
        try:
            if page.client_storage.contains_key("theme"):
                saved_theme = page.client_storage.get("theme")
                page.theme_mode = ft.ThemeMode(saved_theme)
                theme_icon.icon = ft.Icons.LIGHT_MODE if page.theme_mode == ft.ThemeMode.DARK else ft.Icons.DARK_MODE

            if page.client_storage.contains_key("tasks"):
                saved_tasks = page.client_storage.get("tasks")
                if saved_tasks:
                    for item in json.loads(saved_tasks):
                        tasks_view.controls.append(
                            Task(item["name"], item["completed"], update_view, delete_task)
                        )
            update_view()
        except:
            update_view()

    def update_view(e=None):
        status = filter_tabs.tabs[filter_tabs.selected_index].text
        count = 0
        for task in tasks_view.controls:
            task.visible = (status == "all" or 
                          (status == "active" and not task.completed) or 
                          (status == "completed" and task.completed))
            if not task.completed:
                count += 1
        items_left.value = f"{count} active tasks"
        save_data()
        page.update()

    def add_clicked(e):
        if new_task_input.value != "":
            tasks_view.controls.append(Task(new_task_input.value, False, update_view, delete_task))
            new_task_input.value = ""
            update_view()

    def delete_task(task):
        tasks_view.controls.remove(task)
        update_view()

    def clear_completed(e):
        for task in tasks_view.controls[:]:
            if task.completed:
                tasks_view.controls.remove(task)
        update_view()

    def toggle_theme(e):
        page.theme_mode = ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        theme_icon.icon = ft.Icons.LIGHT_MODE if page.theme_mode == ft.ThemeMode.DARK else ft.Icons.DARK_MODE
        save_data()
        page.update()

    theme_icon = ft.IconButton(ft.Icons.DARK_MODE, on_click=toggle_theme)
    filter_tabs = ft.Tabs(
        selected_index=0,
        on_change=update_view,
        tabs=[ft.Tab(text="all"), ft.Tab(text="active"), ft.Tab(text="completed")],
    )

    
    page.add(
        ft.Row([ft.Text("My Tasks", style=ft.TextThemeStyle.HEADLINE_MEDIUM, expand=True), theme_icon]),
        ft.Row([new_task_input, ft.FloatingActionButton(icon=ft.Icons.ADD, on_click=add_clicked)]),
        filter_tabs,
        tasks_view,
        ft.Divider(),
        ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
            items_left,
            ft.TextButton("Clear Completed", on_click=clear_completed, icon=ft.Icons.DELETE_SWEEP)
        ])
    )


    load_data()

ft.app(target=main)
