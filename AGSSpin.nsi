OutFile "AGSSpinSetup64.exe"
Name "AGS Spin The Wheel"
InstallDir $ProgramFiles\AGSSpin

Section

SetOutPath $INSTDIR
File AGSSpin.exe
File win.wav
File wheel.png
File spin.wav
File wheel_anim.gif

CreateShortcut "$SMPROGRAMS\AGS Spin The Wheel.lnk" "$INSTDIR\AGSSpin.exe"
WriteUninstaller $INSTDIR\uninstall.exe

MessageBox MB_OK "AGS Spin The Wheel has successfully been installed"

SectionEnd

Section "Uninstall"
Delete $INSTDIR\AGSSpin.exe
Delete $INSTDIR\win.wav
Delete $INSTDIR\wheel.png
Delete $INSTDIR\uninstall.exe

RMDir $INSTDIR

SectionEnd