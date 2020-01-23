#!/usr/bin/env python3

import argparse
import base64
import gzip
import logging
import os
from hapi.release import release_pb2
import kubernetes
import yaml

parser = argparse.ArgumentParser()
parser.add_argument('--namespace', dest='namespace', default='kube-system', help='Namespace where Tiller stores configmaps')
args = parser.parse_args()

logging.basicConfig(level=logging.INFO)
logging.getLogger('kubernetes').setLevel(logging.INFO)
log = logging.getLogger('deprapi')

wrong = [
	('extensions/v1beta1', 'DaemonSet'),
	('extensions/v1beta1', 'Deployment'),
	('extensions/v1beta1', 'ReplicaSet'),
	('extensions/v1beta1', 'StatefulSet'),
	('apps/v1beta2', 'DaemonSet'),
	('apps/v1beta2', 'Deployment'),
	('apps/v1beta2', 'ReplicaSet'),
	('apps/v1beta2', 'StatefulSet'),
	('extensions/v1beta1', 'PodSecurityPolicy'),
	('extensions/v1beta1', 'NetworkPolicy'),
]

kubernetes.config.load_kube_config()
v1 = kubernetes.client.CoreV1Api()
for configmap in v1.list_namespaced_config_map(args.namespace, label_selector='OWNER=TILLER,STATUS=DEPLOYED').items:
	bindata = gzip.decompress(base64.b64decode(configmap.data['release']))
	release = release_pb2.Release().FromString(bindata)
	log.debug(f'Examining release {release.name}')
	manifests = yaml.safe_load_all(release.manifest)
	deprecated = False

	for m in manifests:
		if m is None:
			# skip empty manifest
			continue
		fulltype = f'{m["apiVersion"]}.{m["kind"]}'
		name = m["metadata"].get('name', '')
		fullname = f'{fulltype} {name}'
		log.debug(f'Examining {fullname}')
		if (m['apiVersion'], m['kind']) in wrong:
			log.info(f'Release {release.name} has deprecated {fullname}')
			deprecated = True
	if deprecated:
		log.error(f'Release {release.name} uses deprecated APIs')
