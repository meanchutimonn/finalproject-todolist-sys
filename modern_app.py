import flet as ft
import os
import ssl
import requests
import datetime

# Fix SSL certificate issue
ssl._create_default_https_context = ssl._create_unverified_context

# --- Configuration ---
API_URL = "http://127.0.0.1:8000"
DB_HOST = "192.168.100.23"

# --- Mock Data ---
MOCK_USERS = [{"username": "Wink"}, {"username": "Smile"}, {"username": "Glasses"}]
MOCK_TASKS = [
    {
        "task_id": 1,
        "title": "Mobile App Design",
        "description": "Design the app UI and interactions.",
        "priority": 1,
        "deadline": datetime.datetime.now().replace(hour=18, minute=0, second=0, microsecond=0).isoformat(),
        "status": "Assign",
        "friend_assignid": 1
    },
    {
        "task_id": 2,
        "title": "Get wireframe design",
        "description": "Complete the wireframes for the new feature.",
        "priority": 2,
        "deadline": (datetime.datetime.now() + datetime.timedelta(days=2)).replace(hour=16, minute=0, second=0, microsecond=0).isoformat(),
        "status": "Processing",
        "friend_assignid": 2
    },
    {
        "task_id": 3,
        "title": "Task management dashboard",
        "description": "Build the dashboard layout and charts.",
        "priority": 1,
        "deadline": (datetime.datetime.now() + datetime.timedelta(days=4)).replace(hour=14, minute=30, second=0, microsecond=0).isoformat(),
        "status": "Done",
        "friend_assignid": 3
    },
    {
        "task_id": 4,
        "title": "Landing Page design",
        "description": "Create a landing page for the new campaign.",
        "priority": 2,
        "deadline": (datetime.datetime.now() + datetime.timedelta(days=1)).replace(hour=11, minute=0, second=0, microsecond=0).isoformat(),
        "status": "Assign",
        "friend_assignid": 4
    },
]

