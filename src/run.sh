# /bin/zsh
toilet -f smblock --metal "gen"
python run.py gen


toilet -f smblock --metal "intermediate code generation"
python run.py test CodeGenSuite