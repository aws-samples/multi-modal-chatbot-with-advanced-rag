import json
import boto3
import logging
import time

logger = logging.getLogger()
logger.setLevel(logging.INFO)

opensearch = boto3.client('opensearch')

def on_event(event, context):
    print(event)
    request_type = event['RequestType']
    if request_type == 'Create': return on_create(event)
    if request_type == 'Update': return on_update(event)
    if request_type == 'Delete': return on_delete(event)
    raise Exception("Invalid request type: %s" % request_type)

def on_create(event):
    props = event["ResourceProperties"]
    print("create new resource with props %s" % props)

    domain_arn = props['DomainArn']
    domain_name = domain_arn.split('/')[-1]
    DEFAULT_REGION = props['DEFAULT_REGION']
    VERSION = props['VERSION']
    
    nori_pkg_id = {
        'us-east-1': {
            '2.3': 'G196105221',
            '2.5': 'G240285063',
            '2.7': 'G16029449', 
            '2.9': 'G60209291',
            '2.11': 'G181660338'
        },
        'us-west-2': {
            '2.3': 'G94047474',
            '2.5': 'G138227316',
            '2.7': 'G182407158', 
            '2.9': 'G226587000',
            '2.11': 'G79602591'
        }
    }

    package_id = nori_pkg_id[DEFAULT_REGION][VERSION]
    print(domain_arn, domain_name, package_id)

    try:
        response = opensearch.associate_package(
            PackageID=package_id,
            DomainName=domain_name
        )
        print(f"Successfully initiated association of package {package_id} with domain {domain_name}")
    except opensearch.exceptions.BaseException as e:
        logger.error(f"Failed to associate package: {e}")
        raise e

    physical_id = f"AssociatePackage-{domain_name}-{package_id}"
    return { 'PhysicalResourceId': physical_id }

def on_update(event):
    physical_id = event["PhysicalResourceId"]
    props = event["ResourceProperties"]
    print("update resource %s with props %s" % (physical_id, props))
    return { 'PhysicalResourceId': physical_id }

def on_delete(event):
    physical_id = event["PhysicalResourceId"]
    print("delete resource %s" % physical_id)
    # Optionally add dissociation logic if required
    return { 'PhysicalResourceId': physical_id }
    
"""
def is_complete(event, context):
    props = event["ResourceProperties"]
    domain_arn = props['DomainArn']
    domain_name = domain_arn.split('/')[-1]
    DEFAULT_REGION = props['DEFAULT_REGION']
    VERSION = props['VERSION']
    
    nori_pkg_id = {
        'us-east-1': {
            '2.3': 'G196105221',
            '2.5': 'G240285063',
            '2.7': 'G16029449', 
            '2.9': 'G60209291',
            '2.11': 'G181660338'
        },
        'us-west-2': {
            '2.3': 'G94047474',
            '2.5': 'G138227316',
            '2.7': 'G182407158', 
            '2.9': 'G226587000',
            '2.11': 'G79602591'
        }
    }

    package_id = nori_pkg_id[DEFAULT_REGION][VERSION]
    print(f"Checking association status for package {package_id} on domain {domain_name}")
    
    response = opensearch.list_packages_for_domain(
        DomainName=domain_name,
        MaxResults=1
    )

    if response['DomainPackageDetailsList'][0]['DomainPackageStatus'] == "ACTIVE":
        is_ready = True
    else:
        in_ready = False
    
    print(f"Is package {package_id} active on domain {domain_name}? {is_ready}")

    return { 'IsComplete': is_ready }
"""