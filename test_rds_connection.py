from sqlalchemy import create_engine,text

aws_engine = create_engine(
    "postgresql://postgres:newsroot@news-sentiment-db.ctge6ym20lr7.ap-south-1.rds.amazonaws.com:5432/postgres"
)

# Test connection
with aws_engine.connect() as conn:
    result = conn.execute(text("SELECT version();"))
    print(result.fetchone())
