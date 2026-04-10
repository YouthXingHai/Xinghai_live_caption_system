# Xinghai Live Caption System

A lightweight broadcast subtitle and teleprompter system for livestream production.

## Features

- WebSocket realtime subtitle switching
- Web controller
- OBS / vMix browser subtitle output
- Actor teleprompter
- Script cue support using [stage directions]
- YAML configuration
- Auto progress save

## Script Format

Each line is one step.

Example:

给我一片繁星 陪伴海棠花开

[灯光渐亮]

给你一湾瀚海 栽下杨柳满怀

Lines inside [] are stage cues.

They appear on teleprompter but not on broadcast subtitles.

## Install

pip install -r requirements.txt

## Run Server

uvicorn server.main:app --reload --host 0.0.0.0

## Outputs

Subtitle:
http://localhost:8000/web/subtitle.html

Teleprompter:
http://localhost:8000/web/teleprompter.html

Web Controller:
http://localhost:8000/web/controller.html

Access the website after adding mDNS and Nginx reverse proxy：

Subtitle: http://infoadmin.local/s

Teleprompter: http://infoadmin.local/t

Controller: http://infoadmin.local/c


## OBS / vMix

Add Browser Source

Resolution:
1920x1080

URL:
http://localhost:8000/subtitle.html
