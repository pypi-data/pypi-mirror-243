"""
  #####
 #     #  ####   ####  #   ##   #      #      #   #
 #       #    # #    # #  #  #  #      #       # #
  #####  #    # #      # #    # #      #        #
       # #    # #      # ###### #      #        #
 #     # #    # #    # # #    # #      #        #
  #####   ####   ####  # #    # ###### ######   #

 ######
 #     # ###### ##### ###### #####  #    # # #    # ###### #####
 #     # #        #   #      #    # ##  ## # ##   # #      #    #
 #     # #####    #   #####  #    # # ## # # # #  # #####  #    #
 #     # #        #   #      #####  #    # # #  # # #      #    #
 #     # #        #   #      #   #  #    # # #   ## #      #    #
 ######  ######   #   ###### #    # #    # # #    # ###### #####


"""

import re
import pandas as pd
from sdutilities.datalink import DataLink


def add_resolution(name, table, key_col, geom_col):
    if table.find(".") < 0:
        raise Exception('The table should be specified as "schema.table"')
    ss_db = DataLink()
    resolutions = ss_db.query_to_df("resolutions", "reference")
    if name.lower() in list(resolutions.name.str.lower()):
        raise Exception(f"{name.upper()} already exists in " + "reference.resolutions")
    schema, tbl = table.split(".")
    tbl_columns = ss_db.query_to_df(
        "columns",
        "information_schema",
        where_clause=f"table_name='{tbl}' and table_schema='{schema}'",
    )
    cols = list(tbl_columns.column_name.str.lower())
    if len(cols) == 0:
        raise Exception(f"{tbl.upper()} not found on the SocialScape database")
    if key_col.lower() not in cols:
        raise Exception(f"{key_col.upper()} not found in {tbl.upper()}")
    if geom_col.lower() not in cols:
        raise Exception(f"{geom_col.upper()} not found in {tbl.upper()}")
    if tbl_columns.loc[tbl_columns.column_name == geom_col, "data_type"].iloc[0] != "USER-DEFINED":
        raise Exception(f"{geom_col.upper()} is not a valid geometry column " + "in {tbl.upper()}")
    ss_db.run_sql(
        f"insert into reference.resolutions select '{name}', "
        + f"'{table}', '{key_col}', '{geom_col}'; commit;"
    )


class Aggregator(object):
    def __init__(self, output_resolution):
        self.SS_DB = DataLink()
        resolutions_table = self.SS_DB.query_to_df("resolutions", "reference")
        if output_resolution.lower() not in list(resolutions_table.name.str.lower()):
            raise Exception(
                f"{output_resolution.upper()} does not exist in "
                + "reference.resolutions! Use add_resolution() before"
                + " instantiating an aggregator at this resolution."
            )
        (
            self.RESOLUTION,
            self.RESOLUTION_TABLE,
            self.KEY,
            self.GEOM,
            self.INTERSECTIONS,
        ) = resolutions_table.loc[resolutions_table.name == output_resolution.lower(),].iloc[0, :]

    def gen_intersection_data(self):
        self.INTERSECTIONS = f"census_transformed.hex_{self.RESOLUTION}_intersections"
        sql = f"""
        drop table if exists {self.INTERSECTIONS};
        commit;
        create table {self.INTERSECTIONS} as
        select a.{self.KEY}, b.hexagon_id,
        ST_AREA(ST_INTERSECTION(a.{
        self.GEOM}, b.shape_detailed)) as "intersection_area",
        ST_AREA(b.shape_detailed) as "hex_area",
        ST_AREA(ST_INTERSECTION(a.{
        self.GEOM}, b.shape_detailed)) / ST_AREA(b.shape_detailed)
        as "pct_within"
        from
        {self.RESOLUTION_TABLE} a
        left join
        census_transformed.hexagon_spatial b
        on ST_INTERSECTS(a.{self.GEOM}, b.shape_detailed);
        commit;
        alter table {self.INTERSECTIONS} owner to sdrc_admins;
        commit;
        delete from {self.INTERSECTIONS} where pct_within < .001;
        commit;
        update reference.resolutions
        set hex_intersection_table = '{self.INTERSECTIONS}'
        where name = '{self.RESOLUTION}';
        commit;
        """
        self.SS_DB.run_sql(sql)

    def aggregate_agg_cols(self, agg_config=None):
        sql = self.agg_query_builder(agg_config)
        return pd.read_sql(sql, self.SS_DB.get_engine())

    def agg_query_builder(self, cfg=None):
        if cfg == None:
            return -1
        method_map = {"EQ": "=", "LT": "<", "GT": ">", "LE": "<=", "GE": ">=", "IN": "in"}
        data_cols = (
            [cfg["data_cols"]] if (not isinstance(cfg["data_cols"], list)) else cfg["data_cols"]
        )
        if "out_col_name" in cfg:
            out_cols = (
                [cfg["out_col_name"]]
                if (not isinstance(cfg["out_col_name"], list))
                else cfg["out_col_name"]
            )
            if "case" in cfg:
                case_cols = (
                    [cfg["case"]["col"]]
                    if (not isinstance(cfg["case"]["col"], list))
                    else cfg["case"]["col"]
                )
                case_methods = (
                    [cfg["case"]["method"]]
                    if (not isinstance(cfg["case"]["method"], list))
                    else cfg["case"]["method"]
                )
                case_constraints = (
                    [cfg["case"]["constraint"]]
                    if (not isinstance(cfg["case"]["constraint"], list))
                    else cfg["case"]["constraint"]
                )
                if "out_col" in cfg["case"]:
                    out_case_cols = (
                        [cfg["case"]["out_col"]]
                        if (not isinstance(cfg["case"]["out_col"], list))
                        else cfg["case"]["out_col"]
                    )
                else:
                    out_case_cols = case_cols
                case_cols = dict(zip(case_cols, out_case_cols))
                tmp_data_cols = []
                tmp_out_cols = []
                for i in range(len(data_cols)):
                    for case_col in case_cols:
                        for case_method in case_methods:
                            for case_constraint in case_constraints:
                                if case_method != "BTW":
                                    tmp_data_cols.append(
                                        f"case when c.{case_col} "
                                        + f"{method_map[case_method]} "
                                        + f"{case_constraint} then "
                                        + f"b.{data_cols[i]} else 0 end"
                                    )
                                else:
                                    tmp_data_cols.append(
                                        f"case when c.{case_col} > "
                                        + f"{case_constraint[0]} and "
                                        + f"c.{case_col} < "
                                        + f"{case_constraint[1]} then "
                                        + f"b.{data_cols[i]} else 0 end"
                                    )
                                tmp_out_cols.append(
                                    out_cols[i]
                                    .replace("%col", case_cols[case_col])
                                    .replace("%method", case_method)
                                    .replace(
                                        "%constraint",
                                        re.sub(
                                            r",", "_", re.sub(r"[() ]", "", str(case_constraint))
                                        ),
                                    )
                                )
                data_cols = tmp_data_cols
                out_cols = tmp_out_cols
            col_dict = dict(zip(data_cols, out_cols))
            col_sql = "".join(
                [
                    f", round(sum(a.pct_within * "
                    + f"greatest(0, {'' if('case' in cfg) else 'b.'}{dc}))::"
                    + f'numeric, 2) as "{col_dict[dc]}"'
                    for dc in col_dict
                ]
            )
        else:
            col_sql = "".join(
                [
                    f", round(sum(a.pct_within * greatest(" + f'0, b.{dc}))::numeric, 2) as "{dc}"'
                    for dc in data_cols
                ]
            )
        case_join_sql = (
            ""
            if ("case" not in cfg)
            else f"left join {cfg['case']['table']} c on " + "a.hexagon_id = c.hexagon_id"
        )
        sql = (
            f"""
        select
        a.{self.KEY}
        """
            + col_sql
            + f"""
        from
        {self.INTERSECTIONS} a
        left join
        {cfg['data_table_name']} b
        on a.hexagon_id = b.hexagon_id {case_join_sql} """
            + f"group by a.{self.KEY};"
        )
        return sql

    def aggregate_med_cols(self, agg_config=None):
        sql = self.med_query_builder(agg_config)
        return pd.read_sql(sql, self.SS_DB.get_engine())

    def med_query_builder(self, cfg=None):
        if cfg == None:
            return -1
        method_map = {"EQ": "=", "LT": "<", "GT": ">", "LE": "<=", "GE": ">=", "IN": "in"}
        data_cols = (
            [cfg["data_cols"]] if (not isinstance(cfg["data_cols"], list)) else cfg["data_cols"]
        )
        if "out_col_name" in cfg:
            out_cols = (
                [cfg["out_col_name"]]
                if (not isinstance(cfg["out_col_name"], list))
                else cfg["out_col_name"]
            )
            if "case" in cfg:
                case_cols = (
                    [cfg["case"]["col"]]
                    if (not isinstance(cfg["case"]["col"], list))
                    else cfg["case"]["col"]
                )
                case_methods = (
                    [cfg["case"]["method"]]
                    if (not isinstance(cfg["case"]["method"], list))
                    else cfg["case"]["method"]
                )
                case_constraints = (
                    [cfg["case"]["constraint"]]
                    if (not isinstance(cfg["case"]["constraint"], list))
                    else cfg["case"]["constraint"]
                )
                if "out_col" in cfg["case"]:
                    out_case_cols = (
                        [cfg["case"]["out_col"]]
                        if (not isinstance(cfg["case"]["out_col"], list))
                        else cfg["case"]["out_col"]
                    )
                else:
                    out_case_cols = case_cols
                case_cols = dict(zip(case_cols, out_case_cols))
                tmp_data_cols = []
                tmp_out_cols = []
                for i in range(len(data_cols)):
                    for case_col in case_cols:
                        for case_method in case_methods:
                            for case_constraint in case_constraints:
                                if case_method != "BTW":
                                    tmp_data_cols.append(
                                        f"case when c.{case_col} "
                                        + f"{method_map[case_method]} "
                                        + f"{case_constraint} then "
                                        + f"b.{data_cols[i]} end"
                                    )
                                else:
                                    tmp_data_cols.append(
                                        f"case when c.{case_col} > "
                                        + f"{case_constraint[0]} and "
                                        + f"c.{case_col} < "
                                        + f"{case_constraint[1]} then "
                                        + f"b.{data_cols[i]} end"
                                    )
                                tmp_out_cols.append(
                                    out_cols[i]
                                    .replace("%col", case_cols[case_col])
                                    .replace("%method", case_method)
                                    .replace(
                                        "%constraint",
                                        re.sub(
                                            r",", "_", re.sub(r"[() ]", "", str(case_constraint))
                                        ),
                                    )
                                )
                data_cols = tmp_data_cols
                out_cols = tmp_out_cols
            col_dict = dict(zip(data_cols, out_cols))
            col_sql = "".join(
                [
                    f", round((sum(a.pct_within * d.b01001e1 * "
                    + f"nullif(nullif({'' if('case' in cfg) else 'b.'}"
                    + f"{dc}, -1), -2))::float"
                    + f" / sum(a.pct_within * d.b01001e1 * "
                    + f"({'' if('case' in cfg) else 'b.'}{dc} >= 0)::int)"
                    + f"::float)::numeric, 2) as "
                    + f'"{col_dict[dc]}"'
                    for dc in col_dict
                ]
            )
        else:
            col_sql = "".join(
                [
                    f", round((sum(a.pct_within * d.b01001e1 * "
                    + f"nullif(nullif(b.{dc}, -1), -2))::"
                    + f"float / sum(a.pct_within "
                    + f"* d.b01001e1 * (b.{dc} >= 0)::int)::float)"
                    + f'::numeric, 2) as "{dc}"'
                    for dc in data_cols
                ]
            )
        case_join_sql = (
            ""
            if ("case" not in cfg)
            else f"left join {cfg['case']['table']} c on " + f"a.hexagon_id=c.hexagon_id"
        )
        sql = (
            f"""
        select
        a.{self.KEY}
        """
            + col_sql
            + f"""
        from
        {self.INTERSECTIONS} a
        left join
        {cfg['data_table_name']} b
        on a.hexagon_id = b.hexagon_id """
            + case_join_sql
            + f"""
               left join census_transformed.acs_population_sample_agg_hex d
               on a.hexagon_id = d.hexagon_id
        group by a.{self.KEY};
        """
        )
        return sql

