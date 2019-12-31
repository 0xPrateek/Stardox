<h1 align="center">
  <br>
  <a href="https://github.com/0xprateek"><img src="https://i.imgur.com/oIMDjCm.png" alt="Stardox"></a>
</h1>

<p align="center">  
  <a href="https://docs.python.org/3/download.html">
    <img src="https://img.shields.io/badge/Python-3.x-green.svg">
  </a>
  <a href="https://github.com/0xprateek/stardox">
    <img src="https://img.shields.io/badge/Version-v1.0.0%20-blue.svg">
  </a>
  <a href="https://github.com/0xprateek/stardox">
    <img src="https://img.shields.io/badge/OS-Linux-orange.svg">
  </a>
  <a href="https://gitter.im/Stardox-gitter/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge"><img src="https://badges.gitter.im/Stardox-gitter/community.svg" alt="Stardox"></a>
  </br></br>
  This Tool is available in:</br>
  <a href = "https://blackarch.org/recon.html"><img src = "https://raw.githubusercontent.com/0xPrateek/Stardox/master/Logo/blackarch.png"></a>

  </br>
</p>

## About [Stardox](https://github.com/0xprateek/stardox)
Stardox is an advanced GitHub stargazers' information gathering tool. It scrapes GitHub for information and displays it 
in list tree view. It can be used for collecting information on your or someone's repository stargazers details.

##### What data it fetches :

1. `Total repsitories`
2. `Total stars`
3. `Total Followers`
4. `Total Following`
5. `Stargazer's Email`


P.S: Many new things will be added soon.

### Gallery

![Image 1](https://i.imgur.com/hkFdQwr.png)

 **Fetching data of repository.**
![Image 2](https://i.imgur.com/BVQJE8s.png)

 **List tree view of fetched data.**
![Image 3](https://i.imgur.com/MIX1VmA.jpg)

### Getting Started

#### Steps to setup :

1. `git clone https://github.com/0xprateek/stardox`
2. `cd stardox`
3. `pip install -r requirements.txt`

#### Starting Stardox :

1. `cd stardox/src`<br/>
2.  a)  **Using Command line arguments** <br/>
         `python3 stardox.py -r https://github.com/Username/repository-URL `<br/>
    b)  **Without Command line arguments**<br/>
     `    python3 stardox.py`<br/>
  #### Usage :
     usage: stardox.py [-h] [-r RURL] [-v] [-s [path]]

  ##### optional arguments:
     -h, --help            show this help message and exit
     -r RURL, --rURL RURL  Path to repository.
     -v, --verbose         Verbose
     -s [path], --save [path]
                        Save the doxed data in a csv file. By default, saved
                        at Desktop.


### Contributing
Any and all contributions, issues, features and tips are welcome.

### License
**Stardox** is licence under [GPL v3.0 license](https://www.gnu.org/licenses/gpl-3.0.en.html)
