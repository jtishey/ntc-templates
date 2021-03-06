"""ntc_templates.parse."""
import os
import sys
try:
    from textfsm import clitable
except ImportError:
    import clitable


def _get_template_dir():
    ntc_template_abspath = os.path.abspath(sys.modules['ntc_templates'].__file__)
    base_dir = os.path.dirname(ntc_template_abspath)
    template_dir = '%s%s%s' % (base_dir, os.sep, 'templates')
    return template_dir


def _clitable_to_dict(cli_table):
    """Convert TextFSM cli_table object to list of dictionaries."""
    objs = []
    for row in cli_table:
        temp_dict = {}
        for index, element in enumerate(row):
            temp_dict[cli_table.header[index].lower()] = element
        objs.append(temp_dict)

    return objs


def parse_output(platform=None, command=None, data=None):
    """Return the structured data based on the output from a network device."""
    template_dir = _get_template_dir()
    cli_table = clitable.CliTable('index', template_dir)

    attrs = dict(
        Command=command,
        Platform=platform
    )
    try:
        cli_table.ParseCmd(data, attrs)
        structured_data = _clitable_to_dict(cli_table)
    except clitable.CliTableError as e:
        raise Exception('Unable to parse command "%s" on platform %s - %s' % (command, platform, str(e)))
        # Invalid or Missing template
        # module.fail_json(msg='parsing error', error=str(e))
        # rather than fail, fallback to return raw text
        # structured_data = [data]

    return structured_data
