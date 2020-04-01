# mlflow-exemplar


## Scenario

Through simulating a real-world-like scenario we can tease out the value of ML flow for an organisation or team, the parameters of the situation are typical in the world of AI / Data, these can be seen below.

- Assume this project is intended to be used by a data science team of N size.

- Assume the team has been given a new dataset, performed an intial EDA and is ready to start modelling.

- The team want to have access to the history of their experiments:
    - For reference in future
    - Ease of recreation / repeat runs.
    - Ability to take an experiment and tweak.

- If the team change a python file in an experiment, viewing an older version of the source file with the experiment run should be possible, as well as running either version.

## Setup.


### Setup Remote Tracking Server.


## Dev Notes

Do I need to run ML Flow on a remote server to ensure all experiments are tracked for a given team? With URL as an ENV Var.

ML Flow offers a UI, in terms of value it seems to be similar to DVC so far, with ability to log much more and group experiments. Remote use for teams may be the greates value, ie a central place to look at experiments.

Value of ML flow - UI, shared history of experiments for modelling, artefacts kept in MLFlow even when server is off?, no need to scan notebooks for experiments - you can log appropiately and scan UI.

For this code, should I assume a n person team eventually, ie deploy and run server on ec2 with auto shut down and turn on and some setup script? first click ops, then extend to iac for a basic ec2? START LOCAL, with n team assumption. This needs setup to log to a bucket.

artifacts range from models, data (training, test sets), images, plots, files etc.

How does ml flow play with Git? experiment source code / versions / data etc.

Can I setup a log reg experiment and also a nn experiment?

use something like the iris data, pull from external source to keep it simple.

## TODO / Questions

Do logged artefacts persist when server down?
how does ml flow relates to code version history? e.g in a notebook?
does mlflow make sense in non notebook development? ie... retraining or is it sandbox only? a sandbox tool?
Can i pickup output from an mlflow experiment from another source and use it?
How does mlflow fit into a docker or other deployment, how can this be automated or hidden behind a MAKE?
Resistance of EDA to modelling, when should i jump to ml flow? is this clunky / slow?
Sagemaker deploy after basic end to end.
Value locally seems limited, it writes data to a local directory, which then would need pushed, remote is only useful option.
need to run mlflow flow ui in same directory as mlruns data directory.
Its use seems most clear in high iteration environments, in which you have a period of > 1 week to have several experiments.

Theory that commit has is not updating when running experiment in a notebook - verified!

Have commit has I can document to go back to in an experiment run, to run an old version of the modelling code.

old commit hash - c7a8077516ae0f89eabae1f590a711fbbd1e8361
new commit has has 2 iterations on lr.
new commit has a3d6238eb739ac970396daa5879c5dd9c7d33f6e
to get a new hash you need to make a commit.

git revert c7a8077516ae0f89eabae1f590a711fbbd1e8361

ec2
server setup to my own ip
ssh in with key
installed mlflow
create s3 bucket
start server
mlflow server --default-artifact-root s3://mlflow-exemplar/ --host 0.0.0.0
I set a custom inbound TCP rule to open port 5000 (mlflow default
I then update the tracking URI programmatically in code.
works connecting to the bucket and ec2 instance.
I setup up credentials in the ec2 via aws configure, it may need this to pull assets from s3 in the server.
I pip installed boto3 as well.

Can you set a tracking URI to a one drive folder?

mlflow run iris_experiment_lr.py -e reproduce -P run_uuid=8f69ab8635db4cef9380c3c8b39fd66b


## Todo

- Tracking Server for collaboration, stop commiting run assets to Git and persistence.

- What if you use DVC to obscure the 'ml-runs' then you can possibly persist that data globally, merging and collaboration could be a challenge if their is an asset delta.


## Resources

 https://towardsdatascience.com/deploying-models-to-production-with-mlflow-and-amazon-sagemaker-d21f67909198