[![license](https://img.shields.io/badge/license-MIT-brightgreen)](https://spdx.org/licenses/MIT.html)
[![pipelines](https://gitlab.com/twiddle/mk-scaffold/badges/master/pipeline.svg)](https://gitlab.com/twiddle/mk-scaffold/pipelines)
[![coverage](https://gitlab.com/twiddle/mk-scaffold/badges/master/coverage.svg)](https://mk-scaffold.docs.twiddle.ovh//coverage/index.html)

# mk-scaffold -- make scaffold

A cookiecutter clone. A command-line utility that creates projects from templates.

## Features

- Conditional questions.
- Templated answers.
- Jinja2 extensions per template project.
- You don't have to know/write Python code to use.
- Project templates can be in any programming language or markup format:
  Python, JavaScript, Ruby, CoffeeScript, RST, Markdown, CSS, HTML, you name it.
  You can use multiple languages in the same project template.

## Installation

You can install the latest version from PyPI package repository.

~~~bash
python3 -mpip install -U mk-scaffold
~~~

## Usage

Sample command line usage:

~~~bash
mk-scaffold clone https://gitlab.com/twiddle/scaffolds/python-cli-template.git
~~~

Sample scaffold template file `scaffold.yml`:

~~~yml
questions:
  - name: "project_name"
    schema:
      min_length: 1

  - name: "project_short_description"
    schema:
      default: "Lorem ipsum sit dolor amet."
      max_length: 120
~~~

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## Locations

  * Documentation: [https://mk-scaffold.docs.twiddle.ovh/](https://mk-scaffold.docs.twiddle.ovh/)
  * Website: [https://gitlab.com/twiddle/mk-scaffold](https://gitlab.com/twiddle/mk-scaffold)
  * PyPi: [https://pypi.org/project/mk-scaffold](https://pypi.org/project/mk-scaffold)
