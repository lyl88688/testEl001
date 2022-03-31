import subprocess


class Shell:
    @staticmethod
    def invoke(cmd):
        output, err = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        o = output.decode("utf-8")
        print(o)
        return o

    def cmdinfo(self,command):
        subp, err= subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
        subp.wait(2)
        print(subp.communicate()[1])



