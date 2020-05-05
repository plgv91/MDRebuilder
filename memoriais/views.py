from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from MDRebuilder.form import ComentarioForm
from PIL import Image, ImageDraw
from datetime import datetime
import PyPDF2
import re
import os
import glob
import zipfile

def home(request):

    if request.POST:

        #código para envio de comentários
        nomeForm = request.POST.get('nome')

        if nomeForm:

            dados = {}
            form = ComentarioForm(request.POST or None)
            dados['form'] = form

            if form.is_valid():
                form.save()
                return redirect('home')

        #código para envio e arquivos
        if request.FILES:

            #arquivo enviado
            uploadedFile = request.FILES['document']
            fs = FileSystemStorage()

            extensaoArquivo = str(uploadedFile.name).split('.')
            if str(extensaoArquivo[1]).upper() != 'PDF':

                dados = {}
                form = ComentarioForm(request.POST or None)
                dados['form'] = form

                return render(request, 'memoriais/home.html', dados)

            BASE_DIR = os.path.dirname(os.path.abspath(__file__))

            #exclui arquivos da pasta para ficar apenas os novos
            excluirArquivos(os.path.join(BASE_DIR + '\..\media\*'))

            now = datetime.now()
            milissegundos = str(now).split('.')
            horario = str(f'{now.hour:02d}') + '-' + str(f'{now.minute:02d}') + '-' + str(f'{now.second:02d}') + '-' + str(milissegundos[1])

            #fs.save(horario + 'MEMORIALDESCRITIVO', uploadedFile)
            fs.save('MEMORIALDESCRITIVO.pdf', uploadedFile)
            #diretorio = os.path.join(BASE_DIR + '\..\media', horario + 'MEMORIALDESCRITIVO.pdf')
            diretorio = os.path.join(BASE_DIR + '\..\media', 'MEMORIALDESCRITIVO.pdf')

            pdfFileObj = open(diretorio, 'rb')
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj, strict=False)
            numPages = pdfReader.getNumPages()
            '''print(numPages)'''

            texto = ''

            for i in range(0, numPages):
                pageObj = pdfReader.getPage(i)
                texto += str(pageObj.extractText())

            #diretorio = os.path.join(BASE_DIR + '\..\media', horario + 'MEMORIAL.txt')
            diretorio = os.path.join(BASE_DIR + '\..\media', 'MEMORIAL.txt')

            arquivo = open(diretorio, 'w')

            texto = texto.replace('\n', '')
            arquivo.write(texto)
            arquivo.close()
            '''print(texto)'''

            texto = texto.replace('.', '')
            texto = texto.replace('N ', 'N:')
            texto = texto.replace('E ', 'E:')

            padraovertice = r'vértice\s[A-Z]\d+-[A-Z]-\d+'
            padraocoordenadaN = r'N:\d+,\d+'
            padraocoordenadaS = r'E:\d+,\d+'

            vertices = []
            coordenadasN = []
            coordenadasE = []

            qtd = 0
            for i in re.findall(padraocoordenadaN, texto):
                coordenadasN.insert(qtd, str(i).replace('N:', ''))
                qtd += 1

            qtd = 0
            for i in re.findall(padraocoordenadaS, texto):
                coordenadasE.insert(qtd, str(i).replace('E:', ''))
                qtd += 1

            qtd = 0
            for i in re.findall(padraovertice, texto):
                vertices.insert(qtd, str(i).replace('vértice ', ''))
                qtd += 1

            arquivoCoordenadas = 'ID;Vertice;N;E\n'
            poligono = []

            minimoN = float(min(coordenadasN).replace(',', '.'))
            minimoE = float(min(coordenadasE).replace(',', '.'))
            maximoN = float(max(coordenadasN).replace(',', '.'))
            maximoE = float(max(coordenadasE).replace(',', '.'))

            for i in range(0, qtd):
                arquivoCoordenadas += str(i + 1) + ';' + vertices[i] + ';' + coordenadasN[i] + ';' + coordenadasE[i] + '\n'
                poligono.append((float(coordenadasN[i].replace(',', '.')) - minimoN, float(coordenadasE[i].replace(',', '.')) - minimoE))
                '''print(vertices[i] + '\t' + coordenadasN[i] + '\t' + coordenadasE[i])'''

            '''print(arquivoCoordenadas)'''

            #diretorio = os.path.join(BASE_DIR + '\..\media', horario + 'COORDENADAS.txt')
            diretorio = os.path.join(BASE_DIR + '\..\media', 'COORDENADAS.txt')

            arquivo = open(diretorio, 'w')

            arquivo.write(arquivoCoordenadas)

            arquivo.close()

            pdfFileObj.close()

            #poligonoMemorial(poligono, horario)
            poligonoMemorial(poligono, int(maximoN - minimoN), int(maximoE - minimoE))

            return HttpResponseRedirect('download')

    dados = {}
    form = ComentarioForm(request.POST or None)
    dados['form'] = form

    return render(request, 'memoriais/home.html', dados)


def excluirArquivos(diretorio):

    #now = datetime.now()

    files = glob.glob(diretorio)

    for f in files:

        #divisao = f.split('-')
        #horarioArquivo = int(str(f'{now.hour:02d}') + '-' + str(f'{now.minute:02d}'))
        #horarioAgora = int(divisao[0] + divisao[1])

        #if horarioAgora > horarioArquivo + 5:
        os.remove(f)


#def poligonoMemorial(poligono, horario):
def poligonoMemorial(poligono, N, E):

    img = Image.new('RGBA', (N, E), '#2E2E2E')
    draw = ImageDraw.Draw(img)
    draw.polygon(poligono, fill='gray', outline='orange')
    #img.save('media/' + horario + 'POLIGONO.png')
    img.save('media/POLIGONO.png')


def download(request):

    if request.POST:

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        diretorio = os.path.join(BASE_DIR + '\..\media')

        arquivoZip = zipfile.ZipFile(diretorio + '\MDRebuilder.zip', 'w')

        for folder, subfolders, files in os.walk(diretorio):

            for file in files:
                if file.endswith('.png') or file.endswith('.txt'):
                    arquivoZip.write(os.path.join(folder, file),
                                      os.path.relpath(os.path.join(folder, file), diretorio),
                                      compress_type=zipfile.ZIP_DEFLATED)

        arquivoZip.close()

        diretorio = os.path.join(BASE_DIR + '\..\media', 'MDRebuilder.zip')

        with open(diretorio, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/force-download")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(diretorio)

        return response

    return render(request, 'memoriais/download.html')