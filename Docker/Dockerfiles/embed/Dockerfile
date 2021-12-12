

FROM python:3
WORKDIR /usr/src/app
COPY . .
RUN pip install pyopenssl
RUN pip install tqdm
RUN pip install pyyaml
RUN pip install requests
RUN pip install beautifulsoup4
CMD ["reference_count_multiprocessing.py"]
ENTRYPOINT ["python3"]
ADD gsearch.py .
ADD tools.json .
ADD tools.yaml .

