!include "MUI.nsh"

OutFile "AGSSpinSetup64.exe"
Name "AGS Spin The Wheel"
InstallDir $ProgramFiles\AGSSpin
BrandingText "Gabriel Alonso-Holt"

!define MUI_HEADERIMAGE_BITMAP "header.bmp"
!define MUI_WELCOMEFINISHPAGE_BITMAP "wizard.bmp"
!define MUI_ICON "setup.ico"

!define MUI_WELCOMEPAGE_TEXT "Setup will guide you through the installation process of AGS Spin The Wheel.\n\nYou should close all other application before continuing.\n\nClick Next to continue and Cancel to exit the Setup Wizard."

Function LaunchLink
	ExecShell "" "$SMPROGRAMS\AGS Spin The Wheel.lnk"
FunctionEnd

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "license.txt"
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES

!define MUI_FINISHPAGE_NOAUTOCLOSE
!define MUI_FINISHPAGE_RUN
!define MUI_FINISHPAGE_RUN_NOTCHECKED
!define MUI_FINISHPAGE_RUN_TEXT "Start AGS Spin The Wheel"
!define MUI_FINISHPAGE_RUN_FUNCTION "LaunchLink"

!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_DIRECTORY
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

!insertmacro MUI_LANGUAGE "English"

Section "Main program"

	SetOutPath $INSTDIR
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\AGSSpin" "DisplayName" "AGS Spin The Wheel"
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\AGSSpin" "DisplayVersion" "1.2"
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\AGSSpin" "Publisher" "Gabriel Alonso-Holt"
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\AGSSpin" "DisplayIcon" "$INSTDIR\setup.ico"
	WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\AGSSpin" "NoModify" 1
	WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\AGSSpin" "NoRepair" 1
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\AGSSpin" "UninstallString" "$INSTDIR\uninstall.exe"

	File AGSSpin.exe
	File win.wav
	File wheel.png
	File spin.wav
	File wheel_anim.gif
	File license.txt
	File spin_config.ini

	CreateShortcut "$SMPROGRAMS\AGS Spin The Wheel.lnk" "$INSTDIR\AGSSpin.exe"
	WriteUninstaller $INSTDIR\uninstall.exe

SectionEnd

Section "Desktop shortcut"

	CreateShortcut "$DESKTOP\AGS Spin The Wheel.lnk" "$INSTDIR\AGSSpin.exe"

SectionEnd

Section "Uninstall"

	DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\AGSSpin"

	Delete $INSTDIR\win.wav
	Delete $INSTDIR\wheel.png
	Delete $INSTDIR\wheel_anim.gif
	Delete $INSTDIR\spin.wav
	Delete $INSTDIR\AGSSpin.exe
	Delete $INSTDIR\license.txt
	Delete $INSTDIR\spin_config.ini
	Delete $INSTDIR\uninstall.exe

	RMDir $INSTDIR

SectionEnd
