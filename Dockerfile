FROM python:3.10
WORKDIR /app
ENV X3DNA=/app/helper/rna_angles_prediction_dssr/dssr
ENV PATH=/app/helper/rna_angles_prediction_dssr/bin:$PATH
COPY requirements.txt .
COPY Makefile .
COPY test.py .
RUN pip install -r requirements.txt &&\
    make install_dssr
# Command to download the RNA-TorsionBERT model
RUN python test.py
COPY . .
CMD ["/bin/bash"]