FROM amazonlinux:latest

USER root
WORKDIR /root/opt
RUN yum update -y
RUN yum install -y gcc make zlib-devel bzip2 bzip2-devel readline-devel git patch tar \
                 sqlite sqlite-devel openssl-devel tk-devel libffi-devel xz-devel less vim 


SHELL ["/bin/bash", "-c"]
RUN git clone https://github.com/yyuu/pyenv.git ~/.pyenv && \
    echo '' >> ~/.bashrc && \
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc && \
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc && \
    echo 'eval "$(pyenv init --path)"' >> ~/.bashrc 

RUN source ~/.bashrc && pyenv install 3.12.4 && \
    pyenv local 3.12.4 && \
	pip install --upgrade pip && pip install pytest pandas

##  元からインストールされているシステムのpython3と明確に切り分けるために、
##  実行環境では、python3.12.4 をpyenv localで使用する。
##  マウントするディレクトリには、Dockerfileでの操作からファイルが作られないみたい
##  (pyenv local 3.12.4 と同じ操作内容の以下の操作で作られないことを確認)
##  touch .python-version && echo '3.12.4' >> .python-version && \
##  そのため、マウント位置を/root/optから/root/opt/taskに変更
##  (docker-compose.ymlにてマウント位置を/root/opt/taskに指定)
##  pyenv local 3.12.4は、マウントする位置の一つ上の/root/optにて実行
##  (サブディテクトリである/root/opt/task以下にも適用される)






