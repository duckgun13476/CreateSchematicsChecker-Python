# CreateSchematicsChecker-Python

## A simple python script for checking Minecraft mod Create to check cheating Schematics
~~玩bug蓝图的熊孩子的对策杀手（bushi~~



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

## Help
Help provided by crackun24.

## Dependencies
- Minecraft
- Create

---
## 概述
这是一个基于机械动力的蓝图检查脚本，使用 Python 运行。该脚本外置，不占用服务器性能，并允许自定义规则。它能够自动筛查蓝图文件夹下的所有 bug 与异常蓝图，防止任何恶意篡改 NBT 的蓝图流入 Minecraft 服务器。

## 功能
- **自动筛查**：自动检查蓝图文件夹下的所有蓝图，识别并过滤出潜在的 bug 与异常蓝图，确保服务器安全。
- **高度自定义规则**：允许用户自定义规则，以针对特定模组实现特殊的 NBT 扫描。
- **基于 MD5 的加速处理**：通过 MD5 校验加速处理，显著提高 Python 的运行速度。
- **传送带篡改校验**：使用全校验算法对 0.5.1 和 6.0.0 版本的传送带进行校验，阻止传送带蓝图的 bug 与复制、卡服、崩服特性。
- **齿轮传动轮配对校验**：在 6.0.0 版本后，基于简单匹配逻辑进行齿轮传动轮的配对校验，防止已知蓝图 bug 与复制特性。
- **多种恶意 NBT 筛查**：针对多种恶意 NBT 篡改值进行筛查，确保蓝图的安全性。
- **自动云端同步**：自动更新 NBT 检查规则，让恶意用户无处可逃。
- **自动更新规则**：已实现自动更新规则功能，确保规则始终保持最新状态。

## 致谢
特别感谢 crackun24 提供的部分代码，以及他在项目中提供的帮助。

## 帮助
帮助由 crackun24 提供。

## 依赖
- Minecraft
- Create

---




