def soma(a, b):
      return a + b
def mult(a, b):
      return a * b


def importar():
      from google.colab import files
      uploaded = files.upload()
      filename = list(uploaded.keys())[0]
      output_filename = filename.replace('.xlsx', ".mf4")
      return (filename, output_filename)
