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

delimiter = '\n' + '-' * 200 + '\n'


def clone_plugin_list(plugins_list:str, filename:str, build_path="buildplugins") -> set:
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

    plugins = {x for x in os.listdir(build_path) if os.path.isdir(os.path.join(build_path, x))}

    return plugins

def read_input(filename:str, build_path="buildplugins") -> set:
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

def build_plugin(plugin, built_plugins):
    rundeck_rootdir = os.getcwd()
    os.chdir(os.getcwd() + "/buildplugins/" + plugin)
    print("{}Building {}{}".format(delimiter, plugin, delimiter))
    run_command('gradle clean build', built_plugins, plugin)
    os.chdir(rundeck_rootdir)

def run_command(command, built_plugins, plugin):
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
    while True:
        output = process.stdout.readline()
        if not output and process.poll() is not None:
            break
        if output:
            print(output.strip().decode('utf-8'))
            if 'BUILD SUCCESSFUL' in output.strip().decode('utf-8'):
                built_plugins.add(plugin)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", dest='file', type=str, help="Input file")
    parser.add_argument("--path", dest='rundeck_home', type=str, help="Rundeck home path")
    parser.add_argument("--plugin", dest='plugin', type=str, help="Rundeck plugin (minimum 5 ch)")
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
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
            sys.exit()
            cloned_plugins_file = (read_input(str(args.file)))
            cloned_plugins.update(cloned_plugins_file)
            for plugin in cloned_plugins_file:
                build_plugin(plugin, built_plugins)
    if args.plugin:
        cloned_plugins_list = clone_plugin_list(args.plugin, 'config/input-verbose.txt')
        cloned_plugins.update(cloned_plugins_list)
        for plugin in cloned_plugins_list:
            build_plugin(plugin, built_plugins)

    print("Successfully built: {}".format(', '.join(map(str, built_plugins))))
    print("Build failed for: {}".format('None' if len(cloned_plugins-built_plugins)==0 else ', '.join(map(str, cloned_plugins-built_plugins))))
    print("{}Copying artifactories into {} Rundeck root directory{}".format(delimiter, args.rundeck_home, delimiter))

    for plugin in built_plugins:
        jarfile = ""
        for f in glob.glob('buildplugins/'+ plugin + '/build/libs/*'):
            jarfile = os.path.split(f)[-1]
        if jarfile:
            print("Copying {} to {}...".format(jarfile, args.rundeck_home))
            shutil.copy2('buildplugins/' + plugin + '/build/libs/' + jarfile, args.rundeck_home)

if __name__ == '__main__':
    main()
