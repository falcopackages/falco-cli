list_templates
==============


.. exec_code::
    :language_output: shell

    # --- hide: start ---
    from falco.management.commands.crud import Command

    Command().print_help("manage.py", "list_templates")
    #hide:toggle
