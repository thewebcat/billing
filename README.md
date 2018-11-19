# Billing System Api
This is a test project

Usage
------------

First you need to install docker, you can take it by this command:
``` {.sourceCode .bash}
$ ./run.sh setup
```

And then build and run project
``` {.sourceCode .bash}
$ ./run.sh stack
```

Up/Down project
``` {.sourceCode .bash}
$ docker-compose up -d
$ docker-compose down
```

Running all tests with coverage report:
``` {.sourceCode .bash}
$ ./run.sh test ci
```

Running tests:
``` {.sourceCode .bash}
$ ./run.sh test style
$ ./run.sh test unit
$ ./run.sh test functional
```