def main(page: ft.Page):
    page.title = "Modern To-Do List"
    page.window_width = 450
    page.window_height = 850
    page.padding = 0
    page.spacing = 0
    page.bgcolor = "#F7F8FD"
    page.theme_mode = ft.ThemeMode.LIGHT

    # State
    state = {"users": MOCK_USERS, "tasks": MOCK_TASKS, "current_user": "Shan", "avatar": "https://i.pravatar.cc/150?u=shan", "offline": False, "notifications": []}

    # --- Functions ---
    def show_notification(message):
        if message:
            page.snack_bar = ft.SnackBar(
                content=ft.Text(message, size=13, color=ft.Colors.WHITE),
                bgcolor="#685CF2",
                action="OK",
                open=True
            )
            page.update()

    def load_data():
        state["offline"] = False
        try:
            r_users = requests.get(f"{API_URL}/users", timeout=2)
            r_tasks = requests.get(f"{API_URL}/tasks", timeout=2)
            if r_users.ok:
                state["users"] = r_users.json()
            else:
                state["offline"] = True
            if r_tasks.ok:
                state["tasks"] = r_tasks.json()
            else:
                state["offline"] = True
        except requests.RequestException:
            state["offline"] = True
            print("Using Mock Data (API Offline)")

    def add_notification(message):
        now = datetime.datetime.now().strftime("%b %d, %Y %H:%M")
        state.setdefault("notifications", []).insert(0, {"message": message, "time": now})
        show_notification(message)

    def navigate_to(screen_func):
        page.clean()
        screen_func()
        page.update()

    # ==================== 1. LOGIN PAGE ====================
    def render_login_page(mode="login"):
        page.bgcolor = "#F7F8FD"
        page.padding = 0
        
        # Auth state
        auth_state = {
            "loading": False,
            "error": ""
        }
        
        username_field = ft.TextField(
            label="Username",
            border_radius=14,
            bgcolor=ft.Colors.WHITE,
            border_color="transparent",
            height=56,
            text_size=14,
            content_padding=ft.Padding(left=16, top=0, right=16, bottom=0)
        )
        email_field = ft.TextField(
            label="Email",
            border_radius=14,
            bgcolor=ft.Colors.WHITE,
            border_color="transparent",
            height=56,
            text_size=14,
            content_padding=ft.Padding(left=16, top=0, right=16, bottom=0)
        )
        
        err_txt = ft.Text("", color="#D32F2F", size=13, weight="w500")
        success_txt = ft.Text("", color="#388E3C", size=13, weight="w500")
        loading_indicator = ft.ProgressRing(width=20, height=20, stroke_width=2, color="#685CF2")

        def on_auth_action(e):
            auth_state["loading"] = True
            auth_state["error"] = ""
            err_txt.value = ""
            success_txt.value = ""
            page.update()
            
            # Validate inputs
            if not username_field.value or not email_field.value:
                auth_state["error"] = "Username and email are required"
                err_txt.value = auth_state["error"]
                auth_state["loading"] = False
                page.update()
                return
            
            # Prepare user data
            user_data = {
                "username": username_field.value,
                "email": email_field.value
            }
            
            # Send to API
            try:
                if mode == "register":
                    response = requests.post(f"{API_URL}/users", json=user_data, timeout=3)
                else:
                    response = requests.post(f"{API_URL}/user_login", json=user_data, timeout=3)
                
                if response.ok:
                    state["current_user"] = username_field.value
                    if mode == "register":
                        success_txt.value = "Account created successfully! Logging in..."
                    else:
                        success_txt.value = "Login successful!"
                    page.update()
                    import time
                    time.sleep(1)
                    load_data()
                    navigate_to(render_main_page)
                else:
                    try:
                        auth_state["error"] = response.json().get("detail", "Authentication failed")
                    except:
                        auth_state["error"] = "Authentication failed"
                    err_txt.value = auth_state["error"]
            except requests.RequestException as ex:
                # Fallback to mock for offline mode
                state["offline"] = True
                state["current_user"] = username_field.value
                auth_state["error"] = ""
                success_txt.value = "Proceeding in offline mode..."
                page.update()
                import time
                time.sleep(1)
                navigate_to(render_main_page)
            finally:
                auth_state["loading"] = False
                page.update()

        title_text = "Welcome Back" if mode == "login" else "Create Account"
        subtitle_text = "Sign in to your account" if mode == "login" else "Join us today"
        button_text = "SIGN IN" if mode == "login" else "CREATE ACCOUNT"
        toggle_text = "Create New Account" if mode == "login" else "Back to Login"

        # Header section with gradient-like background
        header_section = ft.Container(
            bgcolor="#685CF2",
            height=140,
            content=ft.Column([
                ft.Container(height=30),
                ft.Text("To-Do List", size=32, weight="bold", color=ft.Colors.WHITE),
                ft.Text("Manage your tasks efficiently", size=14, color="#E7E5FF")
            ], spacing=6, horizontal_alignment=ft.CrossAxisAlignment.START),
            padding=ft.Padding(left=24, top=20, right=24, bottom=20)
        )

        # Form fields list
        form_fields = [username_field, email_field]

        page.add(
            ft.Column([
                header_section,
                ft.Container(
                    expand=True,
                    content=ft.Column([
                        ft.Container(height=24),
                        ft.Text(title_text, size=28, weight="bold", color="#21244f"),
                        ft.Text(subtitle_text, size=14, color="#888888"),
                        ft.Container(height=28),
                        ft.Column(form_fields, spacing=14),
                        ft.Container(height=6),
                        err_txt,
                        success_txt,
                        ft.Container(height=24),
                        ft.Container(
                            content=ft.Row([
                                ft.Text(button_text, color=ft.Colors.WHITE, weight="bold", size=14),
                                loading_indicator if auth_state["loading"] else ft.Container(width=0)
                            ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                            bgcolor="#685CF2",
                            height=56,
                            border_radius=14,
                            alignment=ft.Alignment.CENTER,
                            on_click=on_auth_action if not auth_state["loading"] else None,
                            shadow=ft.BoxShadow(blur_radius=12, color="#685CF233", offset=ft.Offset(0, 6))
                        ),
                        ft.Container(height=20),
                        ft.Row([
                            ft.Text("Don't have an account? " if mode == "login" else "Already have an account? ", size=13, color="#888888"),
                            ft.TextButton(
                                toggle_text,
                                style=ft.ButtonStyle(
                                    color="#685CF2",
                                    overlay_color="#685CF211"
                                ),
                                on_click=lambda _: navigate_to(lambda: render_login_page("register" if mode == "login" else "login"))
                            )
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=0)
                    ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.START),
                    padding=ft.Padding(left=24, top=0, right=24, bottom=24)
                )
            ], spacing=0, expand=True)
        )

    # ==================== 2. MAIN PAGE ====================
    def render_main_page():
        page.bgcolor = "#F7F8FD"

        search_query = {"value": ""}
        show_search = {"value": False}

        def toggle_search(e=None):
            show_search["value"] = not show_search["value"]
            if not show_search["value"]:
                search_query["value"] = ""
            page.update()

        def filter_tasks(tasks):
            query = search_query["value"].strip().lower()
            if not query:
                return tasks
            return [
                task for task in tasks
                if query in task.get("title", "").lower() or query in task.get("description", "").lower()
            ]

        def rebuild_tasks_list():
            filtered_tasks = filter_tasks(state["tasks"])
            tasks_col.controls.clear()
            
            for t in filtered_tasks:
                task_status = t.get("status", "Assign")
                due_text = ""
                if t.get("deadline"):
                    try:
                        due_date = datetime.datetime.fromisoformat(t["deadline"])
                        due_text = due_date.strftime("%b %d, %Y %H:%M")
                    except Exception:
                        due_text = str(t["deadline"])
                priority_label = "Urgency" if t.get("priority") == 1 else "Importance" if t.get("priority") == 2 else "Normal"
                tasks_col.controls.append(
                    ft.GestureDetector(
                        on_tap=lambda e, task=t: open_task_dialog(task),
                        content=ft.Container(
                            bgcolor=ft.Colors.WHITE,
                            border_radius=18,
                            padding=ft.Padding(18, 16, 18, 16),
                            shadow=ft.BoxShadow(blur_radius=15, color="#10000000", offset=ft.Offset(0, 4)),
                            content=ft.Column([
                                ft.Row([
                                    ft.Text(t.get("title", "Untitled Task"), weight="w600", size=15, color="#222222"),
                                    ft.Container(
                                        content=ft.Text(task_status, size=12, color="#FFFFFF"),
                                        bgcolor="#685CF2" if task_status != "Done" else "#4CAF50",
                                        padding=ft.Padding(8, 4, 8, 4),
                                        border_radius=12
                                    )
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.Container(height=8),
                            ft.Text(t.get("description", ""), size=13, color="#6B6B6B"),
                            ft.Container(height=12),
                            ft.Row([
                                ft.Row([
                                    ft.Icon(ft.icons.Icons.FLAG, size=14, color="#685CF2"),
                                    ft.Text(priority_label, size=12, color="#685CF2")
                                ], spacing=6),
                                ft.Row([
                                    ft.Icon(ft.icons.Icons.EVENT, size=14, color="#A8A8A8"),
                                    ft.Text(due_text, size=12, color="#A8A8A8")
                                ], spacing=6)
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                        ])
                    )
                )
                )
            if not filtered_tasks:
                tasks_col.controls.append(
                    ft.Container(
                        bgcolor=ft.Colors.WHITE,
                        border_radius=18,
                        padding=ft.Padding(18, 16, 18, 16),
                        shadow=ft.BoxShadow(blur_radius=15, color="#10000000", offset=ft.Offset(0, 4)),
                        content=ft.Text("No tasks match your search.", size=14, color="#777777")
                    )
                )
            
            # Update header text
            header_subtitle.value = f"{len(filtered_tasks)} task{'s' if len(filtered_tasks) != 1 else ''} found" if search_query["value"] else f"{len(state['tasks'])} tasks today"

        def on_search_change(e):
            search_query["value"] = e.control.value or ""
            rebuild_tasks_list()
            page.update()

        display_tasks = filter_tasks(state["tasks"])
        task_header_text = f"{len(display_tasks)} task{'s' if len(display_tasks) != 1 else ''} found" if search_query["value"] else f"{len(state['tasks'])} tasks today"

        def sync_task_to_server(task):
            if not task.get("task_id"):
                return
            try:
                response = requests.put(f"{API_URL}/tasks/{task['task_id']}", json=task, timeout=3)
                if response.ok:
                    state["offline"] = False
                else:
                    state["offline"] = True
            except requests.RequestException:
                state["offline"] = True

        def delete_task_from_server(task):
            if not task.get("task_id"):
                return
            try:
                response = requests.delete(f"{API_URL}/tasks/{task['task_id']}", timeout=3)
                if response.ok:
                    state["offline"] = False
                else:
                    state["offline"] = True
            except requests.RequestException:
                state["offline"] = True

        def open_task_dialog(task):
            title_field = ft.TextField(
                label="Title",
                value=task.get("title", ""),
                border_radius=14,
                bgcolor=ft.Colors.WHITE,
                border_color="transparent",
                text_size=14,
                content_padding=ft.Padding(left=16, top=0, right=16, bottom=0)
            )
            desc_field = ft.TextField(
                label="Description",
                value=task.get("description", ""),
                multiline=True,
                min_lines=3,
                border_radius=14,
                bgcolor=ft.Colors.WHITE,
                border_color="transparent",
                text_size=14,
                content_padding=ft.Padding(left=16, top=0, right=16, bottom=0)
            )
            status_text = ft.Text(task.get("status", "Assign"), weight="bold")

            def change_status(new_status):
                if task.get("status") != new_status:
                    task["status"] = new_status
                    status_text.value = new_status
                    add_notification(f"Task '{task.get('title')}' status changed to {new_status}.")
                    sync_task_to_server(task)
                    rebuild_tasks_list()
                    page.update()

            def delete_task(e=None):
                title = task.get("title", "Untitled Task")
                state["tasks"] = [t for t in state["tasks"] if t.get("task_id") != task.get("task_id")]
                delete_task_from_server(task)
                add_notification(f"Task '{title}' deleted.")
                rebuild_tasks_list()
                page.update()
                close_dialog()

            def save_task(e):
                task["title"] = title_field.value
                task["description"] = desc_field.value
                sync_task_to_server(task)
                add_notification(f"Task '{task.get('title')}' updated.")
                rebuild_tasks_list()
                close_dialog()

            def build_status_action(label):
                active = task.get("status") == label
                return ft.Container(
                    content=ft.Text(label, size=12, weight="bold", color="#FFFFFF" if active else "#555555"),
                    bgcolor="#685CF2" if active else "#F0F2F5",
                    padding=ft.Padding(12, 10, 12, 10),
                    border_radius=12,
                    on_click=lambda e, l=label: change_status(l)
                )

            dialog = ft.AlertDialog(
                modal=True,
                title=ft.Row([
                    ft.Text("Edit Task", weight="bold"),
                    ft.PopupMenuButton(
                        icon=ft.icons.Icons.MORE_VERT,
                        icon_color="#666666",
                        items=[
                            ft.PopupMenuItem("Delete", icon=ft.icons.Icons.DELETE, on_click=delete_task),
                            ft.PopupMenuItem("Mark Done", icon=ft.icons.Icons.CHECK, on_click=lambda e: change_status("Done")),
                            ft.PopupMenuItem("Close", icon=ft.icons.Icons.CLOSE, on_click=lambda e: close_dialog())
                        ],
                        menu_position=ft.PopupMenuPosition.BOTTOM_RIGHT
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                content=ft.Column([
                    title_field,
                    ft.Container(height=12),
                    desc_field,
                    ft.Container(height=12),
                    ft.Row([
                        ft.Column([
                            ft.Text("Priority", size=11, color="#777777"),
                            ft.Text("Urgency" if task.get("priority") == 1 else "Importance", weight="bold")
                        ]),
                        ft.Column([
                            ft.Text("Status", size=11, color="#777777"),
                            status_text
                        ])
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Container(height=12),
                    ft.Row([
                        build_status_action("Assign"),
                        build_status_action("Processing"),
                        build_status_action("Done")
                    ], spacing=10),
                    ft.Container(height=12),
                    ft.Row([
                        ft.Icon(ft.icons.Icons.EVENT, size=16, color="#555555"),
                        ft.Text(task.get("deadline", "No deadline"), size=12, color="#555555")
                    ])
                ]),
                actions=[
                    ft.TextButton("Save", on_click=save_task),
                    ft.TextButton("Close", on_click=lambda e: close_dialog())
                ],
                actions_alignment=ft.MainAxisAlignment.END
            )

            def close_dialog():
                dialog.open = False
                page.dialog = None
                page.update()

            page.dialog = dialog
            dialog.open = True
            page.update()

        header = ft.Container(
            padding=ft.Padding(20, 25, 10, 10),
            content=ft.Row([
                ft.Row([
                    ft.CircleAvatar(foreground_image_src=state.get("avatar"), background_image_src=state.get("avatar"), radius=28),
                    ft.Column([
                        ft.Text(f"Hello, {state['current_user']}", size=26, weight="bold", color="#21244f"),
                        (header_subtitle := ft.Text(task_header_text, size=14, color="#777777"))
                    ], spacing=4)
                ], spacing=14),
                ft.Container(
                    content=ft.Icon(ft.icons.Icons.SEARCH, color="#5A5A5A", size=22),
                    bgcolor=ft.Colors.WHITE,
                    width=48, height=48,
                    border_radius=24,
                    alignment=ft.Alignment.CENTER,
                    on_click=lambda e=None: toggle_search(e),
                    shadow=ft.BoxShadow(blur_radius=12, color="#13000000", offset=ft.Offset(0, 4))
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        )

        dashboard = ft.Container(
            width=400,
            bgcolor="#8E85FF",
            border_radius=25,
            padding=ft.Padding(24, 22, 24, 22),
            shadow=ft.BoxShadow(blur_radius=20, color="#1F000000", offset=ft.Offset(0, 10)),
            content=ft.Column([
                ft.Row([
                    ft.Text("Dashboard Design", color=ft.Colors.WHITE, size=18, weight="bold"),
                    ft.Text("85%", color=ft.Colors.WHITE, size=16, weight="bold")
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Container(height=18),
                ft.Row([
                    ft.CircleAvatar(foreground_image_src="https://i.pravatar.cc/100?u=1", background_image_src="https://i.pravatar.cc/100?u=1", radius=14),
                    ft.CircleAvatar(foreground_image_src="https://i.pravatar.cc/100?u=2", background_image_src="https://i.pravatar.cc/100?u=2", radius=14),
                    ft.CircleAvatar(foreground_image_src="https://i.pravatar.cc/100?u=3", background_image_src="https://i.pravatar.cc/100?u=3", radius=14),
                    ft.CircleAvatar(foreground_image_src="https://i.pravatar.cc/100?u=4", background_image_src="https://i.pravatar.cc/100?u=4", radius=14)
                ], spacing=-8),
                ft.Container(height=22),
                ft.ProgressBar(value=0.85, color="#FFFFFF", bgcolor="#4DFFFFFF", height=8),
                ft.Container(height=12),
                ft.Row([
                    ft.Text("progress", color="#EDEFFF", size=12),
                    ft.Text("85%", color=ft.Colors.WHITE, size=12, weight="bold")
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            ], expand=True)
        )

        offline_banner = None
        if state.get("offline"):
            offline_banner = ft.Container(
                width=400,
                bgcolor="#FFF4E5",
                border_radius=18,
                padding=ft.Padding(16, 14, 16, 14),
                content=ft.Row([
                    ft.Icon(ft.icons.Icons.WARNING, color="#D9822B", size=18),
                    ft.Text("Offline mode: using local mock data.", size=12, color="#7A4F00")
                ], alignment=ft.MainAxisAlignment.START, spacing=10)
            )

        task_header = ft.Container(
            padding=ft.Padding(left=4, right=4, top=20, bottom=10),
            content=ft.Column([
                ft.Row([
                    ft.Column([
                        ft.Text("Add Task", size=20, weight="bold", color="#21244f"),
                        ft.Text("All Task", size=14, color="#777777")
                    ]),
                    ft.Container(
                        content=ft.Icon(ft.icons.Icons.ADD, color="white", size=18),
                        bgcolor="#8E85FF",
                        width=44, height=44,
                        border_radius=16,
                        alignment=ft.Alignment.CENTER,
                        on_click=lambda _: navigate_to(render_new_task_page)
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Container(height=12),
                ft.Row([
                    ft.TextField(
                        value=search_query["value"],
                        hint_text="Search tasks...",
                        expand=True,
                        border_radius=18,
                        bgcolor=ft.Colors.WHITE,
                        on_change=on_search_change,
                        visible=show_search["value"],
                        prefix_icon=ft.icons.Icons.SEARCH
                    )
                ])
            ])
        )

        tasks_col = ft.Column(spacing=12)
        rebuild_tasks_list()

        nav = ft.Container(
            bgcolor=ft.Colors.WHITE,
            width=400,
            height=88,
            border_radius=ft.BorderRadius(top_left=30, top_right=30, bottom_left=0, bottom_right=0),
            padding=ft.Padding(0, 0, 0, 0),
            shadow=ft.BoxShadow(blur_radius=20, color="#1A000000", offset=ft.Offset(0, -6)),
            content=ft.Row([
                ft.IconButton(icon=ft.icons.Icons.HOME, icon_color="#685cf2", icon_size=26),
                ft.IconButton(icon=ft.icons.Icons.CALENDAR_TODAY, icon_color="#A8A8A8", icon_size=24, on_click=lambda _: navigate_to(render_calendar_page)),
                ft.Container(
                    content=ft.Icon(ft.icons.Icons.ADD, color="white", size=28),
                    bgcolor="#8E85FF",
                    width=60, height=60,
                    border_radius=30,
                    alignment=ft.Alignment.CENTER,
                    margin=ft.Margin(top=-20),
                    on_click=lambda _: navigate_to(render_new_task_page),
                    shadow=ft.BoxShadow(blur_radius=18, color="#1F685CF2", offset=ft.Offset(0, 6))
                ),
                ft.IconButton(
                    icon=ft.icons.Icons.NOTIFICATIONS_NONE,
                    icon_color="#685cf2" if state.get("notifications") else "#A8A8A8",
                    icon_size=24,
                    on_click=lambda _: navigate_to(render_notifications_page)
                ),
                ft.IconButton(icon=ft.icons.Icons.PERSON_OUTLINE, icon_color="#A8A8A8", icon_size=24, on_click=lambda _: navigate_to(render_profile_page))
            ], alignment=ft.MainAxisAlignment.SPACE_AROUND)
        )

        page.add(
            ft.Column([
                ft.Container(
                    expand=True,
                    content=ft.Column([
                        header,
                        dashboard,
                        *( [offline_banner] if offline_banner else [] ),
                        task_header,
                        tasks_col,
                        ft.Container(height=24)
                    ], spacing=0, scroll=ft.ScrollMode.AUTO)
                ),
                ft.Container(content=nav, alignment=ft.Alignment.CENTER)
            ], spacing=0, expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )

    # ==================== 3. NEW TASK PAGE (LINK TO DB) ====================
    def render_new_task_page():
        title_ref = ft.Ref[ft.TextField]()
        desc_ref = ft.Ref[ft.TextField]()
        
        # Create state helpers for date/time
        selected_date = {"value": datetime.date.today()}
        selected_time = {"value": datetime.datetime.now().time().replace(second=0, microsecond=0)}

        def update_selection_appearance():
            for ref, value in priority_button_refs:
                if ref.current:
                    selected = selected_priority["value"] == value
                    ref.current.bgcolor = "#685CF2" if selected else "#F0F2F5"
                    if isinstance(ref.current.content, ft.Text):
                        ref.current.content.color = "#FFFFFF" if selected else "#4A4A4A"
            for ref, label in status_button_refs:
                if ref.current:
                    selected = selected_status["value"] == label
                    ref.current.bgcolor = "#685CF2" if selected else "#F0F2F5"
                    if isinstance(ref.current.content, ft.Text):
                        ref.current.content.color = "#FFFFFF" if selected else "#4A4A4A"
            for inner_ref, number_ref, order in team_avatar_refs:
                selected = order == selected_friend_order["value"]
                if inner_ref.current:
                    inner_ref.current.bgcolor = "#685CF2" if selected else None
                if number_ref.current:
                    number_ref.current.color = "#FFFFFF" if selected else "#4A4A4A"
            page.update()

        def on_date_changed(e):
            selected_date["value"] = date_picker.value or selected_date["value"]
            date_display.value = selected_date["value"].strftime("%b %d, %Y")
            page.update()

        def on_time_changed(e):
            selected_time["value"] = time_picker.value or selected_time["value"]
            time_display.value = selected_time["value"].strftime("%H:%M")
            page.update()

        date_display = ft.Text(selected_date["value"].strftime("%b %d, %Y"), size=14, color="#222222")
        time_display = ft.Text(selected_time["value"].strftime("%H:%M"), size=14, color="#222222")

        date_picker = ft.DatePicker(
            value=selected_date["value"],
            modal=True,
            open=False,
            on_change=on_date_changed
        )
        time_picker = ft.TimePicker(
            value=selected_time["value"],
            modal=True,
            open=False,
            on_change=on_time_changed
        )

        page.overlay.append(date_picker)
        page.overlay.append(time_picker)

        def open_date_picker(e=None):
            date_picker.open = True
            date_picker.update()
            page.update()

        def open_time_picker(e=None):
            time_picker.open = True
            time_picker.update()
            page.update()
        
        selected_priority = {"value": 1}
        selected_status = {"value": "Assign"}
        selected_friend_order = {"value": 1}
        priority_button_refs = []
        status_button_refs = []
        team_avatar_refs = []
        team_members = [
            {"id": 1, "avatar": "https://i.pravatar.cc/100?u=1", "name": "Wink", "order": 1},
            {"id": 2, "avatar": "https://i.pravatar.cc/100?u=2", "name": "Smile", "order": 2},
            {"id": 3, "avatar": "https://i.pravatar.cc/100?u=3", "name": "Glasses", "order": 3},
        ]

        def update_priority(value):
            selected_priority["value"] = value
            update_selection_appearance()

        def update_status(value):
            selected_status["value"] = value
            update_selection_appearance()

        def select_friend(order):
            selected_friend_order["value"] = order
            update_selection_appearance()

        def save_task_to_db(e):
            if not title_ref.current.value:
                return

            deadline_value = None
            try:
                deadline_date = date_picker.value or selected_date["value"]
                deadline_time = time_picker.value or selected_time["value"]
                if isinstance(deadline_date, str):
                    deadline_date = datetime.date.fromisoformat(deadline_date)
                if isinstance(deadline_time, str):
                    deadline_time = datetime.time.fromisoformat(deadline_time)
                deadline_value = datetime.datetime.combine(deadline_date, deadline_time)
            except Exception:
                deadline_value = None

            task_data = {
                "title": title_ref.current.value,
                "description": desc_ref.current.value,
                "priority": selected_priority["value"],
                "deadline": deadline_value.isoformat() if deadline_value else None,
                "status": selected_status["value"],
                "friend_assignid": selected_friend_order["value"]
            }

            task_data["task_id"] = max([t.get("task_id", 0) for t in state["tasks"]] + [0]) + 1
            notification_text = f"Task '{task_data['title']}' created with status {task_data['status']}."
            try:
                response = requests.post(f"{API_URL}/tasks", json=task_data, timeout=3)
                if response.ok:
                    new_task = response.json()
                    state["tasks"].append(new_task)
                    state["offline"] = False
                else:
                    state["offline"] = True
                    state["tasks"].append(task_data)
                add_notification(notification_text)
            except requests.RequestException as ex:
                state["offline"] = True
                print(f"DB Error: {ex}")
                state["tasks"].append(task_data)
                add_notification(notification_text)

            # Reset selections and form values so the next create-task view starts fresh
            selected_priority["value"] = 1
            selected_status["value"] = "Assign"
            selected_friend_order["value"] = 1
            if title_ref.current:
                title_ref.current.value = ""
            if desc_ref.current:
                desc_ref.current.value = ""
            if date_picker:
                date_picker.value = datetime.date.today()
                date_display.value = date_picker.value.strftime("%b %d, %Y")
            if time_picker:
                time_picker.value = datetime.datetime.now().time().replace(second=0, microsecond=0)
                time_display.value = time_picker.value.strftime("%H:%M")
            update_selection_appearance()
            page.update()

            navigate_to(render_main_page)

        def build_status_button(label):
            selected = selected_status["value"] == label
            ref = ft.Ref[ft.Container]()
            button = ft.Container(
                content=ft.Text(label, size=13, weight="bold", color="#FFFFFF" if selected else "#4A4A4A"),
                bgcolor="#685CF2" if selected else "#F0F2F5",
                padding=ft.Padding(16, 10, 16, 10),
                border_radius=14,
                on_click=lambda _: update_status(label),
                ref=ref
            )
            status_button_refs.append((ref, label))
            return button

        def build_priority_button(label, value):
            selected = selected_priority["value"] == value
            ref = ft.Ref[ft.Container]()
            button = ft.Container(
                content=ft.Text(label, size=13, weight="bold", color="#FFFFFF" if selected else "#4A4A4A"),
                bgcolor="#685CF2" if selected else "#F0F2F5",
                padding=ft.Padding(16, 10, 16, 10),
                border_radius=14,
                on_click=lambda _: update_priority(value),
                ref=ref
            )
            priority_button_refs.append((ref, value))
            return button

        def build_friend_avatar(member):
            inner_ref = ft.Ref[ft.Container]()
            number_ref = ft.Ref[ft.Text]()
            selected = member["order"] == selected_friend_order["value"]
            team_avatar_refs.append((inner_ref, number_ref, member["order"]))
            return ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.CircleAvatar(foreground_image_src=member["avatar"], background_image_src=member["avatar"], radius=20),
                        bgcolor="#685CF2" if selected else None,
                        border_radius=25,
                        padding=ft.Padding(4),
                        ref=inner_ref
                    ),
                    ft.Container(height=6),
                    ft.Text(str(member["order"]), size=12, color="#FFFFFF" if selected else "#4A4A4A", ref=number_ref)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                on_click=lambda _: select_friend(member["order"])
            )

        header = ft.Container(
            padding=ft.Padding(20, 40, 20, 10),
            content=ft.Row([
                ft.IconButton(icon=ft.icons.Icons.ARROW_BACK_IOS_NEW, icon_size=20, on_click=lambda _: navigate_to(render_main_page)),
                ft.Text("New Task", size=24, weight="bold", color="#21244f")
            ], spacing=10)
        )

        page.add(
            ft.Container(
                expand=True,
                bgcolor="#F7F8FD",
                content=ft.Column([
                    header,
                    ft.Container(
                        expand=True,
                        content=ft.Column([
                            ft.Container(
                                padding=ft.Padding(25, 10, 25, 10),
                                content=ft.Column([
                                    ft.Text("Title", size=14, weight="bold"),
                                    ft.TextField(ref=title_ref, hint_text="Conference", border=ft.InputBorder.OUTLINE, border_radius=12)
                                ])
                            ),
                            ft.Container(
                                padding=ft.Padding(25, 10, 25, 10),
                                content=ft.Row([
                                    ft.Container(
                                        bgcolor=ft.Colors.WHITE,
                                        border_radius=18,
                                        padding=ft.Padding(16, 16, 16, 16),
                                        width=190,
                                        shadow=ft.BoxShadow(blur_radius=10, color="#10000000", offset=ft.Offset(0, 4)),
                                        on_click=open_date_picker,
                                        content=ft.Column([
                                            ft.Text("Date", size=12, color="#777777"),
                                            date_display
                                        ])
                                    ),
                                    ft.Container(
                                        bgcolor=ft.Colors.WHITE,
                                        border_radius=18,
                                        padding=ft.Padding(16, 16, 16, 16),
                                        width=140,
                                        shadow=ft.BoxShadow(blur_radius=10, color="#10000000", offset=ft.Offset(0, 4)),
                                        on_click=open_time_picker,
                                        content=ft.Column([
                                            ft.Text("Time", size=12, color="#777777"),
                                            time_display
                                        ])
                                    )
                                ], spacing=12)
                            ),
                            ft.Container(
                                padding=ft.Padding(25, 10, 25, 10),
                                content=ft.Column([
                                    ft.Text("Description", size=14, weight="bold"),
                                    ft.TextField(ref=desc_ref, hint_text="Make a conference video call with teams", border=ft.InputBorder.UNDERLINE, multiline=True, min_lines=3)
                                ])
                            ),
                            ft.Container(
                                padding=ft.Padding(25, 10, 25, 10),
                                content=ft.Column([
                                    ft.Text("Priority", size=14, weight="bold"),
                                    ft.Row([
                                        build_priority_button("Urgency", 1),
                                        build_priority_button("Importance", 2)
                                    ], spacing=12)
                                ])
                            ),
                            ft.Container(
                                padding=ft.Padding(25, 10, 25, 10),
                                content=ft.Column([
                                    ft.Text("Status", size=14, weight="bold"),
                                    ft.Row([
                                        build_status_button("Assign"),
                                        build_status_button("Processing"),
                                        build_status_button("Done")
                                    ], spacing=12)
                                ])
                            ),
                            ft.Container(
                                padding=ft.Padding(25, 10, 25, 10),
                                content=ft.Column([
                                    ft.Text("Teams", size=14, weight="bold"),
                                    ft.Row([
                                        *[build_friend_avatar(member) for member in sorted(team_members, key=lambda x: x["order"])],
                                        ft.Container(
                                            content=ft.Icon(ft.icons.Icons.ADD, color="white", size=20),
                                            bgcolor="#685CF2",
                                            width=44, height=44,
                                            border_radius=16,
                                            alignment=ft.Alignment.CENTER
                                        )
                                    ], spacing=12)
                                ])
                            ),
                            ft.Container(
                                padding=ft.Padding(25, 10, 25, 10),
                                content=ft.Container(
                                    content=ft.Text("CREATE TASK", color="white", weight="bold"),
                                    bgcolor="#403D66", height=55, border_radius=27,
                                    alignment=ft.Alignment.CENTER,
                                    on_click=save_task_to_db
                                )
                            )
                        ], scroll=ft.ScrollMode.AUTO, expand=True)
                    )
                ])
            )
        )
    # ==================== 5. PROFILE & CALENDAR ====================
    def render_profile_page():
        page.bgcolor = "#F7F8FD"
        name_field = ft.TextField(
            label="Name",
            value=state["current_user"],
            border_radius=14,
            bgcolor=ft.Colors.WHITE,
            border_color="transparent",
            height=56,
            content_padding=ft.Padding(left=16, top=0, right=16, bottom=0)
        )

        def update_avatar_preview(e=None):
            avatar_preview.content = ft.CircleAvatar(foreground_image_src=avatar_field.value or state.get("avatar"), background_image_src=avatar_field.value or state.get("avatar"), radius=48)
            page.update()

        avatar_field = ft.TextField(
            label="Avatar URL",
            value=state.get("avatar", ""),
            border_radius=14,
            bgcolor=ft.Colors.WHITE,
            border_color="transparent",
            height=56,
            content_padding=ft.Padding(left=16, top=0, right=16, bottom=0),
            on_change=update_avatar_preview
        )
        avatar_preview = ft.Container(
            content=ft.CircleAvatar(foreground_image_src=state.get("avatar"), background_image_src=state.get("avatar"), radius=48),
            width=100,
            height=100,
            alignment=ft.Alignment.CENTER,
            border_radius=50,
            bgcolor=ft.Colors.WHITE,
            shadow=ft.BoxShadow(blur_radius=12, color="#12000000", offset=ft.Offset(0, 4))
        )

        def update_avatar_preview(e=None):
            avatar_preview.content = ft.CircleAvatar(foreground_image_src=avatar_field.value or state.get("avatar"), background_image_src=avatar_field.value or state.get("avatar"), radius=48)
            page.update()

        def save_profile(e):
            state["current_user"] = name_field.value or state["current_user"]
            state["avatar"] = avatar_field.value or state.get("avatar")
            add_notification("Profile updated successfully.")
            navigate_to(render_main_page)

        page.add(
            ft.Column([
                ft.Container(
                    content=ft.Row([
                        ft.IconButton(icon=ft.icons.Icons.ARROW_BACK_IOS_NEW, icon_size=20, on_click=lambda _: navigate_to(render_main_page)),
                        ft.Text("User Profile", size=26, weight="bold")
                    ], alignment=ft.MainAxisAlignment.START),
                    padding=ft.Padding(20, 20, 0, 10)
                ),
                ft.Container(height=20),
                ft.Row([
                    avatar_preview,
                    ft.Column([
                        ft.Text("Current profile photo", size=12, color="#777777"),
                        ft.Container(height=12),
                        ft.Text(state["current_user"], size=18, weight="bold")
                    ], spacing=6, horizontal_alignment=ft.CrossAxisAlignment.START)
                ], spacing=20, alignment=ft.MainAxisAlignment.START),
                ft.Container(height=24),
                ft.Container(
                    padding=ft.Padding(24, 0, 24, 0),
                    content=ft.Column([
                        name_field,
                        ft.Container(height=16),
                        avatar_field,
                        ft.Container(height=16),
                        ft.Row([
                            ft.Container(
                                content=ft.Text("Save", color=ft.Colors.WHITE, weight="bold"),
                                bgcolor="#685CF2",
                                height=52,
                                alignment=ft.Alignment.CENTER,
                                border_radius=14,
                                expand=True,
                                on_click=save_profile
                            ),
                            ft.Container(width=16),
                            ft.Container(
                                content=ft.Text("Logout", color=ft.Colors.WHITE, weight="bold"),
                                bgcolor="#D32F2F",
                                height=52,
                                alignment=ft.Alignment.CENTER,
                                border_radius=14,
                                expand=True,
                                on_click=lambda _: navigate_to(render_login_page)
                            )
                        ], spacing=0)
                    ], spacing=12)
                )
            ], spacing=0)
        )

    def render_calendar_page():
        selected_day = {"value": datetime.date.today()}
        selected_filter = {"value": "All"}

        def set_selected_day(day):
            selected_day["value"] = day
            page.update()

        def set_filter(value):
            selected_filter["value"] = value
            page.update()

        def get_week_days():
            start = selected_day["value"] - datetime.timedelta(days=7)
            return [start + datetime.timedelta(days=i) for i in range(15)]

        def parse_task_date(task):
            if task.get("deadline"):
                try:
                    return datetime.datetime.fromisoformat(task["deadline"]).date()
                except Exception:
                    return None
            return None

        def get_tasks_for_day():
            tasks = []
            for task in state["tasks"]:
                due_date = parse_task_date(task)
                status = task.get("status", "Assign")
                if selected_filter["value"] == "Completed":
                    if status == "Done" and due_date == selected_day["value"]:
                        tasks.append(task)
                elif selected_filter["value"] == "Ongoing":
                    if status != "Done" and (due_date is None or due_date >= selected_day["value"]):
                        tasks.append(task)
                else:
                    if due_date == selected_day["value"]:
                        tasks.append(task)
            return tasks

        def open_task_dialog(task):
            status_text = ft.Text(task.get("status", "Assign"), weight="bold")

            def change_status(new_status):
                if task.get("status") != new_status:
                    task["status"] = new_status
                    status_text.value = new_status
                    add_notification(f"Task '{task.get('title')}' status changed to {new_status}.")
                    page.update()

            def build_status_action(label):
                active = task.get("status") == label
                return ft.Container(
                    content=ft.Text(label, size=12, weight="bold", color="#FFFFFF" if active else "#555555"),
                    bgcolor="#685CF2" if active else "#F0F2F5",
                    padding=ft.Padding(12, 10, 12, 10),
                    border_radius=12,
                    on_click=lambda e, l=label: change_status(l)
                )

            dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text(task.get("title", "Task Detail"), weight="bold"),
                content=ft.Column([
                    ft.Text(task.get("description", ""), size=13, color="#555555"),
                    ft.Container(height=12),
                    ft.Row([
                        ft.Column([
                            ft.Text("Priority", size=11, color="#777777"),
                            ft.Text("Urgency" if task.get("priority") == 1 else "Importance", weight="bold")
                        ]),
                        ft.Column([
                            ft.Text("Status", size=11, color="#777777"),
                            status_text
                        ])
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Container(height=12),
                    ft.Row([
                        build_status_action("Assign"),
                        build_status_action("Processing"),
                        build_status_action("Done")
                    ], spacing=10),
                    ft.Container(height=12),
                    ft.Row([
                        ft.Icon(ft.icons.Icons.PERSON, size=16, color="#685CF2"),
                        ft.Text(f"Assigned to {task.get('friend_assignid', 'N/A')}", size=12, color="#555555")
                    ]),
                    ft.Container(height=12),
                    ft.Row([
                        ft.Icon(ft.icons.Icons.EVENT, size=16, color="#555555"),
                        ft.Text(task.get("deadline", "No deadline"), size=12, color="#555555")
                    ])
                ]),
                actions=[
                    ft.TextButton("Close", on_click=lambda e: close_dialog())
                ],
                actions_alignment=ft.MainAxisAlignment.END
            )

            def close_dialog():
                dialog.open = False
                page.dialog = None
                page.update()

            page.dialog = dialog
            dialog.open = True
            page.update()

        def build_day_button(day):
            active = day == selected_day["value"]
            return ft.Container(
                content=ft.Column([
                    ft.Text(str(day.day), size=16, weight="bold", color="#FFFFFF" if active else "#444444"),
                    ft.Text(day.strftime("%a"), size=12, color="#FFFFFF" if active else "#888888")
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                bgcolor="#685CF2" if active else "#F5F5FF",
                width=60,
                height=70,
                border_radius=18,
                alignment=ft.Alignment.CENTER,
                on_click=lambda e, d=day: set_selected_day(d)
            )

        def build_filter_button(label):
            active = selected_filter["value"] == label
            return ft.Container(
                content=ft.Text(label, size=12, weight="bold", color="#FFFFFF" if active else "#555555"),
                bgcolor="#685CF2" if active else "#F0F2FF",
                padding=ft.Padding(18, 12, 18, 12),
                border_radius=14,
                on_click=lambda e, v=label: set_filter(v)
            )

        tasks = get_tasks_for_day()

        header = ft.Row([
            ft.IconButton(icon=ft.icons.Icons.ARROW_BACK_IOS_NEW, icon_size=20, on_click=lambda _: navigate_to(render_main_page)),
            ft.Column([
                ft.Text(selected_day["value"].strftime("%A, %b %d"), size=24, weight="bold"),
                ft.Text("Tasks for the selected day", size=12, color="#777777")
            ]),
            ft.Container(
                content=ft.Icon(ft.icons.Icons.ADD, color="white", size=24),
                bgcolor="#685CF2",
                width=50, height=50,
                border_radius=16,
                alignment=ft.Alignment.CENTER,
                on_click=lambda _: navigate_to(render_new_task_page)
            )
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        day_row = ft.Row(
            [build_day_button(day) for day in get_week_days()],
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
            height=90
        )
        filter_row = ft.Row([
            build_filter_button("All"),
            build_filter_button("Ongoing"),
            build_filter_button("Completed")
        ], spacing=10)

        def build_task_card(task):
            completion = 1.0 if task.get("status") == "Done" else 0.5 if task.get("status") == "Processing" else 0.2
            return ft.Container(
                bgcolor=ft.Colors.WHITE,
                border_radius=20,
                padding=ft.Padding(18, 18, 18, 18),
                shadow=ft.BoxShadow(blur_radius=16, color="#12000000", offset=ft.Offset(0, 6)),
                on_click=lambda e, t=task: open_task_dialog(t),
                content=ft.Column([
                    ft.Row([
                        ft.Column([
                            ft.Text(task.get("title", "Untitled Task"), size=16, weight="bold"),
                            ft.Text(task.get("description", ""), size=12, color="#777777")
                        ]),
                        ft.Container(
                            content=ft.Text(f"{int(completion*100)}%", size=12, weight="bold", color="#685CF2"),
                            bgcolor="#F5F6FF",
                            padding=ft.Padding(12, 8, 12, 8),
                            border_radius=14
                        )
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Container(height=18),
                    ft.Row([
                        ft.Row([
                            ft.CircleAvatar(foreground_image_src="https://i.pravatar.cc/100?u=1", background_image_src="https://i.pravatar.cc/100?u=1", radius=14),
                            ft.CircleAvatar(foreground_image_src="https://i.pravatar.cc/100?u=2", background_image_src="https://i.pravatar.cc/100?u=2", radius=14),
                            ft.CircleAvatar(foreground_image_src="https://i.pravatar.cc/100?u=3", background_image_src="https://i.pravatar.cc/100?u=3", radius=14)
                        ], spacing=-8),
                        ft.Text(task.get("deadline", ""), size=11, color="#999999")
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                ])
            )

        task_cards = ft.Column([build_task_card(task) for task in tasks], spacing=14)
        if not tasks:
            task_cards = ft.Column([ft.Text("No tasks due on this day.", size=14, color="#777777")])

        page.add(
            ft.Column([
                header,
                ft.Container(height=20),
                day_row,
                ft.Container(height=18),
                filter_row,
                ft.Container(height=18),
                task_cards
            ], spacing=18, expand=True)
        )

    def render_notifications_page():
        header = ft.Row([
            ft.IconButton(icon=ft.icons.Icons.ARROW_BACK_IOS_NEW, icon_size=20, on_click=lambda _: navigate_to(render_main_page)),
            ft.Text("Notifications", size=24, weight="bold"),
            ft.Container(width=20)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        if state.get("notifications"):
            notification_list = ft.Column([
                ft.Container(
                    bgcolor=ft.Colors.WHITE,
                    border_radius=18,
                    padding=ft.Padding(16, 16, 16, 16),
                    shadow=ft.BoxShadow(blur_radius=12, color="#12000000", offset=ft.Offset(0, 4)),
                    content=ft.Column([
                        ft.Text(note["message"], size=13, color="#21244f"),
                        ft.Container(height=6),
                        ft.Text(note["time"], size=11, color="#777777")
                    ], spacing=6)
                ) for note in state["notifications"]
            ], spacing=12)
        else:
            notification_list = ft.Column([
                ft.Text("No notifications yet.", size=14, color="#777777"),
                ft.Text("You will see updates when tasks are created or status changes.", size=12, color="#999999")
            ], spacing=10)

        page.add(
            ft.Column([
                header,
                ft.Container(height=20),
                notification_list
            ], spacing=18, expand=True)
        )

    # Start App
    render_login_page()

if __name__ == "__main__":
    ft.run(main)
