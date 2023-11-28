READONLY;
CREATE VIEW table11_hdr AS
SELECT seqno,                      //  1
       active_line,                //  2
       active_inactive_seqno,      //  3
       country_group,              //  4
       country_statid_from,        //  5
       country_statid_to,          //  6
       country_lat_from,           //  7
       country_lat_to,             //  8
       country_lon_from,           //  9
       country_lon_to,             // 10
       country_name_1,             // 11
       country_name_2,             // 12
       country_name_3,             // 13
       country_name_4,             // 14
       country_name_5,             // 15
       country_name_6,             // 16
       country_name_7,             // 17
       country_name_8              // 18
FROM era_country_t_table11_hdr
;
