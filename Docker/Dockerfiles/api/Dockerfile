

FROM python:3
WORKDIR /usr/src/app
COPY . .
#RUN pip install pyopenssl
#RUN pip install tqdm
RUN pip install matplotlib
RUN pip install requests
RUN pip install praw
RUN pip install pytrends
CMD ["main.py"]
ENTRYPOINT ["python3"]
ADD /twitter/ twitter.py
ADD reddit/ reddit_api.py
ADD /in_out_results/ user_config.JSON
ADD /google/ gpytrends.py

