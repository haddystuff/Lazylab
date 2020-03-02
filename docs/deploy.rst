Deploy
=================

``deploy`` command work logic can be seen below:

1. Trying to find lab archive in lab archive directory('{PATH_TO_MODULE}/labs/' by default) which name is {lab_name}.lazy.
Actualy .lazy is just a fansy extension name for usual zip archive.
There are config.yml file(it consist of text description of all VMs in lab and lab topology) and raw configs of VMs in .lazy archive.

2. If there is no {lab_name}.lazy archive lazylab trying to download it from LABS_SERVER wich you can change in lazylab.conf file.

3. Checks if syntax is ok in config.yml file.

4. Parsing os versions of VMs and checking if there are image templates of this os in image template directory.

5. If there os no image lazylab trying to download it from {IMAGES_SERVER}.

6. Lazylab cloning image templates.

7. Creates VMs one by one with referred in config.yml parameters.
