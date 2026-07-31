# demo.tape — VHS script for gitroast's README demo GIF
# Install VHS first: https://github.com/charmbracelet/vhs#installation
#   macOS:   brew install vhs
#   Linux:   see VHS README (needs ttyd + ffmpeg as deps)
#
# Run:  vhs demo.tape
# Output: demo.gif (place it at the top of README.md)

Output demo.gif

Set Shell "bash"
Set FontSize 18
Set Width 900
Set Height 500
Set Theme "Dracula"
Set Padding 20
Set TypingSpeed 60ms

Type "gitroast"
Sleep 500ms
Enter
Sleep 4s
