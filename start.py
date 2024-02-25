import argparse
import configparser


def helper(arg_name, arg_value, config, own_err_msg):
    """
    Retrieve default values from config file or user input and write it to config file in the latter case.
    """
    value = arg_value
    if value is None:
        try:
            value = config['General'][arg_name]
        except (configparser.NoSectionError, configparser.NoOptionError):
            print(own_err_msg)
    else:
        config['General'][arg_name] = value


def start():
    config_file = 'defaults.ini'
    config = configparser.ConfigParser()
    try:
        # According to Doc: Use read_file() when file is expected to assist
        config.read_file(open(config_file))
    except FileNotFoundError:
        config['General'] = {}
    p = argparse.ArgumentParser(__file__)
    arg_dir = 'dir'
    p.add_argument(f'--{arg_dir}',
                   help='Top level directory. Here will all files and directories be saved.',
                   type=str)
    arg_firefox_profile = 'firefox_profile'
    p.add_argument(f'--{arg_firefox_profile}',
                   help='Path to the firefox profile.',
                   type=str)
    # TODO: Option for creating pdfs <25-02-2024, Philipp Rost>
    args = p.parse_args()
    dir, firefox_profile = args.dir, args.firefox_profile
    helper(arg_dir, dir, config, 'No default recipe directory set. Please use\n\t--dir DIRECTORY\nif it\'s your first run.')
    helper(arg_firefox_profile, firefox_profile, config, 'No default firefox profile path set. Please use\n\t--firefox_profile PATH\nif it\'s your first run.')
    with open(config_file, 'w') as f:
        config.write(f)


if __name__ == "__main__":
    start()
