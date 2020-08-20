#!/usr/bin/env python
import logging
import sys
import argparse
import os
import subprocess
import configparser


class Retrieve:

    def __init__(self, dataset_path, dataset_name, remote_prefix, encryption, clean=False):
        self.dataset_path = dataset_path
        self.remote_prefix = remote_prefix
        self.dataset_name = dataset_name
        self.clean = clean
        self.url_prefix = 'globus://'
        self.annex_uuid = None
        self.encryption = encryption

    @property
    def remote_path(self):
        return self.url_prefix + self.dataset_name + self.remote_prefix

    def get_remote_path(self):
        return self.remote_path

    @staticmethod
    def _execute_cmd(func, message):
        try:
            stderr = func
            if len(stderr) != 0:
                raise Exception(message + str(stderr))
        except Exception as ex:
            print('An exception occurred: ' + str(ex))
            sys.exit()

# ******************************************************************************************************************** #

    def _get_annex_uuid(self):
        config = configparser.ConfigParser()
        config.read(self.dataset_path + "/.git/config")
        try:
            return config['remote "globus"']['annex-uuid']
        except Exception as ex:
            print('The following exceptions was raised during annex-uuid retrieving: ' + str(ex))
            sys.exit()

    @staticmethod
    def _set_up():
        setup_command = ['git-annex-remote-globus', 'setup']
        process = subprocess.Popen(setup_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        _, error = process.communicate()
        return error

    def _init_remote(self):
        encryption = 'encryption=%s' % self.encryption
        endpoint = 'endpoint=%s' % self.dataset_name
        fileprefix = 'fileprefix=%s' % self.remote_prefix
        initremote_command = \
            ['git', 'annex', 'initremote', 'globus',  'type=external', 'externaltype=globus',
            encryption, endpoint, fileprefix]
        process = subprocess.Popen(initremote_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        _, stderr = process.communicate()
        if len(stderr) != 0:
            print('enabling remote')
            enableremote_command = ['git', 'annex', 'enableremote', 'globus', endpoint, fileprefix]
            process = subprocess.Popen(enableremote_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            _, error = process.communicate()
            return error
        else:
            return stderr

    def initialize(self):
        self._execute_cmd(self._set_up(), 'An error occurred during setup')
        self._execute_cmd(self._init_remote(), 'An error occurred during initialization')
        if not self.annex_uuid:
            self.annex_uuid = self._get_annex_uuid()

# ******************************************************************************************************************** #

    def retrieve_files(self, path, remote_path):
        try:
            # list content
            for elem in os.listdir(path):
                update_path = os.path.join(path, elem)
                update_remote_path = os.path.join(remote_path, elem)
                if os.path.isdir(update_path):
                    # recurse
                    self.retrieve_files(update_path, update_remote_path)
                else:
                    if os.path.islink(update_path):
                        key = str(os.readlink(update_path)).split('/')[-1]
                        # print(key, update_remote_path)
                        self.process(key, update_remote_path)
                    else:
                        pass
        except Exception as ex:
            print('The following exception was raised while retrieving files: ' + str(ex))
            sys.exit()

    def _set_present_key(self, key, val):
        # set present key
        setpresentkey_command = ['git', 'annex', 'setpresentkey', key, self.annex_uuid, str(val)]
        process = subprocess.Popen(setpresentkey_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        _, error = process.communicate()
        return error

    @staticmethod
    def _register_url(key, url):
        # register url
        registerurl_command = ['git', 'annex', 'registerurl', key, url]
        process = subprocess.Popen(registerurl_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        _, error = process.communicate()
        return error

    @staticmethod
    def _rm_url(file_path, url):
        # register url
        registerurl_command = ['git', 'annex', 'rmurl', file_path, url]
        process = subprocess.Popen(registerurl_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        _, error = process.communicate()
        return error

    def process(self, key, path):
        # TODO: add count of errors
        if self.clean:
            self._execute_cmd(self._set_present_key(key, 0),
                              str('An error occurred during setpresent 0 key with path: ' + path))
            file_path = path.split(self.remote_prefix)[1]
            # make sure the file path is valid
            if file_path.startswith('/'):
                file_path = file_path[1:]
            self._execute_cmd(self._rm_url(file_path, path),
                              str('An error occurred during url removal with path: ' + path))
        else:
            self._execute_cmd(self._set_present_key(key, 1),
                              str('An error occurred during setpresent 1 key with path: ' + path))
            self._execute_cmd(self._register_url(key, path),
                              str('An error occurred during url registration with path: ' + path))


def main():
    # Manage argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, help='Local dataset path')
    parser.add_argument('--endpoint', type=str, help='Remote dataset endpoint name')
    parser.add_argument('--fileprefix', type=str, help='Remote dataset files prefix')
    parser.add_argument('--encryption', type=str, default='none', help='Encryption mode')
    parser.add_argument('--clean', action='store_true', help='Specified to clean the repository from urls')
    args = parser.parse_args()
    # Start retrieving
    master = Retrieve(args.path, args.endpoint, args.fileprefix, args.encryption, args.clean)
    master.initialize()
    master.retrieve_files(args.path, master.get_remote_path())
    # TODO:count retrieved files below
    if args.clean:
        print("URLs successfully removed")
    else:
        print("Files successfully retrieved")


if __name__ == "__main__":
    main()

