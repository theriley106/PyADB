# PyADB

## [[Video] Using PyADB to Automate 50 Android Phones Simultaneously](https://www.youtube.com/watch?v=OKAF0-ThbhY)

## Multi-Device Android Automation Using Python

[![N|Solid](android.png)](#)



Python wrapper for the [Android Device Bridge](https://developer.android.com/studio/command-line/adb.html) that allows for multiple devices to be connected simultaneously.

A few of the functions are Phone-Specific, and will only work with select Alcatel One-Touch devices.  This is especially true with the Example/ folder, which contains APP specific automation projects that are specific to the device they were run on.  If you are the owner of an APP, and you would like to remove your Application from the Example/ automation scripts please send me a message on Github

## To Do

I've created a function that will record and replay screen actions using Python's Pickle, but this will be either removed or edited to serve an alternate purpose on the next release.  If I remember correctly, Android 7.0 currently has a method of replaying touch coordinates in a similar way.  There are also a ton of Open-Sourced projects on Github that accomplish the same thing in a much cleaner way.

I will also add a method of interacting with both USB devices and ADB over wifi devices.
