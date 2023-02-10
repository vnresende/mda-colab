def uploading_files():
    from google.colab import files, runtime
    uploaded = files.upload()
    uploaded_files = list(uploaded.keys())
    output_filename = [] 
    for file_name in uploaded_files:
        output_filename.append(file_name.replace('.xlsx', ".mf4"))
    return (uploaded_files, output_filename)
