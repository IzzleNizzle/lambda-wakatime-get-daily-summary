# lambda-wakatime-get-daily-summary
Cloud Function (Lambda) - Grab wakatime daily summary and save. For tracking my ouput


### Build zip for lambda:

```
pip install --target ./package requests==2.28.2
cd package
zip -r ../hello_world.zip .
cd ..
zip hello_world.zip app.py
```

### Reference URL's

Wakatime Documentation:
https://wakatime.com/developers#authentication


### Build Step Helper
Using the XC Build Tool
https://github.com/joerdav/xc

### Trying out github actions to AWS lambda

following this guide: https://aws.amazon.com/blogs/compute/using-github-actions-to-deploy-serverless-applications/

`sam init -r python3.9 -n lambda-wakatime-get-daily-summary --app-template "hello-world"`
