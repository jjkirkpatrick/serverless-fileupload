This is a Work in progress, not all resources are currently defined in Terraform, nor are they optimally configured. 



Application

    Install required modules 
        $ cd /application && yarn install

    To build the application for development with hot reload
        $ cd /application && yarn serve

    To build the application for production 

        $ cd /application && yarn build 

        Once yarn has built the application move the contents of /application/dist to s3

lambda

    build the terraform to deploy the serverless resources 
        $ cd ../chalice && chalice package --pkg-format terraform ../terraform

        Remove the following section from ../terraform/chalice.tf.json, this method of defining providers is no longer supported in TF > 0.13

        "provider": {
          "template": {
            "version": "~> 2"
          },
          "aws": {
            "version": ">= 2, < 4"
          },
          "null": {
            "version": "~> 2"
          }
        },



Terraform 
    cd ../terraform && terraform apply --auto-approve