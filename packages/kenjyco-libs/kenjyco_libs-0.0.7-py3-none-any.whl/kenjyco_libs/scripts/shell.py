import click


@click.command()
@click.option(
    '--no-vi', 'no_vi', is_flag=True, default=False,
    help='Do not use vi editing mode in ipython'
)
@click.option(
    '--no-colors', 'no_colors', is_flag=True, default=False,
    help='Do not use colors / syntax highlighting in ipython'
)
@click.option(
    '--confirm-exit', 'confirm_exit', is_flag=True, default=False,
    help='Prompt "Do you really want to exit ([y]/n)?" when exiting ipython'
)
def main(**kwargs):
    """Start ipython with several things imported"""
    import bg_helper as bh
    import fs_helper as fh
    import input_helper as ih
    import kenjyco_libs as kl
    import settings_helper as sh
    from importlib import import_module
    from pprint import pprint
    things = {'bh': bh, 'fh': fh, 'ih': ih, 'kl': kl, 'sh': sh, 'pprint': pprint}
    optional_imports = [
        ('aws_info_helper', 'ah'),
        ('chloop', 'chloop'),
        ('dt_helper', 'dh'),
        ('expectation_helper', 'eh'),
        ('mongo_helper', 'mh'),
        ('readme_helper', 'rmh'),
        ('redis_helper', 'rh'),
        ('sql_helper', 'sqh'),
        ('testing_helper', 'th'),
        ('webclient_helper', 'wh'),
    ]
    for package_name, import_name in optional_imports:
        try:
            things[import_name] = import_module(package_name)
        except (ImportError, ModuleNotFoundError):
            pass

    ih.start_ipython(
        colors=not kwargs['no_colors'],
        vi=not kwargs['no_vi'],
        confirm_exit=kwargs['confirm_exit'],
        **things
    )


if __name__ == '__main__':
    main()

