# Introduction

Rundeck - https://github.com/rundeck is an open-source runbook automation software that brought operations to a whole new level: operations as a service. Rundeck is developed by Rundeck, Inc. and by the Rundeck community and new users are invited to contribute to the project.
Extended custom functionality can be added through plugins, which are also available as free open-source software at https://github.com/rundeck-plugins and usually developed in top languages such as: Java, Groovy, Python, Shell, PowerShell.

Building, adding or even writing or extending a new plugin, can be a tricky thing to do.
To embrace this challenge, and to ease our work when customizing at scale, this project aims to provide a software skeleton for developing new plugins and an automated process for attaching various plugins to your Rundeck instance.

![Diagram](https://user-images.githubusercontent.com/10680345/72182580-7408ec00-33f4-11ea-9c3a-e76d7f831840.jpg)

### Configuration
1. Make sure you have Rundeck installed.

  See https://docs.rundeck.com/docs/administration/install/

2. Make sure you have the following packages needed to run the plugin builder:

```openjdk-8-jdk python3 python3-pip git gradle```

3. Install python requirements:

```pip3 install -r ./requirements.txt```

### Usage

The build.py script is the entry point of the plugin builder. It takes a list of plugins as a parameter, downloads them from github and installs them in Rundeck's plugin path (usually at /var/lib/rundeck/libext).

If the --file argument is specified, it will install the plugins from the file's specified URLs. If you specify the "--plugin" argument, you can filter a set of plugins from the predefined list of URLs.

For now we've only included plugins that are listed in locations such as:
 - https://docs.rundeck.com/plugins/
 - https://github.com/rundeck-plugins/

If the plugin you wish to add is not yet included in our ./config/input-verbose.txt
options, just add the github HTTPS URL of the repository to your config file and pass the file as an option to the script.
Also, please notify us about what's missing and don't hesitate to add it to our list through a simple commit :)

```
usage: build.py [-h] [--file FILE] [--path RUNDECK_HOME] [--plugin PLUGIN]
                [--list]
optional arguments:
  -h, --help           show this help message and exit
  --file FILE          Rundeck Plugin Input File e.g. --file=config/input-
                       verbose.txt
  --path RUNDECK_HOME  Rundeck Plugins Path e.g. --path=/var/lib/rundeck/libext
  --plugin PLUGIN      Rundeck Plugin Input List: e.g --plugin="vault, slack"
  --list               List the available open-source plugins
```
 Listing available plugins
```
:~/rundeck-plugin-builder# ./build.py --list
docker
openssh-node-execution
rundeck-azure-plugin
slack-incoming-webhook-plugin
git-resource-model
jq-json-logfilter
...
```
- Cloning a small set of plugins using filters
```
./build.py --path=/var/lib/rundeck/libext/ --plugin='vault,slack'
```
- Cloning a set of plugins using an input file
```
./build.py --path=/var/lib/rundeck/libext/ --file=myfile.txt
```

# Why so complicated?
### If you don't necessarily need to do all of this on your local machine, we've containerized all of the above
### Just use our Dockerfile:
```
docker build -t myrundeck .
docker run -dit -p 4440:4440 myrundeck
docker exec -it <ID> /bin/sh
```
### Contributing

Ideas and contributions are fully welcomed and encouraged. Please keep in mind to add value to the project with
each contribution you make.
For further information, read the [Contributing Guide](./.github/CONTRIBUTING.md).

### Licensing

This project is licensed under the Apache V2 License. For more information, see [LICENSE](LICENSE).
