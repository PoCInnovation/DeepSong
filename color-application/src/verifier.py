import os

def verifyPath(app):
    path = app.window.AudioLineEdit.text()

    if (not(os.path.exists(path))):
        app.window.ErrorLabel.setStyleSheet("color:red;")
        app.window.ErrorLabel.setText("*Invalid path")
        return

    if (not(any([path.endswith(ext) for ext in ["wav", "mp3", "mdi"]]))):
        app.window.ErrorLabel.setStyleSheet("color:red;")
        app.window.ErrorLabel.setText("*Invalid file format")
        return

    app.setPath(path)
    app.window.ErrorLabel.setStyleSheet("color:lightgreen;")
    app.window.ErrorLabel.setText("Valid file")

    app.window.fileLoadingLabel.show()
    app.window.FileLoadingProgressBar.show()

    app.loadFile()

    
    
