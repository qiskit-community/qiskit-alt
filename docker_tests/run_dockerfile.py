#!/usr/bin/python

r"""
This is a test docstring.
"""

import subprocess as sb_pr
import fire


def subprocess_execute(command_list):
    """Subprocess_execute executes the command on host OS,
        then dumps the output to STDOUT.
    Arguments:
    command_list: This is a list of string making the command to be executed.
    """
    sb_pr.run(command_list, text=True, check=True)


def action_build(image_name, image_tag, dockerfile_name, docker_path):
    """The function action_build builds the image
    Arguments:
        image_name: Name of the image file.
        image_tag: Tag of the build image file.
        dockerfile_name: This is the Dockerfile to be used for building the image.
        docker_path: working directory of docker.
    """

    image_name_with_tag = image_name + ":" + image_tag
    build_command_list = [
        "docker",
        "build",
        "-t",
        image_name_with_tag,
        "-f",
        dockerfile_name,
        docker_path,
    ]
    return build_command_list


def action_run(image_name, image_tag, user_name, test_file_path, test_file_name):
    """The function action_run runs the container and initiates the tests.
    Arguments:
        image_name: Name of image to be used to build the containers.
        image_tag: The tag of imgaes to be used to build the containers.
        test_file_path: Path of the test file from which tests has to run.
        test_file_name: Name  of the file containing the tests to be done.
    """

    image_name_with_tag = image_name + ":" + image_tag
    run_command_list = [
        "docker",
        "run",
        "-it",
        image_name_with_tag,
        "/usr/bin/su",
        "-l",
        user_name,
        "-c",
        "cd " + image_name + "; sh " + test_file_path + test_file_name,
    ]
    return run_command_list


def action_get_into_fish(image_name, image_tag, user_name):
    """The function action_get_into_fish takes into the fish shell running in the container.
    Arguments:
        image_name: Name of the image to be used to build the container.
        image_tag: The tag of the image which is used to build the container.
        user_name: The user name which logins into the container.
    """

    image_name_with_tag = image_name + ":" + image_tag
    get_fish_command_list = [
        "docker",
        "run",
        "-it",
        image_name_with_tag,
        "/usr/bin/su",
        "-l",
        user_name,
        "-s",
        "/usr/bin/fish",
    ]
    return get_fish_command_list


def action_get_into_bash(image_name, image_tag, user_name):
    """The function action_get_into_bash takes into the bash shell running in the container.
    Arguments:
        image_name: Name of the image to be used to build the container.
        image_tag: The tag of the image which is used to build the container.
        user_name: The user name which logins into the container.
    """

    image_name_with_tag = image_name + ":" + image_tag
    get_bash_command_list = [
        "docker",
        "run",
        "-it",
        image_name_with_tag,
        "/usr/bin/su",
        "-l",
        user_name,
        "-s",
        "/usr/bin/bash",
    ]
    return get_bash_command_list


def action_get_into_rootfish(image_name, image_tag):
    """The function action_get_into_rootfish takes into the fish shell
        running in the container as root.
    Arguments:
        image_name: Name of the image to be used to build the container.
        image_tag: The tag of the image which is used to build the container.
        user_name: The user name which logins into the container.
    """

    image_name_with_tag = image_name + ":" + image_tag
    get_rootfish_command_list = [
        "docker",
        "run",
        "-it",
        image_name_with_tag,
        "/usr/bin/fish",
    ]
    return get_rootfish_command_list


def _cli(
    action="",
    image_name="qiskit_alt",
    image_tag="latest",
    dockerfile_name="Dockerfile",
    user_name="quser",
    test_file_path="./",
    test_file_name="run_init_tests.sh",
    docker_path="..",
    dry_run="false",
):
    """All the arguments of this function are supposed to be passed as command line
        arguments while initiating the python script.
    Arguments:
        action: This are the possible actions to be performed.
                Possible actions are:
                        build: To build the containers
                                Example: ./run_dockerfile.py --action=build
                        run: To run the containers
                        "": To build and then to run the containers.
                        get_into_fish: To get into the fish shell running in the container.
                        get_into_bash: To get into the bash shell running in the container.
                        get_into_rootfish: To get into the fish shell running in the container
                                            as root.

        image_name: The name of the image to be build.
        image_tag: The tag given to the image to be build.
        dockerfile_name: The name of the Dockerfile to be used for building the image.
        user_name: A username in the container.
        test_file_path: The path to the test file which contains all the tests to run.
        docker_path: The working directory for docker.
        dry_run: Either true or false. If true, then only print action, but don't execute it.
    """

    if dry_run == "false":
        _dry_run = False
    elif dry_run == "true":
        _dry_run = True
    else:
        print("dry_run must be either true or false. See ./run_dockerfile.py --help")
        return

    command_lists = []

    if action == "build":
        command_lists.append(action_build(image_name, image_tag, dockerfile_name, docker_path))
    elif action == "run":
        command_lists.append(action_run(image_name, image_tag, user_name, test_file_path, test_file_name))
    elif action == "":
        command_lists.append(action_build(image_name, image_tag, dockerfile_name, docker_path))
        command_lists.append(action_run(image_name, image_tag, user_name, test_file_path, test_file_name))
    elif action == "get_into_fish":
        command_lists.append(action_get_into_fish(image_name, image_tag, user_name))
    elif action == "get_into_bash":
        command_lists.append(action_get_into_bash(image_name, image_tag, user_name))
    elif action == "get_into_rootfish":
        command_lists.append(action_get_into_rootfish(image_name, image_tag))
    else:
        print("Bad arguments, See ./run_dockerfile.py --help")

    for command_list in command_lists:
        command_string = " ".join(map(str, command_list))
        print(command_string + "\n")
        if not _dry_run:
            subprocess_execute(command_list)


if __name__ == "__main__":
    fire.Fire(_cli)
