# Thor - The web server of WeatherMagic

[![Build Status](https://travis-ci.org/WeatherMagic/thor.svg?branch=master)](https://travis-ci.org/WeatherMagic/thor)


<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-generate-toc again -->
**Table of Contents**

- [Thor - The web server of WeatherMagic](#thor---the-web-server-of-weathermagic)
- [Installation for running](#installation-for-running)
- [Installation for development](#installation-for-development)
    - [Exiting virtualenv](#exiting-virtualenv)
    - [Testing](#testing)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

<!-- markdown-toc end -->


# Installation for running

This project is built using Python 3. You need to insteall Python and its package manager pip in order to run thor. You'll also need some netcdf libraries.

On Debian or Ubuntu:

```bash
sudo apt-get install python3 python3-pip netcdf-bin libhdf5-serial-dev libnetcdf-dev
```

ON macOS:

```bash
brew install python3 gfindutils
pip3 install virtualenv
```


# Installation for development

Development requires a couple additional dependencies (see also additional pip dependencies after virtualenv is set up):

On Debian/Ubuntu:

```bash
sudo apt-get install python3-dev python-virtualenv
```

It's recommended to use virtualenv for development which allows for setup and other possibly system damaging procedures without actually running the risk of doing so. To set up the virtual environment for the first time, stand in the source code folder and run:

```bash
virtualenv -p python3 env
```

Then activate the environment, this is the only thing you need to do on consecutive shells you want to develop in:

```bash
source env/bin/activate
```

You're now ready to install the additional python dependencies into your virtual environment using pip:

```bash
pip3 install -U -r dev-requirements.txt
```

To keep everything nice and clean we should also lint our code before commiting it, still standing in the root of the source code folder:

```bash
ln -s src/commit-hook.bash .git/hooks/pre-commit
```

## Exiting virtualenv

In order to escape the virtualenv one can either close the terminal or run:

```bash
deactivate
```

## Testing

Before submitting any pull requests the code should be run through the linter as described under [Development](#development) but also pass all the existing test. Running these on your local machine is as simple as:

```bash
py.test tests/
```


# Installation

To install from source first install the dependencies detailed above and then run the following:

```bash
git clone https://github.com/WeatherMagic/thor.git
cd thor
sudo pip3 install -U -r requirements.txt
sudo pip3 install .
```


# Usage

Magic!


# License

You are granted a licensed to use this program and all of it's components, which we hold the copyright of, under the GNU Affero General Public License version 3. A complete copy of the license is available in the LICENSE.txt file and can also be viewed on the [GNU website](http://www.gnu.org/licenses/agpl-3.0.html).



