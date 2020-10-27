# xIPA

(a.k.a - Extract IPA) - Script to extract IPA files

## Introduction

* Script designed to extract **IPA** of an application installed on a **JailBroken iDevice**
* Tested on multiple applications including **Banking** applications
* Extracts and downloads the **IPA** to your **$PWD**
* The app extracted and downloaded will be **"encrypted"** and you can check this by `otool -arch all -Vl "APP Bundle Name" | grep -A5 LC_ENCRYPT`
* If **"cryptid=0"** means not encrypted else encrypted

## Pre-requisites

* Any linux distro
* An **iOS** app called **Filza** - Optional but comes handy to get app names
* Supports **Python3** only
* Supporting **PIP** libraries to be installed:
    * For SSH - `python3.8 -m pip install --upgrade paramiko`
    * For Command Line Argument Parsing - `python3.8 -m pip install --upgrade argparse`
* Just one application to be installed on **iPhone** or **iPAD** which is **Filza** which can come handy to get app names.

* **MOST IMPORTANT** - A **JailBroken iDevice**

## How does it work

* All you have to do is to run the script and provide all details and it will download the extracted IPA in your **$PWD** which you can later use for re-installation. 
* For re-installation just `scp` your downloaded **IPA** file to **iDevice** and use **Filza** to install.
* I tested it with most of the applications including **Banking** ones and it's working just fine. **_Let me know if it breaks anywhere_**

**NOTE**

> Make sure that the app is running on your **iDevice** before you start the script

> Extraction process will become slow if your **iDevice** sleeps. Make sure that the **iDevice** is wide awake

## Screenshots

* **xIPA - Help**

    ![](attachments/xIPA_help.png)

* **xIPA - Missing iDevice IP to SSH**

    ![](attachments/xIPA_error_hostIP.png)

* **xIPA - Missing App Display Name to Extract {target}**

    ![](attachments/xIPA_error_appName.png)

* **xIPA - Missing Extracted App Name {-o/--output}**

    ![](attachments/xIPA_error_outputName.png)

* **xIPA - App not running**

    ![](attachments/xIPA_error_appnotrunning.png)

* **xIPA - Success: Extracted IPA of VLC App**

    ![](attachments/xIPA_success_extractedIPA.png)

* **xIPA - Success: Downloaded Extracted IPA**

    ![](attachments/xIPA_success_downloadedIPA.png)

> **DISCLAIMER** : **JailBreak** your device at our own risk. This is just to provide **information** and is for **knowledge sharing**.
