import flet as ft

def main(page: ft.Page):
    page.title = "Simple Todo"
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # This list will hold our tasks in memory
    tasks = []

    # 1. Load data from phone storage
    stored_tasks = page.client_storage.get("tasks")
    if stored_tasks:
        tasks = stored_tasks

    def save_and_update():
        # Save the current list to the phone
        page.client_storage.set("tasks", tasks)
        
        # Clear the screen and rebuild the list
        tasks_view.controls.clear()
        for index, task_text in enumerate(tasks):
            tasks_view.controls.append(
                ft.ListTile(
                    title=ft.Text(task_text),
                    trailing=ft.IconButton(
                        ft.Icons.DELETE, 
                        on_click=lambda e, i=index: delete_task(i)
                    )
                )
            )
        page.update()

    def add_task(e):
        if new_task.value:
            tasks.append(new_task.value)
            new_task.value = ""
            save_and_update()

    def delete_task(index):
        tasks.pop(index)
        save_and_update()

    # UI Elements
    new_task = ft.TextField(hint_text="Enter task...", expand=True)
    tasks_view = ft.Column()

    # Build the initial UI
    page.add(
        ft.Text("My To-Do List", style=ft.TextThemeStyle.HEADLINE_MEDIUM),
        ft.Row([new_task, ft.ElevatedButton("Add", on_click=add_task)]),
        tasks_view
    )

    # Show saved tasks immediately
    save_and_update()

ft.app(target=main)
