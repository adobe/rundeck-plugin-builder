### Introduction

#### Rundeck - https://github.com/rundeck is a free open-source runbook automation software that brought operations to a whole new level, operations as a service. Rundeck is developed by Rundeck, Inc. and by the Rundeck community and new users are invited to contribute to the project. Extended custom functionality can be added through plugins, also available as free open-source software at https://github.com/rundeck-plugins and usually developed in top languages such as: Java, Groovy, Python, Shell, PowerShell.
#### Nevertheless, building, adding or even writing or extending a new plugin, can be a tricky thing to do. To fully embrace this challenge, and to ease our work when customizing at scale, this project aims to provide a software skeleton for developing new plugins and an automated process for attaching the plugins to your Rundeck instance.

![Diagram](https://user-images.githubusercontent.com/10680345/72182580-7408ec00-33f4-11ea-9c3a-e76d7f831840.jpg)

### Usage

[TODO]

##### Configuration

[TODO]

##### Starting with gradle

[TODO]

### Build & Run

[TODO]

### Make sure openjdk-8-jdk is installed in your building environment and that it includes java and javac.
### To double check, run the following:
```
java -version
javac -version
```
### Your output should look something like this:
```
java -version
openjdk version "1.8.0_181"
OpenJDK Runtime Environment (build 1.8.0_181-8u181-b13-1~deb9u1-b13)
OpenJDK 64-Bit Server VM (build 25.181-b13, mixed mode)

javac -version
javac 1.8.0_232
```
### Download the source code for the plugins you wish to include. Source code for plugins is available in multiple Rundeck locations such as
 - https://docs.rundeck.com/plugins/
 - https://github.com/rundeck-plugins/

### Build the jars. After building, the jars should reside in build/libs/ as <my_plugin>.jar
```
./gradlew clean build
```

### Contributing

Ideas and contributions are fully welcomed and encouraged. The only recommendation we should keep in mind is to add value with every new submission and to keep Rundeck's trajectory a step ahead of today.
For more information, read the [Contributing Guide](./.github/CONTRIBUTING.md).

### Licensing

This project is licensed under the Apache V2 License. For more information, see [LICENSE](LICENSE).
