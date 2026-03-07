import flet as ft

def main(page: ft.Page):
    page.title = "My Tasks Pro"
    page.bgcolor = "#121212"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    
    page.window_width = 400 
    page.window_height = 800

    def add_task(e):
        if not new_task.value: return
        
        # Priority selection
        selected_priority = list(prio_selector.selected)[0]
        p_color = {"Low": "#2ecc71", "Med": "#f1c40f", "High": "#e74c3c"}[selected_priority]
        
        # Task Container
        task_card = ft.Container(
            bgcolor="#1e1e1e",
            padding=10,
            border_radius=12,
            margin=ft.margin.only(bottom=5)
        )

        # UI using only Text - no icons at all
        task_card.content = ft.Row([
            ft.Container(width=5, height=30, bgcolor=p_color, border_radius=2),
            ft.Checkbox(fill_color="#ebcb8b"),
            ft.Text(new_task.value, expand=True, size=16),
            # Replacing IconButton with TextButton to bypass icon errors
            ft.TextButton(
                content=ft.Text("DELETE", color="#ff5555", size=12, weight="bold"),
                on_click=lambda _: delete_task(task_card)
            ),
        ], vertical_alignment=ft.CrossAxisAlignment.CENTER)
        
        task_view.controls.append(task_card)
        new_task.value = ""
        page.update()

    def delete_task(card):
        task_view.controls.remove(card)
        page.update()

    new_task = ft.TextField(
        hint_text="What needs to be done?",
        expand=True,
        border_color="#333333",
        bgcolor="#1a1a1a",
        border_radius=10,
    )

    prio_selector = ft.SegmentedButton(
        selected=["Low"], 
        allow_multiple_selection=False,
        segments=[
            ft.Segment(value="Low", label=ft.Text("Low")),
            ft.Segment(value="Med", label=ft.Text("Med")),
            ft.Segment(value="High", label=ft.Text("High")),
        ],
    )

    task_view = ft.Column(scroll=ft.ScrollMode.ADAPTIVE, expand=True)

    page.add(
        ft.Text("✨ My Tasks", size=32, weight="bold"),
        ft.Row([
            new_task, 
            # Using a simple button with text for the main "Add" action
            ft.ElevatedButton(
                content=ft.Text("ADD", color="black", weight="bold"),
                bgcolor="#ebcb8b", 
                on_click=add_task
            )
        ]),
        ft.Text("Priority:", size=14, color="white54"),
        prio_selector,
        ft.Divider(height=20, color="transparent"),
        task_view
    )

if __name__ == "__main__":
    ft.app(target=main)