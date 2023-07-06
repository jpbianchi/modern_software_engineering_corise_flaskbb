zip -r "flaskbb_deploy-$1.zip" ./flaskbb ./.ebextensions wsgi.py setup.py setup.cfg requirements.txt flaskbb.cfg celery_worker.py

aws s3 cp "flaskbb_deploy-$1.zip" s3://terraform-state-flaskbb-jpb

aws elasticbeanstalk create-application-version --application-name flaskbb --source-bundle S3Bucket="terraform-state-flaskbb-jpb",S3Key="flaskbb_deploy-$1.zip" --version-label "ver-$1" --description "file permissions" --region "eu-west-3"

aws elasticbeanstalk update-environment --environment-name flaskbb-environment --version-label "ver-$1" --region "eu-west-3"