# Globus special remote initialization tools

This repository aims to enable administrators of datalad datasets in CONP to initialize globus special remote for a given dataset.

After correct initialization, other users will be able to install the given datalad dataset from git and use globus as special remote

Note: This process needs to be followed **once** by administrators to enable users to work with the dataset in the future. 

Therefore, pushing to git annex is a must (see How to use)


## How to use

Globus special remote can be configured to work for a given dataset by launching the ```globus_config.sh``` script.

To enable globus special remote follow these steps:

1 - Grab repository from git

```
git clone globus_tools
```

2 - Launch configuration file by passing the relative arguments for the dataset you are working with

```
./globus_config.sh -d <dataset_root> --endpoint <globus_endpoint> --prefix <files_prefix>
```

Note: the flags --endpoint and --prefix refer to [Globus](https://auth.globus.org) specific information of your dataset


3 - Push to git-annex branch to publish



## How it works

By using the ```git-annex-remote-globus``` API, all dataset files will be recursively registered with globus special remote after successful authentication in [Globus](https://auth.globus.org) and
first time remote initialization with the git annex command ```initremote```

For more details on files registration with globus, see [globus](https://github.com/CONP-PCNO/git-annex-remote-globus) special remote
 