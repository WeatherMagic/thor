# Thor - The web server of WeatherMagic

[![Build Status](https://travis-ci.org/WeatherMagic/thor.svg?branch=master)](https://travis-ci.org/WeatherMagic/thor)


<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-generate-toc again -->
**Table of Contents**

- [Thor - The web server of WeatherMagic](#thor---the-web-server-of-weathermagic)
- [Dependencies](#dependencies)
- [Installation for development](#installation-for-development)
    - [Exiting virtualenv](#exiting-virtualenv)
    - [Testing](#testing)
- [Installation for production](#installation-for-production)
- [Usage](#usage)
- [License](#license)

<!-- markdown-toc end -->


# Dependencies

This project is built using Python 3. You need to insteall Python and its package manager pip in order to run thor. You'll also need some netcdf libraries.

On Debian or Ubuntu:

```bash
sudo apt-get install python3 python3-pip netcdf-bin libhdf5-serial-dev libnetcdf-dev
```

On macOS:

```bash
brew install python3 findutils
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

# Installation for production

To install from source first install the dependencies detailed above and then run the following:

```bash
git clone https://github.com/WeatherMagic/thor.git
cd thor
sudo pip3 install -U -r requirements.txt
sudo pip3 install .
```
# Files 
Before thor can be used weather data needs to be aquired. This is done by downloading data from www.earthsystemcog.org there are a lot of different files that can be downloaded, not all compatible with thor. To simplify the downloading process a wget scripts have been created. 


## Account and permissions
First create an OpenID acoount at ESCOG this is done by going to the following link

https://esgf.esrl.noaa.gov/user/add/?next=http%253A%252F%252Fwww.earthsystemcog.org%252Fprojects%252Fcog%252F

Once an account is created it needs to get the right permissions inorder to download the required files for thor. This can be done by trying to download files from two ESCOG projects. First try to download:

http://aims3.llnl.gov/thredds/fileServer/cmip5_css02_data/cmip5/output1/LASG-CESS/FGOALS-g2/midHolocene/mon/ocean/Omon/r1i1p1/vsfsit/1/vsfsit_Omon_FGOALS-g2_midHolocene_r1i1p1_096001-096912.nc

It will ask for your openID account and password once it notices that your account dosen't have permission it will ask if you want commercial or scientific access. Choose scientific.

Once the first file is downloaded download the folloing file and repeat the procedure.

http://esgf1.dkrz.de/thredds/fileServer/cordex/cordex/output/ARC-44/AWI/ECMWF-ERAINT/evaluation/r1i1p1/AWI-HIRHAM5/v1/day/snm/v20150409/snm_ARC-44_ECMWF-ERAINT_evaluation_r1i1p1_AWI-HIRHAM5_v1_day_20110101-20141231.nc

Now you should have the necessary permissions to do the next step.

## Downloading with wget
To use the wget script to download all required files to use thor simply type the following commands while standing in the thor folder and then follow the instructions in your terminal.

```bash
cd scripts
./Get_ESCOG_files.sh
```

Congratulation you should now have all the required files to start running the thor application.

# Usage

Magic!


# License

You are granted a licensed to use this program and all of it's components, which we hold the copyright of, under the GNU Affero General Public License version 3. A complete copy of the license is available in the LICENSE.txt file and can also be viewed on the [GNU website](http://www.gnu.org/licenses/agpl-3.0.html).
