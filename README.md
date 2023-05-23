# lambda-wakatime-get-daily-summary
Cloud Function (Lambda) - Grab wakatime daily summary and save. For tracking my ouput

### Reference URL's

Wakatime Documentation:
https://wakatime.com/developers#authentication


### Trying out github actions to AWS lambda

following this guide: https://aws.amazon.com/blogs/compute/using-github-actions-to-deploy-serverless-applications/

`sam init -r python3.9 -n lambda-wakatime-get-daily-summary --app-template "hello-world"`

### Build Step Helper
Using the XC Build Tool
https://github.com/joerdav/xc

## Tasks

### build-lambda-zip

Build Lambda Zip file

```sh
pip install --target ./package -r app/requirements.txt
cd package
zip -r ../lambda_bundle.zip .
cd ../app
zip ../lambda_bundle.zip app.py token.json
```
