from sys import argv, exit
import os
import argparse
from packaging import version

import gitlab

GITLAB_API = os.getenv("CI_SERVER_URL")

def check_arg():

    parser = argparse.ArgumentParser(description='A Python package for uploading packages to and downloading packages from Gitlab package registry.')

    parser.add_argument('-a','--action',
                        type=str,
                        default="download",
                        help="upload/download [default: download]")

    parser.add_argument('-k', '--key',
                        required=True,
                        help='Gitlab Private Token')

    parser.add_argument('-r', '--registry',
                        required=True,
                        help="Project name with namespace. [example: it-admin/zdeb-utils]")

    parser.add_argument('-p', '--package',
                        required=True,
                        help="package name [example: mypackage]")

    parser.add_argument('-v','--version',
                        default="__latest__",
                        help='Package Version')

    parser.add_argument('-f','--file',
                        required=True,
                        help='File path to be uploaded or get downloaded into. [example: /path/to/filename.deb] ')

    return parser

# finding package registry project id
def find_package_registry_project_id(token, registry):
    """Returns the project ID of the package registry"""
    gl = gitlab.Gitlab(GITLAB_API, token)
    all_projects = gl.projects.list(get_all=True)
    for project in all_projects:
        if project.path_with_namespace == registry:
            return project
    raise Exception(f"Project not Found {registry}")

def get_latest_version(project, package_name):
    """Finding the latest package version from packages list"""
    print(f"Package Registry:  {project.path_with_namespace}")
    packages = project.packages.list(package_name=package_name, get_all=True)
    packages.sort(key=lambda x: version.parse(x.version), reverse=True )
    latest = packages[0].version
    print(f"Downloading latest version: {package_name} v{latest}")
    return latest


def download_package(project, package, version, filename):
    data = project.generic_packages.download(
        package_name=package,
        package_version=version,
        file_name="package.deb",)
    with open(filename, 'wb') as f:
        f.write(data)
    print("Download Success")


def upload_package(project, package, version, filename):
    filename = os.path.expanduser(filename)
    ret = project.generic_packages.upload(
        package_name=package,
        package_version=version,
        file_name="package.deb",
        path=f"{filename}")
    print(ret.to_json())
    print("Upload Success")
    return project


def main():

    parser = check_arg()
    args = parser.parse_args()
    project = find_package_registry_project_id(args.key, args.registry)

    if args.action == "upload":
        upload_package(project,
                       args.package, args.version,
                       args.file)
    elif args.action == "download":
        version = args.version
        if version == "__latest__":
            version = get_latest_version(project, args.package)

        download_package( project ,
                         args.package, version,
                         args.file)
    else:
        print("Error: action not defined")
        parser.print_usage()
        exit(2)

if __name__ == "__main__":
    main()
    exit(0)
