# DeprAPI
Interrogates your tiller for deprecated resources

## Usage
1. Setup python3 vend: `python3 -m venv venv`
1. Activate venv: `. venv/bin/activate`
1. Install requirements: `pip install -r requirements.txt`
1. Switch to your favorite kubectl context: `kubectl config use-context mycontext`
1. Run the tool: `python deprapi.py --namespace mytillernamespace`

## Example output
```
INFO:deprapi:Release taiga has deprecated apps/v1beta2.Deployment events
INFO:deprapi:Release taiga has deprecated apps/v1beta2.Deployment postgres
INFO:deprapi:Release taiga has deprecated apps/v1beta2.Deployment rabbitmq
INFO:deprapi:Release taiga has deprecated apps/v1beta2.Deployment redis
INFO:deprapi:Release taiga has deprecated apps/v1beta2.Deployment taiga
ERROR:deprapi:Release taiga uses deprecated APIs
```

This means that you have a release named `taiga` in your tiller, which uses
(several) deprecated `apps/v1beta2` `Deployments`.

## How to fix
Upgrade your releases using charts which carry the right API Versions.

## What if you don't
The resources will probably survive a k8s upgrade, but Helm will not be able
to manage (ie, upgrade) these resources, as it will try to query for the 
deprecated API groups, which will fail. You will need to upgrade these 
resources before upgrading to newer k8s.
