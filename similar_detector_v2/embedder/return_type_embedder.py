#!/usr/bin/python2

from argparse import ArgumentParser
from joerntools.APIEmbedder import APIEmbedder

DEFAULT_DIRNAME = 'embedding'

class APIEmbedderCLI(object):
    def __init__(self, description):
        self.description = description
        self._initializeOptParser()

    def _initializeOptParser(self):
        self.argParser = ArgumentParser(description = self.description)
        
        self.argParser.add_argument('-d', '--dirname', nargs='?',
                                    type = str, help="""The directory to write the embedding to.""",
                                    default = DEFAULT_DIRNAME)
    def run(self):
        self._parseCommandLine()        
        apiEmbedder = APIEmbedder()
        apiEmbedder.setOutputDirectory(self.args.dirname)
        apiEmbedder.run()
        
    def _parseCommandLine(self):
        self.args = self.argParser.parse_args()
        self.outputDirectory = self.args.dirname

if __name__ == '__main__':
    description = """apiEmbedder.py - A tool to embed code in vector spaces"""
    embedder = APIEmbedderCLI(description)
    embedder.run()