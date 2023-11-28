READONLY;
CREATE VIEW countryrstrhhdr AS
SELECT seqno, country_group_code,
//       1           2
       country_statid_from_i, country_statid_from_c, country_statid_to_i, country_statid_to_c,
//              3                    4                     5                      6
       country_lat_from, country_lat_to, country_lon_from, country_lon_to,
//              7               8              9               10
       country_name_1,  country_name_2,  country_name_3, country_name_4,
//            11              12              13            14
       country_name_5,  country_name_6,  country_name_7, country_name_8,
//            15              16              17            18
       country_name_with_lat_lon_1, country_name_with_lat_lon_2,
//            19                              20 
       country_name_with_lat_lon_3, country_name_with_lat_lon_4,
//            21                             22
       country_name_with_lat_lon_5, country_name_with_lat_lon_7,
//            23                              24
       country_name_with_lat_lon_6, country_name_with_lat_lon_8,
//            25                              26
       country_grouped_seqno,
//            27
       country_name_grouped_1, country_name_grouped_2, country_name_grouped_3, country_name_grouped_4,
//            28                        29                    30                     31
       country_name_grouped_5, country_name_grouped_6, country_name_grouped_7, country_name_grouped_8,
//            32                        33                    34                     35
       body.offset, body.len
//        36           37
FROM hdr
//WHERE
//ORDERBY
;
