"""Main function unifying all the group's creators.

The groups should only contribute to their own folder (and in some cases to resources-folder), but not to this file.
"""

import argparse
import importlib
import json
import os

from resources.sample_inputs import SAMPLE_INPUTS
import page


def get_input_arguments():
    """Get input arguments given to all groups' creators.
    """
    return SAMPLE_INPUTS[0]


def get_page_layout(creators):
    domains = []
    for creator in creators:
        domains.append(creator.domain)
    return ['word', 'word']


def get_outputs(input_args, n_artifacts_per_creator, creators):
    """Create 'a page' of the book.
    """
    # TODO: Clean out the code and make it simpler.
    all_artifacts = []
    n_imagepaths = 0
    kwargs = {'title': "",
            'poem': "",
            'imagepath1': "",
            'imagepath2': "",
            'imagepath3': "",
            'imagepath4': ""
            }

    print()
    for name, creator in creators:
        domain = creator.domain
        print("Generating for {} ({})...".format(name, domain))
        artifacts = creator.create(*input_args, n_artifacts_per_creator)
        if domain == 'word':
            kwargs['title'] = artifacts[0][0]
        elif domain == 'poetry':
            kwargs['poem'] = artifacts[0][0]
        elif domain == 'image':
            if n_imagepaths == 0:
                kwargs['imagepath1'] = artifacts[0][0]
            if n_imagepaths == 1:
                kwargs['imagepath2'] = artifacts[0][0]
            if n_imagepaths == 2:
                kwargs['imagepath3'] = artifacts[0][0]
            if n_imagepaths == 3:
                kwargs['imagepath4'] = artifacts[0][0]
            n_imagepaths += 1

        print("Output of {} ({}): {}\n".format(name, domain, artifacts))
        all_artifacts.append((name, domain, artifacts))
    #print("All returned artifacts: {}".format(all_artifacts))
    page.create_page(**kwargs)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a book using all creators defined in the config.")
    parser.add_argument('-c', dest='config_file',  default='main_config.json',
                        help='Path to the main config file.')
    parser.add_argument('-p', dest='pages', default=10, type=int,
                        help='Number of "pages" to create. A single page contains artifacts from several domains.')

    args = parser.parse_args()
    n_pages = args.pages
    config = json.load(open(args.config_file))
    folders = config['folders']

    group_creators = []
    n_artifacts_per_creator = 1

    # Initialize each group's creator
    for group_folder in folders:
        group_config = json.load(open(os.path.join(group_folder, 'config.json')))
        module_name = group_config['module_name']
        class_name = group_config['class_name']
        domain = group_config['domain']
        group_kwargs = group_config['init_kwargs']

        # Dynamically import the main-module from the group's folder and the class specified in the config.
        print("Initializing '{}' ({})...".format(group_folder, domain))
        group_module = importlib.import_module("{}.{}".format(group_folder, module_name))
        group_class = getattr(group_module, class_name)
        class_instance = group_class(**group_kwargs)
        group_creators.append([group_folder, class_instance])
        print()

    # Run each groups creator for a number of times specified in command line.
    for _ in range(n_pages):
        input_args = get_input_arguments()
        get_outputs(input_args, n_artifacts_per_creator, group_creators)

