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
    parser.add_argument("--input", dest='input', type=str, help="Input file")
    parser.add_argument("--path", dest='rundeck_home', type=str, help="Rundeck home path")
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    if not args.input or not args.rundeck_home:
        parser.print_help(sys.stderr)
        sys.exit(1)
    if not os.path.isdir(args.rundeck_home):
        print("Rundeck home path is invalid. Exiting...")
        sys.exit(1)
    if args.input:
        if not os.path.isfile(args.input):
            print('The specified input file {} does not exist'.format(args.input))
            sys.exit()
        plugins = read_input(str(args.input))
        built_plugins = set()
        for plugin in plugins:
            build_plugin(plugin, built_plugins)

    print("Successfully built: {}".format(', '.join(map(str, built_plugins))))
    print("Build failed for: {}".format(', '.join(map(str, plugins-built_plugins))))
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
