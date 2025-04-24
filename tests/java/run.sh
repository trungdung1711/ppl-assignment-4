# /bin/zsh
DIRECTORY="$1"
if [ -d "$DIRECTORY" ]; then
  cd "$DIRECTORY" || exit
  toilet -f smblock --metal "assembly-like generation"
  javac MiniGoClass.java
  java -jar ../classfileanalyzer.jar -file MiniGoClass.class
else
  echo "./start <DIR>"
  echo "Directory does not exist!"
fi