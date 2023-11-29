# $ jinja2

A CLI interface to Jinja2

Fork of jinja2-cli

<!-- ``` -->
<!-- $ jinja2 helloworld.tmpl data.json --format=json -->
<!-- $ cat data.json | jinja2 helloworld.tmpl -->
<!-- $ curl -s http://httpbin.org/ip | jinja2 helloip.tmpl -->
<!-- $ curl -s http://httpbin.org/ip | jinja2 helloip.tmpl > helloip.html -->
<!-- ``` -->
<!---->
## Changelog

- Add -F to read value from files
<!-- add a cli option -F to accept a file’s content as value for a key, like `-D key=<content of file>`, but you can use it as `-f key=<path-to-file>` -->

## Installation

### pipx

This is the recommended installation method.

```
$ pipx install jinja2-cli-tddschn
```

### [pip](https://pypi.org/project/jinja2-cli-tddschn/)

```
$ pip install jinja2-cli-tddschn
```


## Usage
```
Usage: jinja2 [options] <input template> <input data>

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  --format=FORMAT       format of input variables: auto, ini, json,
                        querystring, yaml, yml
  -e EXTENSIONS, --extension=EXTENSIONS
                        extra jinja2 extensions to load
  -D key=value          Define template variable in the form of key=value
  -F key=<path-to-file>, --file=key=<path-to-file>
                        Define template variable with a file content in the
                        form of key=<path-to-file>
  -s SECTION, --section=SECTION
                        Use only this section from the configuration
  --strict              Disallow undefined variables to be used within the
                        template
```

## Optional YAML support
If `PyYAML` is present, you can use YAML as an input data source.

`$ pip install jinja2-cli-tddschn[yaml]`

## Optional TOML support
If `toml` is present, you can use TOML as an input data source.

`$ pip install jinja2-cli-tddschn[toml]`

## Optional XML support
If `xmltodict` is present, you can use XML as an input data source.

`$ pip install jinja2-cli-tddschn[xml]`

## Optional HJSON support
If `hjson` is present, you can use HJSON as an input data source.

`$ pip install jinja2-cli-tddschn[hjson]`

## Optional JSON5 support
If `json5` is present, you can use JSON5 as an input data source.

`$ pip install jinja2-cli-tddschn[json5]`

<!-- ## TODO -->
<!--  * Variable inheritance and overrides -->
<!--   * Tests! -->
<!---->

## Develop

```
$ git clone https://github.com/tddschn/jinja2-cli-tddschn.git
$ cd jinja2-cli-tddschn
$ poetry install
```