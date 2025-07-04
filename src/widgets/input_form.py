import flet as ft
            
def input_form(*, label: str, icon: str, disabled: bool = False, keyboard_type:ft.KeyboardType = ft.KeyboardType.TEXT, input_filter:ft.InputFilter = None) -> ft.TextField:
    # Normalize the label for comparison to avoid case-sensitivity issues
    normalized_label = label.lower()

    is_description = (normalized_label == "descripcion")

    # Define min_lines based on whether it's a description
    # This is crucial for setting a minimum visible height
    min_lines_value = 5 if is_description else 1

    # max_lines also depends on whether it's a description
    max_lines_value = 5 if is_description else 1 # If you want it to scroll after 5 lines

    # Determine if it should expand horizontally (e.g., in a Row)
    # Note: expand doesn't directly control vertical height for TextField
    should_expand = True if is_description else False

    # Define max_length (from our previous discussion for character validation)
    max_length_value = 200 if is_description else 50 # Example limits

    # Event handler for dynamic validation (from previous discussion)
    def on_text_changed(e):
        current_length = len(e.control.value)
        # You can add more complex validation here if needed
        if current_length > max_length_value:
            e.control.error_text = f"Máximo {max_length_value} caracteres."
            # Optionally truncate if max_length is not strictly enforced by Flet
            # e.control.value = e.control.value[:max_length_value]
        elif current_length == 0 and e.control.label.lower() != "descripcion": # Example: require text for non-description fields
            e.control.error_text = "Este campo no puede estar vacío."
        else:
            e.control.error_text = None
        e.page.update() # Essential to see error_text changes

    return ft.TextField(
        disabled= disabled,
        keyboard_type= keyboard_type,
        input_filter= input_filter,
        label=label,
        label_style=ft.TextStyle(
            color=ft.Colors.GREY_600,
            weight=ft.FontWeight.BOLD,
            size=14,
        ),
        border_color=ft.Colors.GREY_300,
        bgcolor=ft.Colors.WHITE,
        width=350, # Fixed width for the TextField itself
        text_size=14,
        text_style=ft.TextStyle(
            color=ft.Colors.GREY_600
        ),
        prefix_icon=icon,
        border_radius=ft.border_radius.all(22),
        multiline=is_description, # Use the boolean variable
        min_lines=min_lines_value, # <--- Added this, crucial for minimum height!
        max_lines=max_lines_value, # Use the boolean variable
        max_length=max_length_value, # <--- Added max_length for character limits
        expand=should_expand, # Use the boolean variable
        on_change=on_text_changed, # <--- Added on_change for dynamic validation
    )
    