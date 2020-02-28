# Globus special remote initialization tools

This repository gives administrators of datalad datasets in CONP the necessary tools to:

### 1 - Download dataset data from Globus to be added to datalad/CONP

This step involves the use of [Globus Transfer API](https://docs.globus.org/api/transfer/) to share data between a Globus 
**shared endpoint** where the dataset resides and the administrator's [Globus personal endpoint](https://www.globus.org/globus-connect-personal) 
which, as we will see, it is nothing but a wrapper which turns the administrator's laptop into a Globus endpoint to enable transferring of 
files from the shared endpoint. A shared enpoint instead, is a location in the Globus cloud where data are uploaded and made available to all Globus users.
The reason for using a wrapper (called Globus connect personal) at this point is that Globus only 'knows' the concept of an endpoint (the main data type) and can only transfer data between 
endpoints, hence it is required that a machine is turned into an endpoint 'type' (wrapping) to download data from some other endpoint to its local file system.

1.1 - So, first off, the administrator has to install and configure Globus Connect Personal. To do so, links for all major operating
systems are available [here](https://www.globus.org/globus-connect-personal). [This link](https://docs.globus.org/how-to/globus-connect-personal-linux/)
gives an example use with linux. In any case, the administrator will be required to choose an endpoint name, generate setup keys for installation and 
install and connect to Globus Connect Personal. Assuming the steps in the guide liked above are performed, it is possible to connect to Globus Connect Personal:

``./globusconnect &`` 

and clocking 'connect' on the icon. Globus Online will appear connected with green light if everything went well.

1.2 - Creation of an endpoint can either be done via the [Globus user interface](https://app.globus.org/) or 
via the ``globus`` command provided by the Globus [Command Line Interface (CLI)](https://docs.globus.org/cli/installation/). These two options
are explained in the [guide](https://docs.globus.org/how-to/globus-connect-personal-linux/) more in details and which is available for all OS. 
To install and use the command line, make sure you install the globus cli:

```pip install globus-cli```

Once your endpoint is created, you can check that everything went well by running:

```globus endpoint search --filter-scope my-endpoints```

You should see your endpoint ID displayed. We will use this ID to trasfer files from the shared endpoint to your local endpoint !

1.3 - Now, to better understand the power of Globus Connect Personal, try looking into your endpoint by running:

```globus ls <endpoint-ID>:/home```

That is your local file system ! So we enabled the wrapper we were talking about .... We are ready to set up the transfer to download the dataset

1.3 - Now we are ready to initialize the data transfer from the selected Globus shared endpoint and the administrator's endpoint:

Select the shared endpoint and store its ID into an environment variable (for simplicity). This is going to be the source endpoint. For example

``source_ep=ddb59aef-6d04-11e5-ba46-22000b92c6ec``

Do the same with your endpoint

``your_ep=<endpoint-ID>``

Now, find your user ID, which can be queried with the following command specifying your email address used to register in Globus

``globus get-identities <your-email-address>``

Now save your user ID:

``user_uuid=<your-user-ID>``

Make a folder in your local machine which we can use to transfer data into. For example we can ``mkdir /home/dataset/``

Now initiate the transfer:

``./download.py --source-endpoint $source_ep --destination-endpoint $your_ep --source-path /share/godata/ --destination-path /home/dataset/ --user-uuid $user_uuid --delete``


### 2 - Load dataset to globus special remote for first time setup

Once the desired dataset is downloaded, it can be added to datalad and CONP by using the guide adding_dataset_to_datalad.md. In this way, the dataset
content is expected to be available to CONP users via datalad and git annex which will require a configured special remote to retrieve data when needed.
The use of special remotes is in fact a strategy for git annex to manage very large datasets in a storage-friendly light-weight matter letting them reside 
in different machines and only asking for and transferring them when needed. More information on special remotes is available [here](https://git-annex.branchable.com/special_remotes/)

In this context, this step enables sharing information of the dataset living in Globus with git annex to establish future data transfer connections
In other words, this step configures the globus special remote interface to work with the given dataset so that files can be transferred using the special remote
and become available to CONP users. It is important to note that this step is a for a 'first time setup' of the special remote to work with this dataset

### 3 - Load dataset updates to globus remote via a crawler

In case the dataset content gets updated in Globus shared enpoint, we want these changes to reflect in the globus special remote and therefore, to be seen by git annex.
A crawler would in fact perform checks on eventual enpoint changes and updates of the globus special remote configuration to reflect those changes.


After correct initialization, other users will be able to install the given datalad dataset from git and use globus as special remote

Note: This process needs to be followed **once** by administrators to enable users to work with the dataset in the future. 

Therefore, pushing to git annex is a must (see How to use)


## How to use

Globus special remote can be configured to work for a given dataset by launching the ```globus_config.sh``` script.

To enable globus special remote follow these steps:

1 - Grab repository from git

```
git clone https://github.com/CONP-PCNO/globus_tools.git
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
 