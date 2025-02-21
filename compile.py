from plugins.bottle.bottle import SimpleTemplate

import os.path
import sys

IGNORE_DIRS = [
    'parts'
]
TEMPLATE_DIR = 'templates'

# Use the -t flag if you want to compile for local tests
DEPLOY = not '-t' in sys.argv

class Compiler(object):

    # Function: Run
    # -------------
    # This function compiles all the html files (recursively)
    # from the templates dir into the current folder. Folder
    # hierarchy is preserved
    def run(self):
        templateFilePaths = self.getTemplateFilePaths('')
        for templateFilePath in templateFilePaths:
            self.compileTemplate(templateFilePath)

    #####################
    # Private Helpers
    #####################

    def compileTemplate(self, relativePath):
        print(relativePath)
        pathToRoot = self.getPathToRoot(relativePath)
        filePath = os.path.join(TEMPLATE_DIR, relativePath)
        templateText = open(filePath).read()
        compiledHtml = SimpleTemplate(templateText).render(pathToRoot = pathToRoot)
        self.makePath(relativePath)
        fileName, fileExtension = os.path.splitext(relativePath)
        compiledHtml = compiledHtml.encode('utf8')
        open(relativePath, 'wb').write(compiledHtml)

    def makePath(self, path):
        dirPath = os.path.dirname(path)
        if dirPath == '': return
        if not os.path.exists(dirPath):
            os.makedirs(dirPath)
        
    def getPathToRoot(self, relativePath):
        if DEPLOY:
            return '//web.stanford.edu/class/archive/cs/cs109/cs109.1166/'
        return self.getRelPathToRoot(relativePath)

    def getRelPathToRoot(self, relativePath):
        dirs = self.splitDirs(relativePath)
        depth = len(dirs) - 1
        pathToRoot = ''
        for i in range(depth, 0, -1):
            curr = dirs[i]
            if curr == 'cs106b':
                break
            pathToRoot += '../'
        return pathToRoot

    def splitDirs(self, filePath):
        if filePath == '': return []
        rootPath, last = os.path.split(filePath)
        rootDirs = self.splitDirs(rootPath)
        rootDirs.append(last)
        return rootDirs

    def isTemplateFile(self, fileName):
        extension = os.path.splitext(fileName)[1]
        return extension == '.html'

    def getTemplateFilePaths(self, root):
        if root in IGNORE_DIRS: return []
        paths = []
        templateDirPath = os.path.join(TEMPLATE_DIR, root)
        for fileName in os.listdir(templateDirPath):
            filePath = os.path.join(root, fileName)
            templateFilePath = os.path.join(TEMPLATE_DIR, filePath)
            if os.path.isdir(templateFilePath):
                childPaths = self.getTemplateFilePaths(filePath)
                for childPath in childPaths:
                    paths.append(childPath)
            elif self.isTemplateFile(fileName):
                paths.append(filePath)
        return paths


if __name__ == '__main__':
    Compiler().run()
