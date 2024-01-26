FROM python:3.10
WORKDIR /app
COPY requirements.txt .
COPY Makefile .
RUN pip install -r requirements.txt && \
    make install_dssr
COPY . .
CMD ["/bin/bash"]