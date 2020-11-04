from flask import Blueprint, request, send_file
from gsca.db import mongo
from flask_restful import Api, Resource, fields, marshal_with, reqparse
from pathlib import Path
import subprocess
import uuid

deg = Blueprint("deg", __name__)
api = Api(deg)

# r plot resource

apppath = Path(api.app.root_path).parent.parent.parent  # notice apppath parent
rcommand = "/usr/bin/Rscript"
rscriptpath = apppath / "gsca/rscripts"
resource_pngs = apppath / "gsca/resource/pngs"

if not resource_pngs.exists():
    resource_pngs.mkdir(parents=True)


model_degtable = {
    "entrez": fields.Integer(attribute="entrez"),
    "symbol": fields.String(attribute="symbol"),
    "normal": fields.Float(attribute="normal"),
    "tumor": fields.Float(attribute="tumor"),
    "fc": fields.Float(attribute="fc"),
    "fdr": fields.Float(attribute="fdr"),
    "n_normal": fields.Float(attribute="n_normal"),
    "n_tumor": fields.Float(attribute="n_tumor"),
    "cancertype": fields.String(attribute="cancertype"),
}


class DEGTable(Resource):
    @marshal_with(model_degtable)
    def post(self):
        args = request.get_json()
        condition = {"symbol": {"$in": args["validSymbol"]}}
        output = {"_id": 0}
        res = list()
        for collname in args["validColl"]:
            mcur = mongo.db[collname].find(condition, output)
            for m in mcur:
                m["cancertype"] = collname.rstrip("_deg")
                res.append(m)
        return res


api.add_resource(DEGTable, "/degtable")


class DEGplot(Resource):
    def post(self):
        args = request.get_json()

        res = self.__check_run(args)

        if res["run"]:
            self.__degplot(args, res["filepath"])
        return send_file(str(res["filepath"]), mimetype="image/png")

    def __check_run(self, args):
        uuidname = str(uuid.uuid4())
        filename = uuidname + ".png"
        filepath = resource_pngs / filename

        preanalysised = mongo.db.preanalysised.find_one(
            {"search": "#".join(args["validSymbol"]), "coll": "#".join(args["validColl"]), "purpose": "degplot"},
            {"_id": 0, "uuid": 1},
        )
        print(preanalysised)
        if preanalysised:
            uuidname = preanalysised["uuid"]
            filename = uuidname + ".png"
            filepath = resource_pngs / filename
            run = False if filepath.exists() else True
            return {"run": run, "filepath": filepath}
        else:
            mongo.db.preanalysised.insert_one(
                {
                    "search": "#".join(args["validSymbol"]),
                    "coll": "#".join(args["validColl"]),
                    "purpose": "degplot",
                    "uuid": uuidname,
                }
            )
            return {"run": True, "filepath": filepath}

    def __degplot(self, args, filepath):
        rarg = "#".join(args["validSymbol"]) + "@" + "#".join(args["validColl"])

        cmd = [rcommand, str(rscriptpath / "degplot.R"), rarg, str(filepath), str(apppath)]
        print(cmd)

        subprocess.check_output(cmd, universal_newlines=True)


api.add_resource(DEGplot, "/degplot")