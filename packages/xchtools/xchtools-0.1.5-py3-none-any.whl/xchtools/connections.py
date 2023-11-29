# %%
import os
import pymysql
import pandas as pd
from dynaconf import Dynaconf
from pathlib import Path
from tqdm import tqdm


class XCHConnections:
    """
    init params:
        settings_dir: the directory to settings.toml/.env/.secret.toml
        project_name: optional.

    methods:
        sql2li(sql): return the result of sql in list of list format
        sql2df(sql): return theresult of sql in dataframe format


    """

    def __init__(self, settings_dir, project_name="XCHTOOLS"):
        self.project_name = project_name
        self.init_config(settings_dir=settings_dir, project_name=project_name)

    def init_config(self, settings_dir, project_name="XCHTOOLS"):
        # Usage: input settings file path， return the settings dictionary.
        import os
        from dynaconf import Dynaconf

        settings = Dynaconf(
            env=os.environ.get(f"ENV_FOR_{project_name}") or "development",
            envvar_prefix="XCHTOOLS",
            settings_files=[
                os.path.join(settings_dir, "settings.toml"),
                os.path.join(settings_dir, ".secrets.toml"),
            ],
            environments=True,
            load_dotenv=True,
            dotenv_path=os.path.join(settings_dir, ".env"),
        )
        self.settings = settings

    def _renew_connect_mysql(self):
        if not self.settings.get("db"):
            raise ValueError(
                "settings is emmpty. please specify them in `settings.toml`"
            )
        cdp_params = self.settings.get("db").to_dict()
        conn = pymysql.connect(**cdp_params)
        cur = conn.cursor()
        return conn, cur

    def sql2li(self, sql):
        conn, cursor = self._renew_connect_mysql()
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data

    def sql2li_limit(self, sql, limit=1):
        conn, cursor = self._renew_connect_mysql()
        cursor.execute(sql)
        data = cursor.fetchmany(limit)
        cursor.close()
        conn.close()
        return data

    def sql2df(self, sql) -> pd.DataFrame:
        conn, cursor = self._renew_connect_mysql()
        cursor.execute(sql)
        head = [a[0] for a in cursor.description]
        data = cursor.fetchall()
        df = pd.DataFrame(data)
        df.columns = head
        cursor.close()
        conn.close()
        return df

    def create_tables(self, sql_folder, database):
        conn, cursor = self._renew_connect_mysql()
        conn.select_db(database)
        p = Path(sql_folder)
        sqlfiles = list(p.rglob("*.sql"))
        for sqlfile in tqdm(sqlfiles):
            try:
                with open(sqlfile, "r", encoding="utf8") as f:
                    sql_list = f.read().split(";")[:-1]
                    for sql in sql_list:
                        sql = sql.strip() + ";"
                        cursor.execute(sql)
                conn.commit()
            except Exception as e:
                print(f"Load {sqlfile} failed.  {e}")
        cursor.close()
        conn.close()

    # %%


# %%
if __name__ == "__main__":
    xc = XCHConnections(os.path.dirname(os.path.abspath(__file__)))
    config = xc.settings
    print(config.db)
    # %%
    # xc.sql2df("show databases")
    xc.sql2li_limit("show databases", 3)

    # %%
    xc.sql2li("show tables in information_schema")
    # xc.sql2li("show tables in fundresearch")
    # xc.sql2li("select * from fundresearch.fund_information")
    xc.sql2li("select * from information_schema.TABLES")
    # %%

    path = r"C:\Users\o0oii\Downloads\fundresearch_fundresearch_20231115205701\fundresearch\TABLE"
    xc.create_tables(path, "fundresearch")

# %%
