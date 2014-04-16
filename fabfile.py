from fabric.decorators import task
from fabric.api import local

@task    
def test():
    local('python -m unittest discover -vvv -t core -s core/test -p "*.py"')
    
    
@task
def testJython():
    local('echo $PYTHONPATH')
    local('java -Dpython.path=$PYTHONPATH -jar jython.jar core/readstate.py')