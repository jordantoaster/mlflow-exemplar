# mlflow-exemplar

This project intends to show working use of MLFlow to manage experiments and the assets generated by the experiments. 

The MLFlow tool includes a UI to make it easy to interrogate these experiments and review the parameters, metrics and artifacts generated.

The project showcases a local use of MLFlow, this is not ideal for collaboration or even individual development without additional tools such as DVC as generating model artifacts for dynamic experiment runs can require substantial storage.

The remote use of MLFlow is the focus, as that is of the highest value to data science teams. In this instance I have deployed a tracking server on AWS using an EC2 instance and a S3 bucket to store artifacts.

The repository simulates two experiments for solving a basic classification problem, one which uses a logistic regression and another using a decision tree. These can be viewed in the ``src/experiments/...`` path.

The benefit of MLFlow is a team environment in which you have several people contributing experiments to a code base, letting you have a catalogue of results and assets that can be referred to. How this tool can aid the jump to production remains to be seen, so I will constrain its value to the modelling phase of a project.

## Scenario

Through simulating a real-world-like scenario we can tease out the value of ML flow for an organisation or team, the parameters of the situation are typical in the world of AI / Data, these can be seen below.

- Assume this project is intended to be used by a data science team of N size.

- Assume the team has been given a new dataset, performed an intial EDA and is ready to start modelling.

- The team want to have access to the history of their experiments:
    - For reference in future
    - Ease of recreation / repeat runs.
    - Ability to take an experiment and tweak.

- If the team change a python file in an experiment, viewing an older version of the source file with the experiment run should be possible, as well as running either version.

## Setup Local

Note: The project is setup to assume the use of a remote tracking server, removing the programmatic lines of code from your files is trivial if you want MLFlow to run locally.

1. Clone the repository.

2. Ensure AWS credentials are setup using the ``aws configure`` using the aws-cli tools (assumption these are installed).

3. At the project root inside a terminal run the ``make`` command to build a virtual environment with the required dependencies.

4. Run ``source env/bin/activate`` to start the virtual environment.

5. Run ``python src/experiments/iris_experiment_rf.py`` to start an experiment. This will create a local ``mlruns`` folder which collects the data collected from the experiment. You can run a similar command for the other experiment as well to gain metrics.

6. Run in project root ``mlflow ui`` to spin up a local webapp which shows the data collected from your various experiment runs


## Setup Remote Tracking Server.

1. Run steps 1-5 in the Local instructions.

2. Run `source env.sh` to ensure your remote URL can be accessed in the code, ensure this is updated in advance following the template outlined in the file itself. Only run this now if you have your server setup, else run this after step 8.

3. Now, you need to ensure your EC2 instance and S3 bucket are setup, requirements are noted below and are somewhat straightforward to implement in a click ops manner.

    3.1 Create an S3 bucket, with any name and with no additional configuration.

    3.2 Create an EC2 instance:

        3.2.1 Linux based micro instance.

        3.2.2 Security group setup with an ssh port open to either all ips, or just your own. It should also open port 5000 as a custom TCP port, the mlflow UI will be exposed through this port.

        3.2.3 Ensure you create a public / private key pair, place your public key in any suitable location on your machine.

        3.2.4 Start your instance in the EC2 GUI (dont forget to stop it when your not using the server)

4. You now need to ssh into your EC2 instance, to do this, ensure you are in the same directory as your public key and run in a terminal ``ssh -i "<PUBLIC_KEY_PEM_FILE_NAME>" ec2-user@e<DNS_NAME>`` which will put your into the default directory for the server.

5. Within the server terminal run ``sudo pip install mlflow`` ``sudo pip install boto3``

6. Run ``sudo pip install -U python-dateutil==2.6.1`` to avoid a version conflict with mlflow.

7. Run ``aws configure`` and input your access keys that let you use the S3 bucket, this should be any keys which give programmatic API access to AWS.

8. Start your mlflow server - ``mlflow server --default-artifact-root s3://mlflow-exemplar/ --host 0.0.0.0``

You now have a running server, you can connect to the MLFlow UI in the browser via:

``<PUBLIC_IP>:5000`` e.g. ``35.178.163.55:5000``

You will now be able to create experiments with ML Flow and make use of the tools functionality to its fullest. 

## Other Functionality

If you want to rollback to try out an old experiment, you can follow the process below:

1. Get the commit hash associated with your experiment run - e.g ``c7a8077516ae0f89eabae1f590a711fbbd1e8361``

2. In your project root, with a terminal run ``git checkout c7a8077516ae0f89eabae1f590a711fbbd1e8361``

It is worth nothing this is a branch checkout, and is suited mainly to going back in the source history to review prior experiments. In reality, keeping experiments modular in an appropriate file structure could prove a better approach. E.G create a new experiment where you have introduced newly engineered features rather than editing an old experiment, this is useful with clear outcomes and hypothesis defined.

## Dev Notes

- Experiments are tied to a commit hash, this lets you checkout the code required to create an experiment. Ensure that the hash is changed if you want to recreate a certain experiment by using mlflow as a reference. My concern is a hash may not account for local changes made to a prior commit. VERIFICATION REQUIRED.

## TODO

- What if you use DVC to obscure the 'ml-runs' then you can possibly persist that data globally, merging and collaboration could be a challenge if their is an asset delta.

- No IAC is present for AWS assets.

- The security of the app could be improved to filter on ports and IP's that can access the mlflow server.

- The server has no redundancy or disaster recovery.

## Resources

 https://towardsdatascience.com/deploying-models-to-production-with-mlflow-and-amazon-sagemaker-d21f67909198

 https://medium.com/@GuAndroz/deploy-mlflow-with-docker-compose-8059f16b6039