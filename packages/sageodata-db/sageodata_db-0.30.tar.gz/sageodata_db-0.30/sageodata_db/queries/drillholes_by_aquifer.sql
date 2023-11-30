SELECT          dh.drillhole_no AS dh_no,     --col
                dh.unit_no      AS unit_long, --col
                To_char(dh.map_100000_no)
                                || '-'
                                || To_char(dh.dh_seq_no) AS unit_hyphen, --col
                Trim(To_char(dh.obs_well_plan_code))
                                || Trim(To_char(dh.obs_well_seq_no, '000')) AS obs_no,           --col
                dh.dh_name                                                  AS dh_name,          --col
                dh.amg_easting                                              AS easting,          --col
                dh.amg_northing                                             AS northing,         --col
                dh.amg_zone                                                 AS zone,             --col
                dh.neg_lat_deg_real                                         AS latitude,         --col
                dh.long_deg_real                                            AS longitude,        --col
                summ.aq_subaq                                               AS current_aquifer,  --col
                aqmon.constrn_date                                          AS aquifer_mon_from, --col
                su.map_symbol
                                ||
                CASE
                                WHEN hs_subint.hydro_subunit_code IS NOT NULL THEN '('
                                                                || hs_subint.hydro_subunit_code
                                                                || ')'
                                ELSE ''
                END AS aquifer --col
FROM            dhdb.dd_dh_aquifer_mon_vw aqmon
inner join      dhdb.dd_drillhole_vw dh
ON              aqmon.drillhole_no = dh.drillhole_no
inner join      dhdb.dd_drillhole_summary_vw summ
ON              aqmon.drillhole_no = summ.drillhole_no
inner join      dhdb.st_strat_unit_vw su
ON              aqmon.strat_unit_no = su.strat_unit_no
left outer join
                (
                                SELECT DISTINCT strat_unit_no,
                                                hydro_subunit_code
                                FROM            dhdb.wa_hydrostrat_subint_vw) hs_subint
ON              aqmon.strat_unit_no = hs_subint.strat_unit_no
AND             aqmon.hydro_subunit_code = hs_subint.hydro_subunit_code
left outer join dhdb.wa_hydrostrat_subunit_vw hs_subunit
ON              hs_subint.strat_unit_no = hs_subunit.strat_unit_no
AND             hs_subint.hydro_subunit_code = hs_subunit.hydro_subunit_code
WHERE           aqmon.drillhole_no IN
                (
                                SELECT          a.drillhole_no
                                FROM            dhdb.dd_dh_aquifer_mon_vw a
                                inner join      dhdb.st_strat_unit_vw stu
                                ON              a.strat_unit_no = stu.strat_unit_no
                                left outer join
                                                (
                                                                SELECT DISTINCT strat_unit_no,
                                                                                hydro_subunit_code
                                                                FROM            dhdb.wa_hydrostrat_subint_vw) hss
                                ON              a.strat_unit_no = hss.strat_unit_no
                                AND             a.hydro_subunit_code = hss.hydro_subunit_code
                                WHERE           (
                                                                stu.map_symbol
                                                                                ||
                                                                CASE
                                                                                WHEN hss.hydro_subunit_code IS NOT NULL THEN '('
                                                                                                                || hss.hydro_subunit_code
                                                                                                                || ')'
                                                                                ELSE ''
                                                                END) IN {AQUIFER} ) --arg AQUIFER (sequence of str): aquifer monitored codes e.g. 'Tomw(T1)' or 'Thgr(U1)+Thgr(U2)'
AND dh.deletion_ind = 'N'
ORDER BY        dh_no,
                aquifer_mon_from