# clickzetta-travel

Toolkits including Transpile, Run, And Validate queries, for Evaluating clickzetta with Love.

- Based on [SQLGlot](https://sqlglot.com)
- Transpile SQL to dialect clickzetta
- Run SQL on both original database and clickzetta lakehouse and validate results
- Web UI powered by streamlit

## Getting started

```shell
docker pull clickzetta/clickzetta-travel:dev
mkdir travel
cd travel
docker run -p 8501:8501 -v .:/mnt/userdata clickzetta/clickzetta-travel:dev
```

Open http://localhost:8501 in your browser.

Screenshots
![screenshot of transpile](screenshot-1.png)
![screenshot of run and validate](screenshot-2.png)