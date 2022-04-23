FROM centos/python-38-centos7
LABEL yanqiaoyu <yqy1160058763@qq.com>
USER 0 
ENV PATH $PATH:/usr/local/python3/bin/ 
ENV   PYTHONIOENCODING utf-8 
ENV   LD_LIBRARY_PATH="/usr/local/lib" \
	LIBLEPT_HEADERSDIR="/usr/local/include" \
	PKG_CONFIG_PATH="/usr/local/lib/pkgconfig" \
	TESSDATA_PREFIX="/usr/local/share/tessdata"

ADD   tesseract-4.1.1.tar.gz leptonica-1.80.0.tar.gz requirements.txt / 
ADD   ads.traineddata /usr/local/share/tessdata/
RUN set -ex \
	# 安装python依赖库
	&& curl -o /etc/yum.repos.d/CentOS-Base.repo https://mirrors.aliyun.com/repo/Centos-7.repo \
	&& sed -i -e '/mirrors.cloud.aliyuncs.com/d' -e '/mirrors.aliyuncs.com/d' /etc/yum.repos.d/CentOS-Base.repo \
	&& yum makecache \
	&& yum update 
RUN     yum install -y file libjpeg-devel libpng-devel libtiff-devel zlib-devel gcc-c++ make libXext libSM libXrender
RUN     yum install -y automake libtool opencv
RUN     yum install -y epel-release
RUN     yum install -y supervisor
WORKDIR /
RUN     cd /leptonica-1.80.0 && ./configure && make && make install \
	&& cd /tesseract-4.1.1 && ./autogen.sh && ./configure && make && make install \
	&& rm -rf /leptonica-1.80.0 /tesseract-4.1.1 
# 更新pip
RUN	pip3 install -i https://mirrors.aliyun.com/pypi/simple/  --upgrade pip \
	# 安装wheel
	&& pip3 install -i https://mirrors.aliyun.com/pypi/simple/ -r /requirements.txt \
	# 删除安装包
	&& cd .. \
	&& find / -name "*.py[co]" -exec rm '{}' ';' \
	&& yum clean all \
	&& rm -rf /var/cache/yum 
COPY ./app /app
COPY ./etc/supervisord.conf /etc/supervisord.conf
COPY ./tmp /tmp
WORKDIR /app
ENTRYPOINT ["supervisord", "-c", "/etc/supervisord.conf"]
#ENTRYPOINT ["tail", "-f", "/dev/null"]
