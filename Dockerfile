FROM python:3.10-slim-bullseye

WORKDIR /app


COPY requirements.txt ./

RUN apt-get update && apt-get install -y --no-install-recommends \
    sqlite3 libsqlite3-dev build-essential wget


RUN wget https://www.sqlite.org/2023/sqlite-autoconf-3430000.tar.gz
RUN tar xvf sqlite-autoconf-3430000.tar.gz
RUN cd sqlite-autoconf-3430000 && ./configure --prefix=/usr/local && make && make install
RUN ldconfig
RUN sqlite3 --version


RUN pip install --upgrade pip

RUN pip install langchain-chroma

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV GOOGLE_API_KEY=SUA_API_KEY
ENV CORE_API_URL=http://127.0.0.1:8080/user/me
ENV CORE_API_URL_POST=http://127.0.0.1:8080/pedido
ENV MONGO_URL=localhost:27017

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]