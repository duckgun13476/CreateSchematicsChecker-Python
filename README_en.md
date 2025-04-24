# CreateSchematicsChecker-Python

## A simple python script for checking Minecraft mod Create to check cheating Schematics
~~a helper to avoid bug schematr players~~



![python](https://github.com/user-attachments/assets/eb746af3-f0f4-4710-86b4-a4ad7f176369)

---

# Blueprint Checking Script

## Overview
This is a blueprint checking script based on mechanical power, designed to run with Python. It operates externally without occupying server performance and allows for customizable rules. It automatically checks all blueprints in the folder for bugs and anomalies, preventing any maliciously modified NBT blueprints from entering the Minecraft server.

## Features
- **Automatic Checking**: Automatically checks all blueprints in the folder, identifying and filtering potential bugs and anomalies to ensure server safety.
- **Highly Customizable Rules**: Allows users to customize rules for special NBT scanning tailored to specific mods.
- **MD5-Based Acceleration**: Accelerates processing using MD5 checks, significantly improving Python's runtime speed.
- **Conveyor Belt Tampering Check**: Utilizes a full-check algorithm to validate conveyor belts in versions 0.5.1 and 6.0.0, preventing bugs, duplication, and server crashes.
- **Gear Transmission Pairing Check**: Implements pairing checks for gear transmissions based on simple matching logic after version 6.0.0 to prevent known blueprint bugs and duplication.
- **Multiple Malicious NBT Checks**: Screens for various malicious NBT modification values to ensure blueprint safety.
- **Automatic Cloud Sync**: Automatically updates NBT checking rules, leaving malicious users with no escape.
- **Automatic Rule Updates**: Automatic rule updates have been implemented to ensure that rules are always up to date.

## Acknowledgments
Special thanks to crackun24 for providing parts of the code and for his help in this project.

## Dependencies
- Minecraft
- Create