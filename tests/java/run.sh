# /bin/zsh
DIRECTORY="$1"
FILE="$2"
JAVA="$2"".java"
CLASS="$2"".class"
if [ -d "$DIRECTORY" ]; then
  cd "$DIRECTORY" || exit
  toilet -f smblock --metal "assembly-like generation"
  javac -cp ./.. $JAVA
  java -jar ../classfileanalyzer.jar -file $CLASS
else
  echo "./start <DIR>"
  echo "Directory does not exist!"
fi