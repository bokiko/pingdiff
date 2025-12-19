; PingDiff Installer Script
; Built with Inno Setup

#define MyAppName "PingDiff"
#define MyAppVersion "1.6.0"
#define MyAppPublisher "PingDiff"
#define MyAppURL "https://pingdiff.com"
#define MyAppExeName "PingDiff.exe"

[Setup]
; App identification
AppId={{A7E8F4D2-3B1C-4E5F-9A8B-2C4D6E8F0A1B}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}/download

; Installation settings
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
LicenseFile=
PrivilegesRequiredOverridesAllowed=dialog
OutputDir=installer_output
OutputBaseFilename=PingDiff-Setup-{#MyAppVersion}
Compression=lzma
SolidCompression=yes
WizardStyle=modern

; Upgrade behavior - clean install
CloseApplications=yes
RestartApplications=no
UninstallDisplayIcon={app}\{#MyAppExeName}
UninstallDisplayName={#MyAppName}

; Allow user to choose install location
AllowNoIcons=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Main executable and dependencies (from PyInstaller output folder)
Source: "dist\PingDiff\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#MyAppName}}"; Flags: nowait postinstall skipifsilent

[Code]
// Clean up old installation before installing new version
procedure CurStepChanged(CurStep: TSetupStep);
var
  OldDir: String;
begin
  if CurStep = ssInstall then
  begin
    // Remove old program files (but NOT user data in AppData)
    OldDir := ExpandConstant('{app}');
    if DirExists(OldDir) then
    begin
      DelTree(OldDir, True, True, True);
    end;
  end;
end;

// Show info about where logs are stored
procedure CurPageChanged(CurPageID: Integer);
begin
  if CurPageID = wpFinished then
  begin
    // Could add custom message here if needed
  end;
end;

[Messages]
WelcomeLabel2=This will install [name/ver] on your computer.%n%nPingDiff tests your connection to game servers and helps you find the best server for your location.%n%nYour settings and logs are stored in:%n%APPDATA%\PingDiff

[UninstallDelete]
; Only delete program files, NOT user data in AppData
Type: filesandordirs; Name: "{app}"
