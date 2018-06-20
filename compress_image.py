import os
from PIL import Image, ImageFile
from sys import stderr
from os.path import getsize, isfile, isdir, join
from os import rename, stat
from stat import S_IWRITE
from shutil import move

# Classe para processar e reduzir o tamanho da imagem
class CompressImage(object):

    def __init__(self):
        self.extensions = ['jpg', 'jpeg', 'png']
        self.backupextension = 'compress-backup'

        dirlist = os.listdir("./img")
        for i in dirlist:
            filename = os.path.abspath(i)
            basename = os.path.basename(filename)
            print('Arquivo ' + basename)
            # processor = compressao_img.Compress()
            # processor.processfile(arquivo)

    def processfile(self, filename):
        # Renomeia a imagem especificada para o caminho de backup
        # e grava a imagem original com tamanho reduzido
        try:
            # Ignora arquivos somente leitura
            if (not stat(filename)[0] & S_IWRITE):
                print(
                'Ignorando arquivos somente leitura: "' + filename + '".')
                return False

            # Criando o backup
            backupname = filename + '.' + self.backupextension

            if isfile(backupname):
                print
                'Arquivo ignorado "' + filename + '" pois ja existe arquivo de bakcup criado.'
                return False

            rename(filename, backupname)
        except Exception as e:
            stderr.write('Arquivo ignorado "' + filename + '" pois o backup nao pode ser criado: ' + str(e) + '\n')
            return False

        ok = False

        try:
            # Abrindo a imagem
            with open(backupname, 'rb') as file:
                img = Image.open(file)

                # Verificacao do formato da imagem a ser compactada
                format = str(img.format)
                if format != 'PNG' and format != 'JPEG':
                    print(
                    'Arquivo ignorado: "' + filename + '" - formato nao suportado: ' + format)
                    return False

                # Esta linha evita problemas que podem surgir salvando arquivos JPEG maiores com PIL
                ImageFile.MAXBLOCK = img.size[0] * img.size[1]

                # A opção 'quality' é ignorada para arquivos PNG
                img.save(filename, quality=90, optimize=True)

            # Verifique se realmente foi efetuado a compressão
            origsize = getsize(backupname)
            newsize = getsize(filename)

            if newsize >= origsize:
                print(
                'Nao e possível comprimir a imagem "' + filename + '".')
                return False

            # Compressao com sucesso
            ok = True
        except Exception as e:
            stderr.write('Falha durante o processamento do arquivo "' + filename + '": ' + str(e) + '\n')
        finally:
            if not ok:
                try:
                    move(backupname, filename)
                except Exception as e:
                    stderr.write('ERROR: não foi possivel restaurar o arquivo de backup "' + filename + '": ' + str(e) + '\n')
        return ok

if __name__ == "__main__":
    processor = CompressImage()
    processor.processfile('img.png')