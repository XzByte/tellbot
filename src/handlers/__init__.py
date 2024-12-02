def register_handlers(dispatcher):
    from .start import start_handler
    from .help import help_handler

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)