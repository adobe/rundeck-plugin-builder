### Introduction

#### Rundeck - https://github.com/rundeck is a free open-source runbook automation software that brought operations to a whole new level, operations as a service. Rundeck is developed by Rundeck, Inc. and by the Rundeck community and new users are invited to contribute to the project. Extended custom functionality can be added through plugins, also available as free open-source software at https://github.com/rundeck-plugins and usually developed in top languages such as: Java, Groovy, Python, Shell, PowerShell.
#### Nevertheless, building and adding a new plugin can be a tricky thing to do. To fully embrace this challenge, and to ease our work when customizing at scale, this project aims to provide an automated process for attaching the plugins to your Rundeck instance without being necessary to build Rundeck from scratch.

![Diagram](https://user-images.githubusercontent.com/10680345/72182580-7408ec00-33f4-11ea-9c3a-e76d7f831840.jpg)

### Usage

The build.py script is the entry point of the plugin builder. It takes a list of plugins as a parameter, downloads them from github and installs them in Rundeck's plugin path (usually at /var/lib/rundeck/libext).

It installs the plugins from the URLs found in the file specified with the --file argument. You can also filter the plugins to install from the URLs file by using the "--plugin" argument.

Source code for plugins is available in multiple Rundeck locations such as
 - https://docs.rundeck.com/plugins/
 - https://github.com/rundeck-plugins/

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

##### Configuration
1. Make sure you have Rundeck installed.

  See https://docs.rundeck.com/docs/administration/install/
 
2. Make sure you have the following packages needed to run the plugin builder:

```openjdk-8-jdk python3 python3-pip git gradle```

3. Install python requirements:

```pip3 install -r ./requirements.txt```

An example of configuration is illustrated in the Dockerfile located in the root of the project.

### Build & Run

After the configuration is done, run the script as described in the Usage section.

### Contributing

Ideas and contributions are fully welcomed and encouraged. The only recommendation we should keep in mind is to add value with every new submission and to keep Rundeck's trajectory a step ahead of today.
For more information, read the [Contributing Guide](./.github/CONTRIBUTING.md).

### Licensing

This project is licensed under the Apache V2 License. For more information, see [LICENSE](LICENSE).
