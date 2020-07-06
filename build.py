#!/usr/bin/env python3
##########################################################################################
# Copyright 2020 Adobe. All rights reserved.
# This file is licensed to you under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy
# of the License at http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
# OF ANY KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.
##########################################################################################
import git
import os
import argparse
import sys
import subprocess
import shlex
import re
import shutil
import glob

DELIM = '\n' + '-' * 200 + '\n'
BUILD_PATH = 'buildplugins'
URL_INPUT_VERBOSE_FILE = './config/input-verbose.txt'

def list_plugins_from_file(filename=URL_INPUT_VERBOSE_FILE):
    '''
        Lists the currently available Rundeck plugins as stored in input-verbose.txt
    :param filename:str
    '''
    with open(filename, "r") as f:
        for line in f:
            matchURL = re.match(r'https://github.com/(.*)/(.*)', line)
            if not matchURL:
                continue
            else:
                print(matchURL.group(2))
    sys.exit(1)

def clone_plugin_from_list(plugins_list:str, filename=URL_INPUT_VERBOSE_FILE, build_path=BUILD_PATH) -> set:
    '''
        Clones a set of Rundeck plugins based on a list of strings that match the available plugins
    :param plugins_list:str
    :param filename:str
    :param build_path:str
    :return list: list of cloned plugins
    '''
    if not os.path.isfile(filename):
        print("File does not exist")

    plugins = plugins_list.split(",")

    with open(filename, "r") as f:
        for line in f:
            for p in plugins:
                matchExpr = r'(https://github.com/.*/.*' + p + '.*)'
                matchURL=re.match(matchExpr, line)
                if matchURL:
                    print("Found {}".format(line))
                    if os.path.isdir(os.getcwd() + "/" + build_path + "/" + str(line.strip().split("/")[-1])):
                        print("Repository already exists. Jumping to the next...\n")
                        continue
                    else:
                        print("Cloning {}...\n".format(line.strip().split("/")[-1]))
                        git.Git(build_path).clone(line.strip())
    cloned_plugins = set()
    for plugin in plugins:
        matchStr = r'{}'.format(plugin)
        cloned_plugins.update({x for x in os.listdir(build_path) if os.path.isdir(os.path.join(build_path, x.strip())) and re.match(matchStr, x)})
    if len(cloned_plugins) == 0:
        print("There's not plugin to match this name. Please try something else...")
        sys.exit(1)

    return cloned_plugins

def clone_plugin_from_file(filename:str, build_path=BUILD_PATH) -> set:
    '''
        Clones a set of Rundeck plugins listed in an input file containing specific HTTPS git URLs
    :param filename:str
    :param build_path:str
    :return list: list of cloned plugins
    '''
    if not os.path.isdir(build_path):
        os.mkdir(build_path)
        print ("Build path is created at {}/{}...".format(os.getcwd(), build_path))
    else:
        print("Build path already exists at {}/{}...".format(os.getcwd(), build_path))

    with open(filename,"r") as f:
        for line in f:
            matchURL = re.match( r'https://github.com/(.*)/(.*)', line)
            if not matchURL:
                continue
            plugin = matchURL.group(2)
            print("Cloning {}...".format(plugin))
            if os.path.isdir(os.getcwd() + "/" + build_path + "/" + plugin):
                print("Repository already exists. Jumping to the next...")

            else:
                git.Git(build_path).clone(line.strip())

    plugins = {x for x in os.listdir(build_path) if os.path.isdir(os.path.join(build_path, x))}

    return plugins

def build_plugin(plugin:str, built_plugins:set):
    '''
       Goes into the plugins' home directory, builds the plugin and then goes back to the Rundeck home directory
    :param plugin:str
    :built_plugins: set
    :return
    '''
    rundeck_rootdir = os.getcwd()
    os.chdir(os.getcwd() + "/" + BUILD_PATH + "/" + plugin)
    print("{}Building {}{}".format(DELIM, plugin, DELIM))
    run_command('gradle clean build', built_plugins, plugin)
    os.chdir(rundeck_rootdir)

def run_command(command:str, built_plugins:set, plugin:str):
    '''
       Runs the build command and checks if build ran successfully, in which case it adds the plugin to the set of successfully build plugins
    :param command:str
    :param built_plugins:set
    :param plugin:str
    '''
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
    while True:
        output = process.stdout.readline()
        if not output and process.poll() is not None:
            break
        if output:
            print(output.strip().decode('utf-8'))
            if 'BUILD SUCCESSFUL' in output.strip().decode('utf-8'):
                built_plugins.add(plugin)

def copy_art(built_plugins:set, dest:str):
    '''
        Looks for the specific artifact corresponding to the plugin build and copies it into the Rundeck plugin designated path
    :param built_plugins:set
    :param dest:str
    '''
    for plugin in built_plugins:
        artfile = ""
        for f in glob.glob(BUILD_PATH + '/' + plugin + '/build/libs/*'):
            artfile = os.path.split(f)[-1]
        if artfile:
            print("Copying {} to {}...".format(artfile, dest))
            shutil.copy2(BUILD_PATH + '/' + plugin + '/build/libs/' + artfile, dest)

def main():
    '''
        - Parses arguments and prints specific messages for each scenario
        - Prints the set of successfully built plugins and the set of plugins for which the build has failed
        - Copies artifacts into the Rundeck plugin designated home path
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", dest='file', type=str, help="Rundeck Plugin Input File e.g. --file=config/input-verbose.txt")
    parser.add_argument("--path", dest='rundeck_home', type=str, help="Rundeck Home Path e.g. --path=/var/lib/rundeck/libext")
    parser.add_argument("--plugin", dest='plugin', type=str, help="Rundeck Plugin Input List: e.g --plugin=\"vault, slack\"")
    parser.add_argument("--list", dest='list', action='append_const', const='list_plugins_from_file', help="List the available open-source plugins")
    args = parser.parse_args()

    if args.list:
        list_plugins_from_file(URL_INPUT_VERBOSE_FILE)
    if not args.rundeck_home:
        parser.print_help(sys.stderr)
        sys.exit(1)
    if not os.path.isdir(args.rundeck_home):
        print("Rundeck home path is invalid. Exiting...")
        sys.exit(1)
    if not args.file and not args.plugin:
        print("You need to provide at least one plugin using --file or --plugin")
        sys.exit()

    built_plugins = set()
    cloned_plugins = set()
    if args.file:
        if not os.path.isfile(args.file):
            print('The specified input file {} does not exist'.format(args.file))
            sys.exit(1)
        cloned_plugins_file = clone_plugin_from_file(str(args.file))
        cloned_plugins.update(cloned_plugins_file)
        for plugin in cloned_plugins_file:
            build_plugin(plugin, built_plugins)
    if args.plugin:
        cloned_plugins_list = clone_plugin_from_list(args.plugin)
        cloned_plugins.update(cloned_plugins_list)
        for plugin in cloned_plugins_list:
            build_plugin(plugin, built_plugins)

    print("{}Successfully built: {}".format(DELIM, ', '.join(map(str, built_plugins))))
    print("Build failed for: {}".format('None' if len(cloned_plugins-built_plugins)==0 else ', '.join(map(str, cloned_plugins-built_plugins))))
    print("{}Copying artifacts into the {} Rundeck root directory{}".format(DELIM, args.rundeck_home, DELIM))

    copy_art(built_plugins, args.rundeck_home)

if __name__ == '__main__':
    main()
