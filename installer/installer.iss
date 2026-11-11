[Setup]
AppName=CodeLume Bug Hunter
AppVersion=1.0
DefaultDirName={pf}\CodeLume Bug Hunter
DefaultGroupName=CodeLume Bug Hunter
OutputDir=installer
OutputBaseFilename=CodeLume-Bug-Hunter-Setup
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\CodeLume-Bug-Hunter.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\CodeLume Bug Hunter"; Filename: "{app}\CodeLume-Bug-Hunter.exe"
Name: "{commondesktop}\CodeLume Bug Hunter"; Filename: "{app}\CodeLume-Bug-Hunter.exe"