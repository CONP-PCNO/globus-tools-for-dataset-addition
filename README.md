# Globus special remote initialization tools

This repository gives administrators of datalad datasets in CONP the necessary tools to:

### 1 - Download dataset data from Globus to be added to datalad/CONP

This step involves the use of [Globus Transfer API](https://docs.globus.org/api/transfer/) to share data between a Globus 
**shared endpoint** where the dataset resides and the administrator's [Globus personal endpoint](https://www.globus.org/globus-connect-personal) 
which, as we will see, it is nothing but a wrapper which turns the administrator's laptop into a Globus endpoint to enable transferring 
files from the shared endpoint (or endpoints in general). A shared enpoint instead, is a location in the Globus cloud where data get uploaded and made available to all Globus users (shared).
The reason for using a wrapper (called Globus connect personal) at this point is that Globus only 'knows' the concept of an endpoint (the main data type) and can only transfer data between 
endpoints, hence it is required that a machine is turned into an endpoint 'type' (wrapping) to transfer data to it.

1.1 - So, first off, the administrator has to install and configure Globus Connect Personal to turn his/her laptop into an endpoint. To do so, links for all major operating
systems are available [here](https://www.globus.org/globus-connect-personal). [This link](https://docs.globus.org/how-to/globus-connect-personal-linux/)
gives an example use with Linux OS. In any case, the administrator will be required to choose an endpoint name, generate setup keys for installation and 
install and connect to Globus Connect Personal. Assuming the steps in the guide linked above are performed, it is possible to connect to Globus Connect Personal in two ways:

``./globusconnect &`` 

and clicking 'connect' on the icon. Globus Online will appear connected with green light if everything went well.

Otherwise, for command line users, Globus personal can be started as

``./globusconnectpersonal -start &`` 

1.2 - As hinted above, the creation of an endpoint can either be done via the [Globus user interface](https://app.globus.org/) or 
via the ``globus`` command provided by the Globus [Command Line Interface (CLI)](https://docs.globus.org/cli/installation/). These two options
are explained in the [guide](https://docs.globus.org/how-to/globus-connect-personal-linux/) in more details which is available for all OS. 
To install and use the command line, make sure you install the globus cli:

```pip install globus-cli```

Once your endpoint is created, you can check that everything went well by running:

```globus endpoint search --filter-scope my-endpoints```

You should see your endpoint ID displayed. We will use this ID to trasfer files from the shared endpoint to your local endpoint !

1.3 - Now, to better understand the power of Globus Connect Personal, try looking into your endpoint by running:

```globus ls <endpoint-ID>:/home```

That is your local file system ! So we enabled the wrapper we were talking about .... We are ready to set up the transfer to download the dataset

1.4 - Now we are ready to initialize the data transfer from the selected Globus shared endpoint and the administrator's endpoint:

Select the shared endpoint and store its ID into an environment variable (for simplicity). This is going to be the source endpoint. For example

``source_ep=ddb59aef-6d04-11e5-ba46-22000b92c6ec``

Do the same with your endpoint

``your_ep=<endpoint-ID>``

Now, find your user ID, which can be queried with the following command specifying your email address used to register to Globus

``globus get-identities <your-email-address>``

Now save your user ID:

``user_uuid=<your-user-ID>``

Make a folder in your local machine which we can use to transfer data into or use an existing, one such as ``/home/conp-dataset/project/<newprojectname>``. Then find the dataset path in
the Globus shared point, which will be your ``fileprefix``, the prefix path for all files and folders in the dataset. 
Here we can use ``/source/data`` as an example to illustrate the principle

Now initiate the transfer using the download script in this folder:

``./download.py --source-endpoint $source_ep --destination-endpoint $your_ep --source-path /source/data/ --destination-path /home/conp-dataset/project/<newprojectname> --user-uuid $user_uuid --delete``

Transfer may take time. Check your ```/home/dataset/``` to make sure the transfer was successful. The dataset is ready to be added to CONP


### 2 - Register the dataset with the git-annex globus remote for first time setup

Once the desired dataset is downloaded, it can be added to datalad and CONP by using the guide [adding_dataset_to_datalad.md](https://github.com/CONP-PCNO/conp-documentation/blob/experimental_guide_update/datalad_dataset_addition_procedure.md)
and the [datalad_dataset_addition_experimental.md](https://github.com/CONP-PCNO/conp-documentation/blob/experimental_guide_update/datalad_dataset_addition_experimental.md). After following the guides, the dataset
content is expected to be available to CONP users via datalad and git annex commands and to do so, git annex will require a configured special remote to retrieve data when it requests it.
The use of special remotes is in fact a strategy for git annex to manage very large datasets in a storage-friendly light-weight manner letting them reside 
in different machines and only asking for their transfer when needed. More information on special remotes is available [here](https://git-annex.branchable.com/special_remotes/)

This step enables sharing information of the dataset living in Globus with git annex to establish future data transfer connections.
In other words, this step configures the globus special remote interface to work with the given dataset so that files can be transferred using the configured remote
and become available to CONP users. It is important to note that this step is a 'first time setup' of the special remote to work with the given dataset.

At this point it is assumed that a new datalad dataset was generated at ```conp-dataset/project/<newprojectname>``` by following the guides above. We will work with this dataset to initialize the globus remote

2.1 - So let's go ahead and start the retrieving of the dataset information in Globus that git annex will store in the git-annex branch. First let's install some requirements.

```pip install configparser```
```pip install git-annex-remote-globus```

2.2 - Then we make sure we are in the new dataset root ``conp-dataset/project/<newprojectname>``. The ``fileprefix`` and ``endpoint`` can 
be found in Globus.org dataset page (metadata). The `fileprefix` is the fixed path before the dataset directories. The remote must be initialized


```cd conp-dataset/project/<newprojectname>``` (if you are not there)

```git annex initremote globus type=external externaltype=globus encryption=none endpoint=(dataset_name OR endpoint_ID) fileprefix=fixed/path/to/data```

2.3 - We can then retrieve information about the dataset files by using the retrieve function available in the globus tools repository

```path/to/globus_tools/retrieve.py --path . --endpoint dataset_name --fileprefix fixed/path/to/data --encryption none```

where ``.`` refers to your local directory which should be ``conp-dataset/project/<newprojectname>``

More information on the ``retrieve`` operation behavior can be found under the [globus special remote](https://github.com/gi114/git-annex-remote-globus)
under _Manually registering a dataset with globus remote (internals)_


2.4 - At this point we need to publish this remote configuration, hence we commit and push to the **git-annex branch** of the dataset. Note, this step is requited to
enable users to install the dataset and use the git annex special remote! So test it yourself!

##### Test step 2

a) Go on github and grab the dataset repository:

``datalad install -r https://github.com/conpdataset/dataset.git``

``git-annex-remote-globus setup``

``git annex enableremote globus``

``git annex get path/to/file``



### 3 - Eliminate dataset from git-annex memory

If the dataset is moved to a different endpoint or some changes happen such that the files get moved to different paths, then the git annex will not be able to
retrieve the content of dataset files anymore. All information regarding dataset location in Globus are saved in the git annex branch.

To remove a give file or all files from git annex, all relevant file hashes must be ``setpresent 0`` and all urls must be removed with
``git annex rmurl``. See [globus special remote](https://github.com/gi114/git-annex-remote-globus) for the remote internals.
 
 These steps must be performed before a new dataset or new dataset files get added to git annex. It is better to clear the git annex memory first 
 or it will generate confusion. The ``retrieve`` operation supports removing a whole dataset with the ``--clean`` flag.
 If individual files must be removed, they must be removed manually. Again, check the [globus special remote](https://github.com/gi114/git-annex-remote-globus) for the remote internals.
 
 Therefore, try the following to remove the dataset:
 
 ```path/to/globus_tools/retrieve.py --path . --endpoint dataset_name --fileprefix fixed/path/to/data --encryption none --clean```
 
 where ``.`` refers to your local directory which should be ``conp-dataset/project/<newprojectname>``
