# English Assistant Form		 
This project is related to the implementation of the English Assistant Application, which helps us to learn English as an assistant. And, Also this package has the ability to translate from English to Persian.
## Instruction

1. Install [Python](https://www.python.org/).



2. Install [English Assistant Form](https://github.com/yasharsajadi/EnglishAssistantForm)

Windows:
```
pip install EnglishAssistantForm
```
Linux:
```
pip3 install EnglishAssistantForm
```

## Usage
In the Python file(.pyw):
```
from EnglishAssistantForm.EnglishAssistantForm import App

if __name__ == "__main__":
	app = App()
	app.mainloop()
```

In the Batch file(.bat):
```
@echo off

echo from EnglishAssistantForm.EnglishAssistantForm import App>> "%~dp0%EnglishAssistantApplication.pyw"

echo app = App()>> ""%~dp0%EnglishAssistantApplication.pyw"
echo app.mainloop()>> "%~dp0%EnglishAssistantApplication.pyw"

start pythonw "%~dp0%EnglishAssistantApplication.pyw"

timeout /T 3
del /f "%~dp0%EnglishAssistantApplication.pyw"
```




