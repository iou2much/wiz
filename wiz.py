#!/usr/bin/python
# -*- coding:utf-8 -*-
import re,sqlite3,zipfile,glob,os,sys,shutil

class wiz():
    def extract(self,f):
        try:
            os.mkdir(f[:-4])
            zfile = zipfile.ZipFile(f,'r')
            zfile.extractall(path = f[:-4])
            os.remove(f)
        except:
            #print f
            pass

    def extract_all(self,path):
        file_list = glob.glob('%s/*'%path)

        if '%s/index.html'%path in file_list and '%s/index_files'%path in file_list:
            return

        #print file_list
        for f in file_list:
            if f[-4:] == '.ziw':
                #print f
                self.extract(f)
            elif os.path.isdir(f):
                self.extract_all(f)
        #print '-'*100

    def zip(self,f):
        pass

    re_img = re.compile(r'src="(.*?)"')

    ex_num = 0
    def collect_img(self,path):
        #print (re.escape(r'%s/*'%path))
        #print path
        try:
            flist = os.listdir(path)
            #print flist
        except:
            print ('%s/*'%path)
            self.ex_num += 1
            print self.ex_num
            return
        #print flist
        if 'index.html' in flist:
            content = open('%s/index.html'%path,'r').read().decode('utf-16')
            #print content
            imgs = self.re_img.findall(content)
            imgs = [i.split('/')[-1] for i in imgs]
            try:
                for f in os.listdir('%s/index_files'%path):
                    #print f
                    if f.split('/')[-1] in imgs:
                        #print f
                        continue
                    else:
                        os.remove('%s/index_files/%s'%(path,f))
            except:
                pass
            self.ziw(path)
            shutil.rmtree(path)
        else:
            for f in flist:
                if os.path.isdir('%s/%s'%(path,f)):
                    #print f,os.path.isdir('%s/%s'%(path,f))
                    self.collect_img('%s/%s'%(path,f))

    def ziw(self,name):
        f = zipfile.ZipFile('%s.ziw'%name,'w',zipfile.ZIP_DEFLATED)
        for dirpath, dirnames, filenames in os.walk(name):
            for filename in filenames:
                f.write(os.path.join(dirpath,filename),'%s/%s'%(dirpath.replace(name,''),filename))
        f.close()

    def del_css(self,f):
        pass

if __name__ == '__main__':
    w = wiz()
    #w.extract_all('.')
    w.collect_img('.')
