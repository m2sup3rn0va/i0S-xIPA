# xIPA

(a.k.a - Extract IPA) - Script to extract IPA files

## Introduction

* Script designed to extract **IPA** of an application installed on a **JailBroken iDevice**
* Tested on multiple applications including **Banking** applications
* Extracts and downloads the **IPA** to your **$PWD**

## Pre-requisites

* Any linux distro
* An **iOS** app called **Filza** - Optional but comes handy to get app names
* Supports **Python3** only
* **MOST IMPORTANT** - A **JailBroken iDevice**

## Summary

I came across the idea to write this script when I faced issue extracting the IPA file for analysis. We have a great tool called [**frida-ios-dump**](https://github.com/AloneMonkey/frida-ios-dump), but unfortunately was not working for me. There were lot of errors related to **"diskimagemount"** or **"hooking"** to the process via **"frida"**. The other reason was to learn how to write similar codes.

So, finally I came up with my own **"python script"**, to extract **IPAs** of installed applications for analysis.
The best part about this is there is no need of **Frida** as we are not **hooking** into any process nor we need **USB** connection to get the **IPA**.


Just one application to be installed on **iPhone** or **iPAD** which is **Filza** which can come handy to get app names.
All you have to do is to run the script and provide all details and it will download the extracted IPA in your **$PWD** which you can later use for re-installation.

I tested it with most of the applications including **Banking** ones and it's working just fine. Let me know if it breaks anywhere.


> **DISCLAIMER** : **JailBreak** your device at our own risk. This is just to provide **information** and is for **knowledge sharing**.
