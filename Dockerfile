FROM centos:7.5.1804
MAINTAINER yanqiaoyu <yqy1160058763@qq.com>
 
ENV PATH $PATH:/usr/local/python3/bin/ 
ENV   PYTHONIOENCODING utf-8 
ENV   LD_LIBRARY_PATH="/usr/local/lib" \
      LIBLEPT_HEADERSDIR="/usr/local/include" \
      PKG_CONFIG_PATH="/usr/local/lib/pkgconfig" \
      TESSDATA_PREFIX="/usr/local/share/tessdata"

ADD   tesseract-4.1.1.tar.gz leptonica-1.80.0.tar.gz requirements.txt / 
ADD   ads.traineddata /usr/local/share/tessdata/
RUN set -ex \
	# 替换yum源
	&& mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup \ 
	&& curl -o /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo \
	&& sed -i -e '/mirrors.cloud.aliyuncs.com/d' -e '/mirrors.aliyuncs.com/d' /etc/yum.repos.d/CentOS-Base.repo \	
	# 安装python依赖库
	&& yum makecache \
	&& yum install -y  python3 supervisor file automake libjpeg-devel libpng-devel libtiff-devel zlib-devel libtool gcc-c++ make libXext libSM libXrender\
        && cd /leptonica-1.80.0 && ./configure && make && make install \
        && cd /tesseract-4.1.1 && ./autogen.sh && ./configure && make && make install \
	&& cd .. \
        && rm -rf /leptonica-1.80.0 /tesseract-4.1.1 \
	# 更新pip
	&& pip3 install  --upgrade pip \
	# 安装wheel
	&& pip3 install -i https://mirrors.aliyun.com/pypi/simple/ -r /requirements.txt \
	# 删除安装包
	&& cd .. \
	&& find / -name "*.py[co]" -exec rm '{}' ';' \
	&& yum clean all \
	&& rm -rf /var/cache/yum 
COPY ./app /app
WORKDIR /app
ENTRYPOINT ["sh", "wait-for", "yToolsBox-db:5432", "--", "supervisord", "-c", "/etc/supervisord.conf"]
