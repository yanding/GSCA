import uuid
from gsca import app
from pathlib import Path
from gsca.db import mongo
import subprocess


class AppPaths:
    apppath = Path(app.root_path).parent  # notice apppath parent
    rcommand = "/usr/local/bin/Rscript"
    rscriptpath = apppath / "gsca-r-app"
    resource_pngs = apppath / "gsca-r-plot/pngs"

    if not resource_pngs.exists():
        resource_pngs.mkdir(parents=True)


class CheckTable(AppPaths):
    def __init__(self, args, purpose, rtable):
        self.args = args
        self.purpose = purpose
        self.rtable = rtable

        if not self.resource_tables.exists():
            self.resource_tables.mkdir(parents=True)

    def check_run(self):
        uuidname = str(uuid.uuid4())
        filename = uuidname + ".tsv"
        filepath = self.resource_tables / filename

        preanalysised = mongo.db.preanalysised.find_one(
            {"search": "#".join(self.args["validSymbol"]), "coll": "#".join(self.args["validColl"]), "purpose": self.purpose},
            {"_id": 0, "uuid": 1},
        )
        if preanalysised:
            uuidname = preanalysised["uuid"]
            filename = uuidname + ".tsv"
            filepath = self.resource_tables / filename
            run = False if filepath.exists() else True
            return {"run": run, "filepath": filepath}
        else:
            mongo.db.preanalysised.insert_one(
                {
                    "search": "#".join(self.args["validSymbol"]),
                    "coll": "#".join(self.args["validColl"]),
                    "purpose": self.purpose,
                    "uuid": uuidname,
                }
            )
            return {"run": True, "filepath": filepath}

    def table(self, filepath):
        rargs = "#".join(self.args["validSymbol"]) + "@" + "#".join(self.args["validColl"])
        cmd = [self.rcommand, str(self.rscriptpath / self.rtable), rargs, str(filepath), str(self.apppath)]
        print("\n\n ", " \\\n ".join(cmd), "\n\n")
        subprocess.check_output(cmd, universal_newlines=True)


class CheckTableGSXA(AppPaths):
    def __init__(self, args, purpose, ranalysis, precol, gsxacol):
        args["validColl"] = [x.split("_")[0] + "_all_expr_gene_set.rds.gz" for x in args["validColl"]]
        self.args = args
        self.purpose = purpose
        self.ranalysis = ranalysis
        self.precol = precol
        self.gsxacol = gsxacol
        self.uuid = str(uuid.uuid4())

    def check_run(self):
        run = True
        preanalysised = mongo.db[self.precol].find_one(
            {"search": "#".join(self.args["validSymbol"]), "coll": "#".join(self.args["validColl"]), "purpose": self.purpose},
            {"_id": 0, "uuid": 1},
        )

        if preanalysised:
            self.uuid = preanalysised["uuid"]
            gsxacol = mongo.db[self.gsxacol].find_one({"uuid": self.uuid}, {"_id": 0, "uuid": 1})
            run = False if gsxacol else True
        else:
            mongo.db[self.precol].insert_one(
                {
                    "search": "#".join(self.args["validSymbol"]),
                    "coll": "#".join(self.args["validColl"]),
                    "purpose": self.purpose,
                    "uuid": self.uuid,
                }
            )
        return {"run": run, "uuid": self.uuid}

    def analysis(self):
        rargs = "#".join(self.args["validSymbol"]) + "@" + "#".join(self.args["validColl"])
        cmd = [self.rcommand, str(self.rscriptpath / self.ranalysis), rargs, str(self.apppath), self.uuid, self.gsxacol]
        print("\n\n ", " \\\n ".join(cmd), "\n\n")
        subprocess.check_output(cmd, universal_newlines=True)


class CheckTableGeneSet(AppPaths):
    def __init__(self, args, purpose, ranalysis, precol, gsxacol):

        self.args = args
        self.purpose = purpose
        self.ranalysis = ranalysis
        self.precol = precol
        self.gsxacol = gsxacol
        self.uuid = str(uuid.uuid4())

    def check_run(self):
        run = True
        preanalysised = mongo.db[self.precol].find_one(
            {"search": "#".join(self.args["validSymbol"]), "coll": "#".join(self.args["validColl"]), "purpose": self.purpose},
            {"_id": 0, "uuid": 1},
        )

        if preanalysised:
            self.uuid = preanalysised["uuid"]
            gsxacol = mongo.db[self.gsxacol].find_one({"uuid": self.uuid}, {"_id": 0, "uuid": 1})
            run = False if gsxacol else True
        else:
            mongo.db[self.precol].insert_one(
                {
                    "search": "#".join(self.args["validSymbol"]),
                    "coll": "#".join(self.args["validColl"]),
                    "purpose": self.purpose,
                    "uuid": self.uuid,
                }
            )
        return {"run": run, "uuid": self.uuid}

    def analysis(self):
        rargs = "#".join(self.args["validSymbol"]) + "@" + "#".join(self.args["validColl"])
        cmd = [self.rcommand, str(self.rscriptpath / self.ranalysis), rargs, str(self.apppath), self.uuid, self.gsxacol]
        print("\n\n ", " \\\n ".join(cmd), "\n\n")
        subprocess.check_output(cmd, universal_newlines=True)
