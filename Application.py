import pygubu
from tkinter import *
import tkinter.filedialog as fd
import os

from SecureModule import Protocol

class App:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_from_file("UI.ui")
        
        self.mainwindow = builder.get_object('toplevel', master)
        self.connectButton  = builder.get_object('connectButton', self.mainwindow)
        self.encryptRadioButton = builder.get_object('encryptRadioButton', self.mainwindow)
        self.decryptRadioButton = builder.get_object('decryptRadioButton', self.mainwindow)
        self.selectInputFile = builder.get_object('selectInputFile', self.mainwindow)
        self.selectOutputFile = builder.get_object('selectOutputFile', self.mainwindow)
        
        self.inputFile = builder.get_object('inputFile', self.mainwindow)
        self.outputFile = builder.get_object('outputFile', self.mainwindow)
        
        self.mode = None
        self.sharedSecret = None
        self.nonce = b'password'
        builder.import_variables(self, ['mode', 'inputfile', 'outputfile', 'sharedSecret'])               
        builder.connect_callbacks(self)
        
        self.prtcl = Protocol()
    
    def ModeSelect(self):
        pass

    def SelectInputFile(self):
        file = fd.askopenfilename()
        self.inputFile.delete(0, 'end')
        self.inputFile.insert('end',file)

    def SelectOutputFile(self):
        path = fd.askdirectory()
        self.outputFile.delete(0, 'end')
        self.outputFile.insert('end',path)

    def ProcessFile(self):
        file = self.inputFile.get()
        path = self.outputFile.get()
        mode = self.mode.get()
        success = False
        try:
            if mode == 0:
                success = self.Encrypt(file,path)
            elif mode == 1:
                success = self.Decrypt(file,path)
            
            if success:
                self.success()
            else:
                print('the attempted operation has failed')
        except Exception as e:
            print('the attempted operation has failed: {}'.format(str(e)))

    def Encrypt(self, infile, outpath):
        f = open(infile, "rb")
        plain_text = f.read()
        f.close()
        cipher_text = self.prtcl.EncryptAndProtectMessage(plain_text,self.nonce,self.sharedSecret.get())
        outfile = outpath+'/'+(infile.split('/').pop())+'.secure'
        f = open(outfile, "wb")
        f.write(cipher_text)
        f.close()
        return True

    def Decrypt(self, infile, outpath):
        f = open(infile, "rb")
        cipher_text = f.read()
        f.close()
        plain_text = self.prtcl.DecryptAndVerifyMessage(cipher_text,self.nonce,self.sharedSecret.get())
        filename = infile.split('/').pop().split('.')[:-1]
        outfile = str(outpath+'/'+'.'.join(filename))
        f = open(outfile, "wb")
        f.write(plain_text)
        f.close()
        return True
    
    def success(self):
        path = self.outputFile.get()
        os.startfile(path)

    def run(self):
        self.mainwindow.mainloop()

if __name__ == '__main__':
    app = App()
    app.run()