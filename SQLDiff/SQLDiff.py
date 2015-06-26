__author__ = 'aardr'

## Configuration

import difflib

#from IPython.core.display import HTML
## Configuration

import pypyodbc


class SQLDiff:

    regions = [
        dict(name="DEV", region="Development", cs="DRIVER={SQL Server Native Client 10.0}; SERVER=s4000cs-D-sq01;"
                                                  + "DATABASE=CAPSS_BigSix_P0;Trusted_Connection=yes"),
        dict(name="TEST", region="Testing", cs="DRIVER={SQL Server Native Client 10.0}; SERVER=s4000cs-T-sq01;" +
                                               "DATABASE=CAPSS_BigSix;Trusted_Connection=yes"),
        dict(name="STAGE", region="Staging", cs="DRIVER={SQL Server Native Client 10.0}; SERVER=s4000cs-S-sq01;" +
                                                "DATABASE=CAPSS_BigSix;Trusted_Connection=yes"),
        dict(name="PROD", region="Production", cs="DRIVER={SQL Server Native Client 10.0}; SERVER=s4000cs-P-sq01;" +
                                                  "DATABASE=CAPSS_BigSix;Trusted_Connection=yes")
    ]

    from_object = {}
    to_object = {}

    mismatches_from = []
    mismatches_to = []

    common = [""]

    search_pattern = ""

    def _init__(self):
        self.reset()

    def reset(self):
        self.from_object = {}
        self.to_object = {}
        self.mismatches_from = []
        self.mismatches_to = []
        self.common = []
        self.search_pattern = ""


    def get_mismatches_and_common(self):
        from_set = set(from_object["objects"])
        to_set = set(to_object["objects"])

        self.mismatches_from = list(from_set - to_set)
        self.mismatches_to = list(to_set - from_set)
        self.common = sorted(list(from_set.intersection(to_set)))

    def comparison(self):
        self.get_mismatches_and_common()

        from_display = "<h3>Only in " + self.from_object["region"]
        from_display += "(" + str(len(self.mismatches_from)) + " items)</h3>"
        from_display += "<br />".join(sorted(self.mismatches_from))

        display(HTML(from_display))

        to_display = "<h3>Only in " + self.to_object["region"]
        to_display += "(" + str(len(self.mismatches_to)) + " items)</h3>"
        to_display += "<br />".join(sorted(self.mismatches_to))

        display(HTML(to_display))

    def set_search(self, search_for):
        self.search_pattern = search_for
        self.comparison()

    def discern(self, region):
        output = {"region": "REGION", "objects": "sorted list of region Objects", "cursor": "CURSOR"}

        for item in self.regions:
            if region == item["name"]:
                conn = pypyodbc.connect(item["cs"])
                cursor = conn.cursor()
                output = {"region": item["region"], "cursor": cursor}

        output["objects"] = self.get_object_list(output)

        return output

    def get_object_list(self, region_obj):
        sql_db_objs = "SELECT name FROM sysobjects WHERE xtype in ('FN', 'P') AND category = 0 "
        sql_db_objs += "AND name LIKE '%" + self.search_pattern + "%'"

        region_cursor = region_obj["cursor"]
        db_objects = region_cursor.execute(sql_db_objs).fetchall()

        return sorted([x[0] for x in db_objects])

    def set_from(self, from_region_name):
        self.from_object = self.discern(from_region_name)
        self.comparison()

    def set_to(self, to_region_name):
        self.to_object = self.discern(to_region_name)
        self.comparison()

    def difference(self, routine_name):
        cursor_from = self.from_object["cursor"]
        cursor_to = self.to_object["cursor"]

        sql_obj_text = "SELECT text FROM syscomments WHERE id = "
        sql_obj_text += "(SELECT id FROM sysobjects WHERE name = \'%s\') ORDER BY colid" % routine_name

        obj_first  = [x[0] for x in cursor_from.execute(sql_obj_text).fetchall()]
        obj_second = [x[0] for x in cursor_to.execute(sql_obj_text).fetchall()]

        obj_first  = "".join(obj_first).splitlines()
        obj_second = "".join(obj_second).splitlines()

        html_diff = difflib.HtmlDiff()

        display(HTML(html_diff.make_table(obj_first, obj_second)))




    interact(set_search, search_for="Enter pattern here")
    interact(set_from, from_region_name=dict((item["region"], item["name"]) for item in regions))
    interact(set_to, to_region_name=dict((item["region"], item["name"]) for item in regions))
    interact(difference, routine_name=common)



