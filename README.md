Thor - The web server of WeatherMagic
=============================

[![Build Status](https://travis-ci.org/WeatherMagic/thor.svg?branch=master)](https://travis-ci.org/WeatherMagic/thor)


<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-generate-toc again -->
**Table of Contents**

- [Thor - The web server of WeatherMagic](#thor---the-web-server-of-weathermagic)
    - [Dependencies](#dependencies)
    - [Installation](#installation)
    - [Usage](#usage)
    - [License](#license)
    - [Development](#development)
    - [Testing](#testing)

<!-- markdown-toc end -->


Dependencies
------------

This project is built using Python 3. You need to insteall Python and its package manager pip in order to run thor.

On Debian or Ubuntu:

```bash
sudo apt-get install python3 python3-pip
```

On macOS with homebrew:

```bash
Courage!
```

Installation
------------

To install from source first install the dependencies detailed above and then run the following:

```bash
git clone https://github.com/WeatherMagic/thor.git
cd thor
sudo pip3 install -r requirements.txt
sudo pip3 install .
```



Usage
-----

Magic!


License
-------

You are granted a licensed to use this program and all of it's components, which we hold the copyright of, under the GNU Affero General Public License version 3. A complete copy of the license is available in the LICENSE.txt file and can also be viewed on the [GNU website](http://www.gnu.org/licenses/agpl-3.0.html).



Development
-----------

Development requires a couple additional dependencies (see also additional pip dependencies after virtualenv is set up):

On Debian/Ubuntu:

```bash
sudo apt-get install virtualenv pep8 pylint python3-pytest python3-yaml
```

ON macOS:

```bash
brew install python3
pip3 install virtualenv
```

It's recommended to use virtualenv for development which allows for setup and other possibly system damaging procedures without actually running the risk of doing so. To set up the virtual environment for the first time, stand in the source code folder and run:

```bash
virtualenv -p /usr/bin/python3 env
```

Then activate the environment, this is the only thing you need to do on consecutive shells you want to develop in:

```bash
source env/bin/activate
```

You can test that you are in the virtualenv by checking that the following command results in a path which ends in your source code folder.

```bash
which python
```

You're now ready to install the additional python dependencies into your virtual environment using pip:

```bash
pip3 install -U -r requirements.txt
```

In order to escape the virtualenv one can either close the terminal or run:

```bash
deactivate
```
To install the development version of comet-sensor on your folder into your newly created virtualenv, make sure that you didn't just deactivate it, run:

```bash
pip3 install --editable .
```

To keep everything nice and clean we should also lint our code before commiting it, still standing in the root of the source code folder:

```bash
ln -s `which pre-commit.git-lint.sh` .git/hooks/pre-commit
```


Testing
-------

Before submitting any pull requests the code should be run through the linter as described under [Development](#development) but also pass all the existing test. Running these on your local machine is as simple as:

```bash
py.test tests/
```
