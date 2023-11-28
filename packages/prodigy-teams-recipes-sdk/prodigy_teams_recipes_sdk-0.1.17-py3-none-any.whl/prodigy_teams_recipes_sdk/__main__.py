# This function is exposed via the setup.cfg as the ptr commant, so don't change this!
def main():
    # TODO: Unhack
    import os

    from .engine.cli import cli
    from .engine.registry import get_recipes_registry

    if "PRODIGY_TEAMS_RECIPES_IMPORT" in os.environ:
        value = os.environ["PRODIGY_TEAMS_RECIPES_IMPORT"]
        registry = get_recipes_registry()
        registry.set_load_path([value])
    cli.run()


if __name__ == "__main__":
    main()
