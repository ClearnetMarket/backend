import os

def load_config(mode=os.environ.get('MODE')):

    try:
        print(f"mode is {mode}")
        if mode == 'PRODUCTION':
            from settings_production import ApplicationConfig
            return ApplicationConfig
        elif mode == 'DEVELOPMENT':
            from settings_local import ApplicationConfig
            return ApplicationConfig

        else:
            pass

    except ImportError:
        from settings_local import ApplicationConfig
        return ApplicationConfig